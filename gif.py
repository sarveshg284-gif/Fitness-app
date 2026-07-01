import streamlit as st

st.set_page_config(page_title="Flower Animation", layout="centered")

html_code = """
<!DOCTYPE html>
<html>
<head>

<style>

body{
    margin:0;
    background:black;
    overflow:hidden;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}

.scene{
    position:relative;
    width:350px;
    height:500px;
}

.flower{
    position:absolute;
    bottom:80px;
    left:50%;
    transform:translateX(-50%);
}

.stem{
    width:6px;
    height:220px;
    background:#26ff5d;
    margin:auto;
    animation:grow 3s ease forwards;
}

.petal{
    position:absolute;
    width:45px;
    height:70px;
    background:#ff0088;
    border-radius:50%;
    opacity:0;
    transform:scale(0);
    animation:bloom 1s 2s forwards;
}

.p1{
    top:-40px;
    left:-20px;
    transform:rotate(-35deg);
}

.p2{
    top:-40px;
    left:20px;
    transform:rotate(35deg);
}

.p3{
    top:-70px;
    left:0;
}

.center{
    width:30px;
    height:30px;
    background:#ff4da6;
    border-radius:50%;
    position:absolute;
    top:-20px;
    left:0;
}

.leaf{
    position:absolute;
    width:80px;
    height:25px;
    background:#00ff66;
    border-radius:50px;
}

.left{
    top:100px;
    left:-70px;
    transform:rotate(-40deg);
}

.right{
    top:150px;
    right:-70px;
    transform:rotate(40deg);
}

.text{
    position:absolute;
    top:60px;
    width:100%;
    text-align:center;
    color:white;
    font-size:22px;
    opacity:0;
    animation:show 2s 3s forwards;
}

@keyframes grow{
from{
height:0;
}
to{
height:220px;
}
}

@keyframes bloom{
to{
opacity:1;
transform:scale(1);
}
}

@keyframes show{
to{
opacity:1;
}
}

</style>

</head>

<body>

<div class="scene">

<div class="text">
🌸 @CODE_ZENITH.AI
</div>

<div class="flower">

<div class="stem"></div>

<div class="leaf left"></div>
<div class="leaf right"></div>

<div class="petal p1"></div>
<div class="petal p2"></div>
<div class="petal p3"></div>

<div class="center"></div>

</div>

</div>

</body>
</html>
"""

st.components.v1.html(html_code, height=550)
