import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Open City 2D",
    page_icon="🏙️",
    layout="centered"
)

st.title("🏙️ Open City 2D")
st.caption("WASD / phím mũi tên để chơi • E để vào/ra xe • R để chơi lại")

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
html,body{
    margin:0;
    padding:0;
    background:#111827;
    color:white;
    font-family:Arial,sans-serif;
    text-align:center;
}

#hud{
    display:flex;
    justify-content:center;
    flex-wrap:wrap;
    gap:7px;
    margin:8px;
}

.stat{
    background:#1f2937;
    border-radius:8px;
    padding:7px 10px;
    font-weight:bold;
}

canvas{
    display:block;
    margin:auto;
    width:min(900px,100%);
    height:auto;
    border:3px solid #374151;
    border-radius:10px;
    background:#4d8b45;
}

#message{
    min-height:25px;
    margin:7px;
    color:#facc15;
    font-weight:bold;
}

button{
    border:0;
    border-radius:9px;
    color:white;
    font-weight:bold;
    cursor:pointer;
}

#restart{
    background:#2563eb;
    padding:10px 22px;
    font-size:16px;
}

.controls{
    display:grid;
    grid-template-columns:repeat(3,62px);
    justify-content:center;
    gap:5px;
    margin-top:9px;
}

.controls button{
    height:52px;
    background:#374151;
    font-size:20px;
}

#action{
    margin-top:7px;
    background:#16a34a;
    padding:11px 24px;
    font-size:16px;
}

</style>
</head>

<body>

<div id="hud">

<div class="stat">❤️ <span id="health">100</span></div>
<div class="stat">💰 $<span id="money">100</span></div>
<div class="stat">⭐ <span id="wanted">0</span></div>
<div class="stat">🚗 <span id="car">Đi bộ</span></div>
<div class="stat">📦 <span id="mission">Không có</span></div>

</div>

<canvas id="game" width="900" height="600"></canvas>

<div id="message">
Chào mừng đến Open City!
</div>

<button id="restart">
🔄 Chơi lại
</button>

<button id="action">
🚗 Vào / Ra xe
</button>

<div class="controls">

<div></div>
<button id="up">⬆️</button>
<div></div>

<button id="left">⬅️</button>
<button id="down">⬇️</button>
<button id="right">➡️</button>

</div>

<script>

const canvas=document.getElementById("game");
const ctx=canvas.getContext("2d");

const W=canvas.width;
const H=canvas.height;

const WORLD_W=5000;
const WORLD_H=4000;

let keys={};

let player;
let cars=[];
let police=[];
let npcs=[];
let buildings=[];
let trees=[];
let shops=[];

let camera={
    x:0,
    y:0
};

let money=100;
let health=100;
let wanted=0;

let mission=null;

let running=false;
let lastTime=0;

let gameOver=false;


/* =========================
   INPUT
========================= */

document.addEventListener("keydown",function(e){

    keys[e.key.toLowerCase()]=true;

    if(e.key.toLowerCase()==="e"){
        enterExitCar();
    }

    if(e.key.toLowerCase()==="r"){
        restart();
    }

    if(
        ["arrowup","arrowdown",
         "arrowleft","arrowright",
         " "].includes(e.key.toLowerCase())
    ){
        e.preventDefault();
    }

});

document.addEventListener("keyup",function(e){
    keys[e.key.toLowerCase()]=false;
});


/* =========================
   PLAYER
========================= */

function createPlayer(){

    player={
        x:2500,
        y:2000,
        r:14,
        speed:3.4,
        inCar:false,
        car:null
    };

}


/* =========================
   CITY
========================= */

