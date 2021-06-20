export function install_LGraphTask(vm, litegraph) {
    var vm = vm;
    var LiteGraph = litegraph;

    function LGraphTask(title) {
        this.taskColors = {};
        this.taskColors.selectedColor = "rgb(143, 213, 131)"; // green lighten
        this.taskColors.hoverColor    = "rgb(94, 149, 237)"; // blue lighten
        this.taskColors.defaultColor  = "rgb(228, 205, 92)"; // yellow small darken
        this.taskColors.otherColor    = "rgb(105, 238, 168)"; // green-dark
        this._ctor(title);
    }

    vm.LGraphTask = LiteGraph.LGraphTask = LGraphTask;

    LGraphTask.prototype._ctor = function(title) {
        // this.title = title || { ko: vm.$t('task'), en: vm.$t('task') };
        this.title = title || 'Task';

        this.name = "task";
        this.type = "task";
        this.font_size = 24;
        this.color = this.taskColors.defaultColor;
        // if (this.title.toLowerCase() === "task") {
        //     this.color = defaultColor;
        // } else {
        //     this.color = otherColor;
        // }
        // this.color = LGraphCanvas.node_colors.pale_blue ? LGraphCanvas.node_colors.pale_blue.groupcolor : "#AAA";
        this._bounding = new Float32Array([10, 10, 140, 80]);
        this._pos = this._bounding.subarray(0, 2);
        this._size = this._bounding.subarray(2, 4);
        this._nodes = [];
        this.graph = null;

        this.selected = false;

        this.initProperties();

        // Mouse Event.
        if (vm) {
            this.onSelected = () => {
                this.color = this.taskColors.selectedColor;
                this.selected = true;
                vm.onSelectTask(this);
            }
            this.onDeselected = () => {
                this.color = this.taskColors.defaultColor
                this.selected = false;
                vm.onDeselectTask();
            }
            this.onMouseDown = () => {
                // if (this.task_id != -1) {
                //     this.before_pos = cloneObject(this.pos);
                // }
            }
            this.onMouseEnter = () => {
                if (!this.selected) {
                    this.color = this.taskColors.hoverColor;
                }
            }
            this.onMouseLeave = () => {
                if (!this.selected) {
                    this.color = this.taskColors.defaultColor;
                }
            }
        }

        Object.defineProperty(this, "pos", {
            set: function(v) {
                if (!v || v.length < 2)
                    return;
                this._pos[0] = v[0];
                this._pos[1] = v[1];
            },
            get: function() {
                return this._pos;
            },
            enumerable: true
        });

        Object.defineProperty(this, "size", {
            set: function(v) {
                if (!v || v.length < 2)
                    return;
                this._size[0] = Math.max(140, v[0]);
                this._size[1] = Math.max(80, v[1]);
            },
            get: function() {
                return this._size;
            },
            enumerable: true
        });
    }

    LGraphTask.prototype.initProperties = function () {
        // var url = {
        //     "name": "url",
        //     "type": "str",
        //     "required": false,
        //     "get": true,
        //     "set": true,
        //     "valid": "",
        //     "value": "",
        //     "default": ""
        // }

        var recv_timeout_ms = {
            "title": {
                ko: "리시브 타임아웃 (ms)",
                en: "Receive Timeout (ms)"
            },
            "help": {
                ko: "리시브 타임아웃 값을 밀리초 단위로 설정한다.",
                en: "Set the Receive Timeout value in milliseconds."
            },
            "name": "recv_timeout_ms",
            "type": "int",
            "required": false,
            "rule": "read_and_write",
            "valid": "",
            "value": -1,
            "default_value": -1
        }
        var send_timeout_ms = {
            "title": {
                ko: "샌드 타임아웃 (ms)",
                en: "Send Timeout (ms)"
            },
            "help": {
                ko: "샌드 타임아웃 값을 밀리초 단위로 설정한다.",
                en: "Set the Send Timeout value in milliseconds."
            },
            "name": "send_timeout_ms",
            "type": "int",
            "required": false,
            "rule": "read_and_write",
            "valid": "",
            "value": -1,
            "default_value": -1
        }
        var resurrection = {
            "title": {
                ko: "재실행",
                en: "Resurrection"
            },
            "help": {
                ko: "태스크가 죽었을 시 다시 실행하겠습니까?",
                en: "Do you want to run the task again when it dies?"
            },
            "name": "resurrection",
            "type": "bool",
            "required": false,
            "rule": "read_and_write",
            "valid": "",
            "value": false,
            "default_value": false
        }

        // var trigger_type = {
        //     "title": {
        //         ko: "트리거 타입",
        //         en: "Trigger Type"
        //     },
        //     "help": {
        //         ko: "",
        //         en: ""
        //     },
        //     "name": "trigger_type",
        //     "type": "str",
        //     "required": false,
        //     "rule": "read_and_write",
        //     "valid": {list: "null;count_down;infinity"},
        //     "value": "infinity",
        //     "default_value": "infinity"
        // }
        // var trigger_value = {
        //     "title": {
        //         ko: "트리거 값",
        //         en: "Trigger Value"
        //     },
        //     "help": {
        //         ko: "",
        //         en: ""
        //     },
        //     "name": "trigger_value",
        //     "type": "str",
        //     "required": false,
        //     "rule": "read_and_write",
        //     "valid": "",
        //     "value": "",
        //     "default_value": ""
        // }
        // var trigger_signal = {
        //     "title": {
        //         ko: "트리거 신호",
        //         en: "Trigger Signal"
        //     },
        //     "name": "trigger_signal",
        //     "type": "str",
        //     "required": false,
        //     "rule": "read_and_write",
        //     "valid": "",
        //     "value": "",
        //     "default_value": ""
        // }

        // var log_severity = {
        //     "name": "log_severity",
        //     "type": "str",
        //     "required": false,
        //     "get": true,
        //     "set": true,
        //     "valid": { "list": "debug;info;warning;error" },
        //     "value": "debug",
        //     "default": "debug"
        // }
        // var log_sink = {
        //     "name": "log_sink",
        //     "type": "str",
        //     "required": false,
        //     "get": true,
        //     "set": true,
        //     "valid": "",
        //     "value": "",
        //     "default": ""
        // }
        // var log_arguments = {
        //     "name": "log_arguments",
        //     "type": "str",
        //     "required": false,
        //     "get": true,
        //     "set": true,
        //     "valid": "",
        //     "value": "",
        //     "default": ""
        // }
        // var log_generator = {
        //     "name": "log_generator",
        //     "type": "str",
        //     "required": false,
        //     "get": true,
        //     "set": true,
        //     "valid": "",
        //     "value": "",
        //     "default": ""
        // }
        // var log_disable_subproc_stdout = {
        //     "name": "log_disable_subproc_stdout",
        //     "type": "bool",
        //     "required": false,
        //     "get": true,
        //     "set": true,
        //     "valid": "",
        //     "value": false,
        //     "default": false
        // }
        // var log_disable_subproc_stderr = {
        //     "name": "log_disable_subproc_stderr",
        //     "type": "bool",
        //     "required": false,
        //     "get": true,
        //     "set": true,
        //     "valid": "",
        //     "value": false,
        //     "default": false
        // }
        this.properties = [];
        // this.properties.push(url);
        this.properties.push(recv_timeout_ms);
        this.properties.push(send_timeout_ms);
        this.properties.push(resurrection);
        // this.properties.push(trigger_type);
        // this.properties.push(trigger_value);
        // this.properties.push(trigger_signal);
        // this.properties.push(log_severity);
        // this.properties.push(log_arguments);
        // this.properties.push(log_generator);
        // this.properties.push(log_sink);
        // this.properties.push(log_disable_subproc_stdout);
        // this.properties.push(log_disable_subproc_stderr);
    }

    LGraphTask.prototype.configure = function(o) {
        var canvas = null;
        if (this.graph.list_of_graphcanvas) {
            canvas = this.graph.list_of_graphcanvas[0].canvas;
        }

        if (o.title) {
            this.title = o.title;
        } else {
            this.title = "Task";
        }

        if (o.id) {
            this.id = o.id;
        }

        if (o.properties) {
            this.properties = o.properties;
        }

        if (o.ui_setting) {
            if (canvas && o.ui_setting.bounding) {
                if (!LiteGraph.isInt(o.ui_setting.bounding[0])) {
                    for (var i = 0; i < o.ui_setting.bounding.length; ++i) {
                        if (i % 2 === 0) {
                            o.ui_setting.bounding[i] = o.ui_setting.bounding[i] * canvas.width;
                        } else {
                            o.ui_setting.bounding[i] = o.ui_setting.bounding[i] * canvas.height;
                        }
                    }
                    this._bounding.set(o.ui_setting.bounding);
                } else {
                    this._bounding.set(o.ui_setting.bounding);
                }
            }
            if (o.ui_setting.color) {
                this.color = o.ui_setting.color;
            }
            if (o.ui_setting.font) {
                this.font = o.ui_setting.font;
            }
        } else {
            console.error("Task configure ui setting data is wrong.");
        }
        var all_nodes = this.graph._nodes;
        for (var i = 0; i < all_nodes.length; ++i) {
            var node = all_nodes[i];
            for (var index = 0; index < o.nodes.length; ++index) {
                if (node.id == o.nodes[index]) {
                    this._nodes.push(node);
                }
            }
        }
    }

    LGraphTask.prototype.serialize = function() {
        var canvas = null;
        if (this.graph.list_of_graphcanvas) {
            canvas = this.graph.list_of_graphcanvas[0].canvas;
        }

        var b = this._bounding;
        var nodes_id = [];
        for (var node in this._nodes) {
            nodes_id.push(this._nodes[node].id);
        }
        var serialize = {
            title: this.title,
            id: this.id,
            nodes: nodes_id
        };
        serialize.ui_setting = {};

        if (this.color) {
            serialize.ui_setting.color = this.color;
        }

        if (this.font) {
            serialize.ui_setting.font = this.font;
        }

        if (this.properties) {
            serialize.properties = this.properties;
        }

        if (canvas) {
            if (b) {
                serialize.ui_setting.bounding = [];
                serialize.ui_setting.bounding.push(Math.round(b[0]) / canvas.width);
                serialize.ui_setting.bounding.push(Math.round(b[1]) / canvas.height);
                serialize.ui_setting.bounding.push(Math.round(b[2]) / canvas.width);
                serialize.ui_setting.bounding.push(Math.round(b[3]) / canvas.height);
            } else {
                console.log("Bounding data is empty.");
            }
        } else {
            if (b) {
                serialize.ui_setting.bounding = [Math.round(b[0]), Math.round(b[1]), Math.round(b[2]), Math.round(b[3])];
            } else {
                console.log("Bounding data is empty.");
            }
        }

        return serialize;
    }

    LGraphTask.prototype.move = function(deltax, deltay, ignore_nodes) {
        this._pos[0] += deltax;
        this._pos[1] += deltay;
        if (ignore_nodes)
            return;
        for (var i = 0; i < this._nodes.length; ++i) {
            var node = this._nodes[i];
            node.pos[0] += deltax;
            node.pos[1] += deltay;
        }
    }

    /* unused recomputeInsideNodes.
    // LGraphGroup.prototype.recomputeInsideNodes = function() {
    //     this._nodes.length = 0;
    //     var nodes = this.graph._nodes;
    //     var node_bounding = new Float32Array(4);

    //     for (var i = 0; i < nodes.length; ++i) {
    //         var node = nodes[i];
    //         node.getBounding(node_bounding);
    //         if (!overlapBounding(this._bounding, node_bounding))
    //             continue; //out of the visible area
    //         this._nodes.push(node);
    //     }
    // }
    */

    LGraphTask.prototype.recomputeInsideNodes2 = function(task_index, node, mouse) {
        var task = this.graph.getGroupOnPos(mouse.canvasX, mouse.canvasY);
        if (task) {
            LiteGraph.LGraphCanvas.mvLambda(this, task, node);
        } else {
            var node_bounding = new Float32Array(4);
            node.getBounding(node_bounding);
            if (!LiteGraph.overlapBounding(this._bounding, node_bounding)) {
                for (var i = 0; i < this._nodes.length; ++i) {
                    if (this._nodes[i].id === node.id) {
                        LiteGraph.LGraphCanvas.preventMvLambda(node);
                    }
                }
            }
        }
        return;
        var node_bounding = new Float32Array(4);
        node.getBounding(node_bounding);
        if (!LiteGraph.overlapBounding(this._bounding, node_bounding)) {
            for (var i = 0; i < this._nodes.length; ++i) {
                if (this._nodes[i].id === node.id) {
                    LiteGraph.LGraphCanvas.checkOutTask(this, node);
                }
            }
        } else {
            if (this._nodes.length) {
                var isExisted = false;
                for (var i = 0; i < this._nodes.length; ++i) {
                    if (this._nodes[i].id === node.id) {
                        isExisted = true;
                    }
                }
                if (!isExisted && node.task_id === -1) {
                    LiteGraph.LGraphCanvas.checkInTask(this, node);
                }
            } else {
                this._nodes.length = 0;
                LiteGraph.LGraphCanvas.checkInTask(this, node);
            }
        }
    }

    LGraphTask.prototype.preventResizeForMinSize = function(move_x, move_y) {
        var nodes_max_x = -1;
        var nodes_max_y = -1;
        var empty_nodes_min_size = 100;
        for (var index = 0; index < this._nodes.length; ++index) {
            if (nodes_max_x < (this._nodes[index].pos[0] + this._nodes[index].size[0])) {
                nodes_max_x = (this._nodes[index].pos[0] + this._nodes[index].size[0] + 20);
            }
            if (nodes_max_y < (this._nodes[index].pos[1] + this._nodes[index].size[1])) {
                nodes_max_y = (this._nodes[index].pos[1] + this._nodes[index].size[1] + 20);
            }
        }

        if (nodes_max_x >= (this.pos[0] + move_x)) {
            /*empty*/
        } else {
            if (move_x < empty_nodes_min_size) {
                this.size[0] = empty_nodes_min_size;
            } else {
                this.size[0] = move_x;
            }
        }

        if (nodes_max_y >= (this.pos[1] + move_y)) {
            /*empty*/
        } else {
            if (move_y < empty_nodes_min_size) {
                this.size[1] = empty_nodes_min_size;
            } else {
                this.size[1] = move_y;
            }
        }
        this.computeInputSocket()
    }

    LGraphTask.prototype.isPointInside = function(x, y, margin, skip_title) {
        margin = margin || 0;

        var margin_top = this.graph && this.graph.isLive() ? 0 : 20;
        if (skip_title)
            margin_top = 0;
        if (this.flags && this.flags.collapsed) {
            //if ( distance([x,y], [this.pos[0] + this.size[0]*0.5, this.pos[1] + this.size[1]*0.5]) < LiteGraph.NODE_COLLAPSED_RADIUS)
            if (isInsideRectangle(x, y, this.pos[0] - margin, this.pos[1] - LiteGraph.NODE_TITLE_HEIGHT - margin, (this._collapsed_width || LiteGraph.NODE_COLLAPSED_WIDTH) + 2 * margin, LiteGraph.NODE_TITLE_HEIGHT + 2 * margin))
                return true;
        } else if ((this.pos[0] - 4 - margin) < x && (this.pos[0] + this.size[0] + 4 + margin) > x &&
            (this.pos[1] - margin_top - margin) < y && (this.pos[1] + this.size[1] + margin) > y)
            return true;
        return false;
    }

    LGraphTask.prototype.setDirtyCanvas = function(dirty_foreground, dirty_background) {
        if (!this.graph)
            return;
        this.graph.sendActionToCanvas("setDirty", [dirty_foreground, dirty_background]);
    }

    LGraphTask.prototype.computeInputSocket = function() {
        var inputsocket = null;
        for (var i in this._nodes) {
            if (this._nodes[i].title === " " && this._nodes[i].style === "static") {
                inputsocket = this._nodes[i];
                break;
            }
        }
        if (inputsocket == null) {
            return;
        }
        var inputsocket_x = null;
        var inputsocket_y = null;

        if (inputsocket.flags.horizontal == true) {
            inputsocket_x = (this.pos[0] + (this.size[0] / 2)) - (inputsocket.size[0] / 2);
            inputsocket_y = this.pos[1] + 20;
        } else if (inputsocket.flags.horizontal == false) {
            inputsocket_x = this.pos[0];
            inputsocket_y = (this.pos[1] + (this.size[1] / 2)) - (inputsocket.size[1] / 2);
        }

        if (inputsocket_x != null && inputsocket_y != null) {
            inputsocket.pos = [inputsocket_x, inputsocket_y];
        } else {
            inputsocket.pos = [this.pos[0], this.pos[1]];
        }
    }

    LGraphTask.prototype.taskComputeSize = function(node) {
        var compute = {};
        if (this.pos[0] <= node.pos[0]) {
            compute.leftright = "right";
            compute.h_gap = (node.pos[0] + node.size[0]) - (this.pos[0] + this.size[0]);
        } else {
            compute.leftright = "left";
            compute.h_gap = (this.pos[0]) - (node.pos[0]);
        }

        if (this.pos[1] <= node.pos[1] - 20) {
            compute.updown = "down";
            compute.v_gap = (node.pos[1] + node.size[1]) - (this.pos[1] + this.size[1]);
        } else {
            compute.updown = "up";
            compute.v_gap = (node.pos[1] - 20) - (this.pos[1]);
        }

        if (compute) {
            switch (compute.leftright) {
                case "right":
                    {
                        if (compute.h_gap <= 0) {
                            /*empty*/
                        } else {
                            this.size[0] += compute.h_gap;
                        }
                        break;
                    }
                case "left":
                    {
                        this.pos[0] = node.pos[0];
                        this.size[0] += compute.h_gap;
                        break;
                    }
                default:
                    {
                        /*empty*/
                        break;
                    }
            }
            switch (compute.updown) {
                case "up":
                    {
                        this.pos[1] = node.pos[1] - 20;
                        this.size[1] += compute.v_gap + 20;
                        break;
                    }
                case "down":
                    {
                        if (compute.v_gap <= 0) {
                            /*empty*/
                        } else {
                            this.size[1] += compute.v_gap;
                        }
                        break;
                    }
                default:
                    {
                        /*empty*/
                        break;
                    }
            }
        }
        // console.log("compute:", compute);
        this.computeInputSocket();
    }
}