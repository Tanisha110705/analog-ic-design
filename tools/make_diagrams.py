#!/usr/bin/env python3
"""Generate the conceptual SVG diagrams in assets/.

These are hand-drawn-style schematic redraws and flow charts. They are NOT
simulation output. Device values printed on them are copied from the
Cadence schematics / hand calculations documented in docs/.
Run:  python3 tools/make_diagrams.py
"""
import os
from xml.sax.saxutils import escape

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
FONT = "Helvetica, Arial, sans-serif"
INK = "#1f2933"
MUTED = "#52606d"
ACCENT = "#0b6bcb"
WARN = "#b44d12"
FILL = "#eef4fb"
FILL2 = "#fdf3e7"
GREEN = "#2f7d4f"


class SVG:
    def __init__(self, w, h, title):
        self.w, self.h = w, h
        self.items = []
        self.title = title

    def add(self, s):
        self.items.append(s)

    def line(self, x1, y1, x2, y2, w=2, color=INK, dash=None, arrow=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = ' marker-end="url(#arr)"' if arrow else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{w}"{d}{m}/>')

    def poly(self, pts, w=2, color=INK, fill="none", arrow=False):
        p = " ".join(f"{x},{y}" for x, y in pts)
        m = ' marker-end="url(#arr)"' if arrow else ""
        self.add(f'<polyline points="{p}" fill="{fill}" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"{m}/>')

    def text(self, x, y, s, size=13, anchor="start", color=INK, weight="normal", italic=False):
        st = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{color}" '
                 f'text-anchor="{anchor}" font-weight="{weight}"{st}>{escape(s)}</text>')

    def rect(self, x, y, w, h, fill=FILL, stroke=ACCENT, rx=8, sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def dot(self, x, y, r=3.5):
        self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>')

    def box(self, x, y, w, h, lines, fill=FILL, stroke=ACCENT, size=14, bold_first=True):
        self.rect(x, y, w, h, fill=fill, stroke=stroke)
        n = len(lines)
        lh = size + 5
        y0 = y + h / 2 - (n - 1) * lh / 2 + size / 3
        for i, s in enumerate(lines):
            self.text(x + w / 2, y0 + i * lh, s, size=size if i == 0 else size - 2,
                      anchor="middle", weight="bold" if (i == 0 and bold_first) else "normal",
                      color=INK if i == 0 else MUTED)

    # ---- circuit primitives -------------------------------------------------
    # dir=+1: gate on the left, drain/source legs on the right; dir=-1 mirrors it.
    def _label(self, x, y, dir, label, sub):
        if not label:
            return
        lx = x + dir * 32
        an = "start" if dir > 0 else "end"
        self.text(lx, y - 2, label, size=13, anchor=an, weight="bold")
        if sub:
            self.text(lx, y + 14, sub, size=11, anchor=an, color=MUTED)

    def nmos(self, x, y, label=None, sub=None, dir=1):
        """Drain on top, source at the bottom. Returns terminal coordinates."""
        lx = x + dir * 22
        self.line(x, y - 20, x, y + 20, w=3)
        self.line(x - dir * 9, y - 16, x - dir * 9, y + 16, w=2)
        self.line(x - dir * 34, y, x - dir * 9, y)
        self.poly([(x, y - 14), (lx, y - 14), (lx, y - 42)])
        self.poly([(x, y + 14), (lx, y + 14), (lx, y + 42)])
        tip, base = x + dir * 18, x + dir * 10
        self.add(f'<polygon points="{tip},{y+14} {base},{y+9} {base},{y+19}" fill="{INK}"/>')
        self._label(lx, y, dir, label, sub)
        return {"g": (x - dir * 34, y), "d": (lx, y - 42), "s": (lx, y + 42)}

    def pmos(self, x, y, label=None, sub=None, dir=1):
        """Source on top, drain at the bottom."""
        lx = x + dir * 22
        self.line(x, y - 20, x, y + 20, w=3)
        self.line(x - dir * 9, y - 16, x - dir * 9, y + 16, w=2)
        self.add(f'<circle cx="{x - dir * 13}" cy="{y}" r="4" fill="white" stroke="{INK}" stroke-width="1.8"/>')
        self.line(x - dir * 34, y, x - dir * 17, y)
        self.poly([(x, y - 14), (lx, y - 14), (lx, y - 42)])
        self.poly([(x, y + 14), (lx, y + 14), (lx, y + 42)])
        tip, base = x + dir * 8, x + dir * 16
        self.add(f'<polygon points="{tip},{y-14} {base},{y-19} {base},{y-9}" fill="{INK}"/>')
        self._label(lx, y, dir, label, sub)
        return {"g": (x - dir * 34, y), "s": (lx, y - 42), "d": (lx, y + 42)}

    def resistor(self, x, y1, y2, label=None, sub=None):
        h = y2 - y1
        a, b = y1 + h * 0.2, y2 - h * 0.2
        pts = [(x, y1), (x, a)]
        n = 6
        for i in range(n):
            yy = a + (b - a) * (i + 0.5) / n
            pts.append((x + (9 if i % 2 == 0 else -9), yy))
        pts += [(x, b), (x, y2)]
        self.poly(pts)
        if label:
            self.text(x + 16, (y1 + y2) / 2 - 2, label, size=13, weight="bold")
            if sub:
                self.text(x + 16, (y1 + y2) / 2 + 14, sub, size=11, color=MUTED)

    def cap(self, x, y1, y2, label=None):
        m = (y1 + y2) / 2
        self.line(x, y1, x, m - 5)
        self.line(x - 14, m - 5, x + 14, m - 5, w=2.5)
        self.line(x - 14, m + 5, x + 14, m + 5, w=2.5)
        self.line(x, m + 5, x, y2)
        if label:
            self.text(x + 20, m + 5, label, size=13, weight="bold")

    def gnd(self, x, y):
        self.line(x, y, x, y + 8)
        self.line(x - 12, y + 8, x + 12, y + 8)
        self.line(x - 7, y + 13, x + 7, y + 13)
        self.line(x - 3, y + 18, x + 3, y + 18)

    def vdd(self, x1, x2, y, label="VDD = 1.8 V"):
        self.line(x1, y, x2, y, w=2.5)
        self.text((x1 + x2) / 2, y - 8, label, size=13, anchor="middle", weight="bold")

    def isrc(self, x, y1, y2, label=None, down=True):
        m = (y1 + y2) / 2
        self.line(x, y1, x, m - 16)
        self.line(x, m + 16, x, y2)
        self.add(f'<circle cx="{x}" cy="{m}" r="16" fill="white" stroke="{INK}" stroke-width="2"/>')
        if down:
            self.line(x, m - 9, x, m + 7, arrow=True)
        else:
            self.line(x, m + 9, x, m - 7, arrow=True)
        if label:
            self.text(x - 24, m + 5, label, size=13, anchor="end", weight="bold")

    def vsrc(self, x, y1, y2, label=None, sub=None, ac=False, label_left=True):
        m = (y1 + y2) / 2
        self.line(x, y1, x, m - 16)
        self.line(x, m + 16, x, y2)
        self.add(f'<circle cx="{x}" cy="{m}" r="16" fill="white" stroke="{INK}" stroke-width="2"/>')
        if ac:
            self.add(f'<path d="M{x-9},{m} q4.5,-9 9,0 t9,0" fill="none" stroke="{INK}" stroke-width="1.6"/>')
        else:
            self.text(x, m - 3, "+", size=12, anchor="middle")
            self.text(x, m + 11, "−", size=12, anchor="middle")
        if label:
            an = "end" if label_left else "start"
            lx = x - 24 if label_left else x + 24
            self.text(lx, m - 1, label, size=13, anchor=an, weight="bold")
            if sub:
                self.text(lx, m + 15, sub, size=11, anchor=an, color=MUTED)

    def save(self, name, footer=None):
        if footer:
            self.text(self.w / 2, self.h - 12, footer, size=11, anchor="middle", color=MUTED, italic=True)
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
                f'viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{escape(self.title)}">\n'
                f'<title>{escape(self.title)}</title>\n'
                f'<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
                f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>\n'
                f'<rect width="100%" height="100%" fill="#ffffff"/>\n')
        with open(os.path.join(OUT, name), "w") as f:
            f.write(head + "\n".join(self.items) + "\n</svg>\n")