function createCity(){

    buildings=[];
    trees=[];
    cars=[];
    police=[];
    npcs=[];
    shops=[];

    /* buildings */

    for(let x=100;x<WORLD_W-200;x+=450){

        for(let y=100;y<WORLD_H-200;y+=400){

            let w=280+Math.random()*70;
            let h=220+Math.random()*60;

            buildings.push({
                x:x+60,
                y:y+60,
                w:w,
                h:h,
                color:[
                    "#475569",
                    "#52525b",
                    "#64748b",
                    "#57534e",
                    "#334155"
                ][Math.floor(Math.random()*5)]
            });

        }

    }


    /* trees */

    for(let i=0;i<280;i++){

        trees.push({
            x:Math.random()*WORLD_W,
            y:Math.random()*WORLD_H,
            r:8+Math.random()*10
        });

    }


    /* cars */

    const colors=[
        "#ef4444",
        "#3b82f6",
        "#eab308",
        "#a855f7",
        "#f97316",
        "#14b8a6",
        "#f43f5e"
    ];

    for(let i=0;i<55;i++){

        let horizontal=Math.random()>0.5;

        cars.push({
            x:Math.random()*WORLD_W,
            y:Math.random()*WORLD_H,
            w:44,
            h:23,
            color:colors[
                Math.floor(Math.random()*colors.length)
            ],
            vx:horizontal
                ?(Math.random()>0.5?1.5:-1.5)
                :0,
            vy:horizontal
                ?0
                :(Math.random()>0.5?1.5:-1.5),
            occupied:false
        });

    }


    /* NPC */

    for(let i=0;i<100;i++){

        npcs.push({
            x:Math.random()*WORLD_W,
            y:Math.random()*WORLD_H,
            vx:(Math.random()-0.5)*0.6,
            vy:(Math.random()-0.5)*0.6
        });

    }


    /* shops */

    shops.push(
        {
            x:800,
            y:700,
            type:"hospital",
            name:"🏥 BỆNH VIỆN"
        },
        {
            x:4200,
            y:700,
            type:"shop",
            name:"🏪 CỬA HÀNG"
        },
        {
            x:900,
            y:3300,
            type:"garage",
            name:"🔧 GARAGE"
        }
    );

}


/* =========================
   COLLISION
========================= */

function circleRect(px,py,r,rect){

    let cx=Math.max(
        rect.x,
        Math.min(px,rect.x+rect.w)
    );

    let cy=Math.max(
        rect.y,
        Math.min(py,rect.y+rect.h)
    );

    let dx=px-cx;
    let dy=py-cy;

    return dx*dx+dy*dy<r*r;

}


function blocked(x,y,r){

    for(let b of buildings){

        if(circleRect(x,y,r,b)){
            return true;
        }

    }

    return false;

}


/* =========================
   PLAYER MOVEMENT
========================= */

function movePlayer(dt){

    let dx=0;
    let dy=0;

    if(keys["w"]||keys["arrowup"])dy--;
    if(keys["s"]||keys["arrowdown"])dy++;
    if(keys["a"]||keys["arrowleft"])dx--;
    if(keys["d"]||keys["arrowright"])dx++;

    if(dx===0&&dy===0)return;

    let len=Math.sqrt(dx*dx+dy*dy);

    dx/=len;
    dy/=len;

    let speed=
        player.inCar
        ?6
        :player.speed;

    let nx=player.x+dx*speed*dt;
    let ny=player.y+dy*speed*dt;

    if(
        nx>20 &&
        nx<WORLD_W-20 &&
        !blocked(nx,player.y,player.r)
    ){
        player.x=nx;
    }

    if(
        ny>20 &&
        ny<WORLD_H-20 &&
        !blocked(player.x,ny,player.r)
    ){
        player.y=ny;
    }

    if(player.inCar && player.car){

        player.car.x=player.x;
        player.car.y=player.y;

    }

}


/* =========================
   CARS
========================= */

function updateCars(){

    for(let c of cars){

        if(c.occupied)continue;

        c.x+=c.vx;
        c.y+=c.vy;

        if(c.x<-100)c.x=WORLD_W+100;
        if(c.x>WORLD_W+100)c.x=-100;

        if(c.y<-100)c.y=WORLD_H+100;
        if(c.y>WORLD_H+100)c.y=-100;

    }

}


