const STD_WIDTH = 1000;
const STD_HEIGHT = 1000;
// var USEDATA = null;
// const METADATA = {count: 350, rect_size: 200, state: "right"}

// 1. insert url in video.
const new_video = (src) => {
    var origin_vod = document.createElement("video");
    origin_vod.autoplay = true;
    origin_vod.loop = true;
    origin_vod.controls = false;
    origin_vod.width = STD_WIDTH;
    origin_vod.height = STD_HEIGHT;
    origin_vod.src = src;
    return origin_vod;
}

const vod_canvas = (canvasID) => {
    var canvas = document.getElementById(canvasID);
    canvas.width = STD_WIDTH;
    canvas.height = STD_HEIGHT;
    return canvas;
}

const drawer = (canvas, type) => {
    var painter = canvas.getContext(type);
    return painter;
}

export const resetUsedata = () => {
    USEDATA = null;
}

export const convertCanvas = (src, canvasID, type = "2d") => {
    var video = new_video(src);
    var canvas = vod_canvas(canvasID);
    var painter = drawer(canvas, type);
    return { video: video, canvas: canvas, painter: painter };
}

export const loop = (video, painter) => {
    video.addEventListener("play", (event) => {
        var $this = this;
        console.log("EVENT? ", event);
        painter.font = "30px Verdana";
        painter.strokeStyle = "red";
        painter.lineWidth = 4;
        (function loop() {
            if ($this.paused || $this.ended) {
                return false;
            }
            painter.drawImage($this, 0, 0, STD_WIDTH, STD_HEIGHT);
            // INSERT DRAW BOX METHOD.
            setTimeout(loop, 1000 / 30);
        })()
    }, 0)
    video.addEventListener("loadedmetadata", (event) => {
        console.log("Loaded MetaData: ", event);
    });
    video.addEventListener("pause", (event) => {
        console.log("PAUSE EVENT: ", event);
    });
    video.addEventListener("playing", (event) => {
        console.log("Replay Event: ", event);
    });
}

// Real Method -----------------------------------------------
export const make_virtual_video = (src, vtt) => {
    var v_video = document.createElement("video");
    v_video.width = STD_WIDTH;
    v_video.height = STD_HEIGHT;
    // v_video.loop = true;
    v_video.controls = false;
    v_video.muted = true;
    v_video.autoplay = true;

    if (src) {
        v_video.src = src;
    }

    if (vtt) {
        var track = docmuent.createElement("track");
        track.kind = "subtitles";
        track.src = vtt;
        v_video.appendChild(track);
    }
    return v_video;
}


// export const play = (video, painter) => {
//   var moveX = 0;
//   var moveY = 0;
//   var state = "left";
//   var state_2 = "right";
//   var moveX_2 = 1000;
//   var moveY_2 = 1000;
//   var W = 200;
//   var H = 250;
//   painter.lineWidth = 5;
//   video.addEventListener("play", (event) => {
//     (function loop() {
//       if (video.paused || video.ended) {
//         return false;
//       }
//       // painter.clearRect(0, 0, STD_WIDTH, STD_HEIGHT);
//       if (moveX > 1000) {
//         state = "left"
//       } else if (moveX <= 0) {
//         state = "right";
//       }
//       if (moveX_2 <= 0) {
//         state_2 = "right"
//       } else if (moveX_2 >= 1000) {
//         state_2 = "left";
//       }
//       if (state == "left") {
//         moveX -= 50;
//         moveY -= 50;
//       } else {
//         moveX += 50;
//         moveY += 50;
//       }

//       if(state_2 == "left") {
//         moveX_2 -= 50;
//         moveY_2 -= 50;
//       } else {
//         moveX_2 += 50;
//         moveY_2 += 50;
//       }
//       painter.drawImage(video, 0, 0, STD_WIDTH, STD_HEIGHT);
//       painter.beginPath();
//       painter.rect(moveX, moveY, W, H);
//       painter.rect(moveX_2, moveY_2, W, H);
//       painter.closePath();
//       painter.stroke();
//       setTimeout(loop, 1000 / 20);
//     })()
//   }, 0)
// }




// const video = (src) => {
//   var my_video = document.createElement("video");
//   my_video.autoplay = true;
//   my_video.controls = true;
//   my_video.loop = true;
//   my_video.src = src;
//   my_video.width = 1000;
//   my_video.height = 1000;
//   return my_video;
// }


// const makeVideo = (src) => {
//   return video(src);
// }

// const canvas_context = (id, type) => {
//   var my_canvas = document.getElementById(id);
//   my_canvas.width = 1000;
//   my_canvas.height = 1000;
//   var my_context = my_canvas.getContext(type);
//   return my_canvas, my_context;
// }

// const makeCanvas = (id, type) => {
//   return canvas_context(id, type);
// }

// export const play = (src, id, type, metaData) => {
//   var video = makeVideo(src);
//   var canvas, context = makeCanvas(id, type);
//   video.addEventListener("play", function () {
//     var $this = this;
//     console.log("THIS: ", this);
//     console.log("$THIS: ", $this);
//     console.log("VIDEO: ", video);
//     var count = 350;
//     var rect_size = 500;
//     var state = "right";
//     (function loop() {
//       if ($this.paused || $this.ended) {
//         return false;
//       } else {
//         if (count + rect_size == 1000) {
//           state = "left";
//         } else if (count == 0) {
//           state = "right";
//         }
//         context.drawImage(video, 0, 0, 1000, 1000);
//         context.strokeStyle = "skyblue";
//         context.strokeRect(count, count, rect_size, rect_size);
//         if (state == "right") {
//           ++count;
//         } else {
//           --count;
//         }
//         setTimeout(loop, 1000 / 30);
//       }
//     })()
//   }, 0);
// }


// const set_video = (src, id, loop, autoplay, controls) => {
//   var video = document.getElementById(id);
//   video.src = src;
//   video.loop = loop;
//   video.autoplay = autoplay;
//   video.controls = controls;
//   video.width = 1000;
//   video.height = 1000;
// }