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
    width = 720,
    height = 576;

canvas.width = drawCanvas.width = width;

canvas.height = drawCanvas.height = height;

drawCanvas.onmousedown = function(e) {
    if(started){
        started = false;
        lastX = e.pageX - this.offsetLeft;
        lastY = e.pageY - this.offsetTop;
        
        //delete the begining circle
        drawCtx.clearRect(0, 0, width, height);
        
        ctx.strokeStyle = "#000";
        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.lineTo(lastX, lastY);
        ctx.stroke();
    } else {
        started = true;
        startX = e.pageX - this.offsetLeft;
        startY = e.pageY - this.offsetTop;
        
        drawCtx.beginPath();
        drawCtx.arc(startX, startY, 5, 0, 2 * Math.PI, true);
        drawCtx.fill();
    }
};