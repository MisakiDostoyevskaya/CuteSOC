(() => {
  "use strict";
  const incidents = [
    {id:"CS-1042",severity:"HIGH",event:"Multiple failed login attempts",ip:"192.0.2.10",attempts:3,status:"Suspicious activity detected",time:"19:42:18",ago:"2 min ago",description:"Three failed authentication attempts were observed from the same source address in a short period.",recommendation:"Review authentication logs for this source, confirm whether the activity is expected, and consider temporary rate limiting if reproduced in a real environment."},
    {id:"CS-1041",severity:"MEDIUM",event:"Possible port scan detected",ip:"192.0.2.50",attempts:5,status:"Multiple destination ports contacted",time:"19:38:02",ago:"6 min ago",description:"The source contacted five distinct destination ports. This can be consistent with service discovery or port scanning.",recommendation:"Check the destination hosts and connection history. Validate the activity against approved inventory or authorized scanning windows."},
    {id:"CS-1040",severity:"MEDIUM",event:"Unusual outbound connection",ip:"198.51.100.24",attempts:2,status:"Needs investigation",time:"19:31:44",ago:"12 min ago",description:"A sample outbound connection was flagged for analyst review. This record is illustrative and does not represent a real network event.",recommendation:"In a real deployment, review destination reputation, process ownership, DNS history and network policy before taking action."},
    {id:"CS-1039",severity:"LOW",event:"New service started",ip:"127.0.0.1",attempts:1,status:"Informational event",time:"19:24:09",ago:"20 min ago",description:"A local service-start event is included to demonstrate an informational alert in the dashboard.",recommendation:"Confirm that the service is expected and associated with an approved application. Close as informational if verified."}
  ];
  const $ = (id) => document.getElementById(id);
  const severityRank = {HIGH:3,MEDIUM:2,LOW:1};
  let filtered = incidents.slice();
  let sortState = {key:"time", direction:-1};
  let selectedId = null;
  let streamPaused = false;
  let streamIndex = 0;
  let streamTimer = null;
  const streamEvents = [
    {level:"danger",label:"AUTH",message:"Repeated authentication failure",meta:"192.0.2.10 · 3 failed attempts"},
    {level:"violet",label:"NETWORK",message:"Multiple destination ports contacted",meta:"192.0.2.50 · 5 ports observed"},
    {level:"good",label:"SYSTEM",message:"Local service started",meta:"127.0.0.1 · informational"},
    {level:"violet",label:"NETWORK",message:"Sample outbound connection flagged",meta:"198.51.100.24 · analyst review"}
  ];
  function toast(message){const el=$("toast");el.textContent=message;el.classList.add("show");clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.classList.remove("show"),1900);}
  function severityClass(s){return s.toLowerCase();}
  function renderStats(){
    const high=incidents.filter(x=>x.severity==="HIGH").length, med=incidents.filter(x=>x.severity==="MEDIUM").length, low=incidents.filter(x=>x.severity==="LOW").length;
    $("totalStat").textContent=String(incidents.length).padStart(2,"0");
    $("highStat").textContent=String(high).padStart(2,"0");
    $("mediumStat").textContent=String(med).padStart(2,"0");
    $("ipsStat").textContent=String(new Set(incidents.map(x=>x.ip)).size).padStart(2,"0");
    $("donutTotal").textContent=String(incidents.length).padStart(2,"0");
    $("legendHigh").textContent=high;$("legendMedium").textContent=med;$("legendLow").textContent=low;
    $("navAlertCount").textContent=String(incidents.length).padStart(2,"0");
    $("severityDonut").style.background=`conic-gradient(var(--red) 0 ${high/incidents.length*100}%,var(--pink) ${high/incidents.length*100}% ${(high+med)/incidents.length*100}%,var(--purple) ${(high+med)/incidents.length*100}% 100%)`;
  }
  function renderTable(){
    const q=$("searchInput").value.trim().toLowerCase(), sev=$("severityFilter").value;
    filtered=incidents.filter(x=>(sev==="ALL"||x.severity===sev)&&[x.id,x.severity,x.event,x.ip,x.status,x.time].join(" ").toLowerCase().includes(q));
    filtered.sort((a,b)=>{let av=a[sortState.key],bv=b[sortState.key];if(sortState.key==="severity"){av=severityRank[av];bv=severityRank[bv];}else if(sortState.key==="attempts"){av=Number(av);bv=Number(bv);}else{av=String(av).toLowerCase();bv=String(bv).toLowerCase();}return av<bv?-1*sortState.direction:av>bv?1*sortState.direction:0;});
    $("alertsBody").innerHTML=filtered.map(x=>`<tr class="${selectedId===x.id?"selected":""}"><td><span class="severity ${severityClass(x.severity)}">${x.severity}</span></td><td class="event-name">${x.event}</td><td><code class="ip-code" data-copy="${x.ip}" title="Click to copy IP">${x.ip}</code></td><td>${x.attempts}</td><td class="status-label">${x.status}</td><td class="timestamp">${x.time}</td><td><button class="view-button" data-view="${x.id}">View ↗</button></td></tr>`).join("");
    $("emptyState").classList.toggle("hidden",filtered.length>0);
    $("alertsTable").classList.toggle("hidden",filtered.length===0);
    $("resultCount").textContent=`${filtered.length} incident${filtered.length===1?"":"s"}`;
    $("alertsBody").querySelectorAll("[data-view]").forEach(b=>b.addEventListener("click",()=>showDetail(b.dataset.view)));
    $("alertsBody").querySelectorAll("[data-copy]").forEach(el=>el.addEventListener("click",async()=>{try{await navigator.clipboard.writeText(el.dataset.copy);toast("IP copied ♡");}catch(e){toast("IP: "+el.dataset.copy);}}));
  }
  function showDetail(id){
    const x=incidents.find(i=>i.id===id);if(!x)return;selectedId=id;
    $("detailPlaceholder").classList.add("hidden");$("detailContent").classList.remove("hidden");
    $("detailContent").innerHTML=`<div class="detail-title-row"><h3>${x.event}</h3><span class="severity ${severityClass(x.severity)}">${x.severity}</span></div><p class="detail-description">${x.description}</p><div class="detail-grid"><div class="detail-field"><span>INCIDENT ID</span><strong>${x.id}</strong></div><div class="detail-field"><span>SOURCE IP</span><strong>${x.ip}</strong></div><div class="detail-field"><span>OBSERVED AT</span><strong>${x.time}</strong></div><div class="detail-field"><span>EVENT COUNT</span><strong>${x.attempts}</strong></div><div class="detail-field" style="grid-column:1/-1"><span>CURRENT STATUS</span><strong>${x.status}</strong></div></div><div class="recommendation"><strong>♡ Suggested next step</strong><p>${x.recommendation}</p></div>`;
    renderTable();$("incidentDetail").scrollIntoView({behavior:"smooth",block:"nearest"});
  }
  function renderStream(){
    const event=streamEvents[streamIndex%streamEvents.length], now=new Date(),time=now.toLocaleTimeString("en-GB",{hour:"2-digit",minute:"2-digit",second:"2-digit"});
    const row=document.createElement("div");row.className="stream-event";row.innerHTML=`<span class="stream-time">${time}</span><i class="stream-pin ${event.level==="danger"?"danger":event.level==="good"?"good":""}"></i><div class="stream-message"><strong>${event.label}</strong> · ${event.message}<small>${event.meta} · DEMO</small></div>`;
    $("eventStream").prepend(row);while($("eventStream").children.length>5)$("eventStream").lastElementChild.remove();streamIndex++;
  }
  function startStream(){clearInterval(streamTimer);streamTimer=setInterval(()=>{if(!streamPaused)renderStream();},4500);}
  $("searchInput").addEventListener("input",renderTable);
  $("severityFilter").addEventListener("change",renderTable);
  $("resetFilters").addEventListener("click",()=>{$("searchInput").value="";$("severityFilter").value="ALL";renderTable();toast("Filters cleared ♡");});
  document.querySelectorAll("[data-sort]").forEach(btn=>btn.addEventListener("click",()=>{const key=btn.dataset.sort;sortState={key,direction:sortState.key===key?-sortState.direction:1};renderTable();}));
  document.addEventListener("keydown",e=>{if(e.key==="/"&&!["INPUT","TEXTAREA","SELECT"].includes(document.activeElement.tagName)){e.preventDefault();$("searchInput").focus();}if(e.key==="Escape"){$("aboutModal").classList.add("hidden");}});
  $("pauseStream").addEventListener("click",()=>{streamPaused=!streamPaused;$("pauseStream").textContent=streamPaused?"▶ Resume stream":"Ⅱ Pause stream";toast(streamPaused?"Event stream paused":"Event stream resumed");});
  $("themeNote").addEventListener("click",()=>$("aboutModal").classList.remove("hidden"));
  $("closeModal").addEventListener("click",()=>$("aboutModal").classList.add("hidden"));
  $("understood").addEventListener("click",()=>$("aboutModal").classList.add("hidden"));
  $("aboutModal").addEventListener("click",e=>{if(e.target===$("aboutModal"))$("aboutModal").classList.add("hidden");});
  renderStats();renderTable();renderStream();renderStream();startStream();
})();