def vflow(s, x, y, w, h, gap, steps, fills=None):
    for i, st in enumerate(steps):
        yy = y + i * (h + gap)
        s.box(x, yy, w, h, st, fill=(fills[i] if fills else FILL))
        if i < len(steps) - 1:
            s.line(x + w / 2, yy + h, x + w / 2, yy + h + gap - 2, arrow=True)


# ---------------------------------------------------------------------------
def analog_design_flow():
    s = SVG(900, 760, "Analog design flow used across the studies")
    s.text(450, 34, "Analog Design Flow", size=20, anchor="middle", weight="bold")
    s.text(450, 56, "Device data first, circuit second: every sizing decision is read from a simulated characteristic",
           size=12, anchor="middle", color=MUTED)
    steps = [
        ["MOSFET characterization", "DC sweeps of VGS / VDS on a single device"],
        ["Select operating region", "inversion level via gm/Id"],
        ["Choose gm/Id", "from gain / bandwidth / current budget"],
        ["Determine W and bias", "VGS from gm/Id–VGS, W from Id/W"],
        ["Build the circuit", "Virtuoso schematic"],
        ["DC analysis", "bias current, transfer curve, Iout–Vout"],
        ["AC / pole-zero analysis", "gain magnitude, f−3dB, poles"],
        ["Evaluate gain / bandwidth / current", "compare with the hand calculation"],
        ["Trade-off analysis", "headroom, output resistance, speed"],
    ]
    vflow(s, 60, 80, 380, 56, 18, steps)
    notes = [
        ("PMOS: Id–VGS, Id–VDS, gm, Cgs, Vdsat, Vth, gm/Id, fT", 0),
        ("NMOS gm/Id + Id/W sweeps per design", 1),
        ("CS: 5.34 V⁻¹ · cascode: 13.34 · mirror: 10 · active load: 5.658", 2),
        ("e.g. CS: VGS 760.99 mV, Id/W 72.23 A/m", 3),
        ("UMC 180 nm (umc_18) · active load: n18/p18 devices", 4),
        ("mirror Iout vs Vout at 100 µA and 500 µA", 5),
        ("CS: Spectre pz · cascode: 20.13 MHz −3 dB point", 6),
        ("target vs reported tables in docs/results.md", 7),
        ("simple vs cascode mirror; gain vs bandwidth", 8),
    ]
    for t, i in notes:
        yy = 80 + i * 74 + 33
        s.line(445, yy - 4, 485, yy - 4, w=1.2, color=MUTED, dash="4 3")
        s.text(492, yy, t, size=12, color=MUTED)
    s.save("analog-design-flow.svg", footer="Conceptual flow. Values on the right are documented in docs/ with their evidence.")


