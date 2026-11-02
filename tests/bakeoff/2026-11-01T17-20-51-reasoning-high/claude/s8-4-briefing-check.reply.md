I built the checker with a resolution picker (starting on A/HRC/RES/51/27 if it is in your data), an "Ask AI for a briefing" button that sends only the symbol and title, and a text box for the AI answer or your own text. "Check" extracts the vote counts, date, session and State-by-State claims and compares them with the recorded vote. Each row gets a verdict (matches, wrong, or cannot be checked), and the page explains why "cannot be checked" is not "wrong".

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Briefing checker: Human Rights Council resolutions</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{--accent:#1f6fb2;--bg:#f5f7fa;--ink:#1d2733;--mute:#5b6773;--line:#d9e0e7}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:1020px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:1.7rem;margin:0 0 4px;color:var(--accent)}
h2{font-size:1.2rem;margin:0 0 10px}
.lead{color:var(--mute);margin:0 0 20px}
.card{background:#fff;border:1px solid var(--line);border-radius:8px;padding:18px 20px;margin-bottom:20px}
.how{font-size:.9rem;color:var(--mute);background:#f0f5fa;border-left:3px solid var(--accent);padding:8px 12px;margin:12px 0 0}
.notice{font-size:.92rem;background:#fff8e1;border-left:3px solid #e0a800;padding:8px 12px;margin:10px 0}
.warn{color:#b3261e}
input[type=text],select,textarea{width:100%;font:inherit;padding:8px;border:1px solid #b9c4cf;border-radius:6px;background:#fff}
textarea{min-height:230px;resize:vertical}
button{font:inherit;background:var(--accent);color:#fff;border:0;border-radius:6px;padding:9px 18px;cursor:pointer}
button.alt{background:#fff;color:var(--accent);border:1px solid var(--accent)}
button:disabled{opacity:.5;cursor:default}
a{color:var(--accent)}
dl{display:grid;grid-template-columns:150px 1fr;gap:4px 14px;margin:12px 0 0}
dt{color:var(--mute)} dd{margin:0}
table{width:100%;border-collapse:collapse;margin-top:12px;font-size:.95rem}
th,td{text-align:left;vertical-align:top;padding:9px 8px;border-bottom:1px solid var(--line)}
th{background:#eef3f8}
.ctx{display:block;color:var(--mute);font-size:.85rem;margin-top:4px}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-weight:600;font-size:.9rem}
.v-match{background:#e3f4e8;color:#17692f}
.v-wrong{background:#fce8e6;color:#a8231b}
.v-na{background:#e9ecef;color:#444}
.note{display:block;font-size:.85rem;color:var(--mute);margin-top:4px}
.row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0}
.chip{font-size:.85rem;color:var(--mute)}
details{margin-top:10px} summary{cursor:pointer;color:var(--accent)}
.sum span{margin-right:16px;font-weight:600}
td:first-child{width:130px}
</style>
</head>
<body>
<main>
<h1>Briefing checker: Human Rights Council resolutions</h1>
<p class="lead" id="dataline"></p>

<section class="card">
  <h2>1. Choose a resolution</h2>
  <input type="text" id="flt" placeholder="Filter by symbol, title or year, e.g. 51/27 or death penalty">
  <div style="height:8px"></div>
  <select id="sel" size="7" aria-label="Recorded votes"></select>
  <div id="rec"></div>
  <p class="how"><b>How this is computed:</b> the list is every recorded vote in the data (resolutions and amendments), newest first. The "official total" is the figure published with the record; the "roll call" is our count of the individual State votes in that same record. For a few records the two differ, so both are shown and used below.</p>
</section>

<section class="card">
  <h2>2. The briefing text</h2>
  <div class="row">
    <button id="askBtn">Ask AI for a briefing</button>
    <button id="stopBtn" class="alt" hidden>Stop waiting</button>
    <span id="askStatus" class="chip"></span>
  </div>
  <p class="notice"><b>What leaves your browser:</b> pressing the button sends <b>one request</b> to a language model containing <b>only the symbol and the title</b> of the selected resolution. None of the vote data is sent. Nothing is sent unless you press the button.</p>
  <details><summary>Show the exact prompt that will be sent</summary><pre id="promptView" style="white-space:pre-wrap;background:#f5f7fa;padding:10px;border-radius:6px"></pre></details>
  <p style="margin-bottom:6px"><label for="txt"><b>Briefing text</b>: the AI answer appears here. You can edit it or paste a text of your own.</label></p>
  <textarea id="txt" placeholder="Paste or write a briefing here, e.g. “The resolution was adopted on 6 October 2022 at the 51st session by 20 votes in favour, 16 against and 11 abstentions. France voted against.”"></textarea>
  <div class="row"><button id="checkBtn">Check</button><span class="chip" id="origin"></span></div>
</section>

<section class="card" id="results" hidden>
  <h2>3. What the recorded vote says about each claim</h2>
  <div id="resHead"></div>
  <div id="resBody"></div>
  <p class="notice"><b>“Cannot be checked in this data” is not the same as “wrong”.</b> It means this dataset holds nothing to compare the claim with (for example a State that has no vote in this record, a date that is not about the vote, or a special session). The claim may be true or false; check it against the resolution itself. Only <b>“Wrong”</b> means the recorded vote contradicts the claim.</p>
  <p class="how"><b>How this is computed:</b> plain pattern matching in your browser, no AI. The checker looks for: numbers in favour / against / abstaining (digits or words, e.g. “29 votes to 16”), full or partial dates, the session number, “by consensus / unanimously”, and States named together with “in favour”, “against” or “abstained” in the same clause. It does <b>not</b> check what the resolution says or does. It can misread complex sentences, so read the quoted sentence under each claim.</p>
  <div id="unchecked"></div>
</section>
</main>

<script>
(function(){
const D=window.WORKSHOP_DATA||{};
const H=D.hrc||{records:[],countries:{}};
const recs=(H.records||[]).slice().sort((a,b)=>(b.date||'').localeCompare(a.date||''));
const byId={};recs.forEach(r=>byId[r.id]=r);
const $=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const WORD={yes:'in favour',no:'against',abs:'abstaining'};
const LET={yes:'Y',no:'N',abs:'A'};
const LETWORD={Y:'in favour',N:'against',A:'abstained'};
const MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December'];
const CARD={zero:0,one:1,two:2,three:3,four:4,five:5,six:6,seven:7,eight:8,nine:9,ten:10,eleven:11,twelve:12,thirteen:13,fourteen:14,fifteen:15,sixteen:16,seventeen:17,eighteen:18,nineteen:19,twenty:20,thirty:30,forty:40,fifty:50,sixty:60};
const ORD={first:1,second:2,third:3,fourth:4,fifth:5,sixth:6,seventh:7,eighth:8,ninth:9,tenth:10,eleventh:11,twelfth:12,thirteenth:13,fourteenth:14,fifteenth:15,sixteenth:16,seventeenth:17,eighteenth:18,nineteenth:19,twentieth:20,thirtieth:30,fortieth:40,fiftieth:50,sixtieth:60};
const NW=Object.assign({},CARD,ORD);
const alt=o=>Object.keys(o).sort((a,b)=>b.length-a.length).join('|');
const C='(?:\\d{1,2}|(?:'+alt(CARD)+')(?:[-\\s](?:'+alt(CARD)+'))?)';
const MON='January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec';
const num=s=>/^\d+$/.test(s)?+s:s.toLowerCase().split(/[-\s]+/).reduce((a,t)=>a+(NW[t]||0),0);
const mi=s=>MONTHS.findIndex(x=>x.toLowerCase().slice(0,3)===s.toLowerCase().slice(0,3))+1;
const ALIAS={USA:['usa','united states','united states of america'],GBR:['uk','united kingdom','britain','great britain','united kingdom of great britain and northern ireland'],RUS:['russia','russian federation'],KOR:['south korea','republic of korea'],VNM:['vietnam','viet nam'],CIV:['ivory coast',"cote d'ivoire"],CZE:['czechia','czech republic'],MKD:['north macedonia'],COD:['democratic republic of the congo','drc','dr congo'],VEN:['venezuela'],BOL:['bolivia'],TZA:['tanzania'],IRN:['iran'],MDA:['moldova'],SYR:['syria'],PSE:['palestine']};
const norm=s=>String(s).replace(/[\u2018\u2019]/g,"'").normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();

let cur=null,origin='user',askToken=0;

/* ---------- helpers on records ---------- */
function roll(r){const c={Y:0,N:0,A:0};let n=0;for(const k in (r.votes||{})){const v=r.votes[k];if(c[v]!==undefined){c[v]++;n++;}}return n?c:null;}
function docLink(r){const u=r.doc_url||r.record_url;return u?'<a href="'+esc(u)+'" target="_blank" rel="noopener">'+esc(r.symbol)+'</a>':esc(r.symbol);}
function fmtDate(d){const m=/^(\d{4})-(\d\d)-(\d\d)/.exec(d||'');return m?(+m[3])+' '+MONTHS[+m[2]-1]+' '+m[1]+' ('+d+')':(d||'no date');}
function sessionNum(r){const s=r.session||'';if(/special/i.test(s))return null;let m=s.match(/(\d+)(?:st|nd|rd|th)/)||s.match(/\b(\d+)\b/)||String(r.symbol||'').match(/A\/HRC\/(?:RES\/)?(\d+)\//);return m?+m[1]:null;}
function buildPrompt(r){return 'Write a briefing of about 250 words on Human Rights Council resolution '+r.symbol+', titled "'+r.title+'". Use only what you already know about it; you have no other source. Say when it was adopted, at which session, and how the Council voted (numbers in favour, against and abstaining, and which States voted which way), if you know. If you do not know a detail, say so instead of guessing.';}

/* ---------- header, list ---------- */
(function(){
  const years=recs.map(r=>r.year).filter(Number.isInteger);
  const nA=recs.filter(r=>r.kind==='amendment').length;
  $('dataline').textContent=(H.title||'Human Rights Council recorded votes')+(H.source?' · source: '+H.source:'')+' · n = '+recs.length+' recorded votes ('+(recs.length-nA)+' resolutions, '+nA+' amendments)'+(years.length?' · '+Math.min(...years)+'–'+Math.max(...years):'');
})();
function fillList(keep){
  const q=norm($('flt').value.trim());
  const list=recs.filter(r=>!q||norm(r.symbol+' '+r.title+' '+r.year).includes(q));
  $('sel').innerHTML=list.map(r=>'<option value="'+esc(r.id)+'">'+esc(r.symbol+' ('+(r.year||'?')+') '+(r.kind==='amendment'?'[amendment] ':'')+'— '+String(r.title||'').slice(0,110))+'</option>').join('');
  if(list.length){const want=list.find(r=>r.id===keep)||list[0];$('sel').value=want.id;if(!cur||cur.id!==want.id)choose(want.id);}
}
function choose(id){
  const had=cur&&$('txt').value.trim();
  cur=byId[id]||null;renderRec();$('results').hidden=true;
  $('askBtn').disabled=!cur;$('checkBtn').disabled=!cur;
  $('promptView').textContent=cur?buildPrompt(cur):'';
  if(had)$('askStatus').textContent='The resolution changed: the text below may be about another one.';
}
function renderRec(){
  const r=cur;if(!r){$('rec').innerHTML='<p class="warn">No recorded votes available in this data.</p>';return;}
  const R=roll(r);
  let h='<dl><dt>Symbol</dt><dd>'+docLink(r)+' <span class="chip">('+esc(r.kind||'')+')</span></dd>'
   +'<dt>Title</dt><dd>'+esc(r.title)+'</dd><dt>Date</dt><dd>'+esc(fmtDate(r.date))+'</dd>'
   +'<dt>Session</dt><dd>'+esc(r.session||'not given')+(r.agenda_item?' · '+esc(r.agenda_item):'')+'</dd>'
   +'<dt>Main sponsors</dt><dd>'+((r.main_sponsors||[]).length?esc(r.main_sponsors.join('; ')):'not given')+'</dd>'
   +'<dt>Official total</dt><dd>'+esc(r.yes)+' in favour · '+esc(r.no)+' against · '+esc(r.abstain)+' abstaining</dd>'
   +'<dt>Roll call counted</dt><dd>'+(R?R.Y+' in favour · '+R.N+' against · '+R.A+' abstaining':'no individual votes in this record')+'</dd></dl>';
  if(R&&(R.Y!==r.yes||R.N!==r.no||R.A!==r.abstain))h+='<p class="notice">For this record the official total and the roll call differ (a gap in the source). Both are shown in the checks below.</p>';
  if(R){const g={Y:[],N:[],A:[]};for(const k in r.votes)if(g[r.votes[k]])g[r.votes[k]].push((H.countries||{})[k]||k);
    h+='<details><summary>Show the roll call by State</summary>'+['Y','N','A'].map(l=>'<p><b>'+LETWORD[l]+' ('+g[l].length+'):</b> '+esc(g[l].sort().join(', ')||'none')+'</p>').join('')+'</details>';}
  $('rec').innerHTML=h;
}
$('flt').addEventListener('input',()=>fillList(cur&&cur.id));
$('sel').addEventListener('change',()=>choose($('sel').value));

/* ---------- ask the model ---------- */
$('askBtn').addEventListener('click',async()=>{
  if(!cur)return;
  if(typeof studio==='undefined'||!studio.ask){$('askStatus').textContent='The AI helper is not available here. Paste a text instead.';return;}
  const token=++askToken;
  $('askBtn').disabled=true;$('stopBtn').hidden=false;$('askStatus').textContent='Sent 1 request (symbol and title only). Waiting for the model…';
  try{
    const out=await studio.ask(buildPrompt(cur));
    if(token!==askToken)return;
    $('txt').value=typeof out==='string'?out:JSON.stringify(out);
    origin='ai';$('txt').setAttribute('data-source','ai');
    $('origin').textContent='Text source: AI answer (not verified)';$('askStatus').textContent='Answer received. Now press Check.';
  }catch(e){if(token===askToken)$('askStatus').textContent='The request failed: '+(e&&e.message?e.message:e);}
  if(token===askToken){$('askBtn').disabled=false;$('stopBtn').hidden=true;}
});
$('stopBtn').addEventListener('click',()=>{askToken++;$('askBtn').disabled=false;$('stopBtn').hidden=true;$('askStatus').textContent='Stopped waiting. Any late answer is ignored.';});
$('txt').addEventListener('input',()=>{origin='user';$('txt').removeAttribute('data-source');$('origin').textContent=$('txt').value.trim()?'Text source: pasted or edited by you':'';});

/* ---------- claim extraction ---------- */
function splitSentences(t){
  const out=[];let s=0;const re=/[.!?]+(?=\s|$)|\n+/g;let m;
  function push(a,b){if(t.slice(a,b).trim())out.push({start:a,end:b,text:t.slice(a,b).trim()});}
  while((m=re.exec(t))){
    if(m[0]==='.'&&/(?:^|[\s(.])(?:[A-Z]|No|Nos|Res|Art|St|Dr|Mr|Ms)$/.test(t.slice(Math.max(0,m.index-4),m.index)))continue;
    const e=m.index+m[0].length;push(s,e);s=e;
  }
  push(s,t.length);return out;
}
function findClaims(text,r){
  const claims=[],spans=[],sents=splitSentences(text),R=roll(r);
  const free=(s,e)=>!spans.some(p=>s<p[1]&&e>p[0]);
  const sentOf=i=>sents.find(x=>i>=x.start&&i<x.end)||{text:''};
  const push=(type,written,pos,j)=>claims.push(Object.assign({type,written,pos,sent:sentOf(pos).text},j));
  const scan=(re,fn)=>{let m;while((m=re.exec(text))){const s=m.index,e=s+m[0].length;if(!free(s,e))continue;if(fn(m,s,e)!==false)spans.push([s,e]);}};
  const OFF={yes:'yes',no:'no',abs:'abstain'};

  function judgeCount(key,n){
    const off=Number.isInteger(r[OFF[key]])?r[OFF[key]]:null,ro=R?R[LET[key]]:null;
    const rec='Official total '+WORD[key]+': '+(off==null?'not given':off)+' · roll call counted: '+(ro==null?'no roll call':ro);
    if(off==null&&ro==null)return{v:'na',rec,note:'This record has no figure for this.'};
    const a=off!=null&&n===off,b=ro!=null&&n===ro;
    if(a&&b)return{v:'match',rec,note:''};
    if(a||b)return{v:'match',rec,note:'The official total and the roll call disagree here; the claim agrees with the '+(a?'official total':'roll call')+'.'};
    return{v:'wrong',rec,note:''};
  }
  // counts
  scan(new RegExp('\\b('+C+')(?:\\s+votes?)?\\s+to\\s+('+C+')\\b','gi'),(m,s,e)=>{
    if(!/vot|adopt|pass|approv|carried/i.test(text.slice(Math.max(0,s-60),e+20)))return false;
    push('In favour (count)',m[0],s,judgeCount('yes',num(m[1])));push('Against (count)',m[0],s,judgeCount('no',num(m[2])));
  });
  const F='(?:\\s+(?:votes?|States|members?|countries|delegations?|nations?))?(?:\\s+(?:voted|voting|were|are|being|cast))?';
  const KW={yes:'(?:in\\s+favou?r|yes\\b|for\\b(?=\\s*[,;)]|\\s+and\\b|\\s+(?:the\\s+)?(?:resolution|text|draft|adoption)))',no:'(?:against|opposed|in\\s+opposition|no\\b)',abs:'(?:abstentions?|abstain\\w*)'};
  const TYPE={yes:'In favour (count)',no:'Against (count)',abs:'Abstaining (count)'};
  for(const k of ['yes','no','abs'])scan(new RegExp('\\b('+C+')'+F+'\\s+'+KW[k],'gi'),(m,s)=>push(TYPE[k],m[0],s,judgeCount(k,num(m[1]))));
  scan(new RegExp('\\b(in\\s+favou?r|against|abstentions?)\\s*[:=(]\\s*('+C+')\\b','gi'),(m,s)=>{const k=/^in/i.test(m[1])?'yes':/^ag/i.test(m[1])?'no':'abs';push(TYPE[k],m[0],s,judgeCount(k,num(m[2])));});
  scan(/\bno\s+(abstentions?|votes?\s+against|States\s+(?:voted\s+)?against)/gi,(m,s)=>{const k=/^abst/i.test(m[1])?'abs':'no';push(TYPE[k],m[0],s,judgeCount(k,0));});
  scan(/\b(by\s+consensus|without\s+a\s+(?:recorded\s+)?vote|unanimously)\b/gi,(m,s)=>{
    const una=/unanim/i.test(m[1]);const off=[r.no,r.abstain];
    const rec='A recorded vote exists: '+r.yes+' in favour, '+r.no+' against, '+r.abstain+' abstaining (official totals)';
    if(una)push('Unanimity',m[0],s,(r.no===0&&r.abstain===0)?{v:'match',rec,note:''}:{v:'wrong',rec,note:'Votes against or abstentions were recorded.'});
    else push('Adopted without a vote',m[0],s,{v:'wrong',rec,note:'This dataset holds only recorded votes, so a vote took place.'});
  });
  // dates
  const dm=/^(\d{4})-(\d\d)-(\d\d)/.exec(r.date||'');
  const RD=dm?{y:+dm[1],mo:+dm[2],d:+dm[3]}:null;
  const recDate='Vote date in the record: '+fmtDate(r.date);
  function judgeDate(c,s,e){
    if(!/adopt|vot|passed|approv|carried/i.test(text.slice(Math.max(0,s-35),e+25)))return{v:'na',rec:recDate,note:'The wording does not say this is the date of the vote, and this data holds only the vote date.'};
    if(!RD)return{v:'na',rec:recDate,note:'The record has no usable date.'};
    const ok=c.y===RD.y&&(c.mo==null||c.mo===RD.mo)&&(c.d==null||c.d===RD.d);
    if(ok)return{v:'match',rec:recDate,note:c.d==null?'Only the '+(c.mo?'month and year':'year')+' was claimed.':''};
    return{v:'wrong',rec:recDate,note:(c.y===RD.y&&c.mo===RD.mo&&c.d!=null)?'Same month, different day.':''};
  }
  const dps=[
    [/\b((?:19|20)\d\d)-(\d\d)-(\d\d)\b/g,m=>({y:+m[1],mo:+m[2],d:+m[3]})],
    [new RegExp('\\b(\\d{1,2})(?:st|nd|rd|th)?\\s+(?:of\\s+)?('+MON+')\\.?,?\\s+((?:19|20)\\d\\d)\\b','gi'),m=>({d:+m[1],mo:mi(m[2]),y:+m[3]})],
    [new RegExp('\\b('+MON+')\\.?\\s+(\\d{1,2})(?:st|nd|rd|th)?,?\\s+((?:19|20)\\d\\d)\\b','gi'),m=>({mo:mi(m[1]),d:+m[2],y:+m[3]})],
    [new RegExp('\\b('+MON+')\\.?,?\\s+((?:19|20)\\d\\d)\\b','gi'),m=>({mo:mi(m[1]),y:+m[2]})]
  ];
  for(const [re,f] of dps)scan(re,(m,s,e)=>{const c=f(m);if(c.mo===0||(c.mo!=null&&c.mo>12)||(c.d!=null&&(c.d<1||c.d>31)))return false;push('Date',m[0],s,judgeDate(c,s,e));});
  scan(/\b(?:adopted|passed|approved|voted)\b[^.;\n]{0,40}?\b((?:19|20)\d\d)\b/gi,(m,s,e)=>{
    const ys=s+m[0].lastIndexOf(m[1]);if(!free(ys,ys+4))return false;
    push('Year',m[1],ys,judgeDate({y:+m[1]},s,e));
  });
  // session
  function judgeSession(n,special,pos){
    const recNum=sessionNum(r),rec='Session in the record: '+(r.session||'not given');
    if(special)return{v:'na',rec,note:'Special sessions are numbered separately from regular sessions; the record gives no special-session number to compare.'};
    if(!/adopt|vot|pass|approv|council|hrc/i.test(sentOf(pos).text))return{v:'na',rec,note:'The sentence does not seem to be about this vote.'};
    if(recNum==null)return{v:'na',rec,note:'The record has no regular-session number.'};
    return n===recNum?{v:'match',rec,note:''}:{v:'wrong',rec,note:''};
  }
  scan(/\b(\d{1,3})(?:st|nd|rd|th)\s+(regular\s+|special\s+)?session\b/gi,(m,s)=>push('Session',m[0],s,judgeSession(+m[1],/special/i.test(m[2]||''),s)));
  scan(new RegExp('\\b((?:(?:twenty|thirty|forty|fifty|sixty)[-\\s])?(?:'+alt(ORD)+'))\\s+(regular\\s+|special\\s+)?session\\b','gi'),(m,s)=>push('Session',m[0],s,judgeSession(num(m[1]),/special/i.test(m[2]||''),s)));
  // states
  const names=[],cn=H.countries||{};
  for(const iso in cn){const f=String(cn[iso]);[f,f.replace(/\s*\(.*?\)\s*/g,' ').trim()].forEach(n=>names.push([norm(n),iso]));}
  for(const iso in ALIAS)if(cn[iso])ALIAS[iso].forEach(n=>names.push([n,iso]));
  if(names.length){
    const map={};names.forEach(([n,i])=>{if(n)map[n]=i;});
    const keys=Object.keys(map).sort((a,b)=>b.length-a.length).map(k=>k.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));
    const CUES={Y:/in favou?r|voted (?:yes|for)|\bsupport(?:ed|ing|s)?\b|\bbacked\b|\byes\b/g,N:/\bagainst\b|voted no\b|\bopposed\b|\bopposing\b|\brejected\b|\bobjected\b/g,A:/\babstain\w*|\babstention\w*/g};
    for(const s of sents){
      const raw=text.slice(s.start,s.end),nt=norm(raw),base=nt.length===raw.length?raw:nt;
      const cuts=[0];let cm;const cre=/;|\bwhile\b|\bwhereas\b|\bbut\b|\bhowever\b/gi;
      while((cm=cre.exec(nt)))cuts.push(cm.index);cuts.push(nt.length);
      for(let i=0;i<cuts.length-1;i++){
        const a=cuts[i],b=cuts[i+1],seg=nt.slice(a,b),cues=[];
        for(const L in CUES){const re=new RegExp(CUES[L].source,'g');let x;while((x=re.exec(seg))){const as=s.start+a+x.index;if(free(as,as+x[0].length))cues.push({L,s:x.index,e:x.index+x[0].length});}}
        if(!cues.length)continue;
        const nre=new RegExp('\\b('+keys.join('|')+')\\b','g');let mm;
        while((mm=nre.exec(seg))){
          const ms=mm.index,me=ms+mm[0].length;let best=null,bd=1e9;
          for(const c of cues){const d=c.s>=me?c.s-me:ms-c.e;if(d<bd){bd=d;best=c;}}
          if(!best||bd>200)continue;
          const iso=map[mm[1]],nm=cn[iso]||mm[1];
          const written=base.slice(a+Math.min(ms,best.s),a+Math.max(me,best.e)).trim();
          const pos=s.start+a+ms,claimed=LETWORD[best.L];
          let j;
          if(/\b(?:not|never)\b|n't/.test(seg.slice(Math.max(0,best.s-16),best.s)))j={v:'na',rec:'',note:'The wording looks negated (“not …”), which this checker does not interpret.'};
          else if(!r.votes||!Object.keys(r.votes).length)j={v:'na',rec:'No roll call in this record.',note:''};
          else if(!r.votes[iso])j={v:'na',rec:nm+' has no vote in this roll call.',note:'It was not a Council member at this vote, or the source has a gap. That does not make the claim wrong.'};
          else{const L=r.votes[iso];j={v:L===best.L?'match':'wrong',rec:nm+' voted '+LETWORD[L]+' ('+L+') in the roll call',note:''};}
          push('State: '+nm,written+'  [claimed: '+claimed+']',pos,j);
          if(j.rec==='')j.rec=nm+': '+(r.votes&&r.votes[iso]?'recorded '+LETWORD[r.votes[iso]]:'no recorded vote');
        }
      }
    }
  }
  claims.sort((a,b)=>a.pos-b.pos);
  return{claims,sents};
}

/* ---------- render ---------- */
$('checkBtn').addEventListener('click',()=>{
  const text=$('txt').value;if(!cur)return;
  $('results').hidden=false;
  if(!text.trim()){$('resHead').innerHTML='<p class="warn">The text box is empty. Ask the AI for a briefing or paste a text first.</p>';$('resBody').innerHTML='';$('unchecked').innerHTML='';return;}
  const {claims,sents}=findClaims(text,cur);
  const n={match:0,wrong:0,na:0};claims.forEach(c=>n[c.v]++);
  $('resHead').innerHTML='<p>Checked against '+docLink(cur)+' ('+esc(cur.title)+'), '+esc(fmtDate(cur.date))+'. Text length: '+text.trim().split(/\s+/).length+' words.</p>'
    +'<p class="sum"><span class="badge v-match">'+n.match+' match</span><span class="badge v-wrong">'+n.wrong+' wrong</span><span class="badge v-na">'+n.na+' cannot be checked</span></p>';
  const src=origin==='ai'?' data-source="ai"':'';
  const LABEL={match:'Matches',wrong:'Wrong',na:'Cannot be checked in this data'};
  if(!claims.length){$('resBody').innerHTML='<p>No checkable claims were found in this text. See the box below for what is looked for.</p>';}
  else $('resBody').innerHTML='<table><thead><tr><th>Type</th><th>Claim as written</th><th>What the recorded vote says</th><th>Verdict</th></tr></thead><tbody>'
    +claims.map(c=>'<tr><td>'+esc(c.type)+'</td><td'+src+'>“'+esc(c.written)+'”<span class="ctx">in: '+esc(c.sent.length>220?c.sent.slice(0,220)+'…':c.sent)+'</span></td><td>'+esc(c.rec||'')+'</td><td><span class="badge v-'+c.v+'">'+LABEL[c.v]+'</span>'+(c.note?'<span class="note">'+esc(c.note)+'</span>':'')+'</td></tr>').join('')
    +'</tbody></table>';
  const un=sents.filter(s=>!claims.some(c=>c.pos>=s.start&&c.pos<s.end));
  $('unchecked').innerHTML='<details><summary>'+un.length+' of '+sents.length+' sentences contained nothing this data can check (not verified in any way)</summary>'
    +un.map(s=>'<p'+src+' style="margin:6px 0;color:#444">'+esc(s.text)+'</p>').join('')+'</details>';
});

/* ---------- start ---------- */
if(!recs.length){$('rec').innerHTML='<p class="warn">There are no recorded votes in the data, so nothing can be checked.</p>';$('askBtn').disabled=true;$('checkBtn').disabled=true;}
else{
  const want=recs.find(r=>r.symbol==='A/HRC/RES/51/27');
  fillList(want?want.id:null);
  if(!want)$('askStatus').textContent='A/HRC/RES/51/27 is not in this data; the newest record is selected instead.';
}
})();
</script>
</body>
</html>
```