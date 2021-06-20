import * as axios from "axios";

const client = (serverUrl) => {
    return axios.create({
        baseURL: serverUrl,
        headers: {},
        timeout: 30000// 30초 이내 응답이 없을 시 에러로 간주.
    })
}

function genUUID() {
    function s4() {
        return ((1 + Math.random()) * 0x10000 | 0).toString(16).substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}

function MediaClient(configuration) {
    this.video = configuration.video;
    this.audio = configuration.audio;
    this.data = configuration.data;
    this.video_width = configuration.video_width || 800;
    this.video_height = configuration.video_height || 480;
    this.video_fps = configuration.video_fps || 30;
    this.player = configuration.player;
    this.verbose = configuration.verbose;
    if (this.verbose === null || this.verbose === undefined) {
        this.verbose = false;
    }
    this.host = configuration.host || location.protocol + "//" + window.location.hostname + ":" + window.location.port;
    this.pc_configuration = { iceServers: [{ url: "stun:stun.l.google.com:19302" }] };

    // https://webrtc.org/web-apis/chrome/
    // this.pc_options = { optional: [{ DtlsSrtpKeyAgreement: true }, { RtpDataChannels: true }] };
    this.pc_options = { optional: [{ DtlsSrtpKeyAgreement: true }] }; // RtpDataChannels is legacy old chrome, but recently chrome not working.
    this.media_constraints = { offerToReceiveAudio: true, offerToReceiveVideo: true };
    this.peer_id = genUUID();
    this.early_candidates = [];

    if (this.verbose) {
        console.log("MediaClient: ", configuration);
        console.log("Host URL: ", this.host);
        console.log("Peer ID: ", this.peer_id);
    }
}

MediaClient.prototype.disconnect = function() {
    if (this.pc) {
        try {
            this.pc.close();
        } catch (e) {
            console.log("Failure close peer connection:" + e);
        }
    }
}

MediaClient.prototype.getExchangeUri = function() {
    return "/exchange?peer_id=" + this.peer_id +
        "&videos=" + this.video +
        "&audios=" + this.audio +
        "&datas=" + this.data;
};

MediaClient.prototype.getAddIceCandidateUri = function() {
    return "/ice/candidate/add?peer_id=" + this.peer_id;
};

MediaClient.prototype.getGetIceCandidateUri = function() {
    return "/ice/candidate/get?peer_id=" + this.peer_id;
};

MediaClient.prototype.connect = function() {
    const self = this;
    client(this.host).get("/ice/servers")
        .then(servers => {
            if (servers) {
                self.pc_configuration.iceServers = servers.data;
            }
            if (self.verbose) {
                console.log("SERVERS:", servers.data);
                console.log("Peer connection configuration: ", JSON.stringify(self.pc_configuration));
                console.log("Peer connection options: ", JSON.stringify(self.pc_options));
            }

            try {
                self.pc = new RTCPeerConnection(self.pc_configuration, self.pc_options);
                self.pc.onicecandidate = function(event) {
                    self.onIceCandidate.call(self, event);
                };
                self.pc.onaddstream = function(event) {
                    // const video = self.video_element;
                    const video = self.player.video;
                    if (video) {
                        video.srcObject = event.stream;
                        video.setAttribute("playsinline", true);
                        video.play();
                        if (self.verbose) {
                            console.log("Add stream !!!", event);
                            console.log("Video Muted:", video.muted);
                        }
                    } else {
                        self.destroy();
                    }
                };
                self.pc.oniceconnectionstatechange = function(event) {
                    self.onIceConnectionStateChange.call(self, event);
                };
                self.pc.ondatachannel = function(event) {
                    self.onDataChannel.call(self, event);
                };
            } catch (e) {
                console.error("Peer connection error: ", e);
            }
            if (self.data !== null && self.data !== undefined) {
                try {
                    self.data_channel = self.pc.createDataChannel(self.data);
                    self.data_channel.onopen = function() {
                        if (self.verbose) {
                            console.log("Data channel is open!");
                        }
                    };
                    self.data_channel.onmessage = function(event) {
                        if (self.verbose) {
                            console.log("Data channel recv: ", event.data);
                        }
                    };
                } catch (e) {
                    console.error("Cannot create data channel error: " + e);
                }
            } else {
                console.warn("Data is Empty");
            }

            self.early_candidates.length = 0;

            self.pc.createOffer(self.media_constraints).then(function(offer) {
                if (self.verbose) {
                    console.log("Create offer:" + JSON.stringify(offer));
                }
                self.offer = offer;
                return self.pc.setLocalDescription(offer);
            }).then(function() {
                // Send the offer to the remote peer using the signaling server
                const uri = self.getExchangeUri();
                if (self.verbose) {
                    console.log("Set local description:" + JSON.stringify(self.offer));
                    console.log("Exchange Session Description: " + uri);
                }
                client(self.host).post(uri, self.offer)
                    .then(function(answer) {
                        self.pc.setRemoteDescription(answer.data)
                            .then(function() {
                                for (const candidates in self.early_candidates) {
                                    const uri = self.getAddIceCandidateUri();
                                    client(self.host).post(uri, self.early_candidates[candidates])
                                        .then(function(json_text) {
                                            if (self.verbose) {
                                                console.log("Add ICE Candidate: ", json_text.data)
                                            }
                                        })
                                        .catch(function(err) {
                                            console.error("ERROR:", err);
                                        });
                                }
                                client(self.host).get(self.getGetIceCandidateUri())
                                    .then(function(json_text) {
                                        self.onReceiveIceCandidate(json_text.data);
                                    })
                                    .catch(function(err) {
                                        console.error("ERROR:", err);
                                    });
                            });
                    }).catch(function(e) {
                        console.error("Call error: ", e);
                    });
            }).catch(function(e) {
                console.error("Create offer error: ", e);
            });
        })
        .catch(error => {
            console.error("Connect Get Ice Error:", error);
        })
};

MediaClient.prototype.onIceCandidate = function(event) {
    if (event.candidate) {
        if (this.pc.currentRemoteDescription) {
            if (this.verbose) {
                console.log("Current RemoteDescription: ", this.pc.currentRemoteDescription);
            }
            const self = this;
            client(self.host).post("/ice/candidate/add?peer_id=" + self.peer_id, event.candidate)
                .then(json_data => {
                    if (self.verbose) {
                        console.log("JSON:", json_data);
                    }
                })
                .catch(error => {
                    console.error("onIceCandidate Error:", error);
                })
        } else {
            if (this.verbose) {
                console.log("Push candidate: ", event.candidate);
            }
            this.early_candidates.push(event.candidate);
        }
    } else {
        if (this.verbose) {
            console.log("End of candidates.");
        }
    }
};

MediaClient.prototype.onTrack = function(event) {
    if (this.verbose) {
        console.log("Remote track added: ", JSON.stringify(event));
    }
    // console.log("Remote track added:" +  JSON.stringify(event));
    //
    // var videoElement = document.getElementById(this.videoElement);
    // videoElement.srcObject = event.streams[0];
    // videoElement.setAttribute("playsinline", true);
    // videoElement.play();
};

MediaClient.prototype.onIceConnectionStateChange = function(event) {
    if (this.verbose) {
        console.log("Ice Connection State :", this.pc.iceConnectionState);
    }
    if (this.pc.iceConnectionState === "connected") {
        this.player.onConnected();
    } else if (this.pc.iceConnectionState === "disconnected") {
        this.player.onDisconnected();
    }

    // console.log("oniceconnectionstatechange  state: " + pc.iceConnectionState);
    // var videoElement = document.getElementById(streamer.videoElement);
    // if (videoElement) {
    //     if (pc.iceConnectionState === "connected") {
    //         videoElement.style.opacity = "1.0";
    //     }
    //     else if (pc.iceConnectionState === "disconnected") {
    //         videoElement.style.opacity = "0.25";
    //     }
    //     else if ( (pc.iceConnectionState === "failed") || (pc.iceConnectionState === "closed") )  {
    //         videoElement.style.opacity = "0.5";
    //     }
    // }
};

MediaClient.prototype.onDataChannel = function(event) {
    var self = this;
    if (this.verbose) {
        console.log("Remote data channel created: ", JSON.stringify(event));
    }

    event.channel.onopen = function() {
        if (self.verbose) {
            console.log("remote datachannel open");
        }
        this.send("remote channel openned");
    }
    event.channel.onmessage = function(event) {
        if (self.player.player) {
            self.player.player.onObjectDrawing(event.data);
        } else {
            self.destroy();
        }
        if (self.player.painter) {
            // self.player.painter.onEventDrawing(event.data);
        } else {
            self.destroy();
        }
        // console.log("Recv Data: ##", event.data);
        // console.log("Recv Data type: ##", typeof event.data);
    }
    event.channel.onclose = function() {
        if (self.verbose) {
            console.log("remote datachannel close.");
        }
    }
};

MediaClient.prototype.onReceiveIceCandidate = function(json_text) {
    if (this.verbose) {
        console.log("Receive ICE candidate: " + JSON.stringify(json_text));
    }
    var self = this;
    for (const i in json_text) {
        const candidate = new RTCIceCandidate(json_text[i]);
        if (this.verbose) {
            console.log("Adding ICE candidate :" + JSON.stringify(candidate));
        }
        this.pc.addIceCandidate(candidate)
            .then(function() {
                if (self.verbose) {
                    console.log("Add ICE candidate OK");
                }
            })
            .catch(function(error) {
                console.error("Add ICE candidate error: " + error);
            });
    }
    this.pc.addIceCandidate();
};

MediaClient.prototype.destroy = function() {
    if (this.pc) {
        this.pc.close();
    }
    if (this.player) {
        this.player.destroy();
        this.player.deleteRetry();
        this.player.closeTimer();
    }
}

export const RTCMediaClient = (configuration) => { return new MediaClient(configuration); }