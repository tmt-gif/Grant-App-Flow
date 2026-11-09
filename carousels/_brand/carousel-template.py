import asyncio, base64, pathlib
from playwright.async_api import async_playwright

W, H = 1080, 1350
OUT = pathlib.Path("out"); OUT.mkdir(exist_ok=True)
photo = base64.b64encode(open("photo.jpg","rb").read()).decode()
prof = base64.b64encode(open("profile.jpg","rb").read()).decode()

CSS = f"""
@import url('https://rsms.me/inter/inter.css');
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:{W}px;height:{H}px;overflow:hidden;font-family:Inter,'Inter Display',system-ui,sans-serif;background:#faf8f4;color:#03141e}}
.slide{{position:relative;width:{W}px;height:{H}px;background:#faf8f4;padding:96px 84px 120px}}
.hdr{{display:flex;align-items:center;gap:22px;margin-bottom:64px}}
.hdr img{{width:112px;height:112px;border-radius:50%;object-fit:cover;border:4px solid #004e50}}
.hdr .n{{font-weight:700;font-size:34px;letter-spacing:-.01em}}
.hdr .s{{font-weight:500;font-size:26px;color:#004e50;margin-top:4px}}
.tag{{display:inline-block;font-weight:700;font-size:26px;letter-spacing:.14em;text-transform:uppercase;color:#C8A25F;margin-bottom:30px}}
.num{{font-weight:800;font-size:120px;line-height:1;color:#C8A25F;letter-spacing:-.04em;margin-bottom:18px}}
h1{{font-weight:800;font-size:68px;line-height:1.08;letter-spacing:-.03em;margin-bottom:40px}}
h1.sm{{font-size:66px}}
p{{font-weight:500;font-size:44px;line-height:1.38;color:#03141e;margin-bottom:28px}}
p.lead{{font-size:48px}}
.do{{margin-top:48px;border-left:10px solid #004e50;padding:26px 34px;background:#eef3f1;border-radius:0 18px 18px 0}}
.do b{{display:block;font-size:24px;letter-spacing:.14em;text-transform:uppercase;color:#004e50;margin-bottom:10px}}
.do span{{font-size:40px;line-height:1.35;font-weight:600}}
.ft{{position:absolute;left:84px;right:84px;bottom:52px;display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:28px;color:#004e50}}
.ft .arrow{{display:flex;align-items:center;gap:14px}}
.ft .arrow svg{{width:56px;height:56px}}
.photo{{padding:0}}
.photo img.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center 35%}}
.photo .shade{{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(180deg,rgba(3,20,30,0) 0%,rgba(3,20,30,.55) 35%,rgba(3,20,30,.92) 100%)}}
.photo .card{{position:absolute;left:72px;right:72px;bottom:150px;color:#faf8f4}}
.photo .card .who{{display:flex;align-items:center;gap:18px;margin-bottom:30px}}
.photo .card .who img{{width:84px;height:84px;border-radius:50%;object-fit:cover;border:3px solid #C8A25F}}
.photo .card .who .n{{font-weight:700;font-size:30px}}
.photo .card .who .s{{font-weight:500;font-size:23px;color:#C8A25F;margin-top:3px}}
.photo .card h1{{font-size:66px;color:#faf8f4;margin-bottom:26px}}
.photo .card p{{color:#e9e4d9;font-size:36px;margin:0}}
.photo .ft{{color:#faf8f4}}
.close h1{{font-size:62px}}
.gold{{color:#C8A25F}}
.teal{{color:#004e50}}
"""

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10.5"/><path d="M8 12h8M13 8.5l3.5 3.5L13 15.5"/></svg>'

def hdr():
    return f'<div class="hdr"><img src="data:image/jpeg;base64,{prof}"><div><div class="n">Jessica Shunta</div><div class="s">Church Operations Systems</div></div></div>'

def ft(i, n, last=False):
    arrow = "" if last else f'<div class="arrow"><span>Swipe</span>{ARROW}</div>'
    return f'<div class="ft">{arrow}<div style="margin-left:auto">{i}/{n}</div></div>'

def text_slide(i, n, body, last=False, cls=""):
    return f'<div class="slide {cls}">{hdr()}{body}{ft(i,n,last)}</div>'

def photo_slide(i, n, h, sub):
    return f'''<div class="slide photo"><img class="bg" src="data:image/jpeg;base64,{photo}"><div class="shade"></div>
    <div class="card"><div class="who"><img src="data:image/jpeg;base64,{prof}"><div><div class="n">Jessica Shunta</div><div class="s">Church Operations Systems</div></div></div>
    <h1>{h}</h1><p>{sub}</p></div>{ft(i,n)}</div>'''

