var canvas, ctx, bMouseIsDown = false, iLastX, iLastY,
        $save, $imgs,
        $convert, $imgW, $imgH,
        $sel;
function init () {
    // 绑定canvas
    canvas = document.getElementById('cvs');
    // 设置canvas的style
    canvas.style.backgroundColor = "#e7e7e7";
    canvas.width = 112;
    canvas.height = 140;
    // canvas.getContext(contextType)
    // 这里指定的contextType是'2d'，会创建并返回一个CanvasRenderingContext2D对象，主要用来进行2d绘制
    ctx = canvas.getContext('2d');
    // 绘制的颜色
    ctx.strokeStyle = "black";
    // 绘制线条的粗细
    ctx.lineWidth = 8;
    // 获取保存的button
    $save = document.getElementById('save');
    $clear = document.getElementById('clear');
    // 监控绘画情况
    bind();
    draw();
}
// 监控绘画情况
function bind () {
    canvas.onmousedown = function(e) {
        bMouseIsDown = true;
        iLastX = e.clientX - canvas.offsetLeft + (window.pageXOffset||document.body.scrollLeft||document.documentElement.scrollLeft);
        iLastY = e.clientY - canvas.offsetTop + (window.pageYOffset||document.body.scrollTop||document.documentElement.scrollTop);
    }
    canvas.onmouseup = function() {
        bMouseIsDown = false;
        iLastX = -1;
        iLastY = -1;
    }
    canvas.onmousemove = function(e) {
        if (bMouseIsDown) {
            var iX = e.clientX - canvas.offsetLeft + (window.pageXOffset||document.body.scrollLeft||document.documentElement.scrollLeft);
            var iY = e.clientY - canvas.offsetTop + (window.pageYOffset||document.body.scrollTop||document.documentElement.scrollTop);
            // 路径绘制起始点
            ctx.moveTo(iLastX, iLastY);
            // 绘制直线到指定坐标点
            ctx.lineTo(iX, iY);
            // 描边
            ctx.stroke();
            // 终点作为新的起始点
            iLastX = iX;
            iLastY = iY;
        }
    };
    $save.onclick = function (e) {
        // 返回Canvas图像对应的data URI，即base64地址
        var img = canvas.toDataURL();
        // 发送ajax请求
        $.ajax({
            url: "./back_end/savePic.php",
            type: "POST",
            headers: {
                "Content-type": "application/x-www-form-urlencoded"
            },
            data: {
                img: img,
            },
            success: function(data){
                if(data.length!=1){
                    alert(data);
                }else{
                    document.getElementById("num").innerHTML = data;
                }
                
            }
            //,
            // // 此处是为了有一个loading的效果
            // beforeSend: function(){
            //     $('<div class="loading"></div>').appendTo("body");
            // },
            // complete: function(){
            //     $(".loading").remove();
            // }
        })
    };
    $clear.onclick = function(e) {
        canvas = document.getElementById('cvs');
        canvas.width = 112;
        canvas.height = 140;
        ctx = canvas.getContext("2d");
        ctx.strokeStyle = "black";
        ctx.lineWidth = 8;       
        ctx.beginPath();
        document.getElementById("num").innerHTML = "?";
    }
}
