# Baut alle Szenen von Folge 2 (Jeans) aus cues.json und world.json.
# Aufruf: python3 build/build.py   (aus dem Projektordner)
import json, math

C = json.load(open("build/cues.json"))
W = json.load(open("build/world.json"))
P = W["pts"]

STATIONS = [
    # key, Pass-Kürzel, Badge-Text, Karten-Titel, Karten-Fakt, Icon, km der Strecke HIERHER
    ("in", "IN", "Indien", "Indien", "Baumwolle wächst. Tausende Liter Wasser.", "cotton", 0),
    ("cn", "CN", "China", "China", "Aus Baumwolle wird Garn.", "spool", 4772),
    ("tw", "TW", "Taiwan", "Taiwan", "Das Garn wird indigoblau.", "dye", 835),
    ("pl", "PL", "Polen", "Polen", "Garn wird zu Jeansstoff gewebt.", "weave", 8656),
    ("ph", "PH", "Philippinen", "Philippinen", "Die Jeans wird genäht.", "sew", 9508),
    ("gr", "GR", "Griechenland", "Griechenland", "Stonewash: mit Steinen gewaschen.", "stone", 9635),
    ("de", "DE", "Deutschland", "Deutschland", "Endlich im Laden.", "bag", 1799),
]
TOTAL_KM = sum(s[6] for s in STATIONS)
LEG = 1.3  # Sekunden pro Flugstrecke

ICONS = {
    "cotton": '<circle cx="60" cy="96" r="6" fill="#4f8a3a"/><path d="M60 100 L60 60" stroke="#4f8a3a" stroke-width="6"/>'
              '<circle cx="44" cy="48" r="20" fill="#fff"/><circle cx="76" cy="48" r="20" fill="#fff"/><circle cx="60" cy="32" r="20" fill="#fff"/>'
              '<path d="M38 66 L60 58 L82 66" stroke="#6b4b2a" stroke-width="6" fill="none"/>',
    "spool": '<rect x="34" y="18" width="52" height="12" rx="4" fill="#8a5a3b"/><rect x="34" y="90" width="52" height="12" rx="4" fill="#8a5a3b"/>'
             '<rect x="40" y="30" width="40" height="60" fill="#f5f0e6"/><path d="M40 40 L80 36 M40 52 L80 48 M40 64 L80 60 M40 76 L80 72 M40 88 L80 84" stroke="#d8cfbd" stroke-width="3"/>',
    "dye": '<path d="M30 40 L90 40 L82 100 L38 100 Z" fill="#9aa5aa"/><ellipse cx="60" cy="40" rx="30" ry="9" fill="#1f3f8c"/>'
           '<path d="M60 4 C70 20 76 28 60 34 C44 28 50 20 60 4 Z" fill="#2c55b8"/>',
    "weave": '<rect x="22" y="22" width="76" height="76" rx="8" fill="#2c4f86"/>'
             + "".join(f'<path d="M22 {30+i*12} L98 {30+i*12}" stroke="#4b75b5" stroke-width="5"/>' for i in range(6))
             + "".join(f'<path d="M{30+i*12} 22 L{30+i*12} 98" stroke="#1d3b69" stroke-width="3" stroke-dasharray="6 6"/>' for i in range(6)),
    "sew": '<path d="M20 90 L100 90 L100 70 L50 70 L50 40 L90 40 L90 26 L30 26 L30 90 Z" fill="#e9e3d6"/><path d="M80 40 L80 64" stroke="#555" stroke-width="4"/>'
           '<path d="M10 100 Q 40 80 60 100 T 110 100" stroke="#2c4f86" stroke-width="5" fill="none" stroke-dasharray="6 5"/>',
    "stone": '<ellipse cx="40" cy="84" rx="22" ry="14" fill="#9b9b94"/><ellipse cx="78" cy="88" rx="18" ry="12" fill="#b4b3ab"/><ellipse cx="60" cy="66" rx="16" ry="11" fill="#8a8982"/>'
             '<path d="M30 30 C36 42 40 46 30 52 C20 46 24 42 30 30 Z M70 20 C76 32 80 36 70 42 C60 36 64 32 70 20 Z" fill="#6fb6d9"/>',
    "bag": '<path d="M28 44 L92 44 L86 104 L34 104 Z" fill="#ffd23f"/><path d="M44 44 C44 20 76 20 76 44" stroke="#0b1c25" stroke-width="6" fill="none"/>'
           '<path d="M50 60 L50 90 L60 90 L60 76 L70 90 L80 90 L80 60 Z" fill="#2c4f86"/>',
}
FLAGS = {
    "in": '<rect width="120" height="80" fill="#fff"/><rect width="120" height="27" fill="#ff9933"/><rect y="53" width="120" height="27" fill="#138808"/><circle cx="60" cy="40" r="10" fill="none" stroke="#000080" stroke-width="3"/>',
    "cn": '<rect width="120" height="80" fill="#de2910"/><path d="M24 14 L28 26 L16 19 L32 19 L20 26 Z" fill="#ffde00"/>',
    "tw": '<rect width="120" height="80" fill="#fe0000"/><rect width="60" height="40" fill="#000095"/><circle cx="30" cy="20" r="9" fill="#fff"/>',
    "pl": '<rect width="120" height="40" fill="#fff"/><rect y="40" width="120" height="40" fill="#dc143c"/>',
    "ph": '<rect width="120" height="40" fill="#0038a8"/><rect y="40" width="120" height="40" fill="#ce1126"/><path d="M0 0 L60 40 L0 80 Z" fill="#fff"/><circle cx="18" cy="40" r="7" fill="#fcd116"/>',
    "gr": "".join(f'<rect y="{i*80/9:.2f}" width="120" height="{80/9:.2f}" fill="{"#0d5eaf" if i % 2 == 0 else "#fff"}"/>' for i in range(9))
          + '<rect width="44" height="44.4" fill="#0d5eaf"/><rect x="17.6" width="8.8" height="44.4" fill="#fff"/><rect y="17.8" width="44" height="8.8" fill="#fff"/>',
    "de": '<rect width="120" height="27" fill="#111"/><rect y="27" width="120" height="26" fill="#dd0000"/><rect y="53" width="120" height="27" fill="#ffce00"/>',
}

