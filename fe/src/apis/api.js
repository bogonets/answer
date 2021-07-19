import axios from 'axios'
import { ANSWER_UTIL } from '@/services/answer_util'
import { Observable } from 'rxjs'

const verbose = process.env.NODE_ENV !== 'production';
const utils = ANSWER_UTIL();
const getNow = () => { return utils.getNow(); };
const logger = {
    log: (...args) => {
        if (verbose) {
            console.log(getNow(), "[API] [DEBUG]", ...args);
        }
    },
    warn: (...args) => {
        console.warn(getNow(), "[API] [WARN]", ...args);
    },
    error: (...args) => {
        console.error(getNow(), "[API] [ERROR]", ...args);
    }
}

const FROM_API = '/api';
const HOST_VERSION = '/v1';
const PARAM = {
    initialization: '/initialization',
    users: '/users',
    admin: '/admin',
    login: '/login',
    project: '/project',
    projects: '/projects',
    layouts: '/layouts',
    layout: '/layout',
    check: '/check',
    eventlist: '/eventlist',
    datalist: '/datalist',
    graph: '/graph',
    graphs: '/graphs',
    templates: '/templates',
    properties: '/properties',
    webrtcurls: '/webrtcurls',
    datalistImage: '/datalist-image',
    signal: '/signal',
    stop: '/stop',
    tasks: '/tasks',
    nodes: '/nodes',
    nodeTypes: '/node-types',
    hint: '/hint',
    slots: '/slots',
    image: '/image',
    jupyters: '/jupyters',
    jupyter: '/jupyter',
    pips: '/pips',
    pip: '/pip'
};

const ACCEPT = {
    ALL:  "*/*",
    JSON: "application/json",
    JPEG: "image/jpeg",
    PNG:  "image/png",
    GIF:  "image/gif",
}

const AUTH_TYPE = { basic: 'basic ', bearer: 'bearer ' };
const PROTOCOL = document.location.protocol;
const HOST = document.location.host;
const ORIGIN = document.location.origin;

function API() {
    this.url = ORIGIN;
}

API.prototype.setUrl = function(url) {
    this.url = url;
}

API.prototype.getUrl = function() {
    return this.url;
}

API.prototype.createAxios = function (accept, auth, timeout, access, contentType) {
    var acceptType = accept || ACCEPT.JSON;
    var authType   = auth   || AUTH_TYPE.bearer;
    var timeOut    = timeout || 15000;
    var config = {};
    config.baseURL = this.url || ORIGIN;
    config.timeout = timeOut;
    config.headers = {};
    config.headers.Accept = acceptType;
    if (access) {
        config.headers.Authorization = authType + access;
    }
    if (contentType) {
        config.headers["Content-Type"] = contentType;
    }
    var http = axios.create(config)
    return http;
}

API.prototype.host_basic = function(loginToken) {
    var basic = this.createAxios(ACCEPT.JSON, AUTH_TYPE.basic, 5000, loginToken);
    basic.interceptors.request.use(function (config) {
        return config;
    }, function (error) {
        return Promise.reject(error);
    })
    basic.interceptors.response.use(function (response) {
        return response;
    }, function (error) {
        return Promise.reject(error);
    })
    return basic;
}

API.prototype.host_bearer = function(userToken, refreshToken, timeout) {
    var timelimit = timeout || 15000;
    var bearer = this.createAxios(ACCEPT.JSON, AUTH_TYPE.bearer, timelimit, userToken);
    bearer.interceptors.request.use(function (config) {
        return config;
    }, function (error) {
        return Promise.reject(error);
    })
    bearer.interceptors.response.use(function (response) {
        return response;
    }, function (error) {
        return Promise.reject(error);
    })
    return bearer;
}

// use image get from API.
API.prototype.all_bearer = function(userToken, refreshToken) {
    var bearer = this.createAxios(ACCEPT.ALL, AUTH_TYPE.bearer, 30000, userToken);
    bearer.interceptors.request.use(function (config) {
        return config;
    }, function (error) {
        return Promise.reject(error);
    })
    bearer.interceptors.response.use(function (response) {
        return response;
    }, function (error) {
        return Promise.reject(error);
    })
    return bearer;
}

