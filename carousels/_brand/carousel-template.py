import asyncio, base64, pathlib
from playwright.async_api import async_playwright

W, H = 1080, 1350
OUT = pathlib.Path("out2"); OUT.mkdir(exist_ok=True)
photo = base64.b64encode(open("photo.jpg","rb").read()).decode()
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

N = 13
S = []
S.append(f'''<div class="slide photo"><img class="bg" src="data:image/jpeg;base64,{photo}"><div class="shade"></div><div class="bar"></div>
<div class="card"><div class="line"></div>
<h1>Senior pastor for four years. Not one policy protecting him.</h1>
<p>His church had a pastoral protection policy. It just named the previous first family. 8 lessons from one Saturday call.</p>
<div class="who"><img src="data:image/jpeg;base64,{prof}"><div><div class="n">Jessica Shunta</div><div class="s">Church Operations Systems</div></div></div>
</div>{ft(1,N)}</div>''')

S.append(slide(2,N,'''<div class="tag">The call</div>
<h1>He joined from the car after his grandson's football game.</h1>
<p>His administrator had her list ready. We added members, fixed training access, walked the documents and the QR code.</p>
<p>Then we opened the leadership binder and I asked one question: <span class="teal" style="font-weight:700">Do you have a pastoral protection policy on you?</span></p>'''))

S.append(slide(3,N,tip("Protection","Check whose name is on the policy.",
 "The founder passed. A new pastor stepped up. Four years went by. The policy on file still covered the previous first family.",
 "Pull the policy this week. Read the insured name and the beneficiary out loud. If it is not the current pastor, you have a gap.")))

S.append(slide(4,N,tip("Legacy","Protection is a legacy decision, not a bill.",
 "The church can be the beneficiary. Or the church gets a portion and the first lady gets a portion. No right or wrong. It follows the vision.",
 "Decide what the church receives and what your family receives if you are gone. Write it down. Then match the policy to it.")))

S.append(slide(5,N,'''<div class="mark">&ldquo;</div>
<h1>We all want to be here forever. If we are not, the church should still stand strong, and the first family should still be seen about.</h1>
<div class="by">What I told him on the call</div>''', cls="quote"))

S.append(slide(6,N,tip("Documents","Build the file cabinet.",
 "Financial statements. Bylaws. Voting rights. Board structure. Vendor contracts. One place, sorted by category, where the right people can find them.",
 "List every document that lives in one person's head, inbox, or desk drawer. Those go in first.")))

S.append(slide(7,N,tip("Rollout","Roll it out in phases.",
 "Launch with one group. Get them excited. Let everyone else want in. You will never get 100 percent, but phases get you close.",
 "Name your first group today. Leaders, one ministry, or the people who already ask for things like this.")))

S.append(slide(8,N,tip("Visitors","Put the QR code everywhere.",
 "Visitor table. Back of the pews. Inside the program so an usher can show it on the aisle. A glimpse of it on the stream.",
 "Download the code and put it in three places before Sunday.")))

S.append(slide(9,N,tip("Communication","Know where the message lands.",
 "In their system an announcement goes to email. The event board goes to the member portal. Two tools, two jobs. Mix them up and people miss it.",
 "Before anything goes to the congregation, ask: where will they actually see this?")))

S.append(slide(10,N,tip("Training","Keep training short.",
 "One to three minute videos. The whole set in about an hour. Nobody reads a 100 page manual. People need what to do, when, how, and why it matters.",
 "Cut any training you own down to the steps someone needs to act today.")))

S.append(slide(11,N,tip("Feedback","Ask what they wish it did.",
 "Her first request was member anniversaries. They celebrate them every month. I wrote it down on the call. Systems get better when the people using them are heard.",
 "Ask your team one question this week: what do you wish this did that it does not?")))

S.append(slide(12,N,'''<div class="tag">The point</div>
<h1>Nobody at that church did anything wrong.</h1>
<p>The founder passed. A new pastor stepped up. Four years went by. Nobody owned the update, so it never happened. That is how most gaps start. Not neglect. <span class="teal" style="font-weight:700">Just no one assigned to it.</span></p>
<div class="do"><b>Do this</b><span>Name one person to own the leadership binder, and put their name on it this week.</span></div>'''))

S.append(slide(13,N,'''<div class="tag">As leaders</div>
<h1>We are held to higher standards.</h1>
<p>Protection, structure, and systems are not extra. They are stewardship.</p>
<div class="cta"><p>Send me a message. We can walk through it together and make sure the first family is protected.</p>
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
