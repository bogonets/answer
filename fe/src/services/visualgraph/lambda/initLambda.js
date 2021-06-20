var DEFAULT_TITLEBAR_COLOR = "rgba(33, 33, 33, 0.7)";
var DEFAULT_CONTENT_COLOR = "rgba(68, 68, 68, 0.6)";
var NO_TASK = -1;
var HORIZONTAL_MODE_HEIGHT = 20;
var lambdaColors = {};
lambdaColors.title = {};
lambdaColors.content = {};
// 색상은 무조건 rgb() or rgba() 형식을 가져야한다.
lambdaColors.title.defaultAlpha = "rgba(33, 33, 33, 0.7)";
lambdaColors.title.default      = "rgb(33, 33, 33)";
lambdaColors.content.defaultAlpha = "rgba(68, 68, 68, 0.7)";
lambdaColors.content.default = "rgb(68, 68, 68)";

lambdaColors.title.cyanAlpha      = "rgba(118, 216, 255, 0.7)"; // cyan
lambdaColors.title.whiteApha      = "rgba(255, 255, 255, 0.7)"; // white
lambdaColors.title.yellowAlpha    = "rgba(255, 240, 100, 0.7)"; // yellow
lambdaColors.title.greenDarkAlpha = "rgba(105, 238, 168, 0.7)"; // green-dark
lambdaColors.title.cyan           = "rgb(118, 216, 255)"; // cyan
lambdaColors.title.white          = "rgb(255, 255, 255)"; // white
lambdaColors.title.yellow         = "rgb(255, 240, 100)"; // yellow
lambdaColors.title.greenDark      = "rgb(105, 238, 168)"; // green-dark

lambdaColors.content.cyanAlpha      = "rgba(118, 216, 255, 0.7)"; // cyan
lambdaColors.content.whiteApha      = "rgba(255, 255, 255, 0.7)"; // white
lambdaColors.content.yellowAlpha    = "rgba(255, 240, 100, 0.7)"; // yellow
lambdaColors.content.greenDarkAlpha = "rgba(105, 238, 168, 0.7)"; // green-dark
lambdaColors.content.cyan           = "rgb(118, 216, 255)"; // cyan
lambdaColors.content.white          = "rgb(255, 255, 255)"; // white
lambdaColors.content.yellow         = "rgb(255, 240, 100)"; // yellow
lambdaColors.content.greenDark      = "rgb(105, 238, 168)"; // green-dark

function cloneObject(obj, target) {
    if (obj == null) return null;
    var r = JSON.parse(JSON.stringify(obj));
    if (!target) return r;

    for (var i in r)
        target[i] = r[i];
    return target;
}

function invertColor(color) {
    if (typeof color !== 'string') {
        console.warn('Not string. Input type is ', typeof color);
        return;
    }
    var head = color.substring(0, 4);
    if (head === 'rgba') {
        var step1 = color.split("(");
        var step2 = step1[step1.length - 1].split(")");
        var step3 = step2[0].split(",");
        var result = head + "(";
        for (var index = 0; index < step3.length - 1; ++index) {
            var n = 255 - Number(step3[index]);
            result += n + ",";
        }
        result += Number(step3[step3.length - 1]) + ")";
        return result;
    } else if (head === 'rgb(') {
        var step1 = color.split("(");
        var step2 = step1[step1.length - 1].split(")");
        var step3 = step2[0].split(",");
        var result = head;
        for (var index = 0; index < step3.length - 1; ++index) {
            var n = 255 - Number(step3[index]);
            result += n + ",";
        }
        result += (255 - Number(step3[step3.length - 1])) + ")";
        return result;
    }
}