API.prototype.upload_bearer = function(userToken, refreshToken, contentType) {
    var ct = contentType || "multipart/form-data";
    var bearer = this.createAxios(ACCEPT.ALL, AUTH_TYPE.bearer, 15000, userToken, ct);
    bearer.interceptors.request.use(function (config) {
        return config;
    }, function (error) {
        return Promise.reject(error);
    })
    bearer.interceptors.response.use(function (response) {
        return response;
    }, function (error) {
        return Promise.reject(error);
    })
    return bearer;
}

// ################### ASYNC #######################
API.prototype.checkAdmin = function () {
    var axo = axios.create({
        baseURL: this.url || ORIGIN,
        // baseURL: "https://kr.vuejs.org/v2/guide/index.html",
        headers: {
            Accept: ACCEPT.JSON
        }
    })
    return axo.get(FROM_API + HOST_VERSION + PARAM.initialization, {})
}

API.prototype.signupAdmin = function (signupData) {
    var axo = axios.create({
        baseURL: this.url || ORIGIN,
        headers: {
            Accept: ACCEPT.JSON
        }
    })
    return axo.post(FROM_API + HOST_VERSION + PARAM.users + PARAM.admin, signupData)
}

API.prototype.onLogin = function(token) {
    return Observable
        .fromPromise(this.host_basic(token).post(FROM_API + HOST_VERSION + PARAM.login, {}))
        .map(response => response)
        .catch(error => Observable.throw(error))
}

API.prototype.createProject = function(token, refreshToken, projectName) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.project + "/" + projectName, {}))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.checkDuplicatedProjectname = function(token, refreshToken, projectName) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.project + '/' + projectName))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.getProjects = function(token, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.project, {}))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.rmProject = function(token, refreshToken, projectName) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.project + "/" + projectName, {}))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.editProject = function(token, refreshToken, projectData) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).put(FROM_API + HOST_VERSION + PARAM.projects,  JSON.stringify(projectData)))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.getProject = function(token, project_name, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name, {}))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.getLayouts = function(token, project_name, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name + PARAM.layouts, {}))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

// api/v1/project/${PROJECT_NAME}/layouts/check
API.prototype.isExistLayout = function(token, project_name, layout_name, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name + PARAM.layouts + PARAM.check, { name: layout_name }))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error.request))
}

API.prototype.getLayout = function(token, project_name, layout_name, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name + PARAM.layout + '/' + layout_name, {}))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error.request))
}

API.prototype.sendPanelsData = function(token, project_name, layout_name, panels, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).put(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name + PARAM.layout + '/' + layout_name, { name: layout_name, panels: panels }))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error.request))
}

API.prototype.deleteLayout = function(token, project_name, layout_name, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name + PARAM.layout + '/' + layout_name, {}))
        .map(response => response)
        .catch(error => Observable.throw(error.request))
}

API.prototype.getLambdaTemplates = function(token, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.graph + PARAM.templates, {}))
        .map(response => response.data)
        .catch(error => Observable.throw(error.request))
}

API.prototype.getLambda = function(token, projectName, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.project + "/" + projectName + PARAM.graph, {}))
        .map(response => response.data)
        .catch(error => Observable.throw(error.request))
}

API.prototype.saveLambda = function(token, projectName, visual_data, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.project + "/" + projectName + PARAM.graph, visual_data))
        .map(response => response.data)
        .catch(error => Observable.throw(error))
}

API.prototype.stopTask = function(token, projectName, taskName, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.project + "/" + projectName + PARAM.graph + PARAM.stop + "/" + taskName))
        .map(response => response.data)
        .catch(error => Observable.throw(error))
}

API.prototype.getGraphStatus = function (access, refresh, projectName) {
    return Observable
    .fromPromise(this.host_bearer(access, refresh).get(FROM_API + HOST_VERSION + PARAM.project + "/" + projectName + "/graph/infos"))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}

API.prototype.getPropertyValue = function (access, refresh, projectName, taskName, lambdaName, propertyName) {
    var body = {};
    body.lambda = lambdaName;
    body.property = propertyName;
    return Observable
    .fromPromise(this.host_bearer(access, refresh).get(FROM_API + HOST_VERSION + PARAM.projects + "/" + projectName + `/graphs/main/tasks/${taskName}/lambda-props?q=${JSON.stringify(body)}`))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}

