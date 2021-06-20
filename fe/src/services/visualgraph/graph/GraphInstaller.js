import { install_LiteGraph } from "./LiteGraph.js";
import { install_LGraph } from "./LGraph.js";
import { install_LGraphCanvas } from "./LGraphCanvas.js";
import { install_LGraphTask } from "./LGraphTask.js";
import { install_LGraphNode } from "./LGraphNode.js";

function initialize() {
    if (CanvasRenderingContext2D) {
        CanvasRenderingContext2D.prototype.roundRect = function(x, y, width, height, radius, radius_low) {
            if (radius === undefined) {
                radius = 5;
            }

            if (radius_low === undefined)
                radius_low = radius;

            this.moveTo(x + radius, y);
            this.lineTo(x + width - radius, y);
            this.quadraticCurveTo(x + width, y, x + width, y + radius);

            this.lineTo(x + width, y + height - radius_low);
            this.quadraticCurveTo(x + width, y + height, x + width - radius_low, y + height);
            this.lineTo(x + radius_low, y + height);
            this.quadraticCurveTo(x, y + height, x, y + height - radius_low);
            this.lineTo(x, y + radius);
            this.quadraticCurveTo(x, y, x + radius, y);
        }
    }
}

export function installGraph(vm) {
    initialize();
    var LiteGraph = install_LiteGraph(vm);
    install_LGraph(vm, LiteGraph);
    install_LGraphCanvas(vm, LiteGraph);
    install_LGraphTask(vm, LiteGraph);
    var LGraphNode = install_LGraphNode(vm, LiteGraph);
    LiteGraph.LGraphNode = LGraphNode;
}