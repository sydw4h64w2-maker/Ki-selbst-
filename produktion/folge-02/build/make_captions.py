# Baut compositions/captions.html aus einer Wortliste [{text,start,end}].
# Aufruf: python3 build/make_captions.py build/words.json
import json, re, sys, html

words = json.load(open(sys.argv[1]))
SHOW = {"eins.": "1.", "zwei.": "2.", "drei.": "3.", "vier.": "4.", "fünf.": "5.", "sechs.": "6.", "sieben.": "7.",
        "fünfunddreißigtausend": "35.000", "fünfzigtausend": "50.000", "vierzigtausend.": "40.000.", "Sieben": "7"}
HL = re.compile(r"^(35\.000|50\.000|40\.000\.?|7|[1-7]\.|weiter|Indigo\.|Bäcker\.|Welt\.)$")

groups, cur = [], []
for w in words:
    cur.append(w)
    end_sentence = w["text"][-1] in ".:?!,"
    if len(cur) == 3 or end_sentence:
        groups.append(cur); cur = []
if cur:
    groups.append(cur)

parts, tw = [], []
starts = [round(max(0.1, g[0]["start"] - 0.05), 3) for g in groups]
for i, g in enumerate(groups):
    start = starts[i]
    nxt = starts[i + 1] if i + 1 < len(groups) else g[-1]["end"] + 0.6
    end = round(min(g[-1]["end"] + 0.35, nxt - 0.02), 3)
    spans = []
    for w in g:
        t = SHOW.get(w["text"], w["text"])
        core = t.rstrip(".,:?!") if t not in ("1.", "2.", "3.", "4.", "5.") else t
        cls = ' class="hl"' if HL.match(t) or HL.match(core) else ""
        spans.append(f"<span{cls}>{html.escape(t)}</span>")
    gid = f"cap-g{i}"
    parts.append(f'    <div id="{gid}" class="clip cap-g" data-start="{start}" data-duration="{round(end - start, 3)}">'
                 f'<div class="cap-in">{" ".join(spans)}</div></div>')
    tw.append(f'    tl.fromTo("#{gid} .cap-in", {{ scale: 0.82, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.12, ease: "back.out(2.5)" }}, {start});')

out = f'''<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
      font-family: "Inter", sans-serif;
      pointer-events: none;
    }}
    .cap-g {{
      position: absolute;
      left: 0;
      top: 1190px;
      width: 1080px;
      text-align: center;
      overflow: visible;
    }}
    .cap-in {{
      display: inline-block;
      padding: 0 60px;
      color: #fff;
      font-weight: 900;
      font-size: 76px;
      line-height: 1.1;
      -webkit-text-stroke: 10px #0b1c25;
      paint-order: stroke fill;
      text-shadow: 0 6px 16px rgba(0, 0, 0, 0.45);
    }}
    .cap-in .hl {{
      color: #ffd23f;
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(parts)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(tw)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open("compositions/captions.html", "w").write(out)
print(len(groups), "Gruppen")
