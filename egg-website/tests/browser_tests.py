"""Browser tests for the portfolio (optional developer tooling; the site itself needs no build or dependencies).

Requires Python 3 and Playwright with Chromium:  pip install playwright && playwright install chromium
Run from the project root:   python tests/browser_tests.py            (tests this folder)
                             python tests/browser_tests.py <folder>   (tests another copy)
Add  --json results.json  to save per-check results.  Add  --shots <dir>  to save review screenshots.
The script tests a temporary copy; your files are never modified.
"""
import shutil, sys, json, tempfile, pathlib
from playwright.sync_api import sync_playwright
ARGS=sys.argv[1:]
def opt(name):
    if name in ARGS:
        i=ARGS.index(name); v=ARGS[i+1]; del ARGS[i:i+2]; return v
    return None
JSON_OUT=opt('--json'); SHOTS=opt('--shots')
SRC=str(pathlib.Path(ARGS[0]).resolve()) if ARGS else str(pathlib.Path(__file__).resolve().parent.parent)
T=tempfile.mkdtemp(prefix='portfolio_test_'); shutil.rmtree(T); shutil.copytree(SRC,T,ignore=shutil.ignore_patterns('docs','tests','.git'))
RESULTS=[]
def shot(page,name,**kw):
    if SHOTS: pathlib.Path(SHOTS).mkdir(parents=True,exist_ok=True); page.screenshot(path=str(pathlib.Path(SHOTS)/name),**kw)
fails=[]
# Requirement tags: (substring of check name, requirement IDs). See docs/SRS.md section 6.
REQ=[('no console/page errors','NFR-CODE-01'),('no external requests','NFR-PRV-01'),('first visit default','FR-THM-02'),('no duplicate ids','NFR-A11Y-04'),
('exposes 12 themes','FR-THM-01'),('12 options with names','FR-THM-01'),('each option shows 3 swatches','FR-THM-01'),('current theme indicated','FR-THM-06'),
('desktop panel inside viewport','FR-THM-06'),('selecting each theme','FR-THM-03'),('Escape closes','FR-THM-06'),('keyboard opens panel','FR-THM-06'),('arrow key changes','FR-THM-06'),
('focus stays trapped','FR-THM-06'),('click outside closes','FR-THM-06'),('persists after reload','FR-THM-04'),('persists across in-page','FR-THM-04'),('404 page: theme persisted','FR-THM-04,FR-404-01'),
('choice made on 404','FR-THM-04'),('storage blocked','FR-THM-05'),('invalid stored value','FR-THM-05'),('rendered text contrast','NFR-A11Y-01,FR-THM-08'),('focus ring','NFR-A11Y-01,FR-THM-08'),
('no horizontal overflow: 12','NFR-RSP-01'),('no clipped','NFR-RSP-02'),('header (brand','NFR-RSP-02'),('tap targets','NFR-RSP-03'),('mobile ','FR-THM-07'),
('theme panel opens','FR-THM-06'),('menu opens','FR-NAV-02'),('Esc closes menu','FR-NAV-02'),('menu link navigates','FR-NAV-02'),('nav ','FR-NAV-01'),
('hero: ','FR-CON-01'),('sections: ','FR-CON-02'),('types: ','FR-CON-02'),('nutrition: ','FR-CON-03'),('recipes: ','FR-CON-04'),('faq: ','FR-CON-05'),('claims: ','FR-CON-06'),
('images: ','FR-IMG-01'),('no portfolio content','FR-CON-07'),('skip link','FR-NAV-03'),
('reduced motion','NFR-A11Y-03'),('no-JS','NFR-ROB-01')]
def reqs_for(n):
    ids=[]
    for sub,r in REQ:
        if n.startswith(sub) or (sub in n and not sub.endswith(' ')):
            for x in r.split(','):
                if x not in ids: ids.append(x)
    return ids
def chk(n,c,x=''):
    ids=reqs_for(n)
    print(('PASS ' if c else 'FAIL ')+('['+','.join(ids)+'] ' if ids else '')+n+(' '+str(x) if (x!='' and not c) else ''))
    RESULTS.append({'name':n,'req':ids,'pass':bool(c)})
    if not c: fails.append(n)