def gm_id_flow():
    s = SVG(940, 700, "gm/Id sizing flow")
    s.text(470, 34, "gm/Id Sizing Flow", size=20, anchor="middle", weight="bold")
    s.text(470, 56, "Left: generic procedure used in the studies.  Right: the common-source worked example (UMC 180 nm, N_18_MM, L = 180 nm).",
           size=12, anchor="middle", color=MUTED)
    steps = [
        ["Target Id", "from supply, swing or power budget"],
        ["Target gm", "gm = 2π · CL · GBW (or from gain)"],
        ["Target gm/Id", "gm / Id"],
        ["Find VGS", "gm/Id vs VGS sweep"],
        ["Find Id/W", "Id/W vs gm/Id sweep"],
        ["Calculate W", "W = Id / (Id/W)"],
        ["Build circuit and simulate", "DC, AC, pole-zero"],
        ["Validate", "compare against target"],
    ]
    vflow(s, 60, 76, 330, 54, 18, steps)
    ex = [
        ("Id = 0.9 V / 1.52 kΩ ≈ 0.592 mA", "hand calc (VOUT bias 0.9 V)"),
        ("gm = 2π·5 pF·100 MHz = 3.14 mS", "hand calc"),
        ("gm/Id = 5.34 V⁻¹", "hand calc"),
        ("VGS = 760.986 mV", "marker on simulated gm/Id–VGS"),
        ("Id/W = 72.229 A/m (µA/µm)", "marker on simulated Id/W–gm/Id"),
        ("0.592 mA / 72.229 A/m ≈ 8.20 µm", "calculated · schematic uses 8.4 µm"),
        ("RD = 1.5 kΩ, CL = 5 pF, VIN,DC = 771 mV", "schematic values"),
        ("Spectre pz: DC gain 3.886 V/V, pole 25.97 MHz", "simulated"),
    ]
    for i, (a, b) in enumerate(ex):
        yy = 76 + i * 72
        s.line(392, yy + 27, 470, yy + 27, w=1.2, color=MUTED, dash="4 3")
        s.rect(472, yy + 2, 410, 50, fill=FILL2, stroke=WARN, rx=6, sw=1.2)
        s.text(486, yy + 24, a, size=13, weight="bold")
        s.text(486, yy + 42, b, size=11, color=MUTED, italic=True)
    s.save("gm-id-flow.svg", footer="Conceptual flow. Example numbers are traceable in docs/common-source.md.")