def tip(k, title, body, do):
    return f'<div class="tag">Tip {k}</div><h1 class="sm">{title}</h1><p>{body}</p><div class="do"><b>Do this</b><span>{do}</span></div>'

slides = []
N = 12
slides.append(photo_slide(1, N,
    "He has been senior pastor for 4 years. The church still had no protection policy on him.",
    "8 things every church leader should take from one Saturday onboarding call."))

slides.append(text_slide(2, N, '''
<div class="tag">The call</div>
<h1>Saturday. He was in the car leaving his grandson's football game.</h1>
<p class="lead">His administrator had her list ready. Forty three minutes on the Church Continuity Platform™. Members, training, documents, the visitor QR code.</p>
<p class="lead">Then we got to the leadership binder, and I asked one question.</p>'''))

slides.append(text_slide(3, N, tip(1,
    "Check whose name is on your protection policy.",
    "The only pastoral protection policy his church had was on the previous first family. The founder passed. Leadership changed. The paperwork never caught up.",
    "Pull the policy this week. Read the insured name and the beneficiary. If it is not the current pastor, you have a gap.")))

slides.append(text_slide(4, N, tip(2,
    "Protection is a legacy decision, not just insurance.",
    "The church can be the beneficiary. Or the church gets a portion and a portion goes to the first lady. There is no right or wrong. It depends on the vision.",
    "Write down what you want the church to receive and what you want your family to receive if you are not here. Then get the policy that matches it.")))

slides.append(text_slide(5, N, tip(3,
    "Build the file cabinet.",
    "Financial statements. Bylaws. Voting rights. Board and governance structure. Vendor contracts. One place, organized by category, where the right people can find them.",
    "List every document that lives in one person's head, inbox, or desk drawer. Those go in first.")))

slides.append(text_slide(6, N, tip(4,
    "Roll it out in phases, not all at once.",
    "Launch new systems with one group first. Get them excited. Let the rest of the congregation want in. You will never get 100 percent, but phases get you a lot closer.",
    "Pick your first group. Leaders, a ministry, or the people who already ask for things like this.")))

slides.append(text_slide(7, N, tip(5,
    "Put the visitor QR code everywhere.",
    "On the visitor table. On the back of the pews. Printed inside the program so an usher can show it on the aisle. And a glimpse of it on the stream if you go live.",
    "Download your QR code and put it in at least three places before Sunday.")))

slides.append(text_slide(8, N, tip(6,
    "Know where your message lands before you hit send.",
    "In their system, an announcement goes to email. The event board goes to the member portal. Two tools, two jobs. Mixing them up means people miss what you posted.",
    "Before you send anything to the congregation, ask: where does this show up for them?")))

slides.append(text_slide(9, N, tip(7,
    "Keep training short.",
    "Their training videos are one to three minutes each. The whole set takes about an hour. Nobody reads a 100 page manual. They need what to do, when, how, and why it matters.",
    "Cut any training you own down to the steps someone needs to act today.")))

slides.append(text_slide(10, N, tip(8,
    "Ask your people what they wish it did.",
    "Her first request: member anniversaries. They celebrate them every month. I wrote it down on the call. Systems get better when the people using them are heard.",
    "Ask your team one question this week: what do you wish this did that it does not?")))

slides.append(text_slide(11, N, '''
<div class="tag">The point</div>
<h1>Nobody at that church did anything wrong.</h1>
<p class="lead">The founder passed. A new pastor stepped up. Four years went by. The policy never got updated because nobody owned it.</p>
<p class="lead">That is how most gaps happen. Not neglect. Just no one assigned to it.</p>'''))

slides.append(text_slide(12, N, '''
<div class="tag">As leaders</div>
<h1>We are held to higher standards.</h1>
<p class="lead">Protection, structure, and systems are not extra. They are stewardship. They are how the work continues when we are not in the room.</p>
<p class="lead teal" style="font-weight:700">Send me a message. We can walk through it together and make sure the first family is protected.</p>
<p class="lead gold" style="font-weight:700">Don't put off today what should have been done yesterday.</p>''', last=True, cls="close"))

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":W,"height":H}, device_scale_factor=1)
        for i,s in enumerate(slides,1):
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{s}</body></html>")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT/f"slide-{i:02d}.jpg"), type="jpeg", quality=92)
        await b.close()
asyncio.run(main())
print("done", len(slides))
