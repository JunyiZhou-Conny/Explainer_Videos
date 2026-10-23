// Shared helpers for the Studio pages. The data files are built at deploy time by
// tools/studio_status.py (see .github/workflows/pages.yml); the browser makes no API calls.

function esc(s){ const d = document.createElement('div'); d.textContent = s ?? ''; return d.innerHTML; }

function ago(iso){
  if(!iso) return '';
  const m = Math.round((Date.now() - Date.parse(iso)) / 60000);
  if(m < 1) return '刚刚';
  if(m < 60) return `${m} 分钟前`;
  if(m < 1440) return `${Math.round(m / 60)} 小时前`;
  return `${Math.round(m / 1440)} 天前`;
}

function span(iso){            // "for how long", e.g. 已 3 小时
  if(!iso) return '';
  const m = Math.max(1, Math.round((Date.now() - Date.parse(iso)) / 60000));
  if(m < 60) return `${m} 分钟`;
  if(m < 1440) return `${Math.round(m / 60)} 小时`;
  return `${Math.round(m / 1440)} 天`;
}

function clock(iso){
  const d = new Date(iso);
  return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
}

function dur(s){
  if(!s) return '';
  s = Math.round(s);
  const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), sec = s % 60;
  return h ? `${h}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}` : `${m}:${String(sec).padStart(2, '0')}`;
}

function hours(s){
  s = Math.round(s || 0);
  const h = Math.floor(s / 3600), m = Math.round(s % 3600 / 60);
  return h ? `${h} 小时 ${m} 分` : `${m} 分钟`;
}

function mb(b){ return b ? (b / 1048576).toFixed(0) + ' MB' : ''; }

// Same-origin data files; the query defeats the Pages CDN cache, retries ride out blips.
async function loadData(name, tries = 3){
  for(let i = 1; ; i++){
    try{
      const r = await fetch(`data/${name}?t=${Date.now()}`, {cache: 'no-store'});
      if(!r.ok) throw new Error(`HTTP ${r.status}`);
      return await r.json();
    }catch(e){
      if(i >= tries) throw e;
      await new Promise(res => setTimeout(res, 700 * i));
    }
  }
}

function freshness(el, iso){
  const old = Date.now() - Date.parse(iso) > 2 * 3600 * 1000;
  el.className = 'fresh' + (old ? ' late' : '');
  el.textContent = `数据更新于 ${clock(iso)}（${ago(iso)}）` + (old ? ' · 自动更新可能卡住了' : '');
  el.title = '每次 issue 有新检查点、标签变化，或 main 有推送，一两分钟内自动重建；另外每小时一次兜底。';
}

async function copyText(btn, text){
  try{ await navigator.clipboard.writeText(text); }
  catch(e){
    const t = document.createElement('textarea'); t.value = text; document.body.appendChild(t);
    t.select(); document.execCommand('copy'); t.remove();
  }
  const label = btn.dataset.label ||= btn.textContent;
  btn.textContent = '已复制';
  clearTimeout(btn.__t); btn.__t = setTimeout(() => btn.textContent = label, 1400);
}
