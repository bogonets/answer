 //*********************************************************************************
 // LGraph CLASS
 //*********************************************************************************

 /**
  * LGraph is the class that contain a full graph. We instantiate one and add nodes to it, and then we can run the execution loop.
  *
  * @class LGraph
  * @constructor
  * @param {Object} o data from previous serialization [optional]
  */
 var STATUS_STOPPED = 1;
 var STATUS_RUNNING = 2;

 export function install_LGraph(vm, litegraph) {
     var vm = vm;
     var LiteGraph = litegraph;
     var LGraphCanvas = null;

     function LGraph(config) {
         if (LiteGraph.debug)
             console.log("Graph created");
         this.list_of_graphcanvas = null;
         this.clear();

         if (config)
             this.configure(config);
         this.supported_types = ["number", "string", "boolean"];
         this.vm = vm;
     }
     vm.LGraph = LiteGraph.LGraph = LGraph;

     //used to know which types of connections support this graph (some graphs do not allow certain types)
     LGraph.prototype.getSupportedTypes = function() { return this.supported_types }

     /**
      * Removes all nodes from this graph
      * @method clear
      */

     LGraph.prototype.clear = function() {
         this.stop();
         this.status = STATUS_STOPPED;

         this.last_node_id = 1;
         this.last_link_id = 1;

         this._version = -1; //used to detect changes

         //node onRemove Event.
         if (this._nodes) {
            for (var i = 0; i < this._nodes.length; ++i) {
                var node = this._nodes[i];
                if (node.onRemoved) {
                   node.onRemoved();
                }
            }
         }

        //task onRemove event.
        if (this._tasks) {
            for (var i = 0; i < this._tasks.length; ++i) {
                var task = this._tasks[i];
                if (task.onRemoved) {
                    task.onRemoved();
                }
            }
        }

         //nodes
         this._nodes = [];
         this._nodes_by_id = {};
         this._nodes_in_order = []; //nodes that are executable sorted in execution order
         this._nodes_executable = null; //nodes that contain onExecute

         //other scene stuff
         //  this._groups = []; // now unuse. task instead to group.
         this._tasks = [];

         //links
         this.links = {}; //container with all the links

         //Remove cache data
        //  this._remove_tasks = [];
        //  this._remove_nodes = [];

         //iterations
         this.iteration = 0;

         //custom data
         this.config = {};

         //timing
         this.globaltime = 0;
         this.runningtime = 0;
         this.fixedtime = 0;
         this.fixedtime_lapse = 0.01;
         this.elapsed_time = 0.01;
         this.last_update_time = 0;
         this.starttime = 0;

         this.catch_errors = true;

         //subgraph_data
         this.global_inputs = {};
         this.global_outputs = {};

         //notify canvas to redraw
         this.change();

         this.sendActionToCanvas("clear");
     }

     /**
      * Attach Canvas to this graph
      * @method attachCanvas
      * @param {GraphCanvas} graph_canvas
      */

     LGraph.prototype.attachCanvas = function(graphcanvas) {
         //  if (graphcanvas.constructor != LGraphCanvas)
         //      throw ("attachCanvas expects a LGraphCanvas instance");
         //  if (graphcanvas.graph && graphcanvas.graph != this)
         //      graphcanvas.graph.detachCanvas(graphcanvas);

         graphcanvas.graph = this;
         if (!this.list_of_graphcanvas)
             this.list_of_graphcanvas = [];
         this.list_of_graphcanvas.push(graphcanvas);
     }

     /**
      * Detach Canvas from this graph
      * @method detachCanvas
      * @param {GraphCanvas} graph_canvas
      */
     LGraph.prototype.detachCanvas = function(graphcanvas) {
         if (!this.list_of_graphcanvas)
             return;

         var pos = this.list_of_graphcanvas.indexOf(graphcanvas);
         if (pos == -1)
             return;
         graphcanvas.graph = null;
         this.list_of_graphcanvas.splice(pos, 1);
     }

     /**
      * Starts running this graph every interval milliseconds.
      * @method start
      * @param {number} interval amount of milliseconds between executions, if 0 then it renders to the monitor refresh rate
      */

     LGraph.prototype.start = function(interval) {
         if (this.status == STATUS_RUNNING) {
             return;
         }
         this.status = STATUS_RUNNING;

         if (this.onPlayEvent) {
             this.onPlayEvent();
         }

         this.sendEventToAllNodes("onStart");

         //launch
         this.starttime = LiteGraph.getTime.call();
         this.last_update_time = this.starttime;
         interval = interval || 0;
         var that = this;

         if (interval == 0 && typeof(window) != "undefined" && window.requestAnimationFrame) {
             function on_frame() {
                 if (that.execution_timer_id != -1)
                     return;
                 window.requestAnimationFrame(on_frame);
                 that.runStep(1, !that.catch_errors);
             }
             this.execution_timer_id = -1;
             on_frame();
         } else
             this.execution_timer_id = setInterval(function() {
                 //execute
                 that.runStep(1, !that.catch_errors);
             }, interval);
     }

     /**
      * Stops the execution loop of the graph
      * @method stop execution
      */

     LGraph.prototype.stop = function() {
         if (this.status == STATUS_STOPPED)
             return;

         this.status = STATUS_STOPPED;

         if (this.onStopEvent)
             this.onStopEvent();

         if (this.execution_timer_id != null) {
             if (this.execution_timer_id != -1)
                 clearInterval(this.execution_timer_id);
             this.execution_timer_id = null;
         }

         this.sendEventToAllNodes("onStop");
     }

     /**
      * Run N steps (cycles) of the graph
      * @method runStep
      * @param {number} num number of steps to run, default is 1
      */

     LGraph.prototype.runStep = function(num, do_not_catch_errors) {
         num = num || 1;

         var start = LiteGraph.getTime();
         this.globaltime = 0.001 * (start - this.starttime);

         var nodes = this._nodes_executable ? this._nodes_executable : this._nodes;
         if (!nodes)
             return;

         if (do_not_catch_errors) {
             //iterations
             for (var i = 0; i < num; i++) {
                 for (var j = 0, l = nodes.length; j < l; ++j) {
                     var node = nodes[j];
                     if (node.mode == LiteGraph.ALWAYS && node.onExecute)
                         node.onExecute();
                 }

                 this.fixedtime += this.fixedtime_lapse;
                 if (this.onExecuteStep)
                     this.onExecuteStep();
             }

             if (this.onAfterExecute)
                 this.onAfterExecute();
         } else {
             try {
                 //iterations
                 for (var i = 0; i < num; i++) {
                     for (var j = 0, l = nodes.length; j < l; ++j) {
                         var node = nodes[j];
                         if (node.mode == LiteGraph.ALWAYS && node.onExecute)
                             node.onExecute();
                     }

                     this.fixedtime += this.fixedtime_lapse;
                     if (this.onExecuteStep)
                         this.onExecuteStep();
                 }

                 if (this.onAfterExecute)
                     this.onAfterExecute();
                 this.errors_in_execution = false;
             } catch (err) {
                 this.errors_in_execution = true;
                 if (LiteGraph.throw_errors)
                     throw err;
                 if (LiteGraph.debug)
                     console.log("Error during execution: " + err);
                 this.stop();
             }
         }

         var now = LiteGraph.getTime();
         var elapsed = now - start;
         if (elapsed == 0)
             elapsed = 1;
         this.execution_time = 0.001 * elapsed;
         this.globaltime += 0.001 * elapsed;
         this.iteration += 1;
         this.elapsed_time = (now - this.last_update_time) * 0.001;
         this.last_update_time = now;
     }

     /**
      * Updates the graph execution order according to relevance of the nodes (nodes with only outputs have more relevance than
      * nodes with only inputs.
      * @method updateExecutionOrder
      */
     LGraph.prototype.updateExecutionOrder = function() {
         this._nodes_in_order = this.computeExecutionOrder(false);
         this._nodes_executable = [];
         for (var i = 0; i < this._nodes_in_order.length; ++i)
             if (this._nodes_in_order[i].onExecute)
                 this._nodes_executable.push(this._nodes_in_order[i]);
     }

     //This is more internal, it computes the order and returns it
     LGraph.prototype.computeExecutionOrder = function(only_onExecute, set_level) {
         var L = [];
         var S = [];
         var M = {};
         var visited_links = {}; //to avoid repeating links
         var remaining_links = {}; //to a

         //search for the nodes without inputs (starting nodes)
         for (var i = 0, l = this._nodes.length; i < l; ++i) {
             var node = this._nodes[i];
             if (only_onExecute && !node.onExecute)
                 continue;

             M[node.id] = node; //add to pending nodes

             var num = 0; //num of input connections
             if (node.inputs) {
                 for (var j = 0, l2 = node.inputs.length; j < l2; j++) {
                     if (node.inputs[j] && node.inputs[j].link != null && node.inputs[j].link != -1)
                         num += 1;
                 }
             }

             if (num == 0) //is a starting node
             {
                 S.push(node);
                 if (set_level)
                     node._level = 1;
             } else //num of input links
             {
                 if (set_level)
                     node._level = 0;
                 remaining_links[node.id] = num;
             }
         }

         while (true) {
             if (S.length == 0)
                 break;

             //get an starting node
             var node = S.shift();
             L.push(node); //add to ordered list
             delete M[node.id]; //remove from the pending nodes

             if (!node.outputs)
                 continue;

             //for every output
             for (var i = 0; i < node.outputs.length; i++) {
                 var output = node.outputs[i];
                 //not connected
                 if (output == null || output.links == null || output.links.length == 0)
                     continue;

                 //for every connection
                 for (var j = 0; j < output.links.length; j++) {
                     var link_id = output.links[j];
                     var link = this.links[link_id];
                     if (!link)
                         continue;

                     //already visited link (ignore it)
                     if (visited_links[link.id])
                         continue;

                     var target_node = this.getNodeById(link.target_id);
                     if (target_node == null) {
                         visited_links[link.id] = true;
                         continue;
                     }

                     if (set_level && (!target_node._level || target_node._level <= node._level))
                         target_node._level = node._level + 1;

                     visited_links[link.id] = true; //mark as visited
                     remaining_links[target_node.id] -= 1; //reduce the number of links remaining
                     if (remaining_links[target_node.id] == 0)
                         S.push(target_node); //if no more links, then add to starters array
                 }
             }
         }

         //the remaining ones (loops)
         for (var i in M)
             L.push(M[i]);

         if (L.length != this._nodes.length && LiteGraph.debug)
             console.warn("something went wrong, nodes missing");

         var l = L.length;

         //save order number in the node
         for (var i = 0; i < l; ++i)
             L[i].order = i;

         //sort now by priority
         L = L.sort(function(A, B) {
             var Ap = A.constructor.priority || A.priority || 0;
             var Bp = B.constructor.priority || B.priority || 0;
             if (Ap == Bp)
                 return A.order - B.order;
             return Ap - Bp;
         });

         //save order number in the node, again...
         for (var i = 0; i < l; ++i)
             L[i].order = i;

         return L;
     }

     /**
      * Returns all the nodes that could affect this one (ancestors) by crawling all the inputs recursively.
      * It doesnt include the node itself
      * @method getAncestors
      * @return {Array} an array with all the LGraphNodes that affect this node, in order of execution
      */
     LGraph.prototype.getAncestors = function(node) {
         var ancestors = [];
         var pending = [node];
         var visited = {};

         while (pending.length) {
             var current = pending.shift();
             if (!current.inputs)
                 continue;
             if (!visited[current.id] && current != node) {
                 visited[current.id] = true;
                 ancestors.push(current);
             }

             for (var i = 0; i < current.inputs.length; ++i) {
                 var input = current.getInputNode(i);
                 if (input && ancestors.indexOf(input) == -1) {
                     pending.push(input);
                 }
             }
         }

         ancestors.sort(function(a, b) { return a.order - b.order; });
         return ancestors;
     }

     /**
      * Positions every node in a more readable manner
      * @method arrange
      */
     LGraph.prototype.arrange = function(margin) {
         margin = margin || 40;

         var nodes = this.computeExecutionOrder(false, true);
         var columns = [];
         for (var i = 0; i < nodes.length; ++i) {
             var node = nodes[i];
             var col = node._level || 1;
             if (!columns[col])
                 columns[col] = [];
             columns[col].push(node);
         }

         var x = margin;

         for (var i = 0; i < columns.length; ++i) {
             var column = columns[i];
             if (!column)
                 continue;
             var max_size = 100;
             var y = margin;
             for (var j = 0; j < column.length; ++j) {
                 var node = column[j];
                 node.pos[0] = x;
                 node.pos[1] = y;
                 if (node.size[0] > max_size)
                     max_size = node.size[0];
                 y += node.size[1] + margin;
             }
             x += max_size + margin;
         }

         this.setDirtyCanvas(true, true);
     }


     /**
      * Returns the amount of time the graph has been running in milliseconds
      * @method getTime
      * @return {number} number of milliseconds the graph has been running
      */
     LGraph.prototype.getTime = function() {
         return this.globaltime;
     }

     /**
      * Returns the amount of time accumulated using the fixedtime_lapse var. This is used in context where the time increments should be constant
      * @method getFixedTime
      * @return {number} number of milliseconds the graph has been running
      */

     LGraph.prototype.getFixedTime = function() {
         return this.fixedtime;
     }

     /**
      * Returns the amount of time it took to compute the latest iteration. Take into account that this number could be not correct
      * if the nodes are using graphical actions
      * @method getElapsedTime
      * @return {number} number of milliseconds it took the last cycle
      */

     LGraph.prototype.getElapsedTime = function() {
         return this.elapsed_time;
     }

     /**
      * Sends an event to all the nodes, useful to trigger stuff
      * @method sendEventToAllNodes
      * @param {String} eventname the name of the event (function to be called)
      * @param {Array} params parameters in array format
      */

     LGraph.prototype.sendEventToAllNodes = function(eventname, params, mode) {
         mode = mode || LiteGraph.ALWAYS;

         var nodes = this._nodes_in_order ? this._nodes_in_order : this._nodes;
         if (!nodes)
             return;

         for (var j = 0, l = nodes.length; j < l; ++j) {
             var node = nodes[j];
             if (node[eventname] && node.mode == mode) {
                 if (params === undefined)
                     node[eventname]();
                 else if (params && params.constructor === Array)
                     node[eventname].apply(node, params);
                 else
                     node[eventname](params);
             }
         }
     }

     LGraph.prototype.sendActionToCanvas = function(action, params) {
         if (!this.list_of_graphcanvas)
             return;

         for (var i = 0; i < this.list_of_graphcanvas.length; ++i) {
             var c = this.list_of_graphcanvas[i];
             if (c[action])
                 c[action].apply(c, params);
         }
     }

     /**
      * Adds a new node instasnce to this graph
      * @method add
      * @param {LGraphNode} node the instance of the node
      */

     LGraph.prototype.add = function(node, skip_compute_order) {
         if (!node)
             return;

         //tasks
         if (node.constructor === LiteGraph.LGraphTask) {
             //give him an id
             if (node.id == null || node.id == -1)
                 node.id = ++this.last_task_id;
             else if (this.last_task_id < node.id)
                 this.last_task_id = node.id;
             this._tasks.push(node);
             this.setDirtyCanvas(true);
             this.change();
             node.graph = this;
             this._version++;
             return;
         }

         //nodes
         if (node.id != -1 && this._nodes_by_id[node.id] != null) {
             console.warn("LiteGraph: there is already a node with this ID, changing it");
             node.id = ++this.last_node_id;
         }

         if (this._nodes.length >= LiteGraph.MAX_NUMBER_OF_NODES)
             throw ("LiteGraph: max number of nodes in a graph reached");

         //give him an id
         if (node.id == null || node.id == -1)
             node.id = ++this.last_node_id;
         else if (this.last_node_id < node.id)
             this.last_node_id = node.id;

         node.graph = this;
         this._version++;

         this._nodes.push(node);
         this._nodes_by_id[node.id] = node;

         if (node.onAdded)
             node.onAdded(this);

         if (this.config.align_to_grid)
             node.alignToGrid();

         if (!skip_compute_order)
             this.updateExecutionOrder();

         if (this.onNodeAdded)
             this.onNodeAdded(node);


         this.setDirtyCanvas(true);
         this.change();

         return node; //to chain actions
     }

     /**
      * Removes a node from the graph
      * @method remove
      * @param {LGraphNode} node the instance of the node
      */

     LGraph.prototype.remove = function(node) {
         if (this.list_of_graphcanvas) {
            for (var i = 0; i < this.list_of_graphcanvas.length; ++i) {
                var c = this.list_of_graphcanvas[i];
                c.deselectedAll();
            }
         }

        if (node.constructor === LiteGraph.LGraphTask) {
            var index = this._tasks.indexOf(node);
            if (index != -1) {
                if(this._tasks[index]._nodes) {
                    var nodes = this._tasks[index]._nodes.slice();
                    for (var i = 0; i < nodes.length; ++i) {
                        this.remove(nodes[i]);
                    }
                } 
                this._tasks.splice(index, 1);
            }
            node.graph = null;
            this._version++;
            this.setDirtyCanvas(true, true);
            this.change();
            return;
        }

         if (this._nodes_by_id[node.id] == null)
             return; //not found

         if (node.ignore_remove)
             return; //cannot be removed

         //disconnect inputs
         if (node.inputs)
             for (var i = 0; i < node.inputs.length; i++) {
                 var slot = node.inputs[i];
                 if (slot.link != null || slot.link != -1)
                     node.disconnectInput(i);
             }

         //disconnect outputs
         if (node.outputs)
             for (var i = 0; i < node.outputs.length; i++) {
                 var slot = node.outputs[i];
                 if (slot.links != null && slot.links.length)
                     node.disconnectOutput(i);
             }

         //node.id = -1; //why?

         //callback
         if (node.onRemoved)
             node.onRemoved();

         node.graph = null;
         this._version++;

         //remove from canvas render
         if (this.list_of_graphcanvas) {
             for (var i = 0; i < this.list_of_graphcanvas.length; ++i) {
                 var canvas = this.list_of_graphcanvas[i];
                 if (canvas.selected_nodes[node.id])
                     delete canvas.selected_nodes[node.id];
                 if (canvas.node_dragged == node)
                     canvas.node_dragged = null;
             }
         }

         //remove from containers
        //  if (this._remove_nodes === null || this._remove_nodes === undefined) {
        //      this._remove_nodes = [];
        //  }
        //  if (node.status !== "new") {
        //      this._remove_nodes.push(node.id);
        //  }
         var pos = this._nodes.indexOf(node);
         if (pos != -1)
             this._nodes.splice(pos, 1);
         delete this._nodes_by_id[node.id];

         if (this.onNodeRemoved)
             this.onNodeRemoved(node);

         this.setDirtyCanvas(true, true);
         this.change();

         this.updateExecutionOrder();
     }

     /**
      * Returns a node by its id.
      * @method getNodeById
      * @param {Number} id
      */

     LGraph.prototype.getNodeById = function(id) {
         if (id == null)
             return null;
         return this._nodes_by_id[id];
     }

     /**
      * Returns a list of nodes that matches a class
      * @method findNodesByClass
      * @param {Class} classObject the class itself (not an string)
      * @return {Array} a list with all the nodes of this type
      */

     LGraph.prototype.findNodesByClass = function(classObject) {
         var r = [];
         for (var i = 0, l = this._nodes.length; i < l; ++i)
             if (this._nodes[i].constructor === classObject)
                 r.push(this._nodes[i]);
         return r;
     }

     /**
      * Returns a list of nodes that matches a type
      * @method findNodesByType
      * @param {String} type the name of the node type
      * @return {Array} a list with all the nodes of this type
      */

     LGraph.prototype.findNodesByType = function(type) {
         var type = type.toLowerCase();
         var r = [];
         for (var i = 0, l = this._nodes.length; i < l; ++i)
             if (this._nodes[i].type.toLowerCase() == type)
                 r.push(this._nodes[i]);
         return r;
     }

     /**
      * Returns a list of nodes that matches a name
      * @method findNodesByTitle
      * @param {String} name the name of the node to search
      * @return {Array} a list with all the nodes with this name
      */

     LGraph.prototype.findNodesByTitle = function(title) {
         var result = [];
         for (var i = 0, l = this._nodes.length; i < l; ++i)
             if (this._nodes[i].title == title)
                 result.push(this._nodes[i]);
         return result;
     }

     /**
      * Returns the top-most node in this position of the canvas
      * @method getNodeOnPos
      * @param {number} x the x coordinate in canvas space
      * @param {number} y the y coordinate in canvas space
      * @param {Array} nodes_list a list with all the nodes to search from, by default is all the nodes in the graph
      * @return {LGraphNode} the node at this position or null
      */
     LGraph.prototype.getNodeOnPos = function(x, y, nodes_list, margin) {
         nodes_list = nodes_list || this._nodes;
         for (var i = nodes_list.length - 1; i >= 0; i--) {
             var n = nodes_list[i];
             if (n.isPointInside(x, y, margin))
                 return n;
         }
         return null;
     }

     /**
      * Returns the top-most group in that position
      * @method getGroupOnPos
      * @param {number} x the x coordinate in canvas space
      * @param {number} y the y coordinate in canvas space
      * @return {LGraphTask} the task or null
      */
     LGraph.prototype.getGroupOnPos = function(x, y) {
         for (var i = this._tasks.length - 1; i >= 0; i--) {
             var g = this._tasks[i];
             if (g.isPointInside(x, y, 2, true))
                 return g;
         }
         return null;
     }

     // ********** GLOBALS *****************

     /**
      * Tell this graph it has a global graph input of this type
      * @method addGlobalInput
      * @param {String} name
      * @param {String} type
      * @param {*} value [optional]
      */
     LGraph.prototype.addGlobalInput = function(name, type, value) {
         this.global_inputs[name] = { name: name, type: type, value: value };
         this._version++;

         if (this.onGlobalInputAdded)
             this.onGlobalInputAdded(name, type);

         if (this.onGlobalsChange)
             this.onGlobalsChange();
     }

     /**
      * Assign a data to the global graph input
      * @method setGlobalInputData
      * @param {String} name
      * @param {*} data
      */
     LGraph.prototype.setGlobalInputData = function(name, data) {
         var input = this.global_inputs[name];
         if (!input)
             return;
         input.value = data;
     }

     /**
      * Assign a data to the global graph input (same as setGlobalInputData)
      * @method setInputData
      * @param {String} name
      * @param {*} data
      */
     LGraph.prototype.setInputData = LGraph.prototype.setGlobalInputData;


     /**
      * Returns the current value of a global graph input
      * @method getGlobalInputData
      * @param {String} name
      * @return {*} the data
      */
     LGraph.prototype.getGlobalInputData = function(name) {
         var input = this.global_inputs[name];
         if (!input)
             return null;
         return input.value;
     }

     /**
      * Changes the name of a global graph input
      * @method renameGlobalInput
      * @param {String} old_name
      * @param {String} new_name
      */
     LGraph.prototype.renameGlobalInput = function(old_name, name) {
         if (name == old_name)
             return;

         if (!this.global_inputs[old_name])
             return false;

         if (this.global_inputs[name]) {
             console.error("there is already one input with that name");
             return false;
         }

         this.global_inputs[name] = this.global_inputs[old_name];
         delete this.global_inputs[old_name];
         this._version++;

         if (this.onGlobalInputRenamed)
             this.onGlobalInputRenamed(old_name, name);

         if (this.onGlobalsChange)
             this.onGlobalsChange();
     }

     /**
      * Changes the type of a global graph input
      * @method changeGlobalInputType
      * @param {String} name
      * @param {String} type
      */
     LGraph.prototype.changeGlobalInputType = function(name, type) {
         if (!this.global_inputs[name])
             return false;

         if (this.global_inputs[name].type && this.global_inputs[name].type.toLowerCase() == type.toLowerCase())
             return;

         this.global_inputs[name].type = type;
         this._version++;
         if (this.onGlobalInputTypeChanged)
             this.onGlobalInputTypeChanged(name, type);
     }

     /**
      * Removes a global graph input
      * @method removeGlobalInput
      * @param {String} name
      * @param {String} type
      */
     LGraph.prototype.removeGlobalInput = function(name) {
         if (!this.global_inputs[name])
             return false;

         delete this.global_inputs[name];
         this._version++;

         if (this.onGlobalInputRemoved)
             this.onGlobalInputRemoved(name);

         if (this.onGlobalsChange)
             this.onGlobalsChange();
         return true;
     }

     /**
      * Creates a global graph output
      * @method addGlobalOutput
      * @param {String} name
      * @param {String} type
      * @param {*} value
      */
     LGraph.prototype.addGlobalOutput = function(name, type, value) {
         this.global_outputs[name] = { name: name, type: type, value: value };
         this._version++;

         if (this.onGlobalOutputAdded)
             this.onGlobalOutputAdded(name, type);

         if (this.onGlobalsChange)
             this.onGlobalsChange();
     }

     /**
      * Assign a data to the global output
      * @method setGlobalOutputData
      * @param {String} name
      * @param {String} value
      */
     LGraph.prototype.setGlobalOutputData = function(name, value) {
         var output = this.global_outputs[name];
         if (!output)
             return;
         output.value = value;
     }

     /**
      * Returns the current value of a global graph output
      * @method getGlobalOutputData
      * @param {String} name
      * @return {*} the data
      */
     LGraph.prototype.getGlobalOutputData = function(name) {
         var output = this.global_outputs[name];
         if (!output)
             return null;
         return output.value;
     }

     /**
      * Returns the current value of a global graph output (sames as getGlobalOutputData)
      * @method getOutputData
      * @param {String} name
      * @return {*} the data
      */
     LGraph.prototype.getOutputData = LGraph.prototype.getGlobalOutputData;


     /**
      * Renames a global graph output
      * @method renameGlobalOutput
      * @param {String} old_name
      * @param {String} new_name
      */
     LGraph.prototype.renameGlobalOutput = function(old_name, name) {
         if (!this.global_outputs[old_name])
             return false;

         if (this.global_outputs[name]) {
             console.error("there is already one output with that name");
             return false;
         }

         this.global_outputs[name] = this.global_outputs[old_name];
         delete this.global_outputs[old_name];
         this._version++;

         if (this.onGlobalOutputRenamed)
             this.onGlobalOutputRenamed(old_name, name);

         if (this.onGlobalsChange)
             this.onGlobalsChange();
     }

     /**
      * Changes the type of a global graph output
      * @method changeGlobalOutputType
      * @param {String} name
      * @param {String} type
      */
     LGraph.prototype.changeGlobalOutputType = function(name, type) {
         if (!this.global_outputs[name])
             return false;

         if (this.global_outputs[name].type && this.global_outputs[name].type.toLowerCase() == type.toLowerCase())
             return;

         this.global_outputs[name].type = type;
         this._version++;
         if (this.onGlobalOutputTypeChanged)
             this.onGlobalOutputTypeChanged(name, type);
     }

     /**
      * Removes a global graph output
      * @method removeGlobalOutput
      * @param {String} name
      */
     LGraph.prototype.removeGlobalOutput = function(name) {
         if (!this.global_outputs[name])
             return false;
         delete this.global_outputs[name];
         this._version++;

         if (this.onGlobalOutputRemoved)
             this.onGlobalOutputRemoved(name);

         if (this.onGlobalsChange)
             this.onGlobalsChange();
         return true;
     }

     LGraph.prototype.triggerInput = function(name, value) {
         var nodes = this.findNodesByTitle(name);
         for (var i = 0; i < nodes.length; ++i)
             nodes[i].onTrigger(value);
     }

     LGraph.prototype.setCallback = function(name, func) {
         var nodes = this.findNodesByTitle(name);
         for (var i = 0; i < nodes.length; ++i)
             nodes[i].setTrigger(func);
     }


     LGraph.prototype.connectionChange = function(node, link_info) {
         this.updateExecutionOrder();
         if (this.onConnectionChange)
             this.onConnectionChange(node);
         this._version++;
         this.sendActionToCanvas("onConnectionChange");
     }

     /**
      * returns if the graph is in live mode
      * @method isLive
      */

     LGraph.prototype.isLive = function() {
         if (!this.list_of_graphcanvas)
             return false;

         for (var i = 0; i < this.list_of_graphcanvas.length; ++i) {
             var c = this.list_of_graphcanvas[i];
             if (c.live_mode)
                 return true;
         }
         return false;
     }

     /**
      * clears the triggered slot animation in all links (stop visual animation)
      * @method clearTriggeredSlots
      */
     LGraph.prototype.clearTriggeredSlots = function() {
         for (var i in this.links) {
             var link_info = this.links[i];
             if (!link_info)
                 continue;
             if (link_info._last_time)
                 link_info._last_time = 0;
         }
     }


     /* Called when something visually changed (not the graph!) */
     LGraph.prototype.change = function() {
         if (LiteGraph.debug)
             console.log("Graph changed");
         this.sendActionToCanvas("setDirty", [true, true]);
         if (this.on_change)
             this.on_change(this);
     }

     LGraph.prototype.setDirtyCanvas = function(fg, bg) {
         this.sendActionToCanvas("setDirty", [fg, bg]);
     }

     //save and recover app state ***************************************
     /**
      * Creates a Object containing all the info about this graph, it can be serialized
      * @method serialize
      * @return {Object} value of the node
      */
     LGraph.prototype.serialize = function() {
         var nodes_info = [];
         for (var i = 0, l = this._nodes.length; i < l; ++i)
             nodes_info.push(this._nodes[i].serialize());

         //pack link info into a non-verbose format
         //  var links = [];
         //  for (var i in this.links) //links is an OBJECT
         //  {
         //      var link = this.links[i];
         //      links.push([link.id, link.origin_id, link.origin_slot, link.target_id, link.target_slot, link.type]);
         //  }
         var links = [];
         for (var key in this.links) {
             if (this.links[key]) {
                 links.push(this.links[key]);
             }
         }

         var tasks_info = [];
         for (var i = 0; i < this._tasks.length; ++i)
             tasks_info.push(this._tasks[i].serialize());

         var data = {
             //  last_node_id: this.last_node_id,
             //  last_link_id: this.last_link_id,
             nodes: nodes_info,
             links: links,
             tasks: tasks_info,
             //  config: this.config
         };

        //  if (this._remove_nodes) {
        //      if (this._remove_nodes.length !== 0) {
        //          data.remove_nodes = this._remove_nodes;
        //      }
        //  }

        //  if (this._remove_tasks) {
        //      if (this._remove_tasks.length !== 0) {
        //          data.remove_tasks = this._remove_tasks;
        //      }
        //  }

         return data;
     }


     /**
      * Configure a graph from a JSON string
      * @method configure
      * @param {String} str configure a graph from a JSON string
      * @param {Boolean} returns if there was any error parsing
      */
     LGraph.prototype.configure = function(data, keep_old) {
         if (!data)
             return;

         if (!keep_old)
             this.clear();

         var nodes = data.nodes;

         //decode links info (they are very verbose)
         if (data.links && data.links.constructor === Array) {
             var links = [];
             for (var i = 0; i < data.links.length; ++i) {
                 var link = data.links[i];
                 //give him an id
                 if (link.id == null)
                     link.id = ++this.last_link_id;
                 else if (this.last_link_id < link.id)
                     this.last_link_id = link.id;
                 // array links.
                 //  links[link[0]] = { id: link[0], origin_id: link[1], origin_slot: link[2], target_id: link[3], target_slot: link[4], type: link[5] };

                 // object links.
                 links[link.id] = link;
             }
             data.links = links;
         }

         //copy all stored fields
         for (var i in data)
             this[i] = data[i];

         var error = false;

         //create nodes
         this._nodes = [];
         if (nodes) {
             for (var i = 0, l = nodes.length; i < l; ++i) {
                 var n_info = nodes[i]; //stored info
                 var node = LiteGraph.createNode(n_info.type, n_info.name);
                 if (!node) {
                     vm.$error("LGraph.js", "Load saved node and task. " + n_info.type);
                     error = true;
                     continue;
                 }

                 node.id = n_info.id; //id it or it will create a new id
                 this.add(node, true); //add before configure, otherwise configure cannot create links
             }

             //configure nodes afterwards so they can reach each other
             for (var i = 0, l = nodes.length; i < l; ++i) {
                 var n_info = nodes[i];
                 var node = this.getNodeById(n_info.id);
                 if (node)
                     node.configure(n_info);
             }

            // remove break line
            //  var links = [];
            //  links = data.links;

            //  for(var index = 0; links.length; index++){
            //     for(var node in this._nodes){
            //         if(links[index].origin_id == node.id || links[index].target_id == node.id){
            //             break;
            //         }
            //         links.remove(index);
            //     }
            //  }
         }

         //groups
         //  this._groups.length = 0;
         //  if (data.groups)
         //      for (var i = 0; i < data.groups.length; ++i) {
         //          var group = new LiteGraph.LGraphTask();
         //          group.configure(data.groups[i]);
         //          this.add(group);
         //      }

         //tasks
         this._tasks.length = 0;
         if (data.tasks)
             for (var i = 0; i < data.tasks.length; ++i) {
                 var task = new LiteGraph.LGraphTask();
                 task.graph = this;
                 task.configure(data.tasks[i]);
                 this.add(task);
             }

         this.updateExecutionOrder();
         this._version++;
         this.setDirtyCanvas(true, true);
         return error;
     }

     LGraph.prototype.load = function(url) {
         var that = this;
         var req = new XMLHttpRequest();
         req.open('GET', url, true);
         req.send(null);
         req.onload = function(oEvent) {
             if (req.status !== 200) {
                 console.error("Error loading graph:", req.status, req.response);
                 return;
             }
             var data = JSON.parse(req.response);
             that.configure(data);
         }
         req.onerror = function(err) {
             console.error("Error loading graph:", err);
         }
     }

     LGraph.prototype.onNodeTrace = function(node, msg, color) {
         //TODO
     }

     LGraph.prototype.deselectedAll = function () {
        for (var i = 0; i < this.list_of_graphcanvas.length; ++i) {
            var c = this.list_of_graphcanvas[i];
            c.deselectedAll();
        }
     }
 }