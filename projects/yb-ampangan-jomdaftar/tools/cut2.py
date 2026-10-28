# Joins the two speech parts, drops the party list, trims long pauses, upscales, remaps word times.
import json, subprocess, sys
src = "/home/user/video-yb/src"
out_mp4, out_json = sys.argv[1:3]
PAD = 0.15
# (file, transcript, keep ranges in source seconds)
parts = [
    ("p1.mp4", "tp1.json", [(0.0, 38.95)]),
    ("p2.mp4", "tp2.json", [(0.0, 1.05), (23.25, 62.77)]),
]
sil = {
    "p1.mp4": [(5.55, 6.91), (16.76, 18.21), (22.13, 22.84), (25.88, 26.68), (30.95, 31.81), (34.48, 35.18), (37.62, 38.23)],
    "p2.mp4": [(24.23, 24.90), (29.16, 30.22), (30.74, 31.41), (33.05, 33.78), (52.33, 53.01), (57.63, 58.40)],
}
segs = []  # (file, a, b)
for f, _, ranges in parts:
    for a, b in ranges:
        t = a
        for s, e in sil[f]:
            if s >= a and e <= b:
                segs.append((f, t, s + PAD)); t = e - PAD
        segs.append((f, t, b))
words, acc, plan = [], 0.0, []
for f, a, b in segs:
    plan.append({"file": f, "src_start": round(a, 3), "src_end": round(b, 3), "out_start": round(acc, 3)})
    acc += b - a
for f, tj, _ in parts:
    d = json.load(open(f"{src}/{tj}")); W = d if isinstance(d, list) else d["words"]
    for i, w in enumerate(W):
        # keep a word in the kept segment it overlaps most (Whisper's edges spill into pauses)
        best, ov = None, 0.0
        for p in plan:
            if p["file"] != f: continue
            o_ = min(p["src_end"], w["end"]) - max(p["src_start"], w["start"])
            if o_ > ov: best, ov = p, o_
        if best is None or ov < 0.08: continue
        o = best["out_start"] - best["src_start"]
        words.append({"id": f"{f[:2]}_{i}", "text": w["text"],
                      "start": round(max(best["src_start"], w["start"]) + o, 3),
                      "end": round(min(best["src_end"], w["end"]) + o, 3)})
json.dump({"segments": plan, "duration": round(acc, 3), "words": words}, open(out_json, "w"), indent=1)
inputs, fc, labels = [], [], ""
files = ["p1.mp4", "p2.mp4"]
for f in files: inputs += ["-i", f"{src}/{f}"]
for k, (f, a, b) in enumerate(segs):
    n = files.index(f)
    fc.append(f"[{n}:v]trim={a}:{b},setpts=PTS-STARTPTS[v{k}];[{n}:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{k}]")
    labels += f"[v{k}][a{k}]"
graph = ";".join(fc) + f";{labels}concat=n={len(segs)}:v=1:a=1[cv][ca];[cv]fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.4[ov]"
import os
if os.environ.get("SKIP_VIDEO"): sys.exit(0)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[ov]", "-map", "[ca]",
                "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-g", "30", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", out_mp4], check=True)
print("segments", len(segs), "duration", round(acc, 2))
