# Reproduction

## Requirements

- A licensed Cadence Virtuoso installation with ADE L (or ADE Explorer) and Spectre.
- The foundry PDK for each study, obtained through your institution's or foundry's licensing channel:
  - UMC 180 nm (`umc_18` library: N_18_MM, P_18_MM) for the PMOS, CS, mirror and cascode studies;
  - the 180 nm library providing `n18`/`p18` devices for the active-load study.
- No PDK files, models, license details or Cadence libraries are included in this repository, and none should be committed.

## Status

The original cellviews, netlists and ADE states were not preserved, so **nothing here can be re-run directly**. The steps below rebuild each study from the values documented in [results.md](results.md). None of these simulations was executed as part of preparing this repository.

## General procedure (as followed in the reports)

1. Open Virtuoso and create a library attached to the PDK technology library.
2. Create a schematic cellview and place devices from the PDK (`N_18_MM`, `P_18_MM`, or `n18`/`p18`) plus `analogLib` sources (`vdc`, `vsin`/`vac`, `idc`), resistors and capacitors.
3. Launch ADE L, choose Spectre, set design variables (e.g. `vgs`, `vds`, `Vout`) and copy them from the cellview.
4. Run the analyses below and plot with ViVA / the Calculator.

## Study-by-study

### 1. PMOS characterization

1. P_18_MM, W = 1 µm, L = 180 nm. Source and bulk to ground; `vdc=vgs` on the gate, `vdc=vds` on the drain.
2. DC sweep `vgs` from −1.8 to 0 V; plot I_D. Use Parametric Analysis over `vds` for the I_D–V_GS family.
3. DC sweep `vds` from −1.8 to 0 V; plot I_D; parametric over `vgs` for output curves.
4. With the `vgs` sweep, plot the op-point outputs `gm`, `cgs`, `vdsat`, `vth`, `gmoverid`.
5. In the Calculator, build I_D/W = `getData("M0:id" ?result "dc") / pv("M0" "w" ?result "instance")` and fT = `gm / (2·π·cgs)`, and plot both against `gmoverid`.
6. λ: pick two saturation points on I_D–V_DS and apply λ = (I_D2 − I_D1)/(I_D1·V_DS2 − I_D2·V_DS1). Check the arithmetic (see the [recheck](mos-characterization.md#lambda-recheck)).
7. γ: apply a source-bulk bias, read Vth, and compare with Vth0.

### 2. NMOS gm/Id lookup (per design)

1. N_18_MM, W = 1 µm, L = 180 nm, V_DS at the circuit's expected value (0.9 V CS, 1.8 V mirror, 0.45 V cascode).
2. DC sweep V_GS 0 → 1.8 V; plot `gmoverid` and place a horizontal marker at the target gm/Id to read V_GS.
3. Plot I_D/W vs `gmoverid` and read I_D/W at the target. W = I_D / (I_D/W).

### 3. Common-source amplifier

1. N_18_MM W = 8.4 µm / L = 180 nm; R_D = 1.5 kΩ to VDD = 1.8 V; C_L = 5 pF; gate source DC 771 mV, AC magnitude 1 V.
2. DC sweep of the input source 0 → 1.8 V; plot I_D.
3. AC sweep 1 Hz → 100 GHz; plot V_OUT in dB20 (the original plotted the drain current).
4. Pole-zero analysis from V1 to V(Vout). Expect DC gain ≈ 3.886 and a pole near −25.97 MHz.

### 4. Current mirrors

1. Simple: two N_18_MM, W = 18.49 µm / L = 180 nm; `idc` = 100 µA (then 500 µA) from 1.8 V into the diode-connected device; `vdc=Vout` on the output drain.
2. Cascode: four N_18_MM of the same size, stacked as in [current-mirrors.md](current-mirrors.md).
3. DC sweep `Vout` 0 → 1.8 V; plot the output device's drain current for both I_REF values.
4. Recommended addition: plot d(I_OUT)/d(V_OUT) to extract R_out, and print I_OUT at a fixed V_OUT.

### 5. Cascode amplifier

1. M2 (input) and M1 (cascode), N_18_MM, L = 180 nm, W ≈ 46.5 µm (M1 46.8 µm per hand calc). R_D = 1591 Ω (hand calc; see the [R_D note](cascode-amplifier.md#r_d-inconsistency)). C_L = 5 pF, VDD = 1.8 V, cascode gate 1.078 V, input DC ≈ 574 mV.
2. AC sweep; plot V_OUT in dB20. Read the **peak** gain with a marker, then place a horizontal marker at peak − 3 dB to read f−3dB.
3. Recommended addition: record the supply current to verify the 1 mW target.

### 6. Active-load amplifier

1. Characterize n18/p18 (W = 1 µm, L = 0.18 µm) at V_DS = 0.9 V. Read V_GS and I_D/W at gm/Id = 5.658.
2. Mn W ≈ 9.76 µm; Mp1/Mp2 mirror with Mp2 W ≈ 35.44 µm; C_L = 5 pF; choose I_REF ≈ 0.555 mA and size Mp1 (not documented in the report).
3. AC sweep: compare with max gain 18.966 dB, f−3dB 11.954 MHz and 0 dB at ≈ 105.7 MHz.

## Comparing against targets

Use the [Target vs Achieved](results.md#target-vs-achieved) table. Keep the result types separate (target / simulated / calculated / reported) when adding new data.
