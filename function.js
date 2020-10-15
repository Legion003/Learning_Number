var canvas, ctx, bMouseIsDown = false, iLastX, iLastY,
        $save, $imgs,
        $convert, $imgW, $imgH,
        $sel;
function init () {
    // 绑定canvas
    canvas = document.getElementById('cvs');
    // 设置canvas的style
    canvas.style.backgroundColor = "black";
    canvas.width = 112;
    canvas.height = 140;
    // canvas.getContext(contextType)
    // 这里指定的contextType是'2d'，会创建并返回一个CanvasRenderingContext2D对象，主要用来进行2d绘制
    ctx = canvas.getContext('2d');
    // 绘制的颜色
    ctx.strokeStyle = "white";
    // 绘制线条的粗细
    ctx.lineWidth = 8;
    // 获取保存的button
    $save = document.getElementById('save');
    $imgs = document.getElementById('imgs');
    $imgW = document.getElementById('imgW');
    $imgH = document.getElementById('imgH');
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
        var ztype = "jpeg",
        w = 300,
        h = 200;
        var result = 5;
        var ajax = null;
        // 返回Canvas图像对应的data URI，即base64地址
        var img = canvas.toDataURL();
        // 发送ajax请求
        // 通过XMLHttpRequest可以在不刷新页面的情况下请求特定 URL
        // if (window.XMLHttpRequest) {
        //     // 主流浏览器提供了XMLHttpRequest对象
        //     ajax = new XMLHttpRequest();
        // } else {
        //     //低版本的IE浏览器没有提供XMLHttpRequest对象，IE6以下
        //     //所以必须使用IE浏览器的特定实现ActiveXObject
        //     ajax = new ActiveXObject("Microsoft.XMLHTTP");
        // }
        // ajax.onreadystatechange = function() {
        //     // readyState：状态值  0=>初始化 1=>载入 2=>载入完成 3=>解析 4=>完成
        //     // status：状态码 由HTTP协议根据所提交的信息，服务器所返回的HTTP头信息代码
        //     if (ajax.readyState == 4 && ajax.status == 200) {
        //         alert(ajax.responseText);
        //         result = ajax.responseText;
        //         document.getElementById("num").value=result;
        //     }
        // }
        // // 最后一个参数为true时为异步，执行send（）方法后不等待服务器的执行结果；false为同步
        // ajax.open("POST", "savePic.php", true);
        // ajax.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        // // 将图片发送给php代码
        // ajax.send("img=" + img);
        $.ajax({
            url: "savePic.php",
            type: "POST",
            headers: {
                "Content-type": "application/x-www-form-urlencoded"
            },
            data: {
                img: img,
            },
            success: function(data){
                alert(data);
                document.getElementById("num").value = data;
            },
            beforeSend: function(){
                $('<div class="loading"></div>').appendTo("body");
            },
            compelete: function(){
                $(".loading").remove();
            }
        })
    }
}
