window.onload=function () {
    var box=document.querySelector(".box");
    var box2=document.querySelector(".box .a2");
    box2.onclick=function () {
        var time1=setInterval(function () {
            box.style.opacity-=0.01;
            if(box.style.opacity<0){
                box.style.display="none";
                clearInterval(time1);
            }
        },10);
    };
    var box3=document.querySelector(".box2 .dz");
    var box31=document.querySelector(".box2 .dz .dw");
    var box32=document.querySelector(".box2 .dz span");
    var box4=document.querySelector(".box2 .dizhi");
    box3.onmouseenter=function () {
        box4.classList.add('ondizhi');
    };
    box31.onmouseenter=function () {
        box4.classList.add('ondizhi');
    };
    box32.onmouseenter=function () {
        box4.classList.add('ondizhi');
    };
    box3.onmouseout=function () {
        box4.classList.remove('ondizhi');
    };
    box4.onmouseover= function () {
        box4.classList.add('ondizhi');
        box3.classList.add('onbox2');
    };
    box4.onmouseleave= function () {
        box4.classList.remove('ondizhi');
        box3.classList.remove('onbox2');
    };
    var box5=document.querySelector(".box2 .li");
    var box6=document.querySelector(".box2 .qy");
    box5.onmouseenter=function () {
        box6.classList.add('ondizhi');
    };
    box5.onmouseout=function () {
        box6.classList.remove('ondizhi');
    };
    var box51=document.querySelector(".box2 .li1");
    var box62=document.querySelector(".box2 .wd");
    box51.onmouseenter=function () {
        box62.classList.add('ondizhi');
    };
    box51.onmouseout=function () {
        box62.classList.remove('ondizhi');
    };
    var box7=document.querySelector(".box4 span a");
    var box8=document.querySelector(".box4 .div");
    box7.onmouseenter=function () {
        box8.classList.remove('onyifu');
    };
    box7.onmouseout=function () {
        box8.classList.add('onyifu');
    };
    var box9=document.querySelector(".box5 .box7 .li1");
    var box10=document.querySelector(".box5 .box8");
    box9.onmouseenter=function () {
        box10.classList.remove('onyifu');
    };
    box9.onmouseout=function () {
        box10.classList.add('onyifu');
    };
    box10.onmouseenter=function () {
        box10.classList.remove('onyifu');
    };
    box10.onmouseout=function () {
        box10.classList.add('onyifu');
    };
    var box11=document.querySelector(".box2 img");
    var box12=document.querySelector(".box2 .dewm");
    box11.onmouseenter=function () {
        box12.classList.remove('onyifu');
    };
    box11.onmouseout=function () {
        box12.classList.add('onyifu');
    };
};