export function initialize(self, vm) {
    // box setting.
    if (self.box_data) {
        self.title = self.box_data.info.titles[vm.$store.getters['language/getLanguage']] || self.box_data.info.name;
        if (self.box_data.info) {
            self.info = self.box_data.info;
        }
    
        if (self.box_data.props) {
            self.box_data.props.forEach(prop => {
                if (prop.value === null || prop.value === undefined) {
                    if (prop.default_value) {
                        prop.value = prop.default_value;
                    }
                }
            })
            self.properties = self.box_data.props.slice();
        }

        if (self.box_data.controls) {
            var ctrls = self.box_data.controls;
            if (ctrls.input) {
                var inputs = ctrls.input;
                if (inputs.dynamic !== null && inputs.dynamic !== undefined) {
                    self.dynamicInputSlot = inputs.dynamic;
                } else {
                    self.dynamicInputSlot = false;
                }
                if (inputs.list) {
                    if (inputs.list.length > 0) {
                        for (let index = 0; index < inputs.list.length; ++index) {
                            self.addInput(inputs.list[index].name, inputs.list[index].mimes, true, null);
                        }
                    }
                }
                if (inputs.method !== null && inputs.method !== undefined) {
                    self.inputMethod = inputs.method;
                } else {
                    self.inputMethod = "";
                }
            }
            if (ctrls.output) {
                var outputs = ctrls.output;
                if (outputs.dynamic !== null && outputs.dynamic !== undefined) {
                    self.dynamicOutputSlot = outputs.dynamic;
                } else {
                    self.dynamicOutputsSlot = false;
                }
                if (outputs.list) {
                    if (outputs.list.length > 0) {
                        for (let index = 0; index < outputs.list.length; ++index) {
                            self.addOutput(outputs.list[index].name, outputs.list[index].mimes, true, null);
                        }
                    }
                }
                if (outputs.method !== null && outputs.method !== undefined) {
                    self.outputMethod = outputs.method;
                } else {
                    self.outputMethod = "";
                }
            }

        }
    }

    if (!self.edge) {
        self.edge = "";
    }

    /* UI SETTING ZONE */
    // color setting.
    self.color = lambdaColors.title.defaultAlpha;
    self.bgcolor = lambdaColors.content.defaultAlpha;

    self.title_color = invertColor(self.color);
    // size setting.
    self.size = self.computeSize();
    self.horizontal_height = HORIZONTAL_MODE_HEIGHT;

    // widgets serialize setting.
    self.serialize_widgets = true;

    // flag option setting.
    self.flags = {};
    self.flags.horizontal = true;
    self.flags.collapsed = false;
    self.flags.pinned = false;

    self.shape = 1;


    // init group id.
    self.task_id = NO_TASK; // no group status (value -1).

    // Set height according to type.
    if (self.flags.horizontal) {
        self.size[1] = self.horizontal_height; // height;
    }

    // transfer events to Vue.
    if (vm) {
        self.onMouseDown = () => {
            if (self.task_id != -1) {
                self.before_pos = cloneObject(self.pos);
            }
        }
        self.onMouseEnter = () => {
            if (self.graph) {
                self.graph.list_of_graphcanvas[0].canvas.className = "lgraphcanvas-innode"
            }
        }
        self.onMouseLeave = () => {
            if (self.graph) {
                self.graph.list_of_graphcanvas[0].canvas.className = "lgraphcanvas"
            }
        }
        self.onSelected = () => {
            vm.onSelectLambda(self);
        }
        self.onDeselected = () => {
            vm.onDeselectLambda();
        },
        self.onResizeStop = () => {
            var task = self.getJoinedTask();
            var node_right_bottom = [self.pos[0] + self.size[0], self.pos[1] + self.size[1]];
            if (task.pos[0] < node_right_bottom[0] && task.pos[1] < node_right_bottom[1] && task.pos[0] + task.size[0] > node_right_bottom[0] && task.pos[1] + task.size[1] > node_right_bottom[1]) {

            } else {
                self.computeSize();
                self.pos = [task.pos[0] + 10, task.pos[1] + 10];
            }
        }
    } else {
        console.warn("This Box is not exists Event. vm is", vm);
    }
}