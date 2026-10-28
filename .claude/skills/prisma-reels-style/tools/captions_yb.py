# Caption scene for the YB speech: spelling fixes, short groups, keywords in gold serif italic, dark pill scrim.
import json, sys, html
words_json, out_html = sys.argv[1:3]
W = json.load(open(words_json))["words"]
FIX = {"p1_10": "dikunjungi", "p1_16": "PRISMA", "p1_26": "Gen Z", "p1_42": "ePBMY", "p2_28": "Hari", "p2_29": "mengundi",
       "p2_33": "2026", "p2_66": "menceburkan", "p2_77": "Gen Z,"}
DROP = {"p2_39", "p2_40"}                       # "E, P, B, MY" spelled out -> one word "ePBMY"
SPAN = {"p2_38": ("ePBMY", 44.0)}               # new text, new end
ADD = [  # words Whisper placed inside a trimmed pause
    {"id": "p1_21", "text": "Saya", "start": 15.6, "end": 15.85},
    {"id": "p2_2", "text": "Malaysia.", "start": 35.2, "end": 35.55},
    {"id": "p2_30", "text": "pada", "start": 36.5, "end": 36.8},
]
HOT = {"p1_16", "p1_26", "p1_31", "p1_33", "p1_42", "p1_46", "p2_31", "p2_32", "p2_33", "p2_38",
       "p2_50", "p2_53", "p2_64", "p2_77"}
KEEP = {"Parlimen", "Belia", "18", "hingga", "1", "November", "anak-anak", "dunia"}   # never break after these
START, END = 5.65, 67.8
fix = {"p2_0": (34.56, 34.9), "p2_1": (34.9, 35.2)}
ws = []
for w in W:
    if w["id"] in DROP: continue
    w = dict(w)
    if w["id"] in fix: w["start"], w["end"] = fix[w["id"]]
    if w["id"] in SPAN: w["text"], w["end"] = SPAN[w["id"]]
    w["text"] = FIX.get(w["id"], w["text"])
    ws.append(w)
ws += ADD
ws = [w for w in ws if START <= w["start"] < END]
ws.sort(key=lambda w: w["start"])
groups, cur = [], []
for k, w in enumerate(ws):
    cur.append(w)
    nxt = ws[k + 1] if k + 1 < len(ws) else None
    if nxt and w["text"] in KEEP and len(cur) < 4: continue
    if w["text"][-1] in ".,?!" or len(cur) >= 3 or nxt is None or nxt["start"] - w["end"] >= 0.4:
        groups.append(cur); cur = []
rows, js = [], []
for g, grp in enumerate(groups):
    gs = max(START, grp[0]["start"] - 0.05)
    ge = grp[-1]["end"] + 0.05
    if g + 1 < len(groups): ge = min(ge, max(groups[g + 1][0]["start"] - 0.05, gs + 0.3))
    ge = min(ge, END)
    spans = " ".join(f'<span class="w{" hot" if w["id"] in HOT else ""}">{html.escape(w["text"])}</span>' for w in grp)
    rows.append(f'    <div id="g{g}" class="grp"><span class="pill">{spans}</span></div>')
    js.append(f'    show("#g{g}", {gs:.3f}, {ge:.3f});')
page = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    #root .grp {{
      position: absolute; left: 60px; right: 60px; top: 1190px;
      text-align: center; opacity: 0; visibility: hidden;
    }}
    #root .pill {{
      display: inline; padding: 6px 22px; line-height: 1.55;
      background: rgba(40, 4, 10, 0.62); border-radius: 18px;
      -webkit-box-decoration-break: clone; box-decoration-break: clone;
      font-family: "Poppins", sans-serif; font-weight: 700; font-size: 56px; color: #ffffff;
    }}
    #root .w.hot {{
      font-family: "Playfair Display", serif; font-style: italic; font-weight: 700;
      font-size: 1.2em; color: #f5c22e;
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(rows)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // One short group at a time; keywords are set in gold serif italic.
    function show(group, start, end) {{
      tl.set(group, {{ visibility: "visible" }}, start);
      tl.fromTo(group, {{ opacity: 0, scale: 0.92 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "power2.out" }}, start);
      tl.to(group, {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, end - 0.1);
      tl.set(group, {{ opacity: 0, visibility: "hidden" }}, end);
    }}
{chr(10).join(js)}
    tl.set({{}}, {{}}, {END});
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open(out_html, "w").write(page)
for grp in groups: print(f'{grp[0]["start"]:6.2f} ' + " ".join(w["text"] for w in grp))
