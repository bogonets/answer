import { install_ContextMenu } from "@/services/visualgraph/graph/ContextMenu.js"
import { initialize } from "@/services/visualgraph/lambda/initLambda.js";
// *************************************************************
//   LiteGraph CLASS                                     *******
// *************************************************************

/* FYI: links are stored in graph.links with this structure per object
{
	id: number
	type: string,
	origin_id: number,
	origin_slot: number,
	target_id: number,
	target_slot: number,
	data: *
}; //it can contain color to colorize this particular link
*/

/**
 * The Global Scope. It contains all the registered node classes.
 *
 * @class LiteGraph
 * @constructor
 */
export function install_LiteGraph(vm) {
    var vm = vm;
    var LiteGraph = vm.LiteGraph = {
        CANVAS_GRID_SIZE: 10,

        NODE_TITLE_HEIGHT: 20,
        NODE_SLOT_HEIGHT: 15,
        NODE_WIDGET_HEIGHT: 20,
        NODE_WIDTH: 140,
        NODE_MIN_WIDTH: 50,
        NODE_COLLAPSED_RADIUS: 10,
        NODE_COLLAPSED_WIDTH: 80,
        NODE_TITLE_COLOR: "#999",
        NODE_TEXT_SIZE: 14,
        NODE_TEXT_COLOR: "#AAA",
        NODE_SUBTEXT_SIZE: 12,
        NODE_DEFAULT_COLOR: "#333",
        NODE_DEFAULT_BGCOLOR: "#444",
        NODE_DEFAULT_BOXCOLOR: "#666",
        NODE_DEFAULT_SHAPE: "box",
        DEFAULT_SHADOW_COLOR: "rgba(0,0,0,0.5)",
        DEFAULT_GROUP_FONT: 24,
        RESIZE_AREA_SIZE: 8, // resize threshold.

        LINK_COLOR: "#AAD",
        EVENT_LINK_COLOR: "#F85",
        CONNECTING_LINK_COLOR: "#AFA",

        MAX_NUMBER_OF_NODES: 1000, //avoid infinite loops
        DEFAULT_POSITION: [100, 100], //default node position
        VALID_SHAPES: ["default", "box", "round", "card"], //,"circle"

        //shapes are used for nodes but also for slots
        BOX_SHAPE: 1,
        ROUND_SHAPE: 2,
        CIRCLE_SHAPE: 3,
        CARD_SHAPE: 4,
        ARROW_SHAPE: 5,

        //enums
        INPUT: 1,
        OUTPUT: 2,

        EVENT: -1, //for outputs
        ACTION: -1, //for inputs

        ALWAYS: 0,
        ON_EVENT: 1,
        NEVER: 2,
        ON_TRIGGER: 3,

        UP: 1,
        DOWN: 2,
        LEFT: 3,
        RIGHT: 4,
        CENTER: 5,

        NORMAL_TITLE: 0,
        NO_TITLE: 1,
        TRANSPARENT_TITLE: 2,
        AUTOHIDE_TITLE: 3,

        proxy: null, //used to redirect calls
        node_images_path: "",

        debug: false,
        throw_errors: true,
        allow_scripts: false,
        registered_node_types: {}, //nodetypes by string
        node_types_by_file_extension: {}, //used for droping files in the canvas
        Nodes: {}, //node types by classname

        searchbox_extras: {}, //used to add extra features to the search box

        /**
         * Register a static node class so it can be listed when the user wants to create a new one
         * @method staticRegisterNodeType
         * @param {String} type name of the node and path
         * @param {Class} base_class class containing the structure of a node
         */

        staticRegisterNodeType: function(type, base_class) {
            if (!base_class.prototype)
                throw ("Cannot register a simple object, it must be a class with a prototype");
            base_class.type = type;

            if (LiteGraph.debug)
                console.log("Node registered: " + type);

            var categories = type.split("/");
            var classname = base_class.name;

            var pos = type.lastIndexOf("/");
            base_class.category = type.substr(0, pos);

            if (!base_class.title)
                base_class.title = classname;
            //info.name = name.substr(pos+1,name.length - pos);

            //extend class
            if (base_class.prototype) //is a class
                for (var i in this.LGraphNode.prototype)
                if (!base_class.prototype[i])
                    base_class.prototype[i] = this.LGraphNode.prototype[i];

            Object.defineProperty(base_class.prototype, "shape", {
                set: function(v) {
                    switch (v) {
                        case "default":
                            delete this._shape;
                            break;
                        case "box":
                            this._shape = LiteGraph.BOX_SHAPE;
                            break;
                        case "round":
                            this._shape = LiteGraph.ROUND_SHAPE;
                            break;
                        case "circle":
                            this._shape = LiteGraph.CIRCLE_SHAPE;
                            break;
                        case "card":
                            this._shape = LiteGraph.CARD_SHAPE;
                            break;
                        default:
                            this._shape = v;
                    }
                },
                get: function(v) {
                    return this._shape;
                },
                enumerable: true,
                configurable: true
            });

            this.registered_node_types[type] = base_class;
            if (base_class.constructor.name)
                this.Nodes[classname] = base_class;

            //warnings
            if (base_class.prototype.onPropertyChange)
                console.warn("LiteGraph node class " + type + " has onPropertyChange method, it must be called onPropertyChanged with d at the end");

            if (base_class.supported_extensions) {
                for (var i in base_class.supported_extensions)
                    this.node_types_by_file_extension[base_class.supported_extensions[i].toLowerCase()] = base_class;
            }
        },

        /**
         * Register a dynamic node class so it can be listed when the user wants to create a new one
         * @method dynamicRegisterNodeType
         * @param {String} type name of the node and path
         * @param {Class} base_class class containing the structure of a node
         */

        dynamicRegisterNodeType: function(category, lambda_data, global) {
            var that = this;

            function base_class() {
                if (lambda_data) {
                    this.box_data = that.cloneObject(lambda_data);
                }
                initialize(this, global);
            }
            if (!base_class.prototype)
                throw ("Cannot register a simple object, it must be a class with a prototype");
            base_class.type = category + "/" + lambda_data.info.name;

            if (LiteGraph.debug)
                console.log("Node registered: " + base_class.type);

            var categories = category;
            var classname = lambda_data.info.name;

            // var pos = type.lastIndexOf("/");
            // base_class.category = type.substr(0, pos);
            base_class.category = category;

            if (!base_class.title)
                base_class.title = classname;
            //info.name = name.substr(pos+1,name.length - pos);

            if (lambda_data) {
                if (lambda_data.info) {
                    if (lambda_data.info.titles) {
                        base_class.titles = this.cloneObject(lambda_data.info.titles);
                    }
                }
            }

            //extend class
            if (base_class.prototype) //is a class
                for (var i in this.LGraphNode.prototype)
                if (!base_class.prototype[i])
                    base_class.prototype[i] = this.LGraphNode.prototype[i];

            Object.defineProperty(base_class.prototype, "shape", {
                set: function(v) {
                    switch (v) {
                        case "default":
                            delete this._shape;
                            break;
                        case "box":
                            this._shape = LiteGraph.BOX_SHAPE;
                            break;
                        case "round":
                            this._shape = LiteGraph.ROUND_SHAPE;
                            break;
                        case "circle":
                            this._shape = LiteGraph.CIRCLE_SHAPE;
                            break;
                        case "card":
                            this._shape = LiteGraph.CARD_SHAPE;
                            break;
                        default:
                            this._shape = v;
                    }
                },
                get: function(v) {
                    return this._shape;
                },
                enumerable: true,
                configurable: true
            });

            this.registered_node_types[base_class.type] = base_class;
            if (base_class.constructor.name)
                this.Nodes[classname] = base_class;

            //warnings
            if (base_class.prototype.onPropertyChange)
                console.warn("LiteGraph node class " + type + " has onPropertyChange method, it must be called onPropertyChanged with d at the end");

            if (base_class.supported_extensions) {
                for (var i in base_class.supported_extensions)
                    this.node_types_by_file_extension[base_class.supported_extensions[i].toLowerCase()] = base_class;
            }
        },

        /**
         * Create a new node type by passing a function, it wraps it with a propper class and generates inputs according to the parameters of the function.
         * Useful to wrap simple methods that do not require properties, and that only process some input to generate an output.
         * @method wrapFunctionAsNode
         * @param {String} name node name with namespace (p.e.: 'math/sum')
         * @param {Function} func
         * @param {Array} param_types [optional] an array containing the type of every parameter, otherwise parameters will accept any type
         * @param {String} return_type [optional] string with the return type, otherwise it will be generic
         */
        wrapFunctionAsNode: function(name, func, param_types, return_type) {
            var params = Array(func.length);
            var code = "";
            var names = LiteGraph.getParameterNames(func);
            for (var i = 0; i < names.length; ++i)
                code += "this.addInput('" + names[i] + "'," + (param_types && param_types[i] ? "'" + param_types[i] + "'" : "0") + ");\n";
            code += "this.addOutput('out'," + (return_type ? "'" + return_type + "'" : 0) + ");\n";
            var classobj = Function(code);
            classobj.title = name.split("/").pop();
            classobj.desc = "Generated from " + func.name;
            classobj.prototype.onExecute = function onExecute() {
                for (var i = 0; i < params.length; ++i)
                    params[i] = this.getInputData(i);
                var r = func.apply(this, params);
                this.setOutputData(0, r);
            }
            this.registerNodeType(name, classobj);
        },

        /**
         * Adds this method to all nodetypes, existing and to be created
         * (You can add it to LGraphNode.prototype but then existing node types wont have it)
         * @method addNodeMethod
         * @param {Function} func
         */
        addNodeMethod: function(name, func) {
            LGraphNode.prototype[name] = func;
            for (var i in this.registered_node_types) {
                var type = this.registered_node_types[i];
                if (type.prototype[name])
                    type.prototype["_" + name] = type.prototype[name]; //keep old in case of replacing
                type.prototype[name] = func;
            }
        },

        /**
         * Create a node of a given type with a name. The node is not attached to any graph yet.
         * @method createNode
         * @param {String} type full name of the node class. p.e. "math/sin"
         * @param {String} name a name to distinguish from other nodes
         * @param {Object} options to set options
         */

        createNode: function(type, title, options) {
            var base_class = this.registered_node_types[type];
            if (!base_class) {
                vm.$error("LiteGraph.js", "createNode", "GraphNode type \"" + type + "\" not registered.");
                return null;
            }

            var prototype = base_class.prototype || base_class;

            title = title || base_class.title || type;

            var node = new base_class(title);
            node.type = type;
            node.shapes = LiteGraph.VALID_SHAPES.slice();

            if (!node.title && title) node.title = title;
            if (!node.properties) node.properties = {};
            if (!node.properties_info) node.properties_info = [];
            if (!node.flags) node.flags = {};
            if (!node.size) node.size = node.computeSize();
            if (!node.pos) node.pos = LiteGraph.DEFAULT_POSITION.concat();
            if (!node.mode) node.mode = LiteGraph.ALWAYS;

            //extra options
            if (options) {
                for (var i in options)
                    node[i] = options[i];
            }

            return node;
        },

        /**
         * Returns a registered node type with a given name
         * @method getNodeType
         * @param {String} type full name of the node class. p.e. "math/sin"
         * @return {Class} the node class
         */

        getNodeType: function(type) {
            return this.registered_node_types[type];
        },


        /**
         * Returns a list of node types matching one category
         * @method getNodeType
         * @param {String} category category name
         * @return {Array} array with all the node classes
         */

        getNodeTypesInCategory: function(category, filter) {
            var r = [];
            for (var i in this.registered_node_types) {
                var type = this.registered_node_types[i];
                if (filter && type.filter && type.filter != filter)
                    continue;

                if (category == "") {
                    if (type.category == null)
                        r.push(type);
                } else if (type.category == category)
                    r.push(type);
            }

            // sort in result
            r = r.sort((a,b) => a.title > b.title);
            return r;
        },

        /**
         * Returns a list with all the node type categories
         * @method getNodeTypesCategories
         * @return {Array} array with all the names of the categories
         */

        getNodeTypesCategories: function() {
            var categories = { "": 1 };
            for (var i in this.registered_node_types)
                if (this.registered_node_types[i].category && !this.registered_node_types[i].skip_list)
                    categories[this.registered_node_types[i].category] = 1;
            var result = [];
            for (var i in categories)
                result.push(i);

            // sort in result
            result = result.sort();
            return result;
        },

        //debug purposes: reloads all the js scripts that matches a wilcard
        reloadNodes: function(folder_wildcard) {
            var tmp = document.getElementsByTagName("script");
            //weird, this array changes by its own, so we use a copy
            var script_files = [];
            for (var i in tmp)
                script_files.push(tmp[i]);


            var docHeadObj = document.getElementsByTagName("head")[0];
            folder_wildcard = document.location.href + folder_wildcard;

            for (var i in script_files) {
                var src = script_files[i].src;
                if (!src || src.substr(0, folder_wildcard.length) != folder_wildcard)
                    continue;

                try {
                    if (LiteGraph.debug)
                        console.log("Reloading: " + src);
                    var dynamicScript = document.createElement("script");
                    dynamicScript.type = "text/javascript";
                    dynamicScript.src = src;
                    docHeadObj.appendChild(dynamicScript);
                    docHeadObj.removeChild(script_files[i]);
                } catch (err) {
                    if (LiteGraph.throw_errors)
                        throw err;
                    if (LiteGraph.debug)
                        console.log("Error while reloading " + src);
                }
            }

            if (LiteGraph.debug)
                console.log("Nodes reloaded");
        },

        //separated just to improve if it doesnt work
        cloneObject: function(obj, target) {
            if (obj == null) return null;
            var r = JSON.parse(JSON.stringify(obj));
            if (!target) return r;

            for (var i in r)
                target[i] = r[i];
            return target;
        },

        isValidConnection: function(type_b, type_a) {
            if (!type_a || //generic output
                !type_b || //generic input
                type_a == type_b || //same type (is valid for triggers)
                type_a == LiteGraph.EVENT && type_b == LiteGraph.ACTION)
                return true;

            if (type_b && type_a) {
                // /** tag or group match about links. */
                // var o_group = type_b.group;
                // var i_group = type_a.group;
                // if (o_group || i_group) {
                //     if (o_group === i_group) {
                //         return true;
                //     } else {
                //         return false;
                //     }
                // } else {
                //     var o_tag = type_b.tag;
                //     var i_tag = type_a.tag;
                //     if (o_tag || i_tag) {
                //         if (o_tag === i_tag) {
                //             return true;
                //         } else {
                //             return false;
                //         }
                //     } else {
                //         return true;
                //     }
                // }
                return true;
            } else {
                return false;
            }
            /* // Enforce string type to handle toLowerCase call (-1 number not ok)
            type_a = String(type_a);
            type_b = String(type_b);
            type_a = type_a.toLowerCase();
            type_b = type_b.toLowerCase();

            // For nodes supporting multiple connection types
            if (type_a.indexOf(",") == -1 && type_b.indexOf(",") == -1)
                return type_a == type_b; */

            /** console.log('support');
            // Check all permutations to see if one is valid
            var supported_types_a = type_a.split(",");
            var supported_types_b = type_b.split(",");
            for (var i = 0; i < supported_types_a.length; ++i)
                for (var j = 0; j < supported_types_b.length; ++j)
                    if (supported_types_a[i] == supported_types_b[j])
                        return true;

            return false; */
        },

        registerSearchboxExtra: function(node_type, description, data) {
            this.searchbox_extras[description] = { type: node_type, desc: description, data: data };
        },

        compareObjects: function(a, b) {
            for (var i in a)
                if (a[i] != b[i])
                    return false;
            return true;
        },

        distance: function(a, b) {
            return Math.sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]));
        },

        colorToString: function(c) {
            return "rgba(" + Math.round(c[0] * 255).toFixed() + "," + Math.round(c[1] * 255).toFixed() + "," + Math.round(c[2] * 255).toFixed() + "," + (c.length == 4 ? c[3].toFixed(2) : "1.0") + ")";
        },

        isInsideRectangle: function(x, y, left, top, width, height) {
            if (left < x && (left + width) > x &&
                top < y && (top + height) > y)
                return true;
            return false;
        },

        growBounding: function(bounding, x, y) {
            if (x < bounding[0])
                bounding[0] = x;
            else if (x > bounding[2])
                bounding[2] = x;

            if (y < bounding[1])
                bounding[1] = y;
            else if (y > bounding[3])
                bounding[3] = y;
        },

        isInsideBounding: function(p, bb) {
            if (p[0] < bb[0][0] ||
                p[1] < bb[0][1] ||
                p[0] > bb[1][0] ||
                p[1] > bb[1][1])
                return false;
            return true;
        },

        overlapBounding: function(a, b) {
            var A_end_x = a[0] + a[2];
            var A_end_y = a[1] + a[3];
            var B_end_x = b[0] + b[2];
            var B_end_y = b[1] + b[3];

            if (a[0] > B_end_x ||
                a[1] > B_end_y ||
                A_end_x < b[0] ||
                A_end_y < b[1])
                return false;
            return true;
        },

        hex2num: function(hex) {
            if (hex.charAt(0) == "#") hex = hex.slice(1); //Remove the '#' char - if there is one.
            hex = hex.toUpperCase();
            var hex_alphabets = "0123456789ABCDEF";
            var value = new Array(3);
            var k = 0;
            var int1, int2;
            for (var i = 0; i < 6; i += 2) {
                int1 = hex_alphabets.indexOf(hex.charAt(i));
                int2 = hex_alphabets.indexOf(hex.charAt(i + 1));
                value[k] = (int1 * 16) + int2;
                k++;
            }
            return (value);
        },

        num2hex: function(triplet) {
            var hex_alphabets = "0123456789ABCDEF";
            var hex = "#";
            var int1, int2;
            for (var i = 0; i < 3; i++) {
                int1 = triplet[i] / 16;
                int2 = triplet[i] % 16;

                hex += hex_alphabets.charAt(int1) + hex_alphabets.charAt(int2);
            }
            return (hex);
        },


        ContextMenu: install_ContextMenu(vm),

        closeAllContextMenus: function(ref_window) {
            ref_window = ref_window || window;

            var elements = ref_window.document.querySelectorAll(".litecontextmenu");
            if (!elements.length)
                return;

            var result = [];
            for (var i = 0; i < elements.length; i++)
                result.push(elements[i]);

            for (var i in result) {
                if (result[i].close)
                    result[i].close();
                else if (result[i].parentNode)
                    result[i].parentNode.removeChild(result[i]);
            }
        },

        extendClass: function(target, origin) {
            for (var i in origin) //copy class properties
            {
                if (target.hasOwnProperty(i))
                    continue;
                target[i] = origin[i];
            }

            if (origin.prototype) //copy prototype properties
                for (var i in origin.prototype) //only enumerables
                {
                    if (!origin.prototype.hasOwnProperty(i))
                        continue;

                    if (target.prototype.hasOwnProperty(i)) //avoid overwritting existing ones
                        continue;

                    //copy getters
                    if (origin.prototype.__lookupGetter__(i))
                        target.prototype.__defineGetter__(i, origin.prototype.__lookupGetter__(i));
                    else
                        target.prototype[i] = origin.prototype[i];

                    //and setters
                    if (origin.prototype.__lookupSetter__(i))
                        target.prototype.__defineSetter__(i, origin.prototype.__lookupSetter__(i));
                }
        },

        getParameterNames: function(func) {
            return (func + '')
                .replace(/[/][/].*$/mg, '') // strip single-line comments
                .replace(/\s+/g, '') // strip white space
                .replace(/[/][*][^/*]*[*][/]/g, '') // strip multi-line comments  /**/
                .split('){', 1)[0].replace(/^[^(]*[(]/, '') // extract the parameters
                .replace(/=[^,]+/g, '') // strip any ES6 defaults
                .split(',').filter(Boolean); // split & filter [""]
        },

        isInt: function(number) {
            return parseInt(number) === number && number % 1 === 0;
        },

        makeTaskTitle: function (task, tasks) {
            var lang = vm.$store.getters['language/getLanguage'];
            var result = 'Task'
            var copy = 'Task'
            if (tasks.length === 0) {
                return result;
            }
            var tasksTitles = [];
            for (var i = 0; i < tasks.length; ++i) {
                tasksTitles.push(tasks[i].title);
            }
            var count = 0;
            for (var i = 0; i < tasksTitles.length; ++i) {
                var finder = tasksTitles.indexOf(result);
                if (finder === 0) {
                    count += 2;
                } else if (finder > 0) {
                    count += 1;
                } else {
                    return result;
                }
                result = copy + "_(" + count + ")";
            }
            return result;
        },

        makeLambdaTitle: function (lambda, lambdas, task) {
            var result = lambda.title;
            var copy = lambda.title;
            if (!lambdas) {
                return result;
            }
            var lambdasInTask = [];
            for (var i = 0; i < lambdas.length; ++i) {
                for (var j = 0; j < task._nodes.length; ++j) {
                    if (task._nodes[j].id === lambdas[i].id) {
                        lambdasInTask.push(lambdas[i].title);
                    }
                }
            }
            var count = 0;
            for (var index = 0; index < lambdasInTask.length; ++index) {
                var finder = lambdasInTask.indexOf(result);
                if (finder === 0) {
                    count += 2;
                } else if (finder > 0) {
                    count += 1;
                } else {
                    return result;
                }
                result = copy + "_(" + count + ")";
            }
            return result;
        }
    };

    //timer that works everywhere
    if (typeof(performance) != "undefined")
        LiteGraph.getTime = performance.now.bind(performance);
    else if (typeof(Date) != "undefined" && Date.now)
        LiteGraph.getTime = Date.now.bind(Date);
    else if (typeof(process) != "undefined")
        LiteGraph.getTime = function() {
            var t = process.hrtime();
            return t[0] * 0.001 + t[1] * (1e-6);
        }
    else
        LiteGraph.getTime = function getTime() { return (new Date).getTime(); }

    return LiteGraph;
}