/* =========================
   NPC
========================= */

function updateNPCs(){

    for(let n of npcs){

        n.x+=n.vx;
        n.y+=n.vy;

        if(n.x<10||n.x>WORLD_W-10)n.vx*=-1;
        if(n.y<10||n.y>WORLD_H-10)n.vy*=-1;

    }

}


/* =========================
   ENTER EXIT
========================= */

function enterExitCar(){

    if(gameOver)return;

    if(player.inCar){

        player.inCar=false;

        if(player.car){
            player.car.occupied=false;
        }

        player.car=null;

        document.getElementById("car").innerText="Đi bộ";

        message("Bạn đã xuống xe.");

        return;

    }


    let nearest=null;
    let best=Infinity;

    for(let c of cars){

        if(c.occupied)continue;

        let d=Math.hypot(
            c.x-player.x,
            c.y-player.y
        );

        if(d<best){
            best=d;
            nearest=c;
        }

    }

    if(nearest&&best<75){

        player.inCar=true;
        player.car=nearest;

        nearest.occupied=true;

        player.x=nearest.x;
        player.y=nearest.y;

        document.getElementById("car")
            .innerText="Đang lái";

        message("🚗 Bạn đã vào xe!");

    }else{

        message("Không có xe gần bạn.");

    }

}


/* =========================
   MISSION
========================= */

function newMission(){

    mission={
        x:500+Math.random()*(WORLD_W-1000),
        y:500+Math.random()*(WORLD_H-1000),
        reward:100+Math.floor(Math.random()*250)
    };

    message(
        "📦 Nhiệm vụ mới! Hãy đến điểm vàng."
    );

}


function checkMission(){

    if(!mission)return;

    let d=Math.hypot(
        player.x-mission.x,
        player.y-mission.y
    );

    if(d<65){

        money+=mission.reward;

        message(
            "✅ Hoàn thành! +$"+
            mission.reward
        );

        mission=null;

        setTimeout(
            newMission,
            2500
        );

    }

}


/* =========================
   POLICE
========================= */

function createPolice(){

    if(wanted<1)return;

    if(police.length>=wanted*2)return;

    police.push({
        x:player.x+(Math.random()-0.5)*700,
        y:player.y+(Math.random()-0.5)*700,
        speed:1.5+wanted*0.25
    });

}


function updatePolice(){

    if(wanted<=0){

        police=[];

        return;

    }

    createPolice();

    for(let p of police){

        let dx=player.x-p.x;
        let dy=player.y-p.y;

        let d=Math.hypot(dx,dy);

        if(d>1){

            p.x+=dx/d*p.speed;
            p.y+=dy/d*p.speed;

        }

        if(d<35){

            health-=0.08*wanted;

            if(health<=0){

                health=0;
                gameOver=true;

                message(
                    "🚔 Bạn đã bị bắt!"
                );

            }

        }

    }

}


/* =========================
   WANTED
========================= */

function increaseWanted(){

    wanted=Math.min(
        5,
        wanted+1
    );

    message(
        "🚨 TRUY NÃ! Mức "+wanted
    );

}


function updateWanted(){

    if(wanted>0){

        wanted-=0.002;

        if(wanted<0){
            wanted=0;
        }

    }

}


/* =========================
   SHOPS
========================= */

function checkShops(){

    for(let s of shops){

        let d=Math.hypot(
            player.x-s.x,
            player.y-s.y
        );

        if(d<65){

            if(s.type==="hospital"){

                if(health<100){

                    health=100;

                    message(
                        "🏥 Đã hồi đầy máu!"
                    );

                }

            }

            if(s.type==="shop"){

                if(money>=25){

                    money-=25;
                    health=Math.min(
                        100,
                        health+30
                    );

                    message(
                        "🥤 Mua đồ hồi máu -$25"
                    );

                }

            }

            if(s.type==="garage"){

                if(player.inCar){

                    player.car.color="#22c55e";

                    message(
                        "🔧 Đã sơn xe màu xanh!"
                    );

                }

            }

        }

    }

}


