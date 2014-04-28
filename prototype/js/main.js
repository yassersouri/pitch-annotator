var img = $('#theimage');

var canvas = document.getElementById("canvas"),
    ctx = canvas.getContext("2d"),
    drawCanvas = document.getElementById("drawCanvas"),
    drawCtx = drawCanvas.getContext("2d"),
    started = false,
    lastX = 0,
    lastY = 0,
    curX = 0,
    curY = 0,
    startX = 0,
    startY = 0,
    lineThickness = 1
    width = img.width(),
    height = img.height();

canvas.width = drawCanvas.width = width;

canvas.height = drawCanvas.height = height;

drawCanvas.onmousedown = function(e) {
    if(started){
        started = false;
        lastX = e.pageX - this.offsetLeft;
        lastY = e.pageY - this.offsetTop;
        
        clearCxt(drawCtx);

        drawLine(ctx, startX, startY, lastX, lastY);
    } else {
        started = true;
        startX = e.pageX - this.offsetLeft;
        startY = e.pageY - this.offsetTop;

        drawCircle(drawCtx, startX, startY);
    }
};

function drawLine (ctx, x1, y1, x2, y2) {
    ctx.strokeStyle = "#000";
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
}

function drawCircle (ctx, x, y) {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2 * Math.PI, true);
    ctx.fill();
}

function clearCxt (ctx) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
}