def fmt(x):
    return round(x, 3)

# ---------------- Hook ----------------
def hook():
    g = C["guess"] - C["hook"]
    end = C["intro"] - C["hook"]
    stitch = "".join(f'<path d="M0 {y} L1080 {y+60}" stroke="rgba(255,255,255,0.05)" stroke-width="3"/>' for y in range(-60, 1920, 26))
    return f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; background: linear-gradient(160deg, #2c4f86 0%, #17305a 60%, #0d1c36 100%); }}
    #hk-tex {{ position: absolute; inset: 0; }}
    #hk-jeans-wrap {{ position: absolute; left: 290px; top: 560px; width: 500px; height: 640px; }}
    #hk-title-c, #hk-guess-c {{ position: absolute; inset: 0; }}
    #hk-title {{ position: absolute; left: 0; top: 230px; width: 1080px; text-align: center; color: #fff; font-weight: 900; font-size: 100px; line-height: 1.02; letter-spacing: -0.02em; text-shadow: 0 6px 24px rgba(0,0,0,0.35); }}
    #hk-title .y {{ color: #ffd23f; }}
    #hk-guess {{ position: absolute; left: 140px; top: 300px; width: 800px; padding: 40px 0 46px; border-radius: 40px; background: rgba(11,28,37,0.92); text-align: center; color: #fff; }}
    #hk-guess-km {{ font-weight: 900; font-size: 150px; line-height: 1; color: #ffd23f; font-variant-numeric: tabular-nums; }}
    #hk-guess-sub {{ margin-top: 18px; font-weight: 700; font-size: 52px; }}
  </style>
  <div id="root" data-composition-id="hook" data-width="1080" data-height="1920">
    <svg id="hk-tex" viewBox="0 0 1080 1920">{stitch}</svg>
    <div id="hk-jeans-wrap">
      <svg viewBox="0 0 500 640" width="500" height="640">
        <ellipse cx="250" cy="625" rx="230" ry="16" fill="rgba(0,0,0,0.3)"/>
        <path d="M70 20 L430 20 L470 610 L290 610 L250 250 L210 610 L30 610 Z" fill="#3e6db3"/>
        <path d="M70 20 L430 20 L434 80 L66 80 Z" fill="#2f5896"/>
        <path d="M250 80 L250 240" stroke="#f0b33c" stroke-width="5" stroke-dasharray="10 8"/>
        <path d="M90 110 C150 150 190 140 230 100 M410 110 C350 150 310 140 270 100" stroke="#f0b33c" stroke-width="5" fill="none" stroke-dasharray="10 8"/>
        <path d="M66 80 L434 80" stroke="#f0b33c" stroke-width="5" stroke-dasharray="10 8"/>
        <circle cx="250" cy="52" r="12" fill="#c9a24a"/>
        <rect x="110" y="16" width="22" height="70" rx="6" fill="#2f5896"/><rect x="368" y="16" width="22" height="70" rx="6" fill="#2f5896"/>
        <path d="M60 470 L210 480 M440 470 L290 480" stroke="rgba(255,255,255,0.25)" stroke-width="40"/>
      </svg>
    </div>
    <div id="hk-title-c" class="clip" data-start="0" data-duration="{fmt(g)}"><h1 id="hk-title">Deine Jeans ist<br/><span class="y">weiter gereist</span><br/>als du.</h1></div>
    <div id="hk-guess-c" class="clip" data-start="{fmt(g)}" data-duration="{fmt(end-g)}"><div id="hk-guess"><div id="hk-guess-km">??? km</div><div id="hk-guess-sub">Schätz mal! &#8595;</div></div></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#hk-jeans-wrap", {{ y: 40, rotation: -2 }}, {{ y: 0, rotation: 2, duration: {fmt(g)}, ease: "sine.inOut" }}, 0);
    tl.fromTo("#hk-title", {{ scale: 1 }}, {{ scale: 1.04, duration: {fmt(g-0.1)}, ease: "none" }}, 0);
    tl.to("#hk-jeans-wrap", {{ scale: 0.82, y: 160, duration: 0.5, ease: "power3.out" }}, {fmt(g)});
    tl.fromTo("#hk-guess", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {fmt(g)});
    const seq = ["???", "5.1??", "1?.???", "2?.0??", "4?.???", "???"];
    const km = document.querySelector("#hk-guess-km");
    const st = {{ i: 0 }};
    tl.fromTo(st, {{ i: 0 }}, {{ i: seq.length - 1, duration: 2.2, ease: "none", onUpdate: () => {{ km.textContent = seq[Math.round(st.i)] + " km"; }} }}, {fmt(g+0.8)});
    tl.fromTo("#hk-guess-sub", {{ y: 0 }}, {{ y: 14, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: 7 }}, {fmt(g+0.4)});
    tl.to("#hk-guess", {{ opacity: 0, duration: 0.2 }}, {fmt(end-0.25)});
    window.__timelines["hook"] = tl;
  </script>
</template>
'''

# ---------------- Weltkarte ----------------
def leg_path(a, b):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    if ny > 0:
        nx, ny = -nx, -ny
    k = 0.28 * L
    return f"M{a[0]} {a[1]} Q{mx + nx*k:.1f} {my + ny*k:.1f} {b[0]} {b[1]}"

def welt():
    t0 = C["intro"]
    dur = C["payoff"] - t0
    st_t = [s - t0 for s in C["stations"]]
    legs, pins, cards, tw = [], [], [], []
    for i, (k, code, badge, title, fact, icon, km) in enumerate(STATIONS):
        x, y = P[i]
        pins.append(f'<g id="w-pin-{k}" transform="translate({x} {y})"><circle r="10" fill="#ff5a3a" stroke="#fff" stroke-width="4"/></g>')
        if i > 0:
            legs.append(f'<path id="w-leg-{k}" d="{leg_path(P[i-1], P[i])}" fill="none" stroke="#ffd23f" stroke-width="7" stroke-linecap="round" pathLength="100" stroke-dasharray="100 120" stroke-dashoffset="100"/>')
        nxt = st_t[i + 1] if i + 1 < len(st_t) else dur
        arrive = st_t[i] + (LEG if i > 0 else 0.2)
        cards.append(f'''    <div id="w-card-{k}-c" class="clip w-card-c" data-start="{fmt(arrive)}" data-duration="{fmt(nxt - arrive)}">
      <div class="w-card"><svg viewBox="0 0 120 120" width="150" height="150"><circle cx="60" cy="60" r="58" fill="#cfe0f2"/>{ICONS[icon]}</svg><div><b>{title}</b><span>{fact}</span></div></div>
    </div>''')
    # Kamera: auf Station zoomen, für die Strecke herauszoomen
    S = 1.55
    HOME = '{ x: 0, y: 0, s: 1 }'
    def cam(i):
        x, y = P[i]
        return f'{{ x: {fmt(540 - S*x)}, y: {fmt(760 - S*y)}, s: {S} }}'
    tw.append(f'tl.fromTo("#w-preview", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6 }}, 0.3);')
    tw.append(f'tl.fromTo("#w-tag", {{ y: -30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, 0.2);')
    tw.append(f'tl.to("#w-preview", {{ opacity: 0, duration: 0.4 }}, {fmt(st_t[0] - 0.3)});')
    tw.append(f'tl.to("#w-tag", {{ opacity: 0, duration: 0.3 }}, {fmt(st_t[0] - 0.3)});')
    cum = 0
    for i, (k, code, *_rest) in enumerate(STATIONS):
        km = STATIONS[i][6]
        t = st_t[i]
        if i == 0:
            tw.append(f'tl.fromTo(cam, {HOME}, {{ ...{cam(0)}, duration: 0.9, ease: "power2.inOut", immediateRender: false, onUpdate: camSet }}, {fmt(t)});')
            tw.append(f'tl.fromTo("#w-c-{k}", {{ fill: "#e9dcc0" }}, {{ fill: "#f3b33d", duration: 0.3 }}, {fmt(t+0.2)});')
            tw.append(f'tl.fromTo("#w-pkg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {fmt(t+0.2)});')
            continue
        tw.append(f'tl.fromTo(cam, {cam(i-1)}, {{ ...{HOME}, duration: 0.45, ease: "power2.inOut", immediateRender: false, onUpdate: camSet }}, {fmt(t)});')
        tw.append(f'tl.fromTo("#w-leg-{k}", {{ attr: {{ "stroke-dashoffset": 100 }} }}, {{ attr: {{ "stroke-dashoffset": 0 }}, duration: {LEG-0.1}, ease: "power1.inOut" }}, {fmt(t+0.1)});')
        tw.append(f'tl.fromTo("#w-pkg", {{ motionPath: {{ path: "#w-leg-{k}", align: "#w-leg-{k}", alignOrigin: [0.5, 0.5], start: 0, end: 0 }} }}, {{ motionPath: {{ path: "#w-leg-{k}", align: "#w-leg-{k}", alignOrigin: [0.5, 0.5], start: 0, end: 1 }}, duration: {LEG-0.1}, ease: "power1.inOut", immediateRender: false }}, {fmt(t+0.1)});')
        tw.append(f'tl.fromTo(km, {{ v: {cum} }}, {{ v: {cum+km}, duration: {LEG-0.1}, ease: "power1.inOut", immediateRender: false, onUpdate: showKm }}, {fmt(t+0.1)});')
        tw.append(f'tl.fromTo("#w-c-{k}", {{ fill: "#e9dcc0" }}, {{ fill: "#f3b33d", duration: 0.3 }}, {fmt(t+LEG)});')
        tw.append(f'tl.fromTo(cam, {HOME}, {{ ...{cam(i)}, duration: 0.6, ease: "power2.inOut", immediateRender: false, onUpdate: camSet }}, {fmt(t+LEG)});')
        cum += km
    tw.append(f'tl.fromTo(cam, {cam(len(STATIONS)-1)}, {{ ...{HOME}, duration: 0.8, ease: "power2.inOut", immediateRender: false, onUpdate: camSet }}, {fmt(dur-1.0)});')
    preview = " ".join(leg_path(P[i-1], P[i]) for i in range(1, len(P)))
    nums = "".join(f'<text x="{P[i][0]}" y="{P[i][1]-20}" text-anchor="middle" class="w-num">{i+1}</text>' for i in range(len(P)))
    return f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; background: #0f3a4b; }}
    #w-map {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #w-map .land {{ fill: #e9dcc0; stroke: #cdbd9c; stroke-width: 0.8; }}
    .w-num {{ font-family: "Inter"; font-weight: 900; font-size: 30px; fill: #fff; paint-order: stroke; stroke: #0f3a4b; stroke-width: 6px; }}
    #w-km {{ position: absolute; left: 60px; top: 290px; color: #fff; -webkit-text-stroke: 10px #0b1c25; paint-order: stroke fill; font-weight: 900; font-size: 104px; line-height: 1; font-variant-numeric: tabular-nums; text-shadow: 0 6px 20px rgba(0,0,0,0.4); }}
    #w-km small {{ font-size: 52px; color: #ffd23f; -webkit-text-stroke: 8px #0b1c25; paint-order: stroke fill; }}
    #w-tag {{ position: absolute; left: 0; top: 300px; width: 1080px; text-align: center; }}
    #w-tag span {{ display: inline-block; padding: 14px 30px; border-radius: 999px; background: #ffd23f; color: #0b1c25; font-weight: 900; font-size: 46px; letter-spacing: 0.06em; }}
    .w-card-c {{ position: absolute; inset: 0; }}
    .w-card {{ position: absolute; left: 70px; top: 930px; width: 840px; padding: 18px 26px; border-radius: 30px; background: rgba(255,255,255,0.96); display: flex; align-items: center; gap: 22px; box-shadow: 0 16px 40px rgba(0,0,0,0.35); }}
    .w-card b {{ display: block; font-weight: 900; font-size: 54px; color: #0b1c25; }}
    .w-card span {{ display: block; font-weight: 700; font-size: 38px; color: #2c4f86; line-height: 1.15; }}
  </style>
  <div id="root" data-composition-id="welt" data-width="1080" data-height="1920">
    <svg id="w-map" viewBox="0 0 1080 1920">
      <g id="w-cam">
        {W["land"]}
        <g id="w-preview" fill="none" stroke="rgba(255,255,255,0.75)" stroke-width="4" stroke-dasharray="8 10"><path d="{preview}"/>{nums}</g>
        {"".join(legs)}
        {"".join(pins)}
        <g id="w-pkg" transform="translate({P[0][0]} {P[0][1]})"><g transform="translate(-22 -18)"><rect width="44" height="36" rx="6" fill="#2c4f86" stroke="#fff" stroke-width="4"/><path d="M14 0 L14 36 M30 0 L30 36" stroke="#ffd23f" stroke-width="3"/></g></g>
      </g>
    </svg>
    <div id="w-tag"><span>BEISPIELROUTE</span></div>
    <div id="w-km" data-layout-allow-occlusion><span id="w-km-n">0</span> <small>km</small></div>
{chr(10).join(cards)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const kmEl = document.querySelector("#w-km-n");
    const km = {{ v: 0 }};
    const showKm = () => (kmEl.textContent = Math.round(km.v).toLocaleString("de-DE"));
    const camEl = document.querySelector("#w-cam");
    const cam = {{ x: 0, y: 0, s: 1 }};
    const camSet = () => camEl.setAttribute("transform", `translate(${{cam.x}} ${{cam.y}}) scale(${{cam.s}})`);
    tl.call(() => {{ cam.x = 0; cam.y = 0; cam.s = 1; camSet(); }}, null, 0);
    {chr(10).join("    " + t for t in tw)}
    tl.fromTo("#w-km", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, {fmt(st_t[0])});
''' + "".join(
        f'    tl.fromTo("#w-card-{s[0]}-c .w-card", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.6)" }}, {fmt(st_t[i] + (LEG if i else 0.2))});\n'
        for i, s in enumerate(STATIONS)) + '''    window.__timelines["welt"] = tl;
  </script>
</template>
'''

# ---------------- HUD ----------------
def hud():
    t0 = C["stations"][0]
    dur = C["payoff"] - t0
    st = [s - t0 for s in C["stations"]] + [dur]
    badges, tw, slots = [], [], []
    for i, s in enumerate(STATIONS):
        badges.append(f'    <div id="hud-st{i+1}" class="clip hud-st" data-start="{fmt(st[i])}" data-duration="{fmt(st[i+1]-st[i])}"><div class="hud-badge"><b>STATION {i+1}/7</b><span>{s[2]}</span></div></div>')
        tw.append(f'    tl.fromTo("#hud-st{i+1} .hud-badge", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.25, ease: "power3.out" }}, {fmt(st[i])});')
        stamp_t = st[i] + (LEG if i else 0.3)
        tw.append(f'    tl.fromTo("#hud-stamp-{s[0]}", {{ opacity: 0, scale: 2.2, rotation: -25 }}, {{ opacity: 1, scale: 1, rotation: -10, duration: 0.16, ease: "power4.in" }}, {fmt(stamp_t)});')
        slots.append(f'<div class="hud-slot"><div id="hud-stamp-{s[0]}" class="hud-stamp">{s[1]}</div></div>')
    return f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; font-family: "Inter", sans-serif; pointer-events: none; }}
    .hud-st {{ position: absolute; inset: 0; }}
    .hud-badge {{ position: absolute; left: 60px; top: 190px; padding: 12px 22px; border-radius: 18px; background: rgba(11,28,37,0.9); color: #fff; display: flex; flex-direction: column; gap: 2px; }}
    .hud-badge b {{ font-weight: 900; font-size: 32px; color: #ffd23f; letter-spacing: 0.08em; }}
    .hud-badge span {{ font-weight: 700; font-size: 32px; }}
    #hud-pass {{ position: absolute; left: 600px; top: 190px; width: 420px; padding: 12px 16px 16px; border-radius: 18px; background: #7a1f2b; box-shadow: 0 8px 24px rgba(0,0,0,0.35); }}
    #hud-pass-t {{ color: #f3d48a; font-weight: 900; font-size: 28px; letter-spacing: 0.1em; margin-bottom: 10px; }}
    #hud-slots {{ display: flex; flex-wrap: wrap; gap: 10px; }}
    .hud-slot {{ width: 86px; height: 52px; border-radius: 12px; background: #f6ecd6; display: flex; align-items: center; justify-content: center; }}
    .hud-stamp {{ width: 80px; height: 46px; border-radius: 10px; border: 4px solid #2c4f86; color: #2c4f86; background: #fffaf0; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 28px; opacity: 0; }}
  </style>
  <div id="root" data-composition-id="hud" data-width="1080" data-height="1920">
{chr(10).join(badges)}
    <div id="hud-pass"><div id="hud-pass-t">REISEPASS &middot; JEANS</div><div id="hud-slots">{"".join(slots)}</div></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#hud-pass", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, 0);
{chr(10).join(tw)}
    tl.to("#hud-pass", {{ opacity: 0, duration: 0.3 }}, {fmt(dur-0.4)});
    window.__timelines["hud"] = tl;
  </script>
</template>
'''

# ---------------- Auflösung ----------------
def payoff():
    t0 = C["payoff"]
    dur = C["outro"] - t0
    tL = C["laender"] - t0
    tE = C["echt"] - t0
    tW = C["erde"] - t0
    flags = "".join(f'<svg class="pay-flag" viewBox="0 0 120 80" width="96" height="64">{FLAGS[s[0]]}</svg>' for s in STATIONS)
    return f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; background: radial-gradient(circle at 50% 35%, #1d3f70 0%, #0b1530 70%); color: #fff; }}
    #pay-top {{ position: absolute; left: 0; top: 300px; width: 1080px; text-align: center; }}
    #pay-big {{ font-weight: 900; font-size: 170px; line-height: 1; color: #ffd23f; font-variant-numeric: tabular-nums; }}
    #pay-lbl {{ font-weight: 700; font-size: 48px; margin-top: 6px; }}
    #pay-l {{ position: absolute; left: 0; top: 590px; width: 1080px; text-align: center; }}
    #pay-l b {{ font-weight: 900; font-size: 96px; }}
    .pay-flags {{ display: flex; justify-content: center; gap: 14px; margin-top: 20px; }}
    .pay-flag {{ border-radius: 8px; box-shadow: 0 6px 16px rgba(0,0,0,0.35); }}
    #pay-bars-c {{ position: absolute; inset: 0; }}
    #pay-bars {{ position: absolute; left: 90px; top: 830px; width: 900px; }}
    .pay-bar {{ margin-bottom: 30px; }}
    .pay-bar b {{ display: block; font-weight: 900; font-size: 44px; margin-bottom: 10px; }}
    .pay-track {{ height: 64px; border-radius: 16px; background: rgba(255,255,255,0.12); overflow: hidden; }}
    .pay-fill {{ height: 100%; border-radius: 16px; transform-origin: 0 50%; }}
    #pay-fill-j {{ width: 100%; background: linear-gradient(90deg, #3e6db3, #6fa0e8); }}
    #pay-fill-e {{ width: 80%; background: linear-gradient(90deg, #2f9e6b, #6fd6a0); }}
  </style>
  <div id="root" data-composition-id="payoff" data-width="1080" data-height="1920">
    <div id="pay-top"><div id="pay-big"><span id="pay-km">0</span> km</div><div id="pay-lbl">in Luftlinie</div></div>
    <div id="pay-l"><b>7 Länder</b><div class="pay-flags">{flags}</div></div>
    <div id="pay-bars-c" class="clip" data-start="{fmt(tE)}" data-duration="{fmt(dur-tE)}">
      <div id="pay-bars">
        <div class="pay-bar" id="pay-bar-j"><b>Jeans, echte Wege: bis 50.000 km</b><div class="pay-track"><div class="pay-fill" id="pay-fill-j"></div></div></div>
        <div class="pay-bar" id="pay-bar-e"><b>Einmal um die Erde: 40.000 km</b><div class="pay-track"><div class="pay-fill" id="pay-fill-e"></div></div></div>
      </div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    const kmEl = document.querySelector("#pay-km");
    const k = {{ v: 0 }};
    tl.fromTo("#pay-top", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, 0.1);
    tl.fromTo(k, {{ v: 0 }}, {{ v: {TOTAL_KM}, duration: 1.5, ease: "power2.out", onUpdate: () => (kmEl.textContent = Math.round(k.v).toLocaleString("de-DE")) }}, 0.1);
    tl.fromTo("#pay-l b", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {fmt(tL)});
    tl.fromTo(".pay-flag", {{ opacity: 0, scale: 0.3 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2.4)", stagger: 0.1 }}, {fmt(tL+0.15)});
    tl.fromTo("#pay-bar-j", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {fmt(tE)});
    tl.fromTo("#pay-fill-j", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.4, ease: "power2.out" }}, {fmt(tE+0.2)});
    tl.fromTo("#pay-bar-e", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {fmt(tW)});
    tl.fromTo("#pay-fill-e", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 1.2, ease: "power2.out" }}, {fmt(tW+0.15)});
    window.__timelines["payoff"] = tl;
  </script>
</template>
'''

# ---------------- Schluss ----------------
def outro():
    t0 = C["outro"]
    dur = C["end"] - t0
    tb = C["baecker"] - t0
    tt = C["teaser"] - t0
    ta = C["ask"] - t0
    return f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: "Inter", sans-serif; color: #fff; }}
    #o-a-c, #o-t-c, #o-ask-c {{ position: absolute; inset: 0; }}
    #o-a {{ position: absolute; inset: 0; background: linear-gradient(180deg, #f7d9a8 0%, #f1c47e 100%); }}
    #o-globe {{ position: absolute; left: 290px; top: 560px; width: 500px; height: 500px; }}
    #o-line {{ position: absolute; left: 0; top: 260px; width: 1080px; text-align: center; font-weight: 900; font-size: 86px; line-height: 1.05; color: #0b1c25; }}
    #o-line2 {{ color: #b0461b; }}
    #o-roll {{ position: absolute; left: 640px; top: 900px; width: 260px; height: 170px; }}
    #o-t {{ position: absolute; inset: 0; background: radial-gradient(circle at 50% 48%, #2d4a1e 0%, #0b1c25 62%); }}
    #o-banana {{ position: absolute; left: 290px; top: 500px; width: 500px; height: 500px; }}
    #o-morgen {{ position: absolute; left: 0; top: 250px; width: 1080px; text-align: center; font-weight: 900; font-size: 70px; letter-spacing: 0.14em; color: #ffd23f; }}
    #o-brand {{ position: absolute; left: 0; top: 360px; width: 1080px; text-align: center; font-weight: 700; font-size: 40px; letter-spacing: 0.1em; color: rgba(255,255,255,0.75); }}
    #o-ask {{ position: absolute; left: 110px; top: 700px; width: 860px; padding: 28px 30px; border-radius: 34px 34px 34px 6px; background: #fff; color: #0b1c25; text-align: center; font-weight: 900; font-size: 58px; line-height: 1.1; }}
  </style>
  <div id="root" data-composition-id="outro" data-width="1080" data-height="1920">
    <div id="o-a-c" class="clip" data-start="0" data-duration="{fmt(tt)}">
      <div id="o-a"></div>
      <svg id="o-globe" viewBox="0 0 500 500">
        <circle cx="250" cy="250" r="200" fill="#2f86b3"/>
        <path d="M120 150 C170 110 230 130 220 190 C210 240 150 230 130 280 C110 320 70 260 80 210 Z M290 120 C350 110 410 160 400 220 C380 260 330 240 300 270 C270 300 300 350 260 380 C230 330 250 280 240 230 C230 180 250 130 290 120 Z" fill="#7cc35a"/>
        <g id="o-orbit"><ellipse cx="250" cy="250" rx="240" ry="80" fill="none" stroke="#ffd23f" stroke-width="6" stroke-dasharray="14 12" transform="rotate(-18 250 250)"/></g>
        <g id="o-mini" transform="translate(470 180)"><path d="M-22 -30 L22 -30 L28 30 L4 30 L0 -2 L-4 30 L-28 30 Z" fill="#2c4f86" stroke="#fff" stroke-width="4"/></g>
      </svg>
      <svg id="o-roll" viewBox="0 0 260 170"><path d="M10 120 C10 30 250 30 250 120 C250 160 10 160 10 120 Z" fill="#d9903e"/><path d="M60 70 L90 110 M120 60 L130 110 M180 70 L170 110" stroke="#f5d39c" stroke-width="8" stroke-linecap="round"/></svg>
      <div id="o-line"><div id="o-line1">Einmal um die Welt.</div><div id="o-line2">Und du trägst sie zum Bäcker.</div></div>
    </div>
    <div id="o-t-c" class="clip" data-start="{fmt(tt)}" data-duration="{fmt(dur-tt)}">
      <div id="o-t"></div>
      <div id="o-morgen">MORGEN</div>
      <div id="o-brand">DIE REISE VON &hellip; &middot; FOLGE 3</div>
      <svg id="o-banana" viewBox="0 0 500 500"><path d="M90 140 C120 360 330 430 430 330 C450 310 440 290 420 300 C330 360 190 300 150 130 C145 110 95 110 90 140 Z" fill="#0d1a0f" stroke="#9be564" stroke-width="7"/><path d="M95 135 L80 100 L112 110 Z" fill="#0d1a0f" stroke="#9be564" stroke-width="6"/></svg>
    </div>
    <div id="o-ask-c" class="clip" data-start="{fmt(ta)}" data-duration="{fmt(dur-ta)}">
      <div id="o-ask">Was soll als Nächstes reisen?<br/>Schreib's in die Kommentare!</div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#o-line1", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0.15);
    tl.fromTo("#o-globe", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }}, 0.1);
    tl.fromTo("#o-mini", {{ rotation: 0, svgOrigin: "250 250" }}, {{ rotation: -360, svgOrigin: "250 250", duration: {fmt(max(tt, 1))}, ease: "none" }}, 0);
    tl.fromTo("#o-line2", {{ opacity: 0, scale: 0.6 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)" }}, {fmt(tb)});
    tl.fromTo("#o-roll", {{ y: 200, opacity: 0, rotation: -20 }}, {{ y: 0, opacity: 1, rotation: 0, duration: 0.45, ease: "back.out(1.8)" }}, {fmt(tb)});
    tl.fromTo("#o-banana", {{ opacity: 0, scale: 0.85 }}, {{ opacity: 1, scale: 1, duration: 0.8, ease: "power2.out" }}, {fmt(tt+0.1)});
    tl.fromTo("#o-banana", {{ filter: "drop-shadow(0 0 0px #9be564)" }}, {{ filter: "drop-shadow(0 0 40px #9be564)", duration: 1.5, ease: "sine.inOut", yoyo: true, repeat: 3, immediateRender: false }}, {fmt(tt+0.9)});
    tl.fromTo("#o-morgen", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }}, {fmt(tt+0.1)});
    tl.fromTo("#o-brand", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {fmt(tt+0.6)});
    tl.fromTo("#o-ask", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "back.out(1.6)" }}, {fmt(ta)});
    window.__timelines["outro"] = tl;
  </script>
</template>
'''

# ---------------- Hauptdatei ----------------
def index():
    end = C["end"]
    def host(id_, a, b, z, track, kind="graphics"):
        return (f'      <div id="{id_}" data-composition-id="{id_}" data-composition-src="compositions/{id_}.html"\n'
                f'        data-start="{fmt(a)}" data-duration="{fmt(b-a)}" data-track-index="{track}" data-track-kind="{kind}"\n'
                f'        data-width="1080" data-height="1920" style="z-index: {z}"></div>')
    hosts = [host("hook", 0, C["intro"], 1, 1), host("welt", C["intro"], C["payoff"], 1, 1),
             host("payoff", C["payoff"], C["outro"], 1, 1), host("outro", C["outro"], end, 1, 1),
             host("hud", C["stations"][0], C["payoff"], 5, 3), host("captions", 0, end, 10, 4, "captions")]
    sfx = [("hook", "impact-bass-1", 0.05, 0.35), ("guess", "pop", C["guess"] + 0.05, 0.35), ("cut1", "whoosh-short", C["intro"] - 0.05, 0.3)]
    for i, s in enumerate(C["stations"]):
        if i:
            sfx.append((f"leg{i}", "whoosh" if i % 2 else "whoosh-short", s + 0.1, 0.25))
        sfx.append((f"stamp{i}", "pop", s + (LEG if i else 0.3) + 0.05, 0.35))
    sfx += [("riser", "riser", C["payoff"] - 10.03 + 0.1, 0.22), ("payoff", "impact-bass-1", C["payoff"] + 0.15, 0.4),
            ("erde", "impact-bass-1", C["erde"] + 0.2, 0.3), ("cut2", "whoosh", C["outro"] - 0.05, 0.3), ("teaser", "whoosh-short", C["teaser"] - 0.05, 0.3)]
    dur = {"pop": 0.72, "whoosh": 0.57, "whoosh-short": 0.57, "impact-bass-1": 2.12, "riser": 10.03}
    tracks = {}
    lines = []
    for name, f, t, v in sorted(sfx, key=lambda x: x[2]):
        tr = 6
        while tracks.get(tr, -1) > t:
            tr += 1
        tracks[tr] = t + dur[f]
        lines.append(f'      <audio id="sfx-{name}" class="clip" src="assets/sfx/{f}.mp3" data-start="{fmt(t)}" data-duration="{dur[f]}" data-track-index="{tr}" data-volume="{v}"></audio>')
    voice = (f'      <audio id="voice" class="clip" src="assets/voice.mp3" data-start="0" data-duration="{C["voice_len"]}" data-track-index="5" data-volume="1"></audio>'
             if C.get("voice_len") else "      <!-- Stimme fehlt noch -->")
    return f'''<!doctype html>
<html lang="de" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/gsap.min.js"></script>
    <script src="assets/MotionPathPlugin.min.js"></script>
    <script>gsap.registerPlugin(MotionPathPlugin);</script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b1c25; }}
      #root {{ position: relative; width: 100%; height: 100%; font-family: "Inter", sans-serif; }}
      #root > div {{ position: absolute; inset: 0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{fmt(end)}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
{voice}
{chr(10).join(lines)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''

for name, fn in [("hook", hook), ("welt", welt), ("hud", hud), ("payoff", payoff), ("outro", outro)]:
    open(f"compositions/{name}.html", "w").write(fn())
open("index.html", "w").write(index())
print("Szenen gebaut, Gesamt-km:", TOTAL_KM)