/* =========================
   CAMERA
========================= */

function updateCamera(){

    camera.x=player.x-W/2;
    camera.y=player.y-H/2;

    camera.x=Math.max(
        0,
        Math.min(camera.x,WORLD_W-W)
    );

    camera.y=Math.max(
        0,
        Math.min(camera.y,WORLD_H-H)
    );

}


/* =========================
   DRAW WORLD
========================= */

function drawWorld(){

    ctx.fillStyle="#4d8b45";
    ctx.fillRect(0,0,W,H);


    /* roads */

    ctx.fillStyle="#374151";

    for(
        let x=0;
        x<WORLD_W;
        x+=450
    ){

        ctx.fillRect(
            x-camera.x,
            0,
            105,
            H
        );

    }

    for(
        let y=0;
        y<WORLD_H;
        y+=400
    ){

        ctx.fillRect(
            0,
            y-camera.y,
            W,
            105
        );

    }


    /* road lines */

    ctx.strokeStyle="#facc15";
    ctx.lineWidth=3;
    ctx.setLineDash([25,20]);

    for(
        let x=52;
        x<WORLD_W;
        x+=450
    ){

        ctx.beginPath();

        ctx.moveTo(
            x-camera.x,
            0
        );

        ctx.lineTo(
            x-camera.x,
            H
        );

        ctx.stroke();

    }

    for(
        let y=52;
        y<WORLD_H;
        y+=400
    ){

        ctx.beginPath();

        ctx.moveTo(
            0,
            y-camera.y
        );

        ctx.lineTo(
            W,
            y-camera.y
        );

        ctx.stroke();

    }

    ctx.setLineDash([]);


    /* buildings */

    for(let b of buildings){

        let x=b.x-camera.x;
        let y=b.y-camera.y;

        if(
            x<-400||
            x>W+100||
            y<-400||
            y>H+100
        )continue;

        ctx.fillStyle=b.color;

        ctx.fillRect(
            x,
            y,
            b.w,
            b.h
        );

        ctx.fillStyle="#cbd5e1";

        for(
            let wx=x+25;
            wx<x+b.w-20;
            wx+=48
        ){

            for(
                let wy=y+25;
                wy<y+b.h-15;
                wy+=43
            ){

                ctx.fillRect(
                    wx,
                    wy,
                    17,
                    13
                );

            }

        }

    }


    /* trees */

    for(let t of trees){

        let x=t.x-camera.x;
        let y=t.y-camera.y;

        if(
            x<-30||
            x>W+30||
            y<-30||
            y>H+30
        )continue;

        ctx.fillStyle="#713f12";

        ctx.fillRect(
            x-3,
            y,
            6,
            18
        );

        ctx.fillStyle="#166534";

        ctx.beginPath();

        ctx.arc(
            x,
            y,
            t.r,
            0,
            Math.PI*2
        );

        ctx.fill();

    }

}


/* =========================
   DRAW CARS
========================= */

function drawCars(){

    for(let c of cars){

        let x=c.x-camera.x;
        let y=c.y-camera.y;

        if(
            x<-60||
            x>W+60||
            y<-60||
            y>H+60
        )continue;

        ctx.save();

        ctx.translate(x,y);

        ctx.fillStyle=c.color;

        ctx.fillRect(
            -22,
            -11,
            44,
            22
        );

        ctx.fillStyle="#111827";

        ctx.fillRect(
            -10,
            -8,
            20,
            8
        );

        ctx.fillStyle="#111";

        ctx.fillRect(
            -17,
            -14,
            8,
            5
        );

        ctx.fillRect(
            9,
            -14,
            8,
            5
        );

        ctx.fillRect(
            -17,
            9,
            8,
            5
        );

        ctx.fillRect(
            9,
            9,
            8,
            5
        );

        ctx.restore();

    }

}


