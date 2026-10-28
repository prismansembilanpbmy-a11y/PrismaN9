# Builds the jump-cut talking-head file and the remapped word list.
import json, subprocess, sys
src, transcript, out_mp4, out_json = sys.argv[1:5]
DUR = 67.977
PAD = 0.15
sil = [(0.05,1.49),(11.90,13.19),(24.20,25.03),(26.26,27.17),(33.02,33.99),
       (41.10,41.79),(49.75,50.38),(56.48,57.32),(60.27,61.58)]
keep, t = [], 0.0
for s, e in sil:
    a, b = s + PAD, e - PAD
    if s <= 0.1: t = b; continue
    keep.append((t, a)); t = b
keep.append((t, DUR))
# remap words
d = json.load(open(transcript)); words = d if isinstance(d, list) else d["words"]
def remap(x):
    acc = 0.0
    for a, b in keep:
        if x < a: return acc
        if x <= b: return acc + x - a
        acc += b - a
    return acc
out, segs, acc = [], [], 0.0
for a, b in keep:
    segs.append({"src_start": round(a,3), "src_end": round(b,3), "out_start": round(acc,3)}); acc += b - a
for i, w in enumerate(words):
    out.append({"i": i, "text": w["text"], "start": round(remap(w["start"]),3), "end": round(remap(w["end"]),3)})
json.dump({"segments": segs, "duration": round(acc,3), "words": out}, open(out_json, "w"), indent=1)
parts, labels = [], ""
for k, (a, b) in enumerate(keep):
    parts.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{k}];[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS[a{k}]")
    labels += f"[v{k}][a{k}]"
fc = ";".join(parts) + f";{labels}concat=n={len(keep)}:v=1:a=1[cv][ca];[cv]fps=30,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6[ov]"
subprocess.run(["ffmpeg","-loglevel","error","-y","-i",src,"-filter_complex",fc,"-map","[ov]","-map","[ca]",
    "-c:v","libx264","-crf","18","-preset","medium","-g","30","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000",out_mp4], check=True)
print("segments", len(keep), "duration", round(acc,2))
