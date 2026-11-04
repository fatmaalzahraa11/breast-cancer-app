"""Global CSS + hero banner HTML (animated canvas, counters, SVG illustration)."""

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.stApp {
  background:
    radial-gradient(900px 500px at 8% -10%, rgba(45,212,191,.13), transparent 60%),
    radial-gradient(800px 500px at 100% 0%, rgba(129,140,248,.14), transparent 60%),
    radial-gradient(700px 500px at 50% 120%, rgba(251,113,133,.09), transparent 60%),
    #070b16;
}
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.6rem; padding-bottom: 4rem; max-width: 1280px; animation: fadeUp .7s ease both; }

@keyframes fadeUp { from {opacity:0; transform: translateY(24px);} to {opacity:1; transform:none;} }
@keyframes floaty { 0%,100% { transform: translateY(0);} 50% { transform: translateY(-10px);} }
@keyframes glow { 0%,100% { box-shadow: 0 0 0 0 rgba(45,212,191,.0);} 50% { box-shadow: 0 0 32px 2px rgba(45,212,191,.25);} }
@keyframes shimmer { to { background-position: 200% center; } }
@keyframes pulse { 0%,100% { transform: scale(1);} 50% { transform: scale(1.06);} }
@keyframes spin { to { transform: rotate(360deg);} }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0a1020 0%, #0b1326 100%);
  border-right: 1px solid rgba(255,255,255,.06);
}
[data-testid="stSidebar"] .stRadio > div { gap: 4px; }
[data-testid="stSidebar"] .stRadio label {
  padding: 10px 14px; border-radius: 12px; border: 1px solid transparent;
  transition: all .25s ease; width: 100%; cursor: pointer;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: rgba(45,212,191,.08); border-color: rgba(45,212,191,.25); transform: translateX(4px);
}
.brand { display:flex; align-items:center; gap:12px; margin: 4px 0 18px; }
.brand .logo { width:44px; height:44px; border-radius:14px; display:grid; place-items:center; font-size:24px;
  background: linear-gradient(135deg,#2dd4bf,#818cf8); animation: glow 3.5s ease-in-out infinite; }
.brand .name { font-weight:800; font-size:20px; letter-spacing:.2px; line-height:1.1; }
.brand .tag { font-size:11px; color:#8b97ad; letter-spacing:1.6px; text-transform:uppercase; }
.side-note { font-size:12.5px; color:#8b97ad; line-height:1.55; padding:12px 14px;
  border:1px solid rgba(255,255,255,.07); border-radius:12px; background: rgba(255,255,255,.03); }

/* ---------- headers ---------- */
.page-head { margin: 4px 0 26px; animation: fadeUp .6s ease both; }
.page-head .task { display:inline-block; font-size:12px; font-weight:700; letter-spacing:1.6px; text-transform:uppercase;
  padding:6px 12px; border-radius:999px; color:#2dd4bf; background: rgba(45,212,191,.1); border:1px solid rgba(45,212,191,.3); }
.page-head h1 { font-size:42px; font-weight:800; margin:12px 0 6px; letter-spacing:-.5px;
  background: linear-gradient(90deg,#e6edf7,#9fb4ff,#2dd4bf,#e6edf7); background-size:200% auto;
  -webkit-background-clip:text; background-clip:text; color:transparent; animation: shimmer 6s linear infinite; }
.page-head p { color:#9aa7bd; font-size:16.5px; max-width: 820px; line-height:1.6; margin:0; }
.sec-title { font-size:22px; font-weight:700; margin: 30px 0 12px; display:flex; align-items:center; gap:10px; }
.sec-title:after { content:""; flex:1; height:1px; background: linear-gradient(90deg, rgba(255,255,255,.14), transparent); }

/* ---------- cards ---------- */
.glass { background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08); border-radius: 20px;
  padding: 22px 22px; backdrop-filter: blur(10px); transition: transform .3s ease, box-shadow .3s ease, border-color .3s ease;
  animation: fadeUp .7s ease both; height: 100%; }
.glass:hover { transform: translateY(-6px); border-color: rgba(45,212,191,.35); box-shadow: 0 18px 40px -18px rgba(45,212,191,.35); }
.kpi .label { font-size:12px; letter-spacing:1.4px; text-transform:uppercase; color:#8b97ad; font-weight:600; }
.kpi .value { font-size:34px; font-weight:800; margin-top:6px; line-height:1.1; }
.kpi .sub { font-size:13px; color:#9aa7bd; margin-top:6px; }
.step .num { width:40px; height:40px; border-radius:12px; display:grid; place-items:center; font-weight:800; font-size:17px; color:#06101f;
  background: linear-gradient(135deg,#2dd4bf,#818cf8); margin-bottom:14px; }
.step h4 { margin:0 0 6px; font-size:18px; font-weight:700; }
.step p { margin:0; color:#9aa7bd; font-size:14px; line-height:1.55; }
.chip { display:inline-block; padding:7px 14px; margin:4px 6px 4px 0; border-radius:999px; font-size:13.5px; font-weight:600;
  border:1px solid rgba(255,255,255,.12); background: rgba(255,255,255,.05); transition: all .25s; }
.chip:hover { background: rgba(45,212,191,.15); border-color:#2dd4bf; transform: translateY(-2px); }
.insight { border-left: 3px solid #2dd4bf; background: rgba(45,212,191,.07); padding: 14px 18px; border-radius: 0 14px 14px 0;
  color:#cfe9e6; font-size:14.5px; line-height:1.65; margin: 12px 0 6px; animation: fadeUp .6s ease both; }
.warn { border-left: 3px solid #fbbf24; background: rgba(251,191,36,.07); color:#f6e3b0; }
.check { display:flex; align-items:center; gap:12px; }
.check .ok { width:30px; height:30px; border-radius:50%; background: rgba(45,212,191,.18); color:#2dd4bf; display:grid; place-items:center; font-weight:800; }
.check .bad { background: rgba(251,113,133,.18); color:#fb7185; }
.result { border-radius: 24px; padding: 26px; text-align:center; animation: fadeUp .5s ease both, pulse 3s ease-in-out infinite; }
.result.benign { background: linear-gradient(135deg, rgba(45,212,191,.18), rgba(45,212,191,.05)); border:1px solid rgba(45,212,191,.5); box-shadow: 0 0 40px rgba(45,212,191,.2); }
.result.malignant { background: linear-gradient(135deg, rgba(251,113,133,.2), rgba(251,113,133,.05)); border:1px solid rgba(251,113,133,.55); box-shadow: 0 0 40px rgba(251,113,133,.25); }
.result .big { font-size: 40px; font-weight: 900; letter-spacing:-.5px; }
.result .small { color:#b6c2d6; font-size:14px; margin-top:6px; }
.legend-dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }

/* ---------- streamlit widgets ---------- */
.stButton > button, .stDownloadButton > button {
  border-radius: 14px; border: 1px solid rgba(45,212,191,.45); padding: 0.65rem 1.4rem; font-weight: 700;
  background: linear-gradient(135deg, rgba(45,212,191,.22), rgba(129,140,248,.22)); color: #e6edf7; transition: all .25s ease; }
.stButton > button:hover { transform: translateY(-3px); box-shadow: 0 12px 28px -10px rgba(45,212,191,.6); border-color:#2dd4bf; color:#fff; }
.stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid rgba(255,255,255,.08); }
.stTabs [data-baseweb="tab"] { border-radius: 12px 12px 0 0; padding: 10px 18px; font-weight: 600; transition: background .25s; }
.stTabs [data-baseweb="tab"]:hover { background: rgba(255,255,255,.05); }
[data-testid="stMetric"] { background: rgba(255,255,255,.04); border:1px solid rgba(255,255,255,.08); padding:16px 18px; border-radius:16px; transition: transform .25s; }
[data-testid="stMetric"]:hover { transform: translateY(-4px); }
[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; border: 1px solid rgba(255,255,255,.08); }
.stProgress > div > div > div > div { background: linear-gradient(90deg,#2dd4bf,#818cf8,#fb7185); background-size:200% auto; animation: shimmer 2s linear infinite; }
hr { border-color: rgba(255,255,255,.08); }
"""


def hero_html(n_samples, n_features, n_models):
    return """
<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:transparent;color:#e6edf7;overflow:hidden}
#hero{position:relative;height:520px;border-radius:28px;overflow:hidden;border:1px solid rgba(255,255,255,.09);
  background:linear-gradient(120deg,#08111f,#0d1b33,#10172e,#08111f);background-size:300% 300%;animation:bg 14s ease infinite}
@keyframes bg{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
canvas{position:absolute;inset:0;width:100%;height:100%}
.content{position:relative;z-index:2;height:100%;display:flex;align-items:center;padding:0 56px;gap:30px}
.left{flex:1.25}
.badge{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
  padding:8px 14px;border-radius:999px;color:#2dd4bf;background:rgba(45,212,191,.1);border:1px solid rgba(45,212,191,.35);
  opacity:0;animation:up .8s .1s forwards}
.dot{width:8px;height:8px;border-radius:50%;background:#2dd4bf;animation:blink 1.4s infinite}
@keyframes blink{50%{opacity:.25}}
h1{font-size:58px;line-height:1.04;font-weight:900;letter-spacing:-1.5px;margin:20px 0 14px;opacity:0;animation:up .9s .25s forwards}
.grad{background:linear-gradient(90deg,#2dd4bf,#818cf8,#fb7185,#2dd4bf);background-size:250% auto;-webkit-background-clip:text;background-clip:text;color:transparent;animation:sh 5s linear infinite}
@keyframes sh{to{background-position:250% center}}
.type{font-size:19px;color:#a8b6cc;height:30px;opacity:0;animation:up .9s .45s forwards}
.type b{color:#e6edf7}
.cursor{display:inline-block;width:2px;height:20px;background:#2dd4bf;margin-left:3px;vertical-align:-3px;animation:blink 1s infinite}
.stats{display:flex;gap:14px;margin-top:30px;opacity:0;animation:up .9s .65s forwards}
.stat{padding:14px 20px;border-radius:16px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);backdrop-filter:blur(8px);min-width:110px}
.stat .n{font-size:30px;font-weight:800;color:#fff}
.stat .l{font-size:11px;letter-spacing:1.4px;text-transform:uppercase;color:#8b97ad;margin-top:2px}
.right{flex:.9;display:flex;justify-content:center;opacity:0;animation:up 1s .5s forwards}
svg{width:100%;max-width:400px;filter:drop-shadow(0 0 40px rgba(45,212,191,.25))}
.cell{animation:fl 6s ease-in-out infinite}
.c2{animation-delay:-1.5s}.c3{animation-delay:-3s}.c4{animation-delay:-4.5s}.c5{animation-delay:-2.2s}
@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
.ring{transform-origin:200px 200px;animation:rot 28s linear infinite}
@keyframes rot{to{transform:rotate(360deg)}}
@keyframes up{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
@media(max-width:800px){.right{display:none}h1{font-size:40px}.content{padding:0 26px}}
</style></head><body>
<div id="hero"><canvas id="c"></canvas>
<div class="content">
 <div class="left">
  <span class="badge"><span class="dot"></span>AI-powered diagnostic support</span>
  <h1>Breast Cancer<br><span class="grad">Classification Intelligence</span></h1>
  <div class="type"><span id="t"></span><span class="cursor"></span></div>
  <div class="stats">
   <div class="stat"><div class="n" data-t="__N__">0</div><div class="l">Samples</div></div>
   <div class="stat"><div class="n" data-t="__F__">0</div><div class="l">Features</div></div>
   <div class="stat"><div class="n" data-t="__M__">0</div><div class="l">Models</div></div>
   <div class="stat"><div class="n" data-t="5">0</div><div class="l">Metrics</div></div>
  </div>
 </div>
 <div class="right">
  <svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg">
   <defs>
    <radialGradient id="g1" cx="35%" cy="30%"><stop offset="0" stop-color="#7ef0e1"/><stop offset="1" stop-color="#0f766e"/></radialGradient>
    <radialGradient id="g2" cx="35%" cy="30%"><stop offset="0" stop-color="#c4c9ff"/><stop offset="1" stop-color="#4338ca"/></radialGradient>
    <radialGradient id="g3" cx="35%" cy="30%"><stop offset="0" stop-color="#ffc2cb"/><stop offset="1" stop-color="#be123c"/></radialGradient>
    <radialGradient id="lens" cx="50%" cy="50%"><stop offset="0" stop-color="#0c1a30"/><stop offset="1" stop-color="#050b16"/></radialGradient>
    <clipPath id="clip"><circle cx="200" cy="200" r="150"/></clipPath>
   </defs>
   <circle cx="200" cy="200" r="172" fill="none" stroke="#2dd4bf" stroke-opacity=".35" stroke-width="2" stroke-dasharray="4 10" class="ring"/>
   <circle cx="200" cy="200" r="158" fill="none" stroke="#818cf8" stroke-opacity=".6" stroke-width="4"/>
   <circle cx="200" cy="200" r="150" fill="url(#lens)"/>
   <g clip-path="url(#clip)">
    <g class="cell"><circle cx="150" cy="150" r="46" fill="url(#g1)" opacity=".92"/><circle cx="146" cy="146" r="16" fill="#064e47"/></g>
    <g class="cell c2"><circle cx="258" cy="140" r="34" fill="url(#g2)" opacity=".92"/><circle cx="254" cy="136" r="12" fill="#1e1b6b"/></g>
    <g class="cell c3"><circle cx="230" cy="250" r="52" fill="url(#g3)" opacity=".92"/><circle cx="226" cy="246" r="22" fill="#6b0f28"/><circle cx="238" cy="258" r="9" fill="#6b0f28"/></g>
    <g class="cell c4"><circle cx="130" cy="262" r="30" fill="url(#g1)" opacity=".85"/><circle cx="127" cy="259" r="10" fill="#064e47"/></g>
    <g class="cell c5"><circle cx="300" cy="215" r="22" fill="url(#g2)" opacity=".85"/><circle cx="298" cy="213" r="7" fill="#1e1b6b"/></g>
    <rect x="50" y="-20" width="300" height="46" fill="#2dd4bf" opacity=".16">
      <animate attributeName="y" values="40;340;40" dur="5s" repeatCount="indefinite"/></rect>
    <rect x="50" y="24" width="300" height="2" fill="#2dd4bf" opacity=".9">
      <animate attributeName="y" values="62;362;62" dur="5s" repeatCount="indefinite"/></rect>
   </g>
   <g stroke="#2dd4bf" stroke-width="2" opacity=".8"><path d="M200 36v22M200 342v22M36 200h22M342 200h22"/></g>
  </svg>
 </div>
</div></div>
<script>
const cv=document.getElementById('c'),ctx=cv.getContext('2d');let W,H,P=[],mouse={x:-999,y:-999};
function size(){const r=cv.getBoundingClientRect();W=cv.width=r.width*devicePixelRatio;H=cv.height=r.height*devicePixelRatio}
size();addEventListener('resize',size);
for(let i=0;i<70;i++)P.push({x:Math.random(),y:Math.random(),vx:(Math.random()-.5)*.0006,vy:(Math.random()-.5)*.0006,r:Math.random()*2+1,
 c:['#2dd4bf','#818cf8','#fb7185'][i%3]});
cv.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();mouse.x=(e.clientX-r.left)/r.width;mouse.y=(e.clientY-r.top)/r.height});
cv.parentElement.addEventListener('mousemove',e=>{const r=cv.getBoundingClientRect();mouse.x=(e.clientX-r.left)/r.width;mouse.y=(e.clientY-r.top)/r.height});
function draw(){ctx.clearRect(0,0,W,H);
 for(const p of P){p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>1)p.vx*=-1;if(p.y<0||p.y>1)p.vy*=-1;
  const dx=p.x-mouse.x,dy=p.y-mouse.y,d=Math.hypot(dx,dy);if(d<.12){p.x+=dx*.02;p.y+=dy*.02}}
 for(let i=0;i<P.length;i++){const a=P[i];
  for(let j=i+1;j<P.length;j++){const b=P[j],d=Math.hypot((a.x-b.x)*W,(a.y-b.y)*H);
   if(d<140*devicePixelRatio){ctx.strokeStyle='rgba(129,140,248,'+(1-d/(140*devicePixelRatio))*.35+')';ctx.lineWidth=1;
    ctx.beginPath();ctx.moveTo(a.x*W,a.y*H);ctx.lineTo(b.x*W,b.y*H);ctx.stroke()}}
  ctx.fillStyle=a.c;ctx.globalAlpha=.85;ctx.beginPath();ctx.arc(a.x*W,a.y*H,a.r*devicePixelRatio,0,7);ctx.fill();ctx.globalAlpha=1}
 requestAnimationFrame(draw)}
draw();
document.querySelectorAll('[data-t]').forEach(el=>{const T=+el.dataset.t;let s=null;
 setTimeout(()=>{const step=ts=>{if(!s)s=ts;const k=Math.min((ts-s)/1600,1),e=1-Math.pow(1-k,3);el.textContent=Math.round(T*e);if(k<1)requestAnimationFrame(step)};requestAnimationFrame(step)},700)});
const phrases=['Compare <b>KNN, Decision Tree, Random Forest, ANN and SVM</b>','Tuned with <b>5-fold cross-validation</b>','Malignant is the <b>positive class</b>','Try a <b>live prediction</b> in seconds'];
let pi=0,ci=0,del=false;const t=document.getElementById('t');
function tick(){const txt=phrases[pi].replace(/<[^>]+>/g,'');
 if(!del){ci++;if(ci>=txt.length){del=true;setTimeout(tick,1600);render(txt,ci);return}}
 else{ci-=2;if(ci<=0){del=false;ci=0;pi=(pi+1)%phrases.length}}
 render(txt,ci);setTimeout(tick,del?18:38)}
function render(txt,n){const full=phrases[pi];let out='',cnt=0,tag=false,open=false;
 for(const ch of full){if(ch==='<'){tag=true;out+=ch;continue}if(tag){out+=ch;if(ch==='>')tag=false;continue}
  if(cnt<n){out+=ch;cnt++}}
 // close an open <b> if the text is cut inside bold
 if((out.match(/<b>/g)||[]).length>(out.match(/<\\/b>/g)||[]).length)out+='</b>';t.innerHTML=out}
tick();
</script></body></html>
""".replace("__N__", str(n_samples)).replace("__F__", str(n_features)).replace("__M__", str(n_models))