def mos_characterization():
    s = SVG(960, 560, "MOSFET characterization parameter map")
    s.text(480, 34, "MOSFET Characterization: what is swept and what is derived", size=20, anchor="middle", weight="bold")
    s.rect(30, 70, 310, 420, fill="#ffffff", stroke=MUTED, rx=10, dash="5 4")
    s.text(185, 94, "PMOS testbench (as simulated)", size=14, anchor="middle", weight="bold")
    s.text(185, 112, "UMC 180 nm · P_18_MM · W/L = 1 µm / 180 nm", size=11, anchor="middle", color=MUTED)
    # common node (gnd) on top, device below
    s.line(80, 160, 315, 160, w=2.5)
    s.text(185, 152, "gnd: source and bulk", size=11, anchor="middle", color=MUTED)
    m = s.pmos(180, 290, "M0", "P_18_MM")
    s.line(202, 248, 202, 160)
    s.dot(202, 160)
    s.line(146, 290, 80, 290)
    s.vsrc(80, 160, 290, None)
    s.text(108, 222, "VGS", size=13, weight="bold")
    s.text(108, 238, "−1.8 → 0 V", size=11, color=MUTED)
    s.line(202, 332, 202, 410)
    s.line(202, 410, 315, 410)
    s.vsrc(315, 160, 410, None)
    s.text(300, 356, "VDS", size=13, anchor="end", weight="bold")
    s.text(300, 372, "−1.8 → 0 V", size=11, anchor="end", color=MUTED)
    s.text(185, 462, "DC sweeps + parametric families", size=12, anchor="middle", color=MUTED)
    s.box(380, 110, 170, 52, ["ID", "simulated drain current"], fill=FILL)
    s.box(380, 330, 170, 52, ["Op-point outputs", "Spectre device model"], fill=FILL)
    s.line(342, 200, 376, 140, arrow=True, color=MUTED, w=1.2)
    s.line(342, 300, 376, 352, arrow=True, color=MUTED, w=1.2)
    derived = [
        (600, 70, ["gm", "∂ID/∂VGS"], 136),
        (600, 140, ["gm/Id", "inversion level"], 136),
        (600, 210, ["ID/W", "current density"], 136),
        (600, 280, ["Vdsat", "op-point"], 356),
        (600, 350, ["Vth", "op-point"], 356),
        (600, 420, ["Cgs", "op-point"], 356),
    ]
    for x, y, t, src in derived:
        s.box(x, y, 150, 50, t, fill=FILL2, stroke=WARN)
        s.line(552, src, x - 4, y + 25, arrow=True, color=MUTED, w=1.1)
    s.box(790, 110, 150, 56, ["fT", "gm / (2π·Cgs)"], fill="#eaf6ee", stroke=GREEN)
    s.line(752, 95, 788, 130, arrow=True, color=GREEN, w=1.2)
    s.line(752, 445, 788, 150, arrow=True, color=GREEN, w=1.2)
    s.box(790, 250, 150, 56, ["λ", "two points on ID–VDS"], fill="#eaf6ee", stroke=GREEN)
    s.poly([(465, 108), (465, 58), (952, 58), (952, 278), (944, 278)], color=GREEN, w=1.2, arrow=True)
    s.box(790, 360, 150, 56, ["γ", "Vth(VSB) vs Vth0"], fill="#eaf6ee", stroke=GREEN)
    s.line(752, 375, 788, 388, arrow=True, color=GREEN, w=1.2)
    s.text(480, 515, "Plotted for PMOS: ID–VGS, ID–VDS, gm–VGS, Cgs–VGS, Vdsat–VGS, ID/W–gm/Id, Vth–VGS, gm/Id–VGS, fT–gm/Id.",
           size=12, anchor="middle", color=MUTED)
    s.save("mos-characterization.svg", footer="Conceptual map. Reported: λ = −0.01219 /V (see recheck note), γ = −0.418, Vth0 = −266.446 mV.")