/* =========================
   DRAW NPC
========================= */

function drawNPCs(){

    for(let n of npcs){

        let x=n.x-camera.x;
        let y=n.y-camera.y;

        if(
            x<-20||
            x>W+20||
            y<-20||
            y>H+20
        )continue;

        ctx.fillStyle="#f5c2a0";

        ctx.beginPath();

        ctx.arc(
            x,
            y-9,
            6,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillStyle="#2563eb";

        ctx.fillRect(
            x-6,
            y-3,
            12,
            16
        );

    }

}


/* =========================
   DRAW POLICE
========================= */

function drawPolice(){

    for(let p of police){

        let x=p.x-camera.x;
        let y=p.y-camera.y;

        ctx.fillStyle="#2563eb";

        ctx.beginPath();

        ctx.arc(
            x,
            y,
            15,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillStyle="#ef4444";

        ctx.fillRect(
            x-9,
            y-18,
            18,
            6
        );

    }

}


/* =========================
   DRAW SHOPS
========================= */

function drawShops(){

    for(let s of shops){

        let x=s.x-camera.x;
        let y=s.y-camera.y;

        ctx.fillStyle=
            s.type==="hospital"
            ?"#ef4444"
            :"#f59e0b";

        ctx.beginPath();

        ctx.arc(
            x,
            y,
            25,
            0,
            Math.PI*2
        );

        ctx.fill();

        ctx.fillStyle="white";

        ctx.font="20px Arial";

        ctx.textAlign="center";

        ctx.fillText(
            s.type==="hospital"
            ?"✚"
            :"$",
            x,
            y+7
        );

    }

}


/* =========================
   DRAW PLAYER
========================= */

function drawPlayer(){

    if(player.inCar)return;

    let x=player.x-camera.x;
    let y=player.y-camera.y;

    ctx.fillStyle="#f5c2a0";

    ctx.beginPath();

    ctx.arc(
        x,
        y-12,
        7,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.fillStyle="#2563eb";

    ctx.fillRect(
        x-8,
        y-5,
        16,
        22
    );

    ctx.fillStyle="#111827";

    ctx.fillRect(
        x-8,
        y+17,
        6,
        11
    );

    ctx.fillRect(
        x+2,
        y+17,
        6,
        11
    );

}


/* =========================
   DRAW MISSION
========================= */

function drawMission(){

    if(!mission)return;

    let x=mission.x-camera.x;
    let y=mission.y-camera.y;

    ctx.fillStyle="rgba(250,204,21,.25)";

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        38,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.fillStyle="#facc15";

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        14,
        0,
        Math.PI*2
    );

    ctx.fill();

    ctx.fillStyle="#111";

    ctx.font="bold 16px Arial";
    ctx.textAlign="center";

    ctx.fillText(
        "$",
        x,
        y+6
    );

}


/* =========================
   MINIMAP
========================= */

function drawMinimap(){

    const mw=170;
    const mh=130;

    const x=W-mw-12;
    const y=12;

    ctx.fillStyle="rgba(0,0,0,.65)";

    ctx.fillRect(
        x,
        y,
        mw,
        mh
    );

    ctx.fillStyle="#374151";

    ctx.fillRect(
        x+20,
        y,
        8,
        mh
    );

    ctx.fillRect(
        x+70,
        y,
        8,
        mh
    );

    ctx.fillRect(
        x+120,
        y,
        8,
        mh
    );

    ctx.fillRect(
        x,
        y+40,
        mw,
        8
    );

    ctx.fillRect(
        x,
        y+90,
        mw,
        8
    );


    let px=
        x+
        player.x/WORLD_W*mw;

    let py=
        y+
        player.y/WORLD_H*mh;

    ctx.fillStyle="#22c55e";

    ctx.beginPath();

    ctx.arc(
        px,
        py,
        5,
        0,
        Math.PI*2
    );

    ctx.fill();


    if(mission){

        let mx=
            x+
            mission.x/WORLD_W*mw;

        let my=
            y+
            mission.y/WORLD_H*mh;

        ctx.fillStyle="#facc15";

        ctx.beginPath();

        ctx.arc(
            mx,
            my,
            4,
            0,
            Math.PI*2
        );

        ctx.fill();

    }

}


/* =========================
   DRAW
========================= */

function draw(){

    drawWorld();
    drawMission();
    drawCars();
    drawNPCs();
    drawPolice();
    drawShops();
    drawPlayer();
    drawMinimap();


    if(gameOver){

        ctx.fillStyle="rgba(0,0,0,.7)";

        ctx.fillRect(
            0,
            0,
            W,
            H
        );

        ctx.fillStyle="white";

        ctx.textAlign="center";

        ctx.font="bold 48px Arial";

        ctx.fillText(
            "GAME OVER",
            W/2,
            H/2-20
        );

        ctx.font="22px Arial";

        ctx.fillText(
            "Nhấn R hoặc Chơi lại",
            W/2,
            H/2+30
        );

    }

}


/* =========================
   UI
========================= */

function updateUI(){

    document.getElementById(
        "health"
    ).innerText=Math.max(
        0,
        Math.floor(health)
    );

    document.getElementById(
        "money"
    ).innerText=money;

    document.getElementById(
        "wanted"
    ).innerText=Math.ceil(wanted);

    document.getElementById(
        "mission"
    ).innerText=
        mission
        ?"Đang làm"
        :"Không có";

}


/* =========================
   MESSAGE
========================= */

let messageTimer;

function message(text){

    document.getElementById(
        "message"
    ).innerText=text;

    clearTimeout(messageTimer);

    messageTimer=setTimeout(
        ()=>{
            document.getElementById(
                "message"
            ).innerText=
                "Khám phá thành phố và hoàn thành nhiệm vụ.";
        },
        2500
    );

}


/* =========================
   GAME UPDATE
========================= */

function update(dt){

    if(gameOver)return;

    movePlayer(dt);

    updateCars();

    updateNPCs();

    updatePolice();

    updateWanted();

    checkMission();

    checkShops();

    updateCamera();

    updateUI();

}


/* =========================
   LOOP
========================= */

function loop(time){

    if(!running)return;

    let dt=
        Math.min(
            2,
            (time-lastTime)/16.67
        );

    lastTime=time;

    update(dt);

    draw();

    requestAnimationFrame(loop);

}


/* =========================
   START
========================= */

function start(){

    createPlayer();
    createCity();

    money=100;
    health=100;
    wanted=0;

    police=[];

    gameOver=false;

    newMission();

    running=true;

    updateCamera();

    updateUI();

    message(
        "🏙️ Thành phố đã sẵn sàng!"
    );

    requestAnimationFrame(loop);

}


/* =========================
   RESTART
========================= */

function restart(){

    running=false;

    setTimeout(
        start,
        50
    );

}


/* =========================
   MOBILE CONTROLS
========================= */

function buttonControl(id,key){

    const b=document.getElementById(id);

    b.addEventListener(
        "pointerdown",
        e=>{
            e.preventDefault();
            keys[key]=true;
        }
    );

    b.addEventListener(
        "pointerup",
        e=>{
            e.preventDefault();
            keys[key]=false;
        }
    );

    b.addEventListener(
        "pointerleave",
        ()=>{
            keys[key]=false;
        }
    );

}


buttonControl("up","w");
buttonControl("down","s");
buttonControl("left","a");
buttonControl("right","d");


document.getElementById(
    "action"
).onclick=enterExitCar;


document.getElementById(
    "restart"
).onclick=restart;


start();

</script>

</body>
</html>
"""

components.html(
    html,
    height=850,
    scrolling=False
)
