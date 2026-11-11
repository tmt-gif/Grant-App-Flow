import asyncio, base64, pathlib, sys
from playwright.async_api import async_playwright

W, H = 1080, 1350
OUT = pathlib.Path("out"); OUT.mkdir(exist_ok=True)
A = pathlib.Path("assets")
def b64(n): return base64.b64encode((A/n).read_bytes()).decode()
prof = b64("profile.jpg")

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:transparent}}
body{{width:{W}px;height:{H}px;overflow:hidden;font-family:Inter,'Inter Display',system-ui,sans-serif;color:#03141e}}
.slide{{position:relative;width:{W}px;height:{H}px;background:#faf8f4;padding:110px 84px 140px;overflow:hidden}}
.bar{{position:absolute;top:0;left:0;right:0;height:16px;background:#004e50;z-index:5}}
.hdr{{display:flex;align-items:center;gap:24px;margin-bottom:70px}}
.hdr img{{width:120px;height:120px;border-radius:50%;object-fit:cover;border:5px solid #C8A25F}}
.hdr .n{{font-weight:700;font-size:36px;letter-spacing:-.01em}}
.hdr .s{{font-weight:500;font-size:27px;color:#004e50;margin-top:4px}}
.big{{position:absolute;left:84px;bottom:50px;font-weight:800;font-size:60px;line-height:1;color:#C8A25F;opacity:.6;letter-spacing:-.03em;z-index:6}}
h1,p{{text-wrap:balance}}
h1{{font-weight:800;font-size:76px;line-height:1.05;letter-spacing:-.035em;margin-bottom:44px;position:relative}}
p{{font-weight:500;font-size:46px;line-height:1.36;margin-bottom:30px;position:relative}}
.ft{{position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:flex-end;align-items:center;font-size:30px;color:#004e50;border-top:2px solid #e3dccd;padding-top:26px;min-height:30px;z-index:5}}
.ft .arrow{{display:flex;align-items:center;gap:18px;color:#C8A25F;font-style:italic;font-weight:600;letter-spacing:.02em}}
.ft .arrow svg{{width:150px;height:44px}}
/* cover */
.photo{{padding:0}}
.photo img.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.photo .shade{{position:absolute;left:0;right:0;bottom:0;height:66%;background:linear-gradient(180deg,rgba(3,20,30,0) 0%,rgba(3,20,30,.6) 32%,rgba(3,20,30,.96) 100%)}}
.card{{position:absolute;left:72px;right:72px;bottom:170px;color:#faf8f4;z-index:3}}
.card .line{{width:120px;height:8px;background:#C8A25F;margin-bottom:34px}}
.card h1{{font-size:78px;color:#faf8f4;margin-bottom:30px}}
.card p{{color:#e9e4d9;font-size:36px;margin:0;font-weight:500}}
.card .who{{display:flex;align-items:center;gap:18px;margin-top:40px}}
.card .who img{{width:76px;height:76px;border-radius:50%;object-fit:cover;border:3px solid #C8A25F}}
.card .who .n{{font-weight:700;font-size:28px}}
.card .who .s{{font-weight:500;font-size:22px;color:#C8A25F;margin-top:2px}}
.dark .ft{{color:#faf8f4;border-top-color:rgba(250,248,244,.25)}}
/* photo story slide: photo window on top, her words on navy underneath */
.story{{padding:0;background:#03141e}}
.story img.ph{{position:absolute;top:0;left:0;width:1080px;object-fit:cover}}
.story .fade{{position:absolute;left:0;right:0;height:300px;background:linear-gradient(180deg,rgba(3,20,30,0) 0%,rgba(3,20,30,.55) 55%,rgba(3,20,30,1) 100%)}}
.story .card h1{{margin-bottom:0}}
.story .card h1+p{{margin-top:26px}}
.story.vid{{background:transparent}}
.story.vid .base{{position:absolute;left:0;right:0;bottom:0;background:#03141e}}
/* inset (FaceTime) */
.inset .blur{{position:absolute;inset:-60px;background-size:cover;background-position:center;filter:blur(38px) brightness(.38) saturate(.9)}}
.inset img.scr{{position:absolute;left:50%;transform:translateX(-50%);top:52px;width:536px;height:910px;object-fit:cover;border-radius:44px;border:4px solid #C8A25F;box-shadow:0 30px 80px rgba(0,0,0,.5)}}
.inset .floor{{position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(180deg,rgba(3,20,30,0),rgba(3,20,30,.92) 60%)}}
/* quote */
.quote{{background:#03141e;color:#faf8f4}}
.quote .hdr .n{{color:#faf8f4}} .quote .hdr .s{{color:#C8A25F}}
.quote .mark{{font-weight:800;font-size:260px;line-height:.7;color:#C8A25F;margin-bottom:30px;font-family:Georgia,'DejaVu Serif',serif}}
  .quote h1{{font-size:84px;color:#faf8f4;font-weight:700;line-height:1.15}}
.quote .by{{font-size:30px;color:#C8A25F;font-weight:600;margin-top:10px}}
.gold{{color:#C8A25F}}
"""
ARROW = '<svg viewBox="0 0 120 36" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18c8-14 16-14 24 0s16 14 24 0 16-14 24 0 16 14 24 0h12"/><path d="M104 8l12 10-12 10"/></svg>'
FT = f'<div class="ft"><div class="arrow"><span>swipe left</span>{ARROW}</div></div>'
WHO = f'<div class="who"><img src="data:image/jpeg;base64,{prof}"><div><div class="n">Jessica Shunta</div><div class="s">Church Operations Systems</div></div></div>'
def num(i): return f'<div class="big">{i:02d}</div>'
def hdr(): return f'<div class="hdr"><img src="data:image/jpeg;base64,{prof}"><div><div class="n">Jessica Shunta</div><div class="s">Church Operations Systems</div></div></div>'

def cover(img, h, sub):
    return f'''<div class="slide photo dark"><img class="bg" src="data:image/jpeg;base64,{b64(img)}"><div class="shade"></div><div class="bar"></div>
<div class="card"><div class="line"></div><h1>{h}</h1><p>{sub}</p>{WHO}</div>{FT}</div>'''

def story(i, img, h, sub="", size=76, ph=900, last=False, video=False):
    p = f'<p>{sub}</p>' if sub else ''
    pic = '' if video else f'<img class="ph" style="height:{ph}px" src="data:image/jpeg;base64,{b64(img)}">'
    base = f'<div class="base" style="top:{ph}px"></div>' if video else ''
    foot = '' if last else FT
    who = WHO if last else ''
    bottom = ''
    return f'''<div class="slide story dark {'vid' if video else ''}">{pic}{base}<div class="fade" style="top:{ph-300}px"></div><div class="bar"></div>{num(i)}
<div class="card" {bottom}><div class="line"></div><h1 style="font-size:{size}px">{h}</h1>{p}{who}</div>{foot}</div>'''

def inset(i, img, h, size=76):
    d = b64(img)
    return f'''<div class="slide story inset dark"><div class="blur" style="background-image:url(data:image/jpeg;base64,{d})"></div><div class="floor"></div>
<img class="scr" src="data:image/jpeg;base64,{d}"><div class="bar"></div>{num(i)}
<div class="card"><div class="line"></div><h1 style="font-size:{size}px">{h}</h1></div>{FT}</div>'''

def quote(i, h):
    return f'''<div class="slide quote dark"><div class="bar"></div>{num(i)}{hdr()}<div class="mark">&ldquo;</div><h1>{h}</h1>{FT}</div>'''

S = [
 ("img", cover("cover.jpg", "Before I was an adult, I became a mom.", "Today is Veterans Day. This one is about my oldest son.")),
 ("img", story(2, "humvee.jpg", "Before I was prepared. When I didn&rsquo;t have the tools.", "Parenting was something I did not have the skill set to do at the time.", size=66)),
 ("img", quote(3, "As a Christian, abortion was no option. So I gave birth to my oldest son.")),
 ("img", story(4, "mirror.jpg", "And I am so thankful.", size=88)),
 ("img", story(5, "trio.jpg", "I wanted my child to be respectful.", "I wanted him to be mannerable. I wanted him to be smart.", size=66)),
 ("img", story(6, "selfie.jpg", "I didn&rsquo;t want people to see my child coming and say, &ldquo;Here she go with that bad boy.&rdquo;", size=58)),
 ("img", story(7, "grandmas.jpg", "So I instilled good behaviors, mannerisms, and respect in him.", size=66)),
 ("vid:v1", story(8, None, "I was always so proud of him being so smart.", size=72, video=True)),
 ("img", story(9, "group.jpg", "I talked about him to everybody in the world.", size=76, ph=809)),
 ("img", quote(10, "What I failed to do was talk about him <span class='gold' style='white-space:nowrap'>to him.</span> And tell him how proud I am of him.")),
 ("img", story(11, "desert.jpg", "So this is my veteran.", size=88)),
 ("vid:v2", story(12, None, "The walk you earn.", size=88, video=True)),
 ("img", story(13, "fire.jpg", "My oldest son.", size=96)),
 ("img", inset(14, "facetime.jpg", "My baby.", size=96)),
 ("img", story(15, "triple.jpg", "My husband always reminds me he is not a baby.", size=72)),
 ("img", story(16, "twomen.jpg", "I understand that he is a full-grown man.", size=72)),
 ("img", inset(17, "facetime2.jpg", "He will always be my baby.", size=66)),
 ("img", story(18, "hug.jpg", "Had it not been for him, who knows where I&rsquo;d be.", size=72)),
 ("img", story(19, "party.jpg", "He helped mold me into the unapologetic business woman I am today.", size=62)),
 ("img", story(20, "family4.jpg", "Happy Veterans Day to my Quan.", size=80, last=True)),
]

async def main():
    only = [int(x) for x in sys.argv[1:]]
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":W,"height":H})
        for i,(kind,s) in enumerate(S,1):
            if only and i not in only: continue
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{s}</body></html>")
            await pg.wait_for_timeout(250)
            if kind=="img":
                await pg.screenshot(path=str(OUT/f"slide-{i:02d}.jpg"), type="jpeg", quality=93)
            else:
                await pg.screenshot(path=str(OUT/f"overlay-{i:02d}.png"), type="png", omit_background=True)
        await b.close()
asyncio.run(main()); print("done")