def current_mirror():
    s = SVG(760, 470, "Simple NMOS current mirror")
    s.text(380, 32, "Simple NMOS Current Mirror (as simulated)", size=19, anchor="middle", weight="bold")
    s.vdd(120, 300, 70)
    s.isrc(208, 70, 170, "IREF = 100 µA / 500 µA")
    m2 = s.nmos(230, 262, "M2", "18.49 / 0.18 µm", dir=-1)
    m0 = s.nmos(430, 262, "M0", "18.49 / 0.18 µm", dir=1)
    s.line(208, 170, 208, 220)
    s.dot(208, 196)
    s.poly([(208, 196), (330, 196), (330, 262)])
    s.line(264, 262, 396, 262)
    s.dot(330, 262)
    s.line(208, 304, 208, 360)
    s.line(452, 304, 452, 360)
    s.line(208, 360, 640, 360, w=2.5)
    s.gnd(330, 360)
    s.line(452, 220, 452, 140)
    s.line(452, 140, 640, 140)
    s.text(462, 130, "IOUT", size=13, weight="bold", color=ACCENT)
    s.vsrc(640, 140, 360, None)
    s.text(664, 246, "VOUT", size=13, weight="bold")
    s.text(664, 262, "swept 0 → 1.8 V", size=11, color=MUTED)
    s.text(380, 410, "M2 is diode-connected; with equal sizes M0 copies IREF when VDS0 ≈ VGS.",
           size=12, anchor="middle", color=MUTED)
    s.text(380, 428, "Away from that point Iout follows VOUT through channel-length modulation (L = 180 nm).",
           size=12, anchor="middle", color=MUTED)
    s.save("current-mirror.svg", footer="Redrawn from the Virtuoso schematic (UMC 180 nm, N_18_MM). Not simulation output.")


