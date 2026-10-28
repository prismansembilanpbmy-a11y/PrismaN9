# Local MusicGen bed, same recipe as the media-use skill: one <=30 s seed, crossfade-looped to the target.
import math, sys
import numpy as np
import soundfile as sf
import torch
from transformers import MusicgenForConditionalGeneration, AutoProcessor

out_path, target_s = sys.argv[1], float(sys.argv[2])
prompt = ("uplifting hopeful inspirational background music, warm piano melody, soft strings, "
          "light steady percussion, bright major key, 100 bpm, no vocals")
seed_s, token_rate, xf_s = 28.0, 50, 0.6

torch.manual_seed(8)
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").eval()
sr = int(model.config.audio_encoder.sampling_rate)
inputs = processor(text=[prompt], padding=True, return_tensors="pt")
with torch.no_grad():
    audio = model.generate(**inputs, max_new_tokens=int(seed_s * token_rate), do_sample=True, guidance_scale=3.0)
seed = audio[0, 0].cpu().numpy().astype("float32")
seed *= 0.89 / max(float(np.abs(seed).max()), 1e-6)

want = int(round(target_s * sr))
xf = int(xf_s * sr)
t = np.linspace(0.0, 1.0, xf, dtype="float32")
fo, fi = np.cos(t * math.pi / 2), np.sin(t * math.pi / 2)
out = seed.copy()
while out.shape[0] < want:
    out = np.concatenate([out[:-xf], out[-xf:] * fo + seed[:xf] * fi, seed[xf:]])
out = out[:want]
n_in, n_out = int(0.08 * sr), int(0.5 * sr)
out[:n_in] *= np.linspace(0, 1, n_in, dtype="float32")
out[-n_out:] *= np.linspace(1, 0, n_out, dtype="float32")
sf.write(out_path, out, sr)
print(f"wrote {out_path} {out.shape[0] / sr:.2f}s sr={sr}")