API.prototype.getPropertyValueWithNative = function (access, refresh, projectName, taskName, lambdaName, propertyName) {
    var body = {};
    body.lambda = lambdaName;
    body.property = propertyName;
    this.host_bearer(access, refresh).get(FROM_API + HOST_VERSION + PARAM.projects + "/" + projectName + `/graphs/main/tasks/${taskName}/lambda-props?q=${JSON.stringify(body)}`);
}

API.prototype.setPropertyValue = function (access, refresh, projectName, taskName, lambdaName, propertyName, setValue) {
    var body = {};
    body.lambda = lambdaName;
    body.property = propertyName;
    body.value = setValue.toString();
    return Observable
    .fromPromise(this.host_bearer(access, refresh).put(FROM_API + HOST_VERSION + PARAM.projects + "/" + projectName + `/graphs/main/tasks/${taskName}/lambda-props`, body))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}

API.prototype.setPropertyValueWithNative = function (access, refresh, projectName, taskName, lambdaName, propertyName, setValue) {
    var body = {};
    body.lambda = lambdaName;
    body.property = propertyName;
    body.value = setValue;
    return this.host_bearer(access, refresh).put(FROM_API + HOST_VERSION + PARAM.projects + "/" + projectName + `/graphs/main/tasks/${taskName}/lambda-props`, body);
}

API.prototype.signalLambda = function (access, refresh, projectName, taskName, lambdaName, propertyName, signalData) {
    var header = null;
    if (signalData.output_queries.length > 0) {
        for (let index = 0; index < signalData.output_queries.length; ++index) {
            if (signalData.output_queries[index].includes("image")) {
                header = {};
                header.responseType = 'arraybuffer';
            }
        }
    } 
    return Observable
    .fromPromise(this.all_bearer(access, refresh).post(FROM_API + HOST_VERSION + PARAM.projects + "/" + projectName + `/graphs/main/tasks/${taskName}/lambda-signal`, signalData, header? header : null))
    .map(response => response)
    .catch(error => Observable.throw(error))
}

API.prototype.setEventRoi = function(token, node_id, prop_name, send_data, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).put(FROM_API + HOST_VERSION + PARAM.graphs + '/' + node_id + PARAM.properties + '/' + prop_name, send_data))
        .map(response => response.data)
        .catch(error => Observable.throw(error.request))
}

API.prototype.createLayout = function(token, project_name, body, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name + PARAM.layout, { name: body.name, panels: body.panels }))
        .map(response => response)
        .catch(error => error)
}

API.prototype.getTableDataList = function(token, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.datalist, {}))
        .map(response => response.data.result.obj)
        .catch(error => Observable.throw(error.request))
}

API.prototype.getTableCategoryList = function(token, select_datalist, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.datalist + '/' + select_datalist, {}))
        .map(response => response.data.result.obj)
        .catch(error => Observable.throw(error.request))
}

API.prototype.getTableData = function(token, select_datalist, select_categorylist, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.datalist + '/' + select_datalist + '/' + select_categorylist, {}))
        .map(response => response.data.result.obj)
        .catch(error => Observable.throw(error.request))
}

// get image from api. --version = test.
API.prototype.getImageFromAPI = function (userToken, refreshToken, projectName, taskName, lambdaName, outputName) {
    return Observable
    .fromPromise(this.all_bearer(userToken, refreshToken).get(FROM_API + HOST_VERSION + PARAM.signal + PARAM.projects + '/' + projectName + PARAM.tasks + '/' + taskName + PARAM.nodes + '/' + lambdaName + PARAM.slots + '/' + outputName + PARAM.image, { crossdomain: true, responseType: 'arraybuffer'}))
    .map(res => res)
    .catch(error => Observable.throw(error))
}
API.prototype.getImageFromIndex = function(userToken, index, refreshToken) { // KISCO.
    return Observable
        .fromPromise(this.all_bearer(userToken, refreshToken).get(FROM_API + HOST_VERSION + PARAM.datalistImage + '/' + index, { crossdomain: true, responseType: 'arraybuffer' }))
        // .fromPromise(this.all_bearer(userToken).get('', { crossdomain: true, responseType: 'arraybuffer' }))
        .map(res => res)
        .catch(error => Observable.throw(error.request))
}