def cascode_mirror():
    s = SVG(780, 560, "NMOS cascode current mirror")
    s.text(390, 32, "NMOS Cascode Current Mirror (as simulated)", size=19, anchor="middle", weight="bold")
    s.vdd(120, 300, 66)
    s.isrc(208, 66, 140, "IREF = 100 µA / 500 µA")
    s.nmos(230, 220, "M2", "18.49 / 0.18", dir=-1)
    s.nmos(430, 220, "M0 (cascode)", "18.49 / 0.18", dir=1)
    s.nmos(230, 340, "M1", "18.49 / 0.18", dir=-1)
    s.nmos(430, 340, "M3", "18.49 / 0.18", dir=1)
    s.line(208, 140, 208, 178)
    s.dot(208, 160)
    s.poly([(208, 160), (330, 160), (330, 220)])
    s.line(264, 220, 396, 220)
    s.dot(330, 220)
    s.line(208, 262, 208, 298)
    s.dot(208, 280)
    s.poly([(208, 280), (330, 280), (330, 340)])
    s.line(264, 340, 396, 340)
    s.dot(330, 340)
    s.line(452, 262, 452, 298)
    s.line(208, 382, 208, 440)
    s.line(452, 382, 452, 440)
    s.line(208, 440, 660, 440, w=2.5)
    s.gnd(330, 440)
    s.line(452, 178, 452, 110)
    s.line(452, 110, 660, 110)
    s.text(462, 100, "IOUT", size=13, weight="bold", color=ACCENT)
    s.vsrc(660, 110, 440, None)
    s.text(684, 270, "VOUT", size=13, weight="bold")
    s.text(684, 286, "0 → 1.8 V", size=11, color=MUTED)
    s.text(390, 488, "M1/M3 set the current; M0 holds M3's drain near M1's drain, shielding it from VOUT.",
           size=12, anchor="middle", color=MUTED)
    s.text(390, 506, "Cost: VOUT must exceed roughly VGS + Vdsat before M0 and M3 are both saturated.",
           size=12, anchor="middle", color=MUTED)
    s.save("cascode-mirror.svg", footer="Redrawn from the Virtuoso schematic (UMC 180 nm, N_18_MM). All four devices 18.49 µm / 180 nm.")


def common_source():
    s = SVG(740, 500, "Common-source amplifier with resistive load")
    s.text(370, 32, "Common-Source Amplifier, Resistive Load (as simulated)", size=19, anchor="middle", weight="bold")
    s.vdd(300, 670, 80)
    s.resistor(360, 80, 190, "RD = 1.5 kΩ", "hand calc: 1.52 kΩ")
    s.line(360, 190, 360, 218)
    s.dot(360, 205)
    s.nmos(338, 260, "M1", "W/L = 8.4 µm / 180 nm")
    s.line(360, 205, 520, 205)
    s.dot(520, 205)
    s.line(520, 205, 580, 205, arrow=True)
    s.text(586, 210, "VOUT", size=13, weight="bold", color=ACCENT)
    s.cap(520, 205, 380, "CL = 5 pF")
    s.line(360, 302, 360, 380)
    s.line(140, 380, 670, 380, w=2.5)
    s.gnd(360, 380)
    s.line(304, 260, 140, 260)
    s.vsrc(140, 260, 380, None, ac=True)
    s.text(116, 312, "VIN", size=13, anchor="end", weight="bold")
    s.text(116, 328, "DC 771 mV", size=11, anchor="end", color=MUTED)
    s.text(116, 342, "AC mag 1 V", size=11, anchor="end", color=MUTED)
    s.vsrc(670, 80, 380, None)
    s.text(694, 236, "1.8 V", size=12, color=MUTED)
    s.text(370, 432, "Av ≈ −gm·(RD ‖ ro); one dominant pole at the output node, p ≈ 1 / (2π·Rout·Cout)",
           size=12, anchor="middle", color=MUTED)
    s.text(370, 450, "Spectre pz: DC gain 3.886 V/V, pole −25.97 MHz, RHP zero +154.1 GHz",
           size=12, anchor="middle", color=ACCENT)
    s.save("common-source.svg", footer="Redrawn from the Virtuoso schematic (UMC 180 nm, N_18_MM). Not simulation output.")


