# Evidence Audit

This file records where every result in the repository comes from and what is missing. It was written before any documentation, and it is the reference for every number elsewhere.

## Sources

| ID | Source | Content used here |
|---|---|---|
| **R2** | Course report "Assessment 2" (Jan–Feb 2026) | Common-source amplifier with resistive load (gm/Id method); NMOS gm/Id sweeps; simple and cascode current mirrors at 100 µA and 500 µA |
| **R3** | Course report "Assessment 3" (Jan–Feb 2026) | PMOS characterization (9 plots, λ, γ); cascode amplifier with resistive load |
| **R6** | Course report "Lab DA-6" (Mar–Apr 2026) | Common-source amplifier with active load. **Its PLL section belongs to [pll-cadence-virtuoso](https://github.com/Tanisha110705/pll-cadence-virtuoso) and is not used here.** |

The reports are scanned notebook pages plus Cadence screenshots. The original PDFs are **not** committed. Their screenshots contain a university server hostname, a home-directory path and a student registration number. The relevant screenshots were cropped to the plot or schematic canvas and committed instead (see [repository-guide.md](repository-guide.md)).

When this audit was made, the Git repository itself was empty: no schematics, netlists, ADE states, Cadence libraries, layouts or logs. Every result therefore comes from the three reports.

## Block-by-block findings

### Device characterization

| Item | PMOS (R3) | NMOS (R2, R3, R6) |
|---|---|---|
| Technology | UMC 180 nm, `umc_18` library (report text, "umc" in schematic tab) | UMC 180 nm N_18_MM (R2, R3); n18 devices in a `*_scl` library (R6) |
| Device | P_18_MM, W = 1 µm, L = 180 nm | W = 1 µm, L = 180 nm testbenches |
| Bias | Source and bulk at 0 V; V_GS, V_DS swept −1.8 → 0 V | V_GS swept 0 → 1.8 V; V_DS = 0.9 V (R2 CS, hand sketch), 1.8 V (R2 mirror), 0.45 V (R3), 0.9 V (R6) |
| Plots | I_D–V_GS, I_D–V_DS (with families), gm, Cgs, Vdsat, I_D/W–gm/Id, Vth, gm/Id, fT–gm/Id | gm/Id–V_GS, I_D/W–gm/Id or I_D/W–V_GS, I_D–V_GS |
| Extracted numbers | Vth0 = −266.446 mV (marker); λ = −0.01219 /V, γ = −0.418 (hand calc) | Marker values per design (see [gm-id-methodology.md](gm-id-methodology.md)) |
| Not extracted | Numeric gm, Cgs, Vdsat or fT values | Vth, λ for NMOS |

### Common-source amplifier, resistive load (R2)

| Item | Value | Evidence |
|---|---|---|
| Topology | NMOS CS, resistor load, CL to ground | Schematic |
| Device | N_18_MM, W = 8.4 µm, L = 180 nm | Schematic label |
| RD / CL / VDD | 1.5 kΩ / 5 pF / 1.8 V | Schematic labels |
| Input bias | V_IN DC = 771 mV, AC magnitude 1 V (sine amplitude 10 mV also set) | Property editor |
| Targets | \|Av\| = 4 V/V, GBW = 100 MHz, CL = 5 pF | Handwritten aim |
| DC gain | 3.88553 V/V | Spectre `pz` log |
| Pole / zero | −2.59652 × 10⁷ Hz / +1.54112 × 10¹¹ Hz | Spectre `pz` log |
| Reported gain | "around 3.8 V/V" | Report conclusion |
| Bandwidth | No marker on a V_OUT curve. The pole value is the bandwidth evidence | — |

### Current mirrors (R2)

| Item | Value | Evidence |
|---|---|---|
| Simple topology | 2 × N_18_MM, M2 diode-connected | Schematic (100 µA and 500 µA) |
| Cascode topology | 4 × N_18_MM, stacked diode-connected reference | Schematic (100 µA only) |
| W/L | 18.49 µm / 180 nm, all devices, both currents | Schematic labels |
| I_REF | 100 µA, 500 µA (`idc`) | Schematic labels |
| Output | VOUT swept 0 → 1.8 V | Plot x-axis, `vdc=Vout` |
| Output resistance, matching error | **Not measured** | — |

### Cascode amplifier (R3)

| Item | Value | Evidence |
|---|---|---|
| Topology | NMOS input M2, NMOS cascode M1, resistor load, CL | Schematic |
| Targets | 20 dB, 1 mW, 20 MHz BW, CL = 5 pF | Handwritten aim |
| W | M2 46.5 µm, M1 46.8 µm (hand calc); schematic label ≈ 46.5 µm (low resolution) | Notes, schematic |
| Cascode gate bias | 1.078 V | Schematic `vdc=1.078`; marker 1.07896 V |
| Results | Max gain 17.7657 dB (as reported), f−3dB 20.1298 MHz | AC plot markers, report text |
| Power | **Not simulated** | — |

### Common-source amplifier with active load (R6)

| Item | Value | Evidence |
|---|---|---|
| Topology | NMOS CS, PMOS current-mirror load, I_REF, CL | Hand-drawn diagram only |
| Targets | UGB 100 MHz, 1 mW, CL 5 pF, overdrive 200 mV | Handwritten aim |
| Sizing | NMOS W = 9.7588 µm, PMOS W = 35.44349 µm | Hand calc from marker values |
| Results | Max gain 18.966 dB; −3 dB level 15.9665 dB; f−3dB 11.9539 MHz; gain at 100 MHz = 475.455 mdB; 0 dB frequency ≈ 105.712 MHz | Handwritten results (signed by the instructor) |
| Schematic / AC plot / op-point | **Not in report** | — |

### Physical design

No layout, DRC, LVS, extracted (PEX) simulation or parasitic analysis exists for any block.

## Confirmed from repository

Nothing. The repository was empty before this work.

## Confirmed from reports

- All schematics, plot screenshots, marker values and hand calculations listed above.
- Tools: Virtuoso Schematic Editor, ADE L, ADE Parametric Analysis, Spectre (`spectre.out`), Virtuoso Visualization & Analysis XL. Simulation temperature 27 °C (status bar).

## Confirmed by both

Not applicable (empty repository).

## Missing evidence

- Netlists, ADE states, Cadence libraries; nothing is re-runnable.
- Cascode-mirror 500 µA schematic. The report's figure for it is a second copy of the simple-mirror schematic with `idc=500u`. The 500 µA cascode **curve** does exist in the Iout–VOUT plot.
- A V_OUT AC plot for the CS amplifier (the "AC response" plot shows |I(M1/D)| in mA).
- The PMOS Vth at |VSB| = 1.8 V (−520 mV) used for γ: no plot.
- Active-load amplifier schematic screenshot, AC plot, DC operating point and output swing.
- Supply-current or power simulation for any amplifier.
- Transient results for any block.
- Operating-region printouts for any transistor.
- Corners, Monte Carlo, noise, PSRR, CMRR, slew rate, linearity.

## Report / repository inconsistencies

1. **PMOS λ arithmetic (R3).** The formula λ = (I_D2 − I_D1)/(I_D1·V_DS2 − I_D2·V_DS1) with the stated inputs gives ≈ −0.206 /V, not −0.01219 /V. The written numerator has its sign flipped, and the first denominator term is written as −54.777 instead of +54.777. The reported value is kept as reported and flagged. See [mos-characterization.md](mos-characterization.md#lambda-recheck).
2. **Cascode amplifier "max gain" (R3).** 17.7657 dB is a horizontal marker that intersects the response at 20.1298 MHz. The passband plateau is drawn above the 20 dB gridline. This is consistent with 17.7657 dB being the (peak − 3 dB) level, which would put the peak near 20.8 dB, but the peak value itself was never read out.
3. **Cascode amplifier RD (R3).** The hand calculation gives RD = 1591 Ω. The schematic label reads "1K" at the screenshot's resolution. A 5 pF load with a 20.13 MHz −3 dB point implies ≈ 1.58 kΩ, which agrees with 1591 Ω rather than 1 kΩ (1 kΩ would give ≈ 31.8 MHz). The value actually simulated cannot be confirmed.
4. **CS amplifier W and V_GS (R2).** gm/Id = 5.34 gives V_GS = 760.986 mV and I_D/W = 72.229 A/m, i.e. W ≈ 8.20 µm. The schematic uses W = 8.4 µm and V_IN = 771 mV, a small manual adjustment that is not explained in the report.
5. **CS amplifier threshold (R2).** The report conclusion places the threshold at "around 0.7 to 0.8 V". The drain-current sweep shows conduction starting near 0.4–0.5 V. 0.76–0.77 V is the chosen bias point, not the threshold.
6. **Mirror sizing (R2).** The notes compute gm/Id = 10 for 100 µA but list W = 18.48 µm "for 100 µA". 100 µA / 27.04 A/m = 3.70 µm, while 500 µA / 27.04 A/m = 18.49 µm. The schematic W matches the 500 µA calculation, and the same W was used at 100 µA.
7. **Cascode report wording (R3).** The typed aim reads "a power of 1 mW (in dB) = 20 MHz"; the handwritten aim clarifies "power = 1 mW, bandwidth = 20 MHz". The conclusion calls the circuit a "common source amplifier".
8. **Active-load technology (R6).** Its testbenches use `n18`/`p18` devices in a library named `*_scl`, not the UMC `N_18_MM`/`P_18_MM` used in R2/R3. Results from the two technologies should not be compared directly.

## Material belonging to another repository

R6, pages 2–4: PLL architecture (PFD, charge pump, R = 1 kΩ / C = 227 pF loop filter, VCO, divide-by-128, 2.561 GHz output). This belongs to [Tanisha110705/pll-cadence-virtuoso](https://github.com/Tanisha110705/pll-cadence-virtuoso) and appears here only as a cross-reference.

## Claims that must not be made

- That the cascode amplifier met (or failed) its 20 dB target. The evidence is ambiguous.
- Any amplifier power consumption as a simulated result.
- Any mirror output resistance, matching error or compliance voltage as a measured number.
- That all transistors were verified in saturation.
- Any DRC, LVS, layout, post-layout, corner, Monte Carlo, noise, PSRR, CMRR, slew or linearity result.
- Transient behaviour of any block.
- A positive λ, or a corrected λ value presented as the project result.
- That the active-load amplifier used UMC 180 nm.
