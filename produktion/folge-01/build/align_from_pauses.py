# Legt Wortzeiten aus Sprechpausen fest: jede Phrase füllt die Sprechstrecke zwischen zwei Pausen.
# Aufruf: python3 build/align_from_pauses.py assets/voice.mp3 build/phrases.txt build/words.json
import json, re, subprocess, sys
audio, phrases_file, out = sys.argv[1:4]
log = subprocess.run(["ffmpeg", "-hide_banner", "-i", audio, "-af", "silencedetect=noise=-40dB:d=0.18", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio],
                           capture_output=True, text=True).stdout)
st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", log)]
phrases = [l.strip() for l in open(phrases_file, encoding="utf-8") if l.strip()]
if st and st[0] < 0.05:  # Stille am Anfang
    lead = en.pop(0); st.pop(0)
else:
    lead = 0.0
if len(st) > len(en):  # Stille am Ende
    tail = st.pop()
else:
    tail = dur
spans = list(zip([lead] + en, st + [tail]))
assert len(spans) == len(phrases), f"{len(spans)} Sprechstrecken, aber {len(phrases)} Phrasen"
words = []
for (a, b), p in zip(spans, phrases):
    ws = p.split()
    wt = [len(w) + 2 for w in ws]
    tot = sum(wt); t = a
    for w, x in zip(ws, wt):
        d = (b - a) * x / tot
        words.append({"text": w, "start": round(t, 3), "end": round(t + d, 3)})
        t += d
json.dump(words, open(out, "w"), ensure_ascii=False, indent=0)
for (a, b), p in zip(spans, phrases):
    print(f"{a:6.2f}-{b:6.2f}  {p}")
