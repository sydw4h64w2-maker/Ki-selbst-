# Schätzt Wortzeiten aus segments.json, solange es noch keine echte Sprachaufnahme gibt.
import json, sys
segs = json.load(open(sys.argv[1]))
out = []
for a, b, text in segs:
    ws = text.split()
    weights = [len(w) + 3 + (6 if w[-1] in ".:?!" else 0) for w in ws]
    tot = sum(weights); t = a
    for w, wt in zip(ws, weights):
        d = (b - a) * wt / tot
        out.append({"text": w, "start": round(t, 3), "end": round(t + d * 0.85, 3)})
        t += d
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=0)