def cascode_amplifier():
    s = SVG(800, 560, "Cascode amplifier with resistive load")
    s.text(400, 32, "Cascode Amplifier, Resistive Load (as simulated)", size=19, anchor="middle", weight="bold")
    s.vdd(300, 720, 78)
    s.resistor(380, 78, 175, "RD", "1591 Ω hand calc; see notes")
    s.line(380, 175, 380, 198)
    s.dot(380, 190)
    s.line(380, 190, 600, 190)
    s.dot(600, 190)
    s.line(600, 190, 650, 190, arrow=True)
    s.text(656, 195, "VOUT", size=13, weight="bold", color=ACCENT)
    s.cap(600, 190, 440, "CL = 5 pF")
    s.nmos(358, 240, "M1 (cascode)", "W/L ≈ 46.5–46.8 µm / 180 nm")
    s.line(380, 282, 380, 318)
    s.nmos(358, 360, "M2 (input)", "W/L = 46.5 µm / 180 nm")
    s.line(380, 402, 380, 440)
    s.line(210, 440, 720, 440, w=2.5)
    s.gnd(380, 440)
    s.line(324, 240, 210, 240)
    s.vsrc(210, 240, 440, None)
    s.text(192, 330, "VB = 1.078 V", size=12, anchor="end", weight="bold")
    s.text(192, 346, "cascode gate", size=11, anchor="end", color=MUTED)
    s.line(324, 360, 280, 360)
    s.vsrc(280, 360, 440, None, ac=True)
    s.text(300, 404, "VIN", size=12, weight="bold")
    s.text(300, 420, "≈ 574 mV DC", size=11, color=MUTED)
    s.vsrc(720, 78, 440, None)
    s.text(744, 260, "1.8 V", size=12, color=MUTED)
    s.text(400, 490, "Rout ≈ RD ‖ (gm1·ro1·ro2) ≈ RD, so gain ≈ gm2·RD and the output pole ≈ 1/(2π·RD·CL).",
           size=12, anchor="middle", color=MUTED)
    s.text(400, 508, "Reported: max gain 17.7657 dB, f−3dB 20.1298 MHz (targets: 20 dB, 20 MHz).",
           size=12, anchor="middle", color=ACCENT)
    s.save("cascode-amplifier.svg", footer="Redrawn from the Virtuoso schematic (UMC 180 nm, N_18_MM). RD label discrepancy discussed in docs/cascode-amplifier.md.")


def active_load():
    s = SVG(760, 540, "Common-source amplifier with PMOS current-mirror active load")
    s.text(380, 32, "Common-Source Amplifier with Active Load (design topology)", size=19, anchor="middle", weight="bold")
    s.vdd(150, 600, 78)
    s.pmos(230, 160, "Mp1", "diode-connected", dir=-1)
    s.pmos(430, 160, "Mp2 (load)", "W ≈ 35.4 µm (hand calc)", dir=1)
    s.line(208, 118, 208, 78)
    s.line(452, 118, 452, 78)
    s.line(264, 160, 396, 160)
    s.dot(330, 160)
    s.line(208, 202, 208, 270)
    s.dot(208, 226)
    s.poly([(208, 226), (330, 226), (330, 160)])
    s.isrc(208, 270, 390, "IREF", down=True)
    s.line(208, 390, 208, 440)
    s.line(452, 202, 452, 268)
    s.dot(452, 240)
    s.line(452, 240, 660, 240, arrow=True)
    s.text(666, 245, "VOUT", size=13, weight="bold", color=ACCENT)
    s.dot(620, 240)
    s.cap(620, 240, 440, "CL = 5 pF")
    s.nmos(430, 310, "Mn (input)", "W ≈ 9.76 µm (hand calc)")
    s.line(452, 352, 452, 440)
    s.line(396, 310, 340, 310)
    s.text(332, 315, "VIN", size=13, anchor="end", weight="bold")
    s.line(160, 440, 680, 440, w=2.5)
    s.gnd(452, 440)
    s.text(380, 484, "Av ≈ −gmn·(ron ‖ rop): the load is a current source, so gain no longer depends on a resistor drop.",
           size=12, anchor="middle", color=MUTED)
    s.text(380, 502, "Reported (handwritten): max gain 18.966 dB, f−3dB 11.9539 MHz, 0 dB crossing ≈ 105.7 MHz.",
           size=12, anchor="middle", color=ACCENT)
    s.save("active-load.svg", footer="Redrawn from the hand-drawn circuit diagram; no amplifier schematic screenshot exists. Devices n18/p18, L = 0.18 µm.")