API.prototype.getImageLatest = function(userToken, pluginName, category, refreshToken) { // KISCO.
    return Observable
        .fromPromise(this.all_bearer(userToken, refreshToken).get(FROM_API + HOST_VERSION + PARAM.datalist + "/" + pluginName + "/" + category + PARAM.image, { responseType: 'arraybuffer' }))
        .map(res => res)
        .catch(error => Observable.throw(error.request))
}

API.prototype.cvtOnlineImageToData = function (url) {
    var req = axios.create({
        headers: {
            Accept: '*/*',
        } 
    })

    req.get(url, { crossdomain: false, responseType: 'arraybuffer' })
    .then(res => {
        var bin = Buffer.from(res.data, 'binary').toString('base64');
        var result = "data:image/*;base64," + bin;
        console.log(result);
    })
    .catch(err => console.error('ERROR - Can not Get Image', err))
}

API.prototype.getCoreVersion = function () {
    return Observable
    .fromPromise(this.host_bearer().get(FROM_API + HOST_VERSION + "/version/core", {}))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}

API.prototype.getApiVersion = function () {
    return Observable
    .fromPromise(this.host_bearer().get(FROM_API + HOST_VERSION + "/version/api", {}))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}

// ------------------------ Jupyter -----------------------------
API.prototype.getJupyters = function (token, refreshToken, projectName) {
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.project + '/' + projectName + PARAM.jupyters)
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.newJupyter = function (token, refreshToken, projectName, newJupyterName) {
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.project + '/' + projectName + PARAM.jupyters, {name: newJupyterName})
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.deleteJupyters = function (token, refreshToken, projectName, deleteJupyters) {
    return new Promise((resolve, reject) => {
        // this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.project + '/' + projectName + PARAM.jupyters, {names: deleteJupyters})
        this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.project + '/' + projectName + PARAM.jupyters + '/' + deleteJupyters)
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.getJupyterPips = function (token, refreshToken) {
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.pips)
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.getJupyterPip = function (token, refreshToken, pipName) {
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.pips + '/' + pipName)
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.addJupyterPips = function (token, refreshToken, pips) {
    if (typeof pips !== 'string') {
        return Promise.reject('TypeError: send Pip type is ' + (typeof pips));
    }
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken, 60000).post(FROM_API + HOST_VERSION + PARAM.pips, {package: pips})
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.addJupyterPip = function (token, refreshToken, pip) {
    if (typeof pip !== 'string') {
        return Promise.reject('TypeError: send Pip type is ' + (typeof pip));
    }
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken, 60000).post(FROM_API + HOST_VERSION + PARAM.pips, {package: pip})
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.removePips = function (token, refreshToken, pips) {
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.pips, {package: pips})
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.removePip = function (token, refreshToken, pip) {
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.pips + '/' + pip)
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.getJupyterFiles = function (token, refreshToken, lambdaType, propName) {
    return Observable
    .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.nodeTypes + '/' + lambdaType + PARAM.properties + '/' + propName + PARAM.hint))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}

// members manage.
API.prototype.signupMember = function(token, refreshToken, signupData) {
    var data = signupData;
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.users, data ))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.getMembersList = function(token, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.users, {}))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.rmMember = function(token, refreshToken, rmMember) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.users, { data: JSON.stringify(rmMember) }))
        // .fromPromise(this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.users + '/' + rmMember))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.editMember = function(token, refreshToken, editData) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).put(FROM_API + HOST_VERSION + PARAM.users,  JSON.stringify(editData)))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}

API.prototype.checkDuplicatedUsername = function(token, refreshToken, userID) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.users + '/' + userID))
        .map(response => response.data.result)
        .catch(error => Observable.throw(error))
}
// --------------RTC--------------------
API.prototype.getRtcHost = function(token, refreshToken) {
    return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.graph + PARAM.webrtcurls, {}))
        .map(response => response.data)
        .catch(error => Observable.throw(error.request))
}

