# Generates compositions/captions.html from assets/words.json with spelling fixes.
import json, sys, html
words_json, out_html = sys.argv[1:3]
d = json.load(open(words_json)); W = d["words"]
FIX = {5: "Nur", 6: "Fatihah", 7: "binti", 10: "PRISMA", 11: "Negeri", 19: "Kuala", 20: "Lumpur",
       25: "Tihah", 26: "mewakili", 27: "Negeri", 32: "terletak", 34: "Kuala", 44: "fizikal.",
       49: "UMCCed", 52: "Diploma", 53: "Pengurusan.", 64: "atlet", 66: "Negeri", 68: "Tihah"}
HOT = {14, 15, 41, 75, 78, 81, 35, 65}   # words in yellow
START, END = 3.1, 55.0                   # captions live between hook and slogan
ws = []
for w in W:
    i = w["i"]
    if i < 4 or w["start"] >= END: continue
    t = FIX.get(i, w["text"])
    if i == 65:  # "paracata" -> two words sharing its time
        mid = (w["start"] + w["end"]) / 2
        ws.append(dict(i="65a", text="para", start=w["start"], end=mid, hot=True))
        ws.append(dict(i="65b", text="catur", start=mid, end=w["end"], hot=True)); continue
    ws.append(dict(i=i, text=t, start=w["start"], end=w["end"], hot=i in HOT))
# group: break at punctuation, a 150 ms gap, or 4 words
groups, cur = [], []
for k, w in enumerate(ws):
    cur.append(w)
    nxt = ws[k + 1] if k + 1 < len(ws) else None
    if w["text"] in ("Kuala", "para", "Negeri", "binti", "orang", "kelainan") and len(cur) < 6 and nxt: continue
    if (w["text"][-1] in ".,?!" or len(cur) >= 4 or nxt is None or nxt["start"] - w["end"] >= 0.4):
        groups.append(cur); cur = []
# fold one-word groups into a neighbour (Whisper's word gaps are loose)
merged = []
for grp in groups:
    if merged and (len(grp) == 1 or len(merged[-1]) == 1) and len(merged[-1]) + len(grp) <= 5 \
            and merged[-1][-1]["text"][-1] not in ".":
        merged[-1] = merged[-1] + grp
    else:
        merged.append(grp)
groups = merged
rows, js = [], []
for g, grp in enumerate(groups):
    gs = max(START + 0.05, grp[0]["start"] - 0.05)
    ge = grp[-1]["end"] + 0.05
    if g + 1 < len(groups): ge = min(ge, groups[g + 1][0]["start"] - 0.06)
    ge = min(ge, END)
    spans = " ".join(
        f'<span id="w{w["i"]}" class="w{" hot" if w["hot"] else ""}">{html.escape(w["text"])}</span>' for w in grp)
    rows.append(f'    <div id="g{g}" class="grp">{spans}</div>')
    js.append(f'  show("#g{g}", {gs:.3f}, {ge:.3f}, [' + ", ".join(
        f'["#w{w["i"]}", {max(gs, w["start"]):.3f}]' for w in grp) + "]);")
page = f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    #root .grp {{
      position: absolute; left: 60px; right: 60px; top: 1170px;
      text-align: center; opacity: 0; visibility: hidden;
      font-family: "Poppins", sans-serif; font-weight: 800; font-size: 62px; line-height: 1.15;
      color: #ffffff; -webkit-text-stroke: 3px rgba(10, 14, 40, 0.9); paint-order: stroke fill;
      text-shadow: 0 6px 18px rgba(0, 0, 0, 0.55);
    }}
    #root .w {{ display: inline-block; color: #ffffff; }}
    #root .w.hot.on {{ color: #f7c600; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(rows)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // One group at a time; key words turn yellow as they are spoken.
    function show(group, start, end, words) {{
      tl.set(group, {{ visibility: "visible" }}, start);
      tl.fromTo(group, {{ opacity: 0, scale: 0.92 }}, {{ opacity: 1, scale: 1, duration: 0.12, ease: "power2.out" }}, start);
      words.forEach(([w, t]) => {{
        if (document.querySelector(w).classList.contains("hot")) tl.set(w, {{ className: "w hot on" }}, t);
      }});
      tl.to(group, {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, end - 0.1);
      tl.set(group, {{ opacity: 0, visibility: "hidden" }}, end);
    }}
{chr(10).join(js)}
    tl.set({{}}, {{}}, 55.02);
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open(out_html, "w").write(page)
for grp in groups: print(f'{grp[0]["start"]:6.2f} ' + " ".join(w["text"] for w in grp))