def tradeoff_map():
    s = SVG(920, 560, "Design trade-off map")
    s.text(460, 32, "Trade-off Map", size=20, anchor="middle", weight="bold")
    s.text(460, 52, "Qualitative axes, not to scale. Points are placed by topology, not by measured values.",
           size=12, anchor="middle", color=MUTED)
    # left: mirror plane
    ox, oy, w, h = 90, 470, 340, 360
    s.line(ox, oy, ox + w, oy, arrow=True)
    s.line(ox, oy, ox, oy - h, arrow=True)
    s.text(ox + w / 2, oy + 34, "Minimum output voltage (headroom used) →", size=12, anchor="middle")
    s.add(f'<text x="{ox-30}" y="{oy-h/2}" font-family="{FONT}" font-size="12" fill="{INK}" text-anchor="middle" '
          f'transform="rotate(-90 {ox-30} {oy-h/2})">Output resistance / current accuracy →</text>')
    s.add(f'<circle cx="{ox+80}" cy="{oy-90}" r="9" fill="{ACCENT}"/>')
    s.text(ox + 96, oy - 94, "Simple mirror", size=13, weight="bold")
    s.text(ox + 96, oy - 78, "≈ Vdsat headroom, Rout ≈ ro", size=11, color=MUTED)
    s.add(f'<circle cx="{ox+220}" cy="{oy-290}" r="9" fill="{WARN}"/>')
    s.text(ox + 236, oy - 294, "Cascode mirror", size=13, weight="bold")
    s.text(ox + 236, oy - 278, "≈ VGS+Vdsat · Rout ≈ gm·ro²", size=11, color=MUTED)
    s.line(ox + 92, oy - 100, ox + 210, oy - 280, arrow=True, color=MUTED, w=1.2, dash="5 4")
    s.text(ox + 170, oy - 185, "+2 devices, +1 bias level", size=11, color=MUTED)
    # right: list
    x0 = 500
    rows = [
        ("Gain vs bandwidth", "Larger RD raises gm·RD but lowers 1/(2π·RD·CL)."),
        ("Output resistance vs headroom", "Cascoding stacks a device and one more Vdsat."),
        ("Current accuracy vs complexity", "Cascode mirror held Iout ≈ IREF; simple did not."),
        ("Width vs capacitance", "Wider W at fixed Id → higher gm/Id, more Cgs."),
        ("Cascode gain vs swing", "Two stacked devices share the 1.8 V supply."),
        ("Sizing vs speed", "Low gm/Id (strong inversion) → higher fT."),
    ]
    for i, (a, b) in enumerate(rows):
        yy = 92 + i * 70
        s.rect(x0, yy, 390, 56, fill=FILL if i % 2 == 0 else FILL2, stroke=ACCENT if i % 2 == 0 else WARN, rx=6, sw=1.2)
        s.text(x0 + 14, yy + 23, a, size=13, weight="bold")
        s.text(x0 + 14, yy + 42, b, size=11, color=MUTED)
    s.save("tradeoff-map.svg", footer="General principles. Project observations are labelled as such in docs/.")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in (analog_design_flow, gm_id_flow, mos_characterization, current_mirror, cascode_mirror,
              common_source, cascode_amplifier, active_load, tradeoff_map):
        f()
    print("ok")