// ################### SYNC #######################
// API.prototype.createLayout = function(token, project_name, body) {
//     this.host_bearer(token, this.url).post(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name + PARAM.layout, { name: body.name, panels: body.panels })
//         .then(res => res)
//         .catch(err => err)
// }
API.prototype.setEventList = (token, project_name, event_list, refreshToken) => {
    this.host_bearer(token, refreshToken).put(FROM_API + HOST_VERSION + PARAM.project + '/' + project_name + PARAM.eventlist, { eventlist: event_list })
}


// ################## minIO #########################
API.prototype.getBuckets = function (token, refreshToken, projectName) {
    return Observable
    .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets`, {}))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}
API.prototype.createBucket = function (token, refreshToken, projectName, bucketName) {
    return Observable
    .fromPromise(this.host_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets`, { bucketName: bucketName }))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}
API.prototype.deleteBuckets = function (token, refreshToken, projectName, bucketName) {
    return Observable
    .fromPromise(this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}`, {}))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}
API.prototype.getBucketsObjects = function (token, refreshToken, projectName, bucketName, prefix) {
    if (prefix) {
        return Observable
        .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}/objects?q={"prefix": "${prefix}"}`, {}))
        .map(response => response.data)
        .catch(error => Observable.throw(error))
    }
    return Observable
    .fromPromise(this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}/objects`, {}))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}
API.prototype.getBucketsObjects2 = function (token, refreshToken, projectName, bucketName, page, pageSize, order, filter, prefix) {
    if (prefix) {
        return new Promise((resolve, reject) => {
            this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}/objects/?page=${page}&pageSize=${pageSize}&order=${order}&filter=${filter}&q={"prefix": "${prefix}"}`, {})
            .then(response => {
                resolve(response.data);
            })
            .catch(error => {
                reject(error);
            })
        })
    }
    return new Promise((resolve, reject) => {
        this.host_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}/objects/?page=${page}&pageSize=${pageSize}&order=${order}&filter=${filter}`, {})
        .then(response => {
            resolve(response.data);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.getBucketsObject = function (token, refreshToken, projectName, bucketName, objectName, prefix, isImage) {
    return Observable
        .fromPromise(this.all_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}/objects/${prefix ? prefix : ''}${objectName}`, { crossdomain: true, responseType: 'blob' }))
        .map(response => response)
        .catch(error => Observable.throw(error))
}
API.prototype.getBucketsObject2 = function (token, refreshToken, projectName, bucketName, objectName, prefix, isImage) {
    return new Promise((resolve, reject) => {
        this.all_bearer(token, refreshToken).get(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}/objects/${prefix ? prefix : ''}${objectName}`, { crossdomain: true, responseType: 'blob' })
        .then(response => {
            resolve(response);
        })
        .catch(error => {
            reject(error);
        })
    })
}
API.prototype.uploadBucketsObject = function (token, refreshToken, projectName, bucketName, formData) {
    return Observable
    .fromPromise(this.upload_bearer(token, refreshToken).post(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}/objects`, formData))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}
API.prototype.deleteBucketsObject = function (token, refreshToken, projectName, bucketName, objectName, prefix) {
    return Observable
    .fromPromise(this.host_bearer(token, refreshToken).delete(FROM_API + HOST_VERSION + PARAM.projects + `/${projectName}/buckets/${bucketName}/objects/${prefix ? prefix : ''}${objectName}`, {}))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}
// ################## ##### #########################

// ################## AIRJOY #########################
API.prototype.getAirjoyManageNonMetricData = function (access, refresh, projectName) {
    return Observable
    .fromPromise(this.host_bearer(access, refresh).get(FROM_API + HOST_VERSION + "/extra/airjoy"+ PARAM.project + "/" + projectName + "/manage/non-metric"))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}

API.prototype.getAirjoyManageMetricData = function (access, refresh, projectName) {
    return Observable
    .fromPromise(this.host_bearer(access, refresh).get(FROM_API + HOST_VERSION + "/extra/airjoy"+ PARAM.project + "/" + projectName + "/manage/metric"))
    .map(response => response.data)
    .catch(error => Observable.throw(error))
}

export const REST_API = () => { return new API(); }