import sha256 from 'sha256'
import base64 from 'base'
import { Observable } from 'rxjs'

import jwt from 'jsonwebtoken'

function answer_util() {

}

answer_util.prototype.wait = function (msecs) {
    var start = new Date().getTime()
    var cur = start
    while (cur - start < msecs) {
        cur = new Date().getTime()
    }
}

answer_util.prototype.makeHash = function (string) {
    return sha256(string)
}

answer_util.prototype.decodeToken = function (token) {
    return jwt.decode(token);
}

answer_util.prototype.dashboard_jTos = function (panels_data) {
    var jsonToString = "";
    for (var index = 0; index < panels_data.length; ++index) {
        if (index != panels_data.length - 1) {
            jsonToString += JSON.stringify(panels_data[index]) + '|';
        } else {
            jsonToString += JSON.stringify(panels_data[index]);
        }
    }
    return jsonToString;
}

answer_util.prototype.dashboard_sToj = function (stringPanelData) {
    var result = [];
    if (!stringPanelData) {
        // alert("Not String type.");
        return result;
    }
    var temp = stringPanelData.split('|');
    for (var idx = 0; idx < temp.length; ++idx) {
        result.push(JSON.parse(temp[idx]))
    }
    return result;
}

answer_util.prototype.cloneObject = function (obj, t) {
    if (obj == null) return null;
    var r = JSON.parse(JSON.stringify(obj));
    if (!t) return r;

    for (var i in r)
        t[i] = r[i];
    return t;
}

answer_util.prototype.getBrowser = function () {
    var browser = null;
    if ((navigator.userAgent.indexOf("Opera") || navigator.userAgent.indexOf('OPR')) != -1) {
        browser = 'Opera';
    } else if (navigator.userAgent.indexOf("Chrome") != -1) {
        browser = 'Chrome';
    } else if (navigator.userAgent.indexOf("Safari") != -1) {
        browser = 'Safari';
    } else if (navigator.userAgent.indexOf("Firefox") != -1) {
        browser = 'Firefox';
    } else if ((navigator.userAgent.indexOf("MSIE") != -1) || (!!document.documentMode == true)) { //IF IE > 10
        browser = 'IE';
    } else {
        browser = 'unknown';
    }
    return browser;
}

answer_util.prototype.arrayToCsv = function (array) {
    var copy = this.cloneObject(array);
    var result = "";
    for (var index = 0; index < copy.length - 1; ++index) {
        result += copy[index] + ",";
    }
    if (!!copy[copy.length - 1]) {
        result += copy[copy.length - 1];
    }
    return result;
}

answer_util.prototype.isEmptyObject = function (object) {
    return Object.keys(obj).length === 0 && JSON.stringify(obj) === JSON.stringify({});
}

answer_util.prototype.getNow = function (style) {
    var type = style || "ISO";
    var date = new Date();
    var today = "" + date.getFullYear() + "-" + this.iTos((date.getMonth() + 1), 2) + "-" + this.iTos(date.getDate(), 2);
    var time = "" + this.iTos(date.getHours(), 2) + ":" + this.iTos(date.getMinutes(), 2) + ":" + this.iTos(date.getSeconds(), 2) + "." + date.getMilliseconds();
    if (type === "ISO") {
        return today + "T" + time;
    } else {
        return today + " " + time;
    }
}

answer_util.prototype.cvtTime = function (dateString) {
    if (!dateString) {
        return "";
    }
    var spt = dateString.split("T");
    var date = spt[0].split("-");
    var time = spt[1].split(":");
    if (time[time.length -1].length > 2) {
        time[time.length -1] = time[time.length -1].substring(0, 2);
    }
    var result = {
        year: date[0] || null,
        month: date[1] || null,
        day: date[2] || null,
        hour: time[0] || null,
        min: time[1] || null,
        sec: time[2] || null
    }
    return result;
}

answer_util.prototype.iTos = function (n, width) {
    n = n + '';
    if (width) {
        return n.length >= width ? n : new Array(width - n.length + 1).join('0') + n;
    } else {
        return n;
    }
}

answer_util.prototype.makeColor = function (alpha) {
    var R = Math.floor(Math.random() * 180) + 1;
    var G = Math.floor(Math.random() * 180) + 1;
    var B = Math.floor(Math.random() * 180) + 1;
    var A = alpha || 0.2;
    return `rgba(${R}, ${G}, ${B}, ${A})`;
}

answer_util.prototype.convertByteType = function (size) {
    if (size === null || size === undefined || typeof size !== 'number') {
        return "0B";
    }
    if (size < 1024) {
        return `${size}B`;
    } else if (size < Math.pow(1024, 2)) {
        size = size / 1024;
        return `${size.toFixed(0)}KB`;
    } else if (size < Math.pow(1024, 3)) {
        size = size / Math.pow(1024, 2);
        return `${size.toFixed(0)}MB`;
    } else if (size < Math.pow(1024, 4)) {
        size = size / Math.pow(1024, 3);
        return `${size.toFixed(0)}GB`;
    } else if (size < Math.pow(1024, 5)) {
        size = size / Math.pow(1024, 4);
        return `${size.toFixed(0)}TB`;
    }
}

export const ANSWER_UTIL = () => { return new answer_util(); }