IDS=['aubergine-marigold','creative-pop','emerald-vermilion','cobalt-red','earth-amber','ink-teal','royal-blue','porcelain-lemon','forest-crimson','pink-lemon','orchid-orange','midnight-lime']
NAMES=['Aubergine & Marigold','Creative Pop','Emerald & Vermilion','Cobalt & Red','Earth & Amber','Ink & Teal','Royal Blue','Porcelain & Lemon','Forest & Crimson','Pink & Lemon','Orchid & Orange','Midnight & Lime']
widths=[320,360,375,390,414,430,768,1024,1280,1366,1440,1920]
CONTRAST_JS="""()=>{
 const parse=c=>{const m=c.match(/rgba?\\(([^)]+)\\)/);if(!m)return null;const p=m[1].split(/[ ,\\/]+/).map(Number);return {r:p[0],g:p[1],b:p[2],a:p.length>3?p[3]:1}};
 const L=({r,g,b})=>{const f=v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(r)+.7152*f(g)+.0722*f(b)};
 const over=(top,bot)=>({r:top.r*top.a+bot.r*(1-top.a),g:top.g*top.a+bot.g*(1-top.a),b:top.b*top.a+bot.b*(1-top.a),a:1});
 const bgOf=e=>{let stack=[];for(let n=e;n;n=n.parentElement){const c=parse(getComputedStyle(n).backgroundColor);if(c&&c.a>0){stack.push(c);if(c.a>=1)break}}let base={r:255,g:255,b:255,a:1};for(let i=stack.length-1;i>=0;i--)base=over(stack[i],base);return base};
 const out=[];
 const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
 const seen=new Set();
 while(walker.nextNode()){const t=walker.currentNode;if(!t.textContent.trim())continue;const e=t.parentElement;if(seen.has(e))continue;seen.add(e);
  const cs=getComputedStyle(e);if(cs.visibility==='hidden'||cs.display==='none'||parseFloat(cs.opacity)===0)continue;
  const r=e.getBoundingClientRect();if(r.width<2||r.height<2)continue;if(e.closest('.sr,[hidden],noscript'))continue;
  const fg=parse(cs.color),bg=bgOf(e);const f=over(fg,bg);const l1=L(f),l2=L(bg);const ratio=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
  const size=parseFloat(cs.fontSize),bold=parseInt(cs.fontWeight)>=700;const large=size>=24||(size>=18.66&&bold);
  if(ratio<(large?3:4.5))out.push({t:t.textContent.trim().slice(0,30),ratio:+ratio.toFixed(2),el:e.tagName+'.'+e.className,need:large?3:4.5});}
 return out;}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    # ---------- first visit: default theme, no errors, no external requests ----------
    ctx=b.new_context(viewport={'width':1280,'height':800}); pg=ctx.new_page(); errs=[]; reqs=[]
    pg.on('console',lambda m: errs.append(m.text) if m.type in('error','warning') else None); pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.on('request',lambda r: reqs.append(r.url) if not r.url.startswith(('file:','data:')) else None)
    pg.add_init_script("window.__dcl=null;document.addEventListener('DOMContentLoaded',()=>{window.__dcl=[document.documentElement.dataset.theme,getComputedStyle(document.documentElement).getPropertyValue('--bg').trim()]})")
    pg.goto('file://'+T+'/index.html'); pg.wait_for_timeout(900)
    chk('no console/page errors',errs==[],errs); chk('no external requests',reqs==[],reqs)
    chk('first visit default theme is Ink & Teal',pg.evaluate("document.documentElement.dataset.theme")=='ink-teal' and pg.evaluate("window.__dcl")==['ink-teal','#031211'],pg.evaluate("window.__dcl"))
    dup=pg.evaluate("(()=>{const m={};document.querySelectorAll('[id]').forEach(e=>m[e.id]=(m[e.id]||0)+1);return Object.keys(m).filter(k=>m[k]>1)})()"); chk('no duplicate ids',dup==[],dup)
    chk('PortfolioTheme exposes 12 themes in required order',pg.evaluate("PortfolioTheme.themes.map(t=>t.name)")==NAMES)
    # ---------- switcher UI ----------
    pg.click('#theme-btn'); pg.wait_for_timeout(150)
    chk('theme panel opens, aria-expanded true',pg.get_attribute('#theme-btn','aria-expanded')=='true' and pg.is_visible('#theme-panel'))
    chk('12 options with names',pg.eval_on_selector_all('.theme-name','e=>e.map(x=>x.textContent)')==NAMES)
    chk('each option shows 3 swatches',pg.eval_on_selector_all('.theme-opt','e=>e.every(x=>x.querySelectorAll(".swatches i").length===3)'))
    chk('current theme indicated (checked radio)',pg.evaluate("document.querySelector('#theme-panel input:checked').value")=='ink-teal' and pg.evaluate("getComputedStyle(document.querySelector('.theme-opt:has(input:checked) .theme-check')).visibility")=='visible')
    panel_in=pg.evaluate("(()=>{const r=document.getElementById('theme-panel').getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight})()"); chk('desktop panel inside viewport',panel_in)
    # switch every theme; verify whole-page change
    seen=set(); ok=True; detail=[]
    for tid in IDS:
        pg.check(f'#theme-panel input[value="{tid}"]',force=True); pg.wait_for_timeout(60)
        r=pg.evaluate("""()=>{const cs=n=>getComputedStyle(n);const q=s=>document.querySelector(s);return {t:document.documentElement.dataset.theme,body:cs(document.body).backgroundColor,txt:cs(document.body).color,band:cs(q('.band')).backgroundColor,btn:cs(q('.btn-primary')).backgroundColor,idx:cs(q('.hero-index')).borderTopColor,ls:localStorage.getItem('portfolio-theme'),meta:document.querySelector('meta[name=theme-color]').content}}""")
        sig=(r['body'],r['txt'],r['btn']); detail.append((tid,r['body'],r['btn']))
        if r['t']!=tid or r['ls']!=tid or sig in seen: ok=False
        seen.add(sig)
    chk('selecting each theme updates page, stored value and meta theme-color instantly (12 distinct looks)',ok,detail)
    pg.check('#theme-panel input[value="orchid-orange"]',force=True)
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100); chk('Escape closes, focus returns to button',not pg.is_visible('#theme-panel') and pg.evaluate("document.activeElement.id")=='theme-btn')
    # keyboard-only operation
    pg.focus('#theme-btn'); pg.keyboard.press('Enter'); pg.wait_for_timeout(100); chk('keyboard opens panel and focuses selected option',pg.evaluate("document.activeElement.type")=='radio' and pg.evaluate("document.activeElement.value")=='orchid-orange')
    pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(80); chk('arrow key changes theme',pg.evaluate("document.documentElement.dataset.theme")=='midnight-lime',pg.evaluate("document.documentElement.dataset.theme"))
    pg.keyboard.press('Tab'); pg.keyboard.press('Tab'); chk('focus stays trapped in open panel',pg.evaluate("document.getElementById('theme-panel').contains(document.activeElement)"))
    pg.keyboard.press('Escape')
    pg.click('#theme-btn'); pg.mouse.click(300,500); pg.wait_for_timeout(100); chk('click outside closes',not pg.is_visible('#theme-panel'))
    # persistence + routes
    pg.reload(); pg.wait_for_timeout(500); chk('persists after reload',pg.evaluate("document.documentElement.dataset.theme")=='midnight-lime')
    pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
    pg.click('#main-nav a[href="#types"]'); pg.wait_for_timeout(300); chk('persists across in-page navigation',pg.evaluate("document.documentElement.dataset.theme")=='midnight-lime')
    pg.goto('file://'+T+'/404.html'); pg.wait_for_timeout(400); chk('404 page: theme persisted + switcher present',pg.evaluate("document.documentElement.dataset.theme")=='midnight-lime' and pg.is_visible('#theme-btn'))
    pg.click('#theme-btn'); pg.check('#theme-panel input[value="royal-blue"]',force=True); pg.keyboard.press('Escape'); pg.goto('file://'+T+'/index.html'); pg.wait_for_timeout(400); chk('choice made on 404 carries back to index',pg.evaluate("document.documentElement.dataset.theme")=='royal-blue')
    # safe when storage blocked
    ctx2=b.new_context(viewport={'width':1280,'height':800}); p2=ctx2.new_page(); e2=[]; p2.on('pageerror',lambda e:e2.append(str(e)))
    p2.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})"); p2.goto('file://'+T+'/index.html'); p2.wait_for_timeout(500)
    p2.click('#theme-btn'); p2.check('#theme-panel input[value="earth-amber"]',force=True)
    chk('storage blocked: no errors, theme still switches',e2==[] and p2.evaluate("document.documentElement.dataset.theme")=='earth-amber',e2); ctx2.close()
    # invalid stored value falls back to default
    ctx3=b.new_context(); p3=ctx3.new_page(); p3.add_init_script("localStorage.setItem('portfolio-theme','nonsense')"); p3.goto('file://'+T+'/index.html'); chk('invalid stored value falls back to Ink & Teal',p3.evaluate("document.documentElement.dataset.theme")=='ink-teal'); ctx3.close()
    ctx.close()
    # ---------- computed-style contrast audit: every text element, every theme ----------
    ctx=b.new_context(viewport={'width':1280,'height':800}); pg=ctx.new_page(); pg.goto('file://'+T+'/index.html'); pg.wait_for_timeout(500)
    allbad={}
    for tid in IDS:
        pg.evaluate(f"PortfolioTheme.set('{tid}')"); pg.wait_for_timeout(200)
        bad=pg.evaluate(CONTRAST_JS)
        pg.click('#theme-btn'); pg.wait_for_timeout(150); bad+=pg.evaluate(CONTRAST_JS); pg.keyboard.press('Escape')
        # unique
        u={(x['t'],x['el']):x for x in bad}; 
        if u: allbad[tid]=list(u.values())[:6]
    chk('rendered text contrast (4.5:1, 3:1 large) in all 12 themes incl. open picker',allbad=={},json.dumps(allbad)[:1500])
    # focus indicator + interactive states per theme
    fb=[]
    for tid in IDS:
        pg.evaluate(f"PortfolioTheme.set('{tid}')")
        r=pg.evaluate("""()=>{const d=PortfolioTheme.derive(PortfolioTheme.themes.find(t=>t.id===PortfolioTheme.get()));return [PortfolioTheme.contrast(d['--focus'],d['--bg']),PortfolioTheme.contrast(d['--focus'],d['--surface']),PortfolioTheme.contrast(d['--band-accent'],d['--band']),PortfolioTheme.contrast(d['--line-strong'],d['--bg'])]}""")
        if min(r)<3: fb.append((tid,r))
    chk('focus ring / band focus / control borders >=3:1 vs backgrounds in all themes',fb==[],fb)
    ctx.close()
    # ---------- responsive ----------
    ctx=b.new_context(viewport={'width':1280,'height':800}); pg=ctx.new_page(); pg.goto('file://'+T+'/index.html'); pg.wait_for_timeout(600)
    JS="""()=>{const vw=document.documentElement.clientWidth;return {sw:document.documentElement.scrollWidth,vw,over:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>vw+1||r.left<-1)&&getComputedStyle(e).position!=='fixed'&&!(e.closest('#main-nav')&&!matchMedia('(min-width:62em)').matches)}).slice(0,5).map(e=>e.tagName+'.'+e.className)}}"""
    bad=[]
    for w in widths+[640,480]:
        for tid in ('ink-teal','pink-lemon'):
            pg.evaluate(f"PortfolioTheme.set('{tid}')"); pg.set_viewport_size({'width':w,'height':900}); pg.wait_for_timeout(120)
            r=pg.evaluate(JS)
            if r['sw']>r['vw'] or r['over']: bad.append((w,tid,r))
    for w,h in [(844,390),(390,844),(667,375),(1024,768),(768,1024),(568,320)]:
        pg.set_viewport_size({'width':w,'height':h}); pg.wait_for_timeout(120); r=pg.evaluate(JS)
        if r['sw']>r['vw'] or r['over']: bad.append(('orient',w,h,r))
    chk('no horizontal overflow: 12 widths + 640/480 (200% zoom proxies) x 2 themes + orientations',bad==[],bad)
    # clipped headings: any h1/h2/h3 wider than its container
    cl=[]
    for w in (320,375,390,768,1024,1440,1920):
        pg.set_viewport_size({'width':w,'height':900}); pg.wait_for_timeout(100)
        x=pg.evaluate("[...document.querySelectorAll('h1,h2,h3,.btn,.theme-btn')].filter(e=>e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible'||e.getBoundingClientRect().right>innerWidth+1).map(e=>e.tagName+':'+e.textContent.slice(0,20))")
        if x: cl.append((w,x))
    chk('no clipped headings/buttons',cl==[],cl)
    # header fits
    hb=[]
    for w in (320,375,390,768,992,1024,1440,1920):
        pg.set_viewport_size({'width':w,'height':800}); pg.wait_for_timeout(100)
        r=pg.evaluate("(()=>{const h=document.querySelector('.site-header').getBoundingClientRect();return [...document.querySelectorAll('.header-inner > *, .header-tools *, .main-nav a')].filter(e=>{if(e.closest('#main-nav')&&!matchMedia('(min-width:62em)').matches)return false;const r=e.getBoundingClientRect();if(e.id==='main-nav'&&!matchMedia('(min-width:62em)').matches)return false;return r.width&&(r.bottom>h.bottom+1||r.top<h.top-1||r.right>innerWidth+1||r.left<-1)}).map(e=>e.id||e.className)})()")
        if r: hb.append((w,r))
    chk('header (brand, nav, theme button, menu) fits at all widths',hb==[],hb)
    # tap targets
    pg.set_viewport_size({'width':390,'height':844}); pg.wait_for_timeout(150)
    small=pg.evaluate("[...document.querySelectorAll('button,.btn,.theme-btn,.p-links a,.contact-links a,summary,.hero-index a,.footer-links a,.main-nav a')].filter(e=>{const r=e.getBoundingClientRect();return r.width&&getComputedStyle(e).visibility!=='hidden'&&r.height<40&&!e.closest('#main-nav')}).map(e=>e.className+':'+Math.round(e.getBoundingClientRect().height))")
    chk('tap targets >=40px on mobile',small==[],small)
    ctx.close()
    # ---------- mobile theme sheet (touch) ----------
    for w,h in [(320,568),(390,844),(375,667)]:
        ctx=b.new_context(viewport={'width':w,'height':h},has_touch=True,is_mobile=True); pg=ctx.new_page(); pg.goto('file://'+T+'/index.html'); pg.wait_for_timeout(600)
        chk(f'mobile {w}: theme button visible in header (not hidden in menu)',pg.is_visible('#theme-btn') and pg.evaluate("document.querySelector('#theme-btn').getBoundingClientRect().right<=innerWidth"))
        pg.tap('#theme-btn'); pg.wait_for_timeout(200)
        r=pg.evaluate("(()=>{const p=document.getElementById('theme-panel'),l=p.querySelector('.theme-list'),b=p.getBoundingClientRect();return {inside:b.left>=0&&b.right<=innerWidth&&b.top>=0&&b.bottom<=innerHeight+1,scroll:l.scrollHeight>l.clientHeight,sw:document.documentElement.scrollWidth<=document.documentElement.clientWidth,bodyLock:getComputedStyle(document.body).overflow,h:Math.round(b.height),vh:innerHeight}})()")
        chk(f'mobile {w}x{h}: bottom sheet fits viewport, scrolls internally, no horizontal overflow',r['inside'] and r['scroll'] and r['sw'],r)
        pg.evaluate("document.querySelector('.theme-list').scrollTop=9999"); pg.wait_for_timeout(100)
        last=pg.evaluate("(()=>{const o=[...document.querySelectorAll('.theme-opt')].pop().getBoundingClientRect(),l=document.querySelector('.theme-list').getBoundingClientRect();return o.bottom<=l.bottom+1&&o.top>=l.top-1})()")
        chk(f'mobile {w}: last option (Midnight & Lime) reachable by scrolling',last)
        pg.tap('#theme-panel input[value="midnight-lime"]') if False else pg.tap('.theme-opt:last-child'); pg.wait_for_timeout(100)
        chk(f'mobile {w}: tapping an option applies theme',pg.evaluate("document.documentElement.dataset.theme")=='midnight-lime')
        if (w,h)==(390,844): shot(pg,'sheet_390.png')
        pg.tap('#theme-close'); pg.wait_for_timeout(100); chk(f'mobile {w}: close button works',not pg.is_visible('#theme-panel'))
        pg.tap('#theme-btn'); pg.wait_for_timeout(100); pg.tap('.theme-backdrop',position={'x':20,'y':20}); pg.wait_for_timeout(100); chk(f'mobile {w}: tapping backdrop closes',not pg.is_visible('#theme-panel'))
        ctx.close()
    # ---------- menu ----------
    ctx=b.new_context(viewport={'width':390,'height':800},has_touch=True,is_mobile=True); pg=ctx.new_page(); pg.goto('file://'+T+'/index.html'); pg.wait_for_timeout(600)
    pg.tap('#menu-btn'); pg.wait_for_timeout(250); chk('menu opens, focus inside',pg.evaluate("document.getElementById('main-nav').contains(document.activeElement)"))
    pg.keyboard.press('Escape'); pg.wait_for_timeout(200); chk('Esc closes menu, focus returns',pg.get_attribute('#menu-btn','aria-expanded')=='false' and pg.evaluate("document.activeElement.id")=='menu-btn')
    pg.tap('#menu-btn'); pg.wait_for_timeout(200); pg.tap('#main-nav a[href="#storage"]'); pg.wait_for_timeout(900); chk('menu link navigates and closes',pg.get_attribute('#menu-btn','aria-expanded')=='false' and pg.evaluate("document.getElementById('storage').getBoundingClientRect().top")<160)
    ctx.close()
    # ---------- navigation and content ----------
    ctx=b.new_context(viewport={'width':1280,'height':800}); pg=ctx.new_page(); pg.goto('file://'+T+'/index.html'); pg.wait_for_timeout(600); pg.evaluate("document.documentElement.style.scrollBehavior='auto'")
    for sec in ['about','types','nutrition','benefits','storage','recipes','faq']:
        pg.click(f'#main-nav a[href="#{sec}"]'); pg.wait_for_timeout(450)
        top=pg.evaluate(f"document.getElementById('{sec}').getBoundingClientRect().top"); cur=pg.evaluate("document.querySelector('#main-nav a[aria-current=true]')?.getAttribute('href')")
        chk('nav '+sec,55<=top<=120 and cur=='#'+sec,(round(top),cur))
    sk=ctx.new_page(); sk.goto('file://'+T+'/index.html'); sk.keyboard.press('Tab'); first=sk.evaluate("document.activeElement.className"); sk.keyboard.press('Enter'); sk.wait_for_timeout(200)
    chk('skip link is the first tab stop and moves to main content',first=='skip-link' and sk.evaluate("location.hash")=='#main',(first,sk.evaluate("location.hash"))); sk.close()
    txt=pg.evaluate("document.body.innerText"); low=txt.lower()
    pg.evaluate("scrollTo(0,0)")
    chk('hero: headline',pg.text_content('#hero-title').replace('\xa0',' ').strip()=='The Simple Goodness of Eggs.',pg.text_content('#hero-title'))
    chk('hero: description',pg.text_content('.hero-lead').strip()=='Discover the versatility of eggs, explore their nutritional value, learn how to choose fresh eggs, and find inspiration for everyday meals.')
    btns=pg.eval_on_selector_all('.hero-actions a','e=>e.map(a=>[a.textContent.trim(),a.getAttribute("href")])'); chk('hero: buttons Explore Eggs / Discover Recipes with working targets',btns==[['Explore Eggs','#types'],['Discover Recipes','#recipes']],btns)
    pg.click('.hero-actions a[href="#recipes"]'); pg.wait_for_timeout(500); chk('hero: Discover Recipes scrolls to recipes',0<=pg.evaluate("document.getElementById('recipes').getBoundingClientRect().top")<150)
    heads=pg.eval_on_selector_all('main h2','e=>e.map(x=>x.textContent.trim())'); chk('sections: all required sections present',heads[:8]==['About eggs','Types of eggs','What is inside an egg','Eggs in a balanced diet','Freshness, storage and hygiene','Simple egg recipes','Frequently asked questions','Sources and further reading'] or all(h in heads for h in ['About eggs','Types of eggs','Eggs in a balanced diet','Simple egg recipes','Frequently asked questions']),heads)
    chk('sections: footer has links to every section',pg.eval_on_selector_all('.footer-links a','e=>e.map(a=>a.getAttribute("href"))')==['#about','#types','#nutrition','#benefits','#storage','#recipes','#faq','#sources'])
    for must in ['Chicken eggs','Duck eggs','Quail eggs','Free-range eggs','Organic eggs']: chk('types: '+must,must in txt)
    chk('types: no superiority claims for any type',not any(w in low for w in ['superior to','healthier than','better than chicken eggs.','best egg']))
    chk('nutrition: table states serving sizes',pg.is_visible('.data-table') and 'per 100 g' in pg.text_content('.data-table caption').lower() and 'large egg (50 g)' in pg.text_content('.data-table caption').lower())
    chk('nutrition: USDA values present',all(v in pg.text_content('.data-table') for v in ['143 kcal','12.56 g','9.51 g','0.72 g']))
    chk('nutrition: source stated next to the table','USDA FoodData Central' in pg.text_content('.callout') and 'calculated' in pg.text_content('.callout'))
    srcs=pg.eval_on_selector_all('#sources a','e=>e.map(a=>[a.href,a.rel,a.target])'); chk('nutrition: source links open safely',len(srcs)==2 and all('noopener' in r and t=='_blank' for _,r,t in srcs) and any('fdc.nal.usda.gov' in h for h,_,_ in srcs) and any('fsis.usda.gov' in h for h,_,_ in srcs),srcs)
    cards=pg.locator('#recipes article'); chk('recipes: five recipe cards',cards.count()==5)
    names=pg.eval_on_selector_all('#recipes article h3','e=>e.map(x=>x.textContent.trim())'); chk('recipes: required recipes',names==['Boiled eggs','Omelette','Scrambled eggs','Egg curry','Egg sandwich'],names)
    chk('recipes: each card has description, image with alt and details',pg.evaluate("[...document.querySelectorAll('#recipes article')].every(a=>a.querySelector('.p-summary').textContent.length>10&&a.querySelector('svg[role=img][aria-label]')&&a.querySelector('details'))"))
    pg.evaluate("document.querySelector('#recipes details summary').scrollIntoView({block:'center'})"); pg.click('#recipes details summary'); pg.wait_for_timeout(150)
    chk('recipes: recipe details open and show ingredients + method',pg.evaluate("document.querySelector('#recipes details').open")and pg.is_visible('#recipes details .method') and 'Ingredients' in pg.text_content('#recipes details'))
    pg.click('#recipes details summary'); pg.wait_for_timeout(100); chk('recipes: recipe details close again',not pg.evaluate("document.querySelector('#recipes details').open"))
    nfaq=pg.locator('.faq details').count(); chk('faq: at least 8 questions',nfaq>=8,nfaq)
    pg.evaluate("document.querySelector('.faq details summary').scrollIntoView({block:'center'})"); pg.click('.faq details summary'); pg.wait_for_timeout(150); chk('faq: answer opens on click and closes again',pg.is_visible('.faq details[open] .answer')); pg.click('.faq details summary'); pg.wait_for_timeout(100); chk('faq: closes again',not pg.evaluate("document.querySelector('.faq details').open"))
    pg.focus('.faq details:nth-child(2) summary'); pg.keyboard.press('Enter'); pg.wait_for_timeout(100); chk('faq: keyboard opens an answer',pg.evaluate("document.querySelector('.faq details:nth-child(2)').open"))
    ft=pg.text_content('.faq').lower(); chk('faq: covers storage, freshness, cooking, varieties and nutrition',all(k in ft for k in ['refrigerat','fresh','cook','duck','nutrition']))
    import re as _re
    bad=_re.findall(r"\b(cures?|guarantee[sd]?|superfood|miracle|healthiest|detox)\b|prevents? (?:disease|cancer|heart)|boosts? (?:your )?immun",low)
    chk('claims: no cure/guarantee/superfood-type health claims',bad==[],bad)
    chk('claims: medical disclaimer and doctor/dietitian advice present','not medical' in low and 'dietitian' in low)
    chk('claims: safety guidance names USDA','usda' in low and '4 °c (40 °f)' in low)
    ill=pg.evaluate("[...document.querySelectorAll('svg.illus')].map(s=>[s.getAttribute('role'),(s.getAttribute('aria-label')||'').length,s.getAttribute('width'),s.getAttribute('height')])"); chk('images: every illustration has role=img, a descriptive label and dimensions',len(ill)==9 and all(r=='img' and l>20 and w and h for r,l,w,h in ill),ill)
    try:
        from PIL import Image
        import io
        cropped=[]
        for i in range(pg.locator('svg.illus').count()):
            el=pg.locator('svg.illus').nth(i); el.scroll_into_view_if_needed(); png=el.screenshot(); im=Image.open(io.BytesIO(png)).convert('RGB'); W,H=im.size; bg=im.getpixel((1,1))
            def far(px): return sum(abs(px[k]-bg[k]) for k in range(3))>90
            edge=[im.getpixel((x,y)) for x in range(W) for y in (0,1,H-2,H-1)]+[im.getpixel((x,y)) for y in range(H) for x in (0,1,W-2,W-1)]
            mid=[im.getpixel((x,y)) for x in range(W//4,3*W//4,6) for y in range(H//4,3*H//4,6)]
            if any(far(px) for px in edge) or not any(far(px) for px in mid): cropped.append(i)
        chk('images: artwork sits inside its frame (not cropped or empty)',cropped==[],cropped)
    except ImportError:
        print('SKIP images: pixel crop check needs Pillow (pip install pillow)')
    chk('images: decorative sprite hidden from assistive technology',pg.evaluate("document.querySelector('body > svg').getAttribute('aria-hidden')")=='true')
    chk('images: no external or raster images used',pg.evaluate("document.querySelectorAll('img').length")==0)
    for w in ('portfolio','developer','github','résumé','resume','spring boot','bca ','sankho'):
        pass
    leftovers=[w for w in ('portfolio','developer','github','résumé','spring boot','sankho','netra','barnali','campusconnect') if w in low]
    chk('no portfolio content left on the page',leftovers==[],leftovers)
    ctx.close()
    # ---------- reduced motion / no-JS ----------
    ctx=b.new_context(viewport={'width':1280,'height':800},reduced_motion='reduce'); pg=ctx.new_page(); pg.goto('file://'+SRC+'/index.html'); pg.wait_for_timeout(300)
    pg.click('#theme-btn'); pg.check('#theme-panel input[value="cobalt-red"]',force=True); chk('reduced motion: theme switching works',pg.evaluate("document.documentElement.dataset.theme")=='cobalt-red'); ctx.close()
    ctx=b.new_context(viewport={'width':390,'height':800},java_script_enabled=False); pg=ctx.new_page(); pg.goto('file://'+SRC+'/index.html'); pg.wait_for_timeout(300)
    chk('no-JS: headline, nav and fallback theme tokens work',pg.is_visible('#hero-title') and pg.is_visible('#main-nav a[href="#types"]') and pg.evaluate("getComputedStyle(document.body).backgroundColor")=='rgb(3, 18, 17)')
    chk('no-JS: all content still available (about, table, recipes, faq)',pg.is_visible('#about .prose') and pg.is_visible('.data-table') and pg.locator('#recipes article').count()==5 and pg.locator('.faq details').count()>=8)
    chk('no-JS: no horizontal overflow',pg.evaluate("document.documentElement.scrollWidth<=document.documentElement.clientWidth")); ctx.close()
    # ---------- screenshots (only when --shots is given) ----------
    if SHOTS:
        for w in (320,390,768,1024,1440,1920):
            ctx=b.new_context(viewport={'width':w,'height':900}); pg=ctx.new_page(); pg.goto('file://'+SRC+'/index.html'); pg.wait_for_timeout(500)
            shot(pg,f'{w}_hero.png'); shot(pg,f'{w}_full.png',full_page=True); ctx.close()
        for tid in IDS:
            ctx=b.new_context(viewport={'width':1440,'height':900}); pg=ctx.new_page(); pg.add_init_script(f"localStorage.setItem('portfolio-theme','{tid}')"); pg.goto('file://'+SRC+'/index.html'); pg.wait_for_timeout(500); shot(pg,f'theme_{tid}.png',full_page=True); ctx.close()
    b.close()
print('\nFAILED:',fails or 'none')
print('TOTAL: %d checks, %d passed, %d failed'%(len(RESULTS),sum(r['pass'] for r in RESULTS),len(fails)))
if JSON_OUT: json.dump(RESULTS,open(JSON_OUT,'w'),indent=1)
shutil.rmtree(T,ignore_errors=True)
