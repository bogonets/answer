export function drawLine(painter, first_point, second_point, lineColor, lineWidth) {
    painter.strokeStyle = lineColor;
    painter.lineWidth = lineWidth;
    painter.beginPath();
    painter.moveTo(first_point.x, first_point.y);
    painter.lineTo(second_point.x, second_point.y);
    painter.stroke();
    painter.closePath();
}

export function drawRect(painter, start_point, width, height, color, lineWidth, fill) {
    painter.beginPath();
    painter.lineWidth = lineWidth;
    painter.rect(start_point.x, start_point.y, width, height);
    if (fill) {
        painter.fillStyle = color || "skyblue";
        painter.fill();
    } else {
        painter.strokeStyle = color || "skyblue";
        painter.stroke();
    }
    painter.closePath();
}

export function drawPoly(painter, points, color, lineWidth, closeEnd, fill) {
    if (closeEnd) {
        painter.beginPath();
        painter.moveTo(points[0].x, points[0].y);
        for (var index = 1; index < points.length; ++index) {
            painter.lineTo(points[index].x, points[index].y);
        }
        painter.closePath();
    } else {
        painter.moveTo(points[0].x, points[0].y);
        for (var index = 1; index < points.length; ++index) {
            painter.lineTo(points[index].x, points[index].y);
        }
    }
    painter.lineWidth = lineWidth;
    if (fill) {
        painter.fillStyle = color || "skyblue";
        painter.fill();
    } else {
        painter.strokeStyle = color || "skyblue";
        painter.stroke();
    }
}

export function drawPolyForCache(painter, points, last_point, color, lineWidth, closeEnd, fill) {
    if (closeEnd) {
        painter.beginPath();
        painter.moveTo(points[0].x, points[0].y);
        for (var index = 1; index < points.length; ++index) {
            painter.lineTo(points[index].x, points[index].y);
        }
        painter.lineTo(last_point.x, last_point.y);
        painter.closePath();
    } else {
        painter.moveTo(points[0].x, points[0].y);
        for (var index = 1; index < points.length; ++index) {
            painter.lineTo(points[index].x, points[index].y);
        }
        painter.lineTo(last_point.x, last_point.y);
    }
    painter.lineWidth = lineWidth;
    if (fill) {
        painter.fillStyle = color || "skyblue";
        painter.fill();
    } else {
        painter.strokeStyle = color || "skyblue";
        painter.stroke();
    }
}

export function drawArc(painter, center_point, radius, sAngle, eAngle, color, lineWidth, fill) {
    painter.beginPath();
    painter.lineWidth = lineWidth;
    painter.arc(center_point.x, center_point.y, radius, sAngle, eAngle * Math.PI);
    if (fill) {
        painter.fillStyle = color || "skyblue";
        painter.fill();
    } else {
        painter.strokeStyle = color || "skyblue";
        painter.stroke();
    }
    painter.closePath();
}

export function drawArcWithSize(painter, center_point, width, height, sAngle, eAngle, color, lineWidth, fill) {
    var radius = Math.sqrt(Math.pow(width, 2) + Math.pow(height, 2));
    painter.beginPath();
    painter.lineWidth = lineWidth;
    painter.arc(center_point.x, center_point.y, radius, sAngle, eAngle * Math.PI);
    if (fill) {
        painter.fillStyle = color || "skyblue";
        painter.fill();
    } else {
        painter.strokeStyle = color || "skyblue";
        painter.stroke();
    }
    painter.closePath();
}

export function drawText(painter, start_point, text, color, align = "", fill = true, font_style = "50px Comic Sans MS") {
    painter.font = font_style;
    if (align != "") {
        painter.textAlign = align;
    }
    if (fill) {
        painter.fillStyle = color || "skyblue";
        painter.fillText(text, start_point.x, start_point.y);
    } else {
        painter.strokeStyle = color || "skyblue";
        painter.strokeText(text, start_point.x, start_point.y);
    }
}

export function clearAll(painter, canvas) {
    painter.clearRect(0, 0, canvas.width, canvas.height);
}

export function clearArea(painter, start_point, width, height, lineWidth = 5) {
    painter.clearRect(start_point.x, start_point.y, width, height);
}

export function clearPoly(painter, points, color, lineWidth, closeEnd, fill) {
    var temp_painter = painter;
    temp_painter.globalCompositeOperation = 'destination-out';
    if (closeEnd) {
        temp_painter.beginPath();
        temp_painter.moveTo(points[0].x, points[0].y);
        for (var index = 1; index < points.length; ++index) {
            temp_painter.lineTo(points[index].x, points[index].y);
        }
        temp_painter.closePath();
    } else {
        temp_painter.moveTo(points[0].x, points[0].y);
        for (var index = 1; index < points.length; ++index) {
            temp_painter.lineTo(points[index].x, points[index].y);
        }
    }
    temp_painter.lineWidth = lineWidth;
    if (fill) {
        temp_painter.fillStyle = color;
        temp_painter.fill();
    } else {
        temp_painter.strokeStyle = color;
        temp_painter.stroke();
    }
}


// vod draw object .
export function drawPoly2(painter, points, color, lineWidth, closeEnd, fill) {
    var avg_x = 0;
    var avg_y = 0;
    if (closeEnd) {
        painter.beginPath();
    }
    painter.moveTo(points[0][0], points[0][1]);
    avg_x = points[0][0];
    avg_y = points[0][1];
    for (var index = 1; index < points.length; ++index) {
        painter.lineTo(points[index][0], points[index][1]);
        avg_x += points[index][0];
        avg_y += points[index][1];
    }
    if (closeEnd) {
        painter.closePath();
    }
    painter.lineWidth = lineWidth;
    if (fill) {
        painter.fillStyle = color || "skyblue";
        painter.fill();
    } else {
        painter.strokeStyle = color || "skyblue";
        painter.stroke();
    }

    return { x: avg_x / points.length, y: avg_y / points.length };
}