import asyncio, base64, pathlib
from playwright.async_api import async_playwright

W, H = 1080, 1350
OUT = pathlib.Path("out"); OUT.mkdir(exist_ok=True)
photo = base64.b64encode(open("photo.jpg","rb").read()).decode()
logo = base64.b64encode(open("logo-circle.png","rb").read()).decode()
prof = base64.b64encode(open("profile.jpg","rb").read()).decode()

CSS = f"""
@import url('https://rsms.me/inter/inter.css');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{H}px;overflow:hidden;font-family:Inter,'Inter Display',system-ui,sans-serif;background:#faf8f4;color:#03141e}}
.slide{{position:relative;width:{W}px;height:{H}px;background:#faf8f4;padding:110px 84px 140px;overflow:hidden}}
.bar{{position:absolute;top:0;left:0;right:0;height:16px;background:#004e50}}
.hdr{{display:flex;align-items:center;gap:24px;margin-bottom:70px}}
.hdr img{{width:120px;height:120px;border-radius:50%;object-fit:cover;border:5px solid #C8A25F}}
.hdr .n{{font-weight:700;font-size:36px;letter-spacing:-.01em}}
.hdr .s{{font-weight:500;font-size:27px;color:#004e50;margin-top:4px}}
.big{{position:absolute;right:70px;top:40px;font-weight:800;font-size:250px;line-height:1;color:#C8A25F;opacity:.13;letter-spacing:-.06em}}
.tag{{display:inline-block;font-weight:700;font-size:26px;letter-spacing:.16em;text-transform:uppercase;color:#C8A25F;margin-bottom:28px}}
h1{{font-weight:800;font-size:76px;line-height:1.05;letter-spacing:-.035em;margin-bottom:44px;position:relative}}
p{{font-weight:500;font-size:46px;line-height:1.36;margin-bottom:30px;position:relative}}
.do{{position:absolute;left:84px;right:84px;bottom:170px;background:#004e50;color:#faf8f4;padding:40px 44px;border-radius:22px}}
.do b{{display:block;font-size:24px;letter-spacing:.16em;text-transform:uppercase;color:#C8A25F;margin-bottom:14px}}
.do span{{font-size:40px;line-height:1.32;font-weight:600}}
.ft{{position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:flex-end;align-items:center;font-size:30px;color:#004e50;border-top:2px solid #e3dccd;padding-top:26px;min-height:30px}}
.ft .arrow{{display:flex;align-items:center;gap:18px;color:#C8A25F;font-style:italic;font-weight:600;letter-spacing:.02em}}
.ft .arrow svg{{width:150px;height:44px}}
.photo{{padding:0}}
.photo img.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 35%}}
.photo .shade{{position:absolute;left:0;right:0;bottom:0;height:66%;background:linear-gradient(180deg,rgba(3,20,30,0) 0%,rgba(3,20,30,.6) 32%,rgba(3,20,30,.96) 100%)}}
.photo .card{{position:absolute;left:72px;right:72px;bottom:170px;color:#faf8f4}}
.photo .card .line{{width:120px;height:8px;background:#C8A25F;margin-bottom:34px}}
.photo .card h1{{font-size:78px;color:#faf8f4;margin-bottom:30px}}
.photo .card p{{color:#e9e4d9;font-size:36px;margin:0;font-weight:500}}
.photo .card .who{{display:flex;align-items:center;gap:18px;margin-top:40px}}
.photo .card .who img{{width:76px;height:76px;border-radius:50%;object-fit:cover;border:3px solid #C8A25F}}
.photo .card .who .n{{font-weight:700;font-size:28px}}
.photo .card .who .s{{font-weight:500;font-size:22px;color:#C8A25F;margin-top:2px}}
.photo .ft{{color:#faf8f4;border-top-color:rgba(250,248,244,.25)}}
.quote{{background:#03141e;color:#faf8f4}}
.quote .hdr .n{{color:#faf8f4}} .quote .hdr .s{{color:#C8A25F}}
.quote .big{{opacity:.22}}
.quote .mark{{font-weight:800;font-size:260px;line-height:.7;color:#C8A25F;margin-bottom:30px;font-family:Georgia,serif}}
.quote h1{{font-size:70px;color:#faf8f4;font-weight:700;line-height:1.15}}
.quote .by{{font-size:30px;color:#C8A25F;font-weight:600;margin-top:10px}}
.quote .ft{{color:#faf8f4;border-top-color:rgba(250,248,244,.2)}}
.close .cta{{position:absolute;left:84px;right:84px;bottom:170px;background:#004e50;color:#faf8f4;padding:44px 48px;border-radius:22px}}
.close .cta p{{color:#faf8f4;font-weight:700;font-size:44px;margin-bottom:22px}}
.close .cta p.k{{color:#C8A25F;font-size:38px;margin:0}}
.teal{{color:#004e50}} .gold{{color:#C8A25F}}
"""

ARROW = '<svg viewBox="0 0 120 36" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18c8-14 16-14 24 0s16 14 24 0 16-14 24 0 16 14 24 0h12"/><path d="M104 8l12 10-12 10"/></svg>'

def hdr(i=None):
    num = f'<div class="big">{i:02d}</div>' if i else ''
    return f'<div class="bar"></div>{num}<div class="hdr"><img src="data:image/jpeg;base64,{prof}"><div><div class="n">Jessica Shunta</div><div class="s">Church Operations Systems</div></div></div>'

def ft(i, n, last=False):
    if last: return ""
    return f'<div class="ft"><div class="arrow"><span>swipe left</span>{ARROW}</div></div>'

def slide(i, n, body, last=False, cls=""):
    return f'<div class="slide {cls}">{hdr(i)}{body}{ft(i,n,last)}</div>'

def tip(k, title, body, do):
    return f'<div class="tag">{k}</div><h1>{title}</h1><p>{body}</p><div class="do"><b>Do this</b><span>{do}</span></div>'


CSS += """
.logo{position:absolute;width:150px;height:150px;border-radius:50%}
.photo .logo{left:72px;top:52px;width:130px;height:130px}
.slide .logo.s2{position:relative;display:block;width:190px;height:190px;margin-top:34px}
.close .logo{position:relative;display:block;width:120px;height:120px;margin-bottom:26px}
"""

N = 14
S = []
S.append(f'''<div class="slide photo"><img class="bg" src="data:image/jpeg;base64,{photo}"><div class="shade"></div><div class="bar"></div>
<img class="logo" src="data:image/png;base64,{logo}">
<div class="card"><div class="line"></div>
<h1>Their leaders are so excited. Here are their first 60 minutes.</h1>
<p>Carrone Baptist Church, Pennsylvania, joined the Church Continuity Platform&trade;. Here is what we did.</p>
<div class="who"><img src="data:image/jpeg;base64,{prof}"><div><div class="n">Jessica Shunta</div><div class="s">Church Operations Systems</div></div></div>
</div>{ft(1,N)}</div>''')

S.append(slide(2,N,f'''<div class="tag">The call</div>
<h1>One screen share. Every leader added live.</h1>
<p>Carrone Baptist Church in Pittsburgh. The pastor and first lady were already inside. Now the leaders who will run the back end got their first look.</p>
<img class="logo s2" src="data:image/png;base64,{logo}">'''))

S.append(slide(3,N,tip("Settings","Start in settings. That is the back office.",
 "Church info, logo, colors, and weekly services live here. Your members never see this side.",
 "Add every gathering: Sunday worship, Sunday school, Bible study. They become your attendance options.")))

S.append(slide(4,N,tip("Access","Match the role to the job.",
 "We added each leader live and picked a role from a dropdown. You can change it when their role changes, or remove it from the same screen.",
 "List who needs back end access and what they should see. Choose the role by that, not by title.")))

S.append(slide(5,N,'''<div class="mark">&ldquo;</div>
<h1>Just because you add pastor here, it does not give them any special permissions. It is only a title.</h1>
<div class="by">What I told them on the call</div>''', cls="quote"))

S.append(slide(6,N,tip("Giving","Connect Stripe once.",
 "Cards, Apple Pay, Cash App, PayPal. One connection takes them all, so each member gives the way they already do.",
 "Put the EIN, the church address, and the church phone number in front of you before you start.")))

S.append(slide(7,N,tip("Guardrails","Fixing a deposit takes two people.",
 "You cannot just delete a wrong number and retype it. A second person has to verify. The record shows who entered it, who verified it, the date, and the time.",
 "Name the two people who will enter and verify. Use the notes field every time.")))

S.append(slide(8,N,tip("Giving data","See the trend without asking anyone.",
 "Twelve weeks and twelve months of history. Each giver shows the last gift, the year to date, and how often they give. Recurring givers sit in one place.",
 "Start entering gifts now so your first 12 week trend begins to fill in.")))

S.append(slide(9,N,tip("The vault","Do not start from scratch.",
 "Communication templates, continuity binders, emergency plans, governance documents. Fill in only what applies to your church.",
 "Pick one document this month. One a month or one a quarter is plenty.")))

S.append(slide(10,N,tip("Forms","Two or three questions. That is it.",
 "Build a survey in minutes. Send it to members only or to anyone with the link. The short ones perform best.",
 "Cut your next survey to three questions. Close it when you have your answers, or it stays out there.")))

S.append(slide(11,N,tip("Training","Turn trainings on and off.",
 "Trainings are included and not tied to any denomination. Switch each one on or off to roll out at your pace.",
 "Pick the first training your leaders will take. Keep the rest off until they are ready.")))

S.append(slide(12,N,tip("Attendance","Let people check themselves in.",
 "Print the QR code for each service. The platform learns who shows up every week. Add a note when something is different. A year from now you will not remember why.",
 "Print the Sunday school QR code and put it at the door.")))

S.append(slide(13,N,'''<div class="tag">The point</div>
<h1>Leaders get excited when they can see it.</h1>
<p>They watched a screen, asked questions, and saw their own team added in real time. <span class="teal" style="font-weight:700">Seeing it is what moves people.</span></p>
<div class="do"><b>Do this</b><span>Invite one leader this week. Then ask what they wish it did.</span></div>'''))

S.append(slide(14,N,f'''<div class="tag">As leaders</div>
<h1>We are held to higher standards.</h1>
<p>Structure and systems are not extra. They are stewardship.</p>
<div class="cta"><p>Send me a message. We can walk through it together and see what your church needs first.</p>
<p class="k">Don't put off today what should have been done yesterday.</p></div>''', last=True, cls="close"))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":W,"height":H})
        for i,s in enumerate(S,1):
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{s}</body></html>")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f"slide-{i:02d}.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main()); print("done")
