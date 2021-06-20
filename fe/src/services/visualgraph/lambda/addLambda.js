var vm = null;
var DEFAULT_TITLEBAR_COLOR = "rgba(33, 33, 33, 0.7)";
var DEFAULT_CONTENT_COLOR = "rgba(68, 68, 68, 0.6)";
var NO_TASK = -1;
var HORIZONTAL_MODE_HEIGHT = 20;

function cloneObject(obj, target) {
    if (obj == null) return null;
    var r = JSON.parse(JSON.stringify(obj));
    if (!target) return r;

    for (var i in r)
        target[i] = r[i];
    return target;
}

// function InputSocket() {
//     this.title = "InputSocket";
//     this.addInput("in", "");

//     if (!this.edge) {
//         this.edge = "";
//     }

//     // color setting.
//     this.color = "rgba(33, 33, 33, 0.7)";
//     this.bgcolor = "rgba(68, 68, 68, 0.6)";

//     // size setting.
//     this.size = this.computeSize();
//     this.horizontal_height = HORIZONTAL_MODE_HEIGHT;

//     // widgets serialize setting.
//     this.serialize_widgets = true;

//     // flag option setting.
//     this.flags = {};
//     this.flags.horizontal = false;
//     this.flags.collapsed = false;
//     this.flags.pinned = false;

//     this.properties = [];
//     var url = {
//         "name": "url",
//         "type": "str",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": ""
//     }
//     var recv_timeout_ms = {
//         "name": "recv_timeout_ms",
//         "type": "int",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": ""
//     }
//     var send_timeout_ms = {
//         "name": "send_timeout_ms",
//         "type": "int",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": ""
//     }
//     var log_severity = {
//         "name": "log_severity",
//         "type": "str",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": ""
//     }
//     var log_sink = {
//         "name": "log_sink",
//         "type": "str",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": ""
//     }
//     var log_arguments = {
//         "name": "log_arguments",
//         "type": "str",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": ""
//     }
//     var log_generator = {
//         "name": "log_generator",
//         "type": "str",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": ""
//     }
//     var resurrection = {
//         "name": "resurrection",
//         "type": "bool",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": "",
//         "value": false
//     }
//     var trigger_type = {
//         "name": "trigger_type",
//         "type": "str",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": "",
//         "value": "infinity"
//     }
//     var trigger_value = {
//         "name": "trigger_value",
//         "type": "str",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": "",
//         "value": ""
//     }
//     var trigger_signal = {
//         "name": "trigger_signal",
//         "type": "str",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": "",
//         "value": ""
//     }
//     var log_disable_subproc_stdout = {
//         "name": "log_disable_subproc_stdout",
//         "type": "bool",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": "",
//         "value": false
//     }
//     var log_disable_subproc_stderr = {
//         "name": "log_disable_subproc_stderr",
//         "type": "bool",
//         "required": false,
//         "get": true,
//         "set": true,
//         "valid": "",
//         "value": false
//     }
//     this.properties.push(url);
//     this.properties.push(recv_timeout_ms);
//     this.properties.push(send_timeout_ms);
//     this.properties.push(log_severity);
//     this.properties.push(resurrection);
//     this.properties.push(log_arguments);
//     this.properties.push(log_generator);
//     this.properties.push(log_sink);
//     this.properties.push(trigger_type);
//     this.properties.push(trigger_value);
//     this.properties.push(trigger_signal);
//     this.properties.push(log_disable_subproc_stdout);
//     this.properties.push(log_disable_subproc_stderr);

//     // init group id.
//     this.task_id = -1;

//     // Set height according to type.
//     if (this.flags.horizontal) {
//         this.size[1] = this.horizontal_height; // height;
//     }

//     // transfer events to Vue.
//     if (vm) {
//         this.onMouseDown = () => {
//             // if (this.task_id != -1) {
//             //     this.before_pos = cloneObject(this.pos);
//             // }
//         }
//         this.onMouseEnter = () => {
//             if (this.graph) {
//                 this.graph.list_of_graphcanvas[0].canvas.className = "lgraphcanvas-innode"
//             }
//         }
//         this.onMouseLeave = () => {
//             if (this.graph) {
//                 this.graph.list_of_graphcanvas[0].canvas.className = "lgraphcanvas"
//             }
//         }
//         this.onSelected = () => {
//             vm.onSelectLambda(this);
//         }
//         this.onDeselected = () => {
//             vm.onDeselectLambda();
//         }
//     } else {
//         console.warn("This Box is not exists Event. vm is", vm);
//     }
// }

function makeCategory(template) {
    if (!template) {
        return null;
    }
    if (template.info) {
        if (template.info.category) {
            return template.info.category;
        } else {
            vm.$warn("addLambda.js", "makeCategory", "Not found category of info in template But return non-category");
            return 'non-category';
        }
    } else {
        return null;
    }
}

export const addLambda = (global, lambda_data) => {
    vm = global;
    var templates = lambda_data;
    for (var template of templates) {
        var category = makeCategory(template);
        if (category !== null && category !== undefined) {
            vm.LiteGraph.dynamicRegisterNodeType(category, template, vm);
        } else {
            vm.$error("addLambda.js", "makeCategory", "Not found info of template", template);
            continue;
        }
    }
    // legacy.
    // for (var key in data) {
    //     for (var index = 0; index < data[key].length; ++index) {
    //         vm.LiteGraph.dynamicRegisterNodeType(key, data[key][index], vm);
    //     }
    // }
    // vm.LiteGraph.staticRegisterNodeType("tail/inputsocket", InputSocket);
}