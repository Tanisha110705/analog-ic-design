# Results

Every number in this repository, with its type and evidence.

**Type legend**

- **Target**: a specification from the report's aim.
- **Simulated**: a Spectre output or a ViVA marker visible in a screenshot.
- **Plot reading**: read by eye from gridlines in a screenshot (approximate).
- **Hand calc**: a value from the report's handwritten calculations.
- **Calculated**: computed in this repository from values in the rows above.
- **Reported**: stated in the report with no screenshot behind it.
- **Schematic**: a component value shown on a Virtuoso schematic.

## Device Characterization

### PMOS (UMC 180 nm, P_18_MM, W/L = 1 µm / 180 nm)

| Block | Metric | Value | Type | Evidence |
|---|---|---:|---|---|
| PMOS | Vth at V_SB = 0 | −266.446 mV | Simulated | [07-vth-vs-vgs.png](../device-characterization/pmos/07-vth-vs-vgs.png) |
| PMOS | I_D1 at V_DS1 = −1.49704 V | −42.61116 µA | Hand calc (read from simulation) | R3 notebook |
| PMOS | I_D2 at V_DS2 = −1.28551 V | −41.19137 µA | Hand calc (read from simulation) | R3 notebook |
| PMOS | λ | −0.01219 /V | Hand calc (reported result) | R3 |
| PMOS | λ, same formula and inputs | ≈ −0.206 /V | Calculated | [recheck](mos-characterization.md#lambda-recheck) |
| PMOS | Vth at \|V_SB\| = 1.8 V | −520 mV | Reported | R3 notebook |
| PMOS | φF assumed | 0.7 V | Hand calc input | R3 notebook |
| PMOS | γ | −0.418 | Hand calc (reported result) | R3 |
| PMOS | γ recomputed | −0.4187 | Calculated | [doc](mos-characterization.md#body-effect-coefficient-γ) |
| PMOS | gm/Id range | ≈ 1–26 V⁻¹ over V_GS = −1.8 → 0 V | Plot reading | [08-gmid-vs-vgs.png](../device-characterization/pmos/08-gmid-vs-vgs.png) |

### NMOS gm/Id sweeps

| Block | Metric | Value | Type | Evidence |
|---|---|---:|---|---|
| CS sweep (N_18_MM) | V_GS at gm/Id = 5.34 | 760.986 mV | Simulated | [plot](../device-characterization/nmos-gm-id/cs-gmid-and-id-vs-vgs.png) |
| CS sweep | I_D/W at gm/Id = 5.34 | 72.22945 A/m | Simulated | [plot](../device-characterization/nmos-gm-id/cs-id-per-w-vs-gmid.png) |
| Mirror sweep (N_18_MM) | V_GS at gm/Id = 10 | 589.0284 mV | Simulated | [plot](../device-characterization/nmos-gm-id/mirror-gmid-and-id-vs-vgs.png) |
| Mirror sweep | I_D/W at gm/Id = 10 | 27.04044 A/m | Simulated | [plot](../device-characterization/nmos-gm-id/mirror-id-per-w-vs-gmid.png) |
| Cascode sweep (N_18_MM, V_DS 0.45 V) | V_GS at gm/Id = 13.34 (M2) | 573.927 mV | Simulated | [plot](../amplifiers/cascode/cascode-id-per-w-vs-vgs.png) |
| Cascode sweep | I_D/W (M2) | 12.03357 A/m | Simulated | [plot](../amplifiers/cascode/cascode-id-per-w-vs-vgs.png) |
| Cascode sweep | Bias voltage at gm/Id = 13.34 (M1) | 1.07896 V | Simulated | [plot](../amplifiers/cascode/cascode-gmid-vs-vgs.png) |
| Cascode sweep | I_D/W (M1) | 11.95023 A/m | Hand calc | R3 notebook |
| Active-load sweep (n18) | V_GS at gm/Id = 5.658 | 783.739 mV | Simulated | [plot](../amplifiers/active-load/nmos-gmid-vs-vgs.png) |
| Active-load sweep (n18) | I_D/W | 56.871 A/m | Simulated | [plot](../amplifiers/active-load/nmos-id-per-w-vs-gmid.png) |
| Active-load sweep (p18) | Gate voltage at gm/Id = 5.658 (source at 0.9 V) | 89.239 mV | Simulated | [plot](../amplifiers/active-load/pmos-gmid-vs-vgs.png) |
| Active-load sweep (p18) | I_D/W | −15.6869 A/m | Simulated | [plot](../amplifiers/active-load/pmos-id-per-w-vs-gmid.png) |

## Common-Source

| Block | Metric | Value | Type | Evidence |
|---|---|---:|---|---|
| CS | Gain target | 4 V/V (4.8 V/V with margin) | Target | R2 aim |
| CS | GBW target | 100 MHz | Target | R2 aim |
| CS | C_L | 5 pF | Target / Schematic | [schematic](../amplifiers/common-source/cs-schematic.png) |
| CS | gm | 3.14 mS | Hand calc | R2 |
| CS | R_D | 1.52 kΩ (hand) / 1.5 kΩ (schematic) | Hand calc / Schematic | [schematic](../amplifiers/common-source/cs-schematic.png) |
| CS | I_D | 0.592 mA | Hand calc | R2 |
| CS | gm/Id | 5.34 V⁻¹ | Hand calc | R2 |
| CS | W | 8.20 µm (calc) / 8.4 µm (schematic) | Calculated / Schematic | [schematic](../amplifiers/common-source/cs-schematic.png) |
| CS | L | 180 nm | Schematic | same |
| CS | V_IN DC bias | 771 mV | Schematic | same |
| CS | DC gain | 3.88553 V/V (11.79 dB) | Simulated (Spectre pz) | [log](../amplifiers/common-source/cs-spectre-pz-log.png) |
| CS | Midband gain (report wording) | ≈ 3.8 V/V | Reported | R2 conclusion |
| CS | Pole | −25.9652 MHz | Simulated (Spectre pz) | [log](../amplifiers/common-source/cs-spectre-pz-log.png) |
| CS | Zero (RHP) | +154.112 GHz | Simulated (Spectre pz) | [log](../amplifiers/common-source/cs-spectre-pz-log.png) |
| CS | Gain × pole | ≈ 100.9 MHz | Calculated | — |
| CS | Short-circuit drain current plateau | ≈ 3.17 mA per V (gm ≈ 3.17 mS) | Plot reading | [plot](../amplifiers/common-source/cs-ac-current-and-dc-transfer.png) |

## Current Mirrors

| Block | Metric | Value | Type | Evidence |
|---|---|---:|---|---|
| Mirrors | Overdrive assumption | 200 mV | Target | R2 aim |
| Mirrors | gm/Id target | 10 V⁻¹ | Hand calc | R2 |
| Mirrors | W/L, all devices | 18.49 µm / 180 nm | Schematic | [schematics](../current-mirrors) |
| Mirrors | W for 100 µA at gm/Id = 10 | 3.70 µm | Calculated | — |
| Mirrors | W for 500 µA at gm/Id = 10 | 18.49 µm | Calculated | — |
| Simple | I_REF | 100 µA, 500 µA | Schematic | [100 µA](../current-mirrors/simple/simple-mirror-100uA-schematic.png), [500 µA](../current-mirrors/simple/simple-mirror-500uA-schematic.png) |
| Simple | I_OUT at V_OUT = 1.8 V (100 µA) | ≈ 205 µA | Plot reading | [plot](../current-mirrors/simple/simple-mirror-iout-vs-vout.png) |
| Simple | I_OUT at V_OUT = 1.8 V (500 µA) | ≈ 740 µA | Plot reading | same |
| Cascode | I_REF | 100 µA (schematic), 500 µA (plot legend only) | Schematic / plot | [schematic](../current-mirrors/cascode/cascode-mirror-100uA-schematic.png) |
| Cascode | I_OUT at V_OUT = 1.8 V (100 µA) | ≈ 100 µA | Plot reading | [plot](../current-mirrors/cascode/cascode-mirror-iout-vs-vout.png) |
| Cascode | I_OUT at V_OUT = 1.8 V (500 µA) | ≈ 505 µA | Plot reading | same |
| Cascode | V_OUT where I_OUT flattens | ≈ 0.6 V (100 µA), ≈ 0.75–0.8 V (500 µA) | Plot reading | same |
| Both | Output resistance, mirror error | Not measured | — | — |

## Cascode Amplifier

| Block | Metric | Value | Type | Evidence |
|---|---|---:|---|---|
| Cascode | Gain target | 20 dB | Target | R3 aim |
| Cascode | Bandwidth target | 20 MHz | Target | R3 aim |
| Cascode | Power target | 1 mW | Target | R3 aim |
| Cascode | C_L | 5 pF | Target / Schematic | [schematic](../amplifiers/cascode/cascode-amplifier-schematic.png) |
| Cascode | R_D | 1591 Ω (hand); label reads "1K" | Hand calc / Schematic | see [inconsistency](cascode-amplifier.md#r_d-inconsistency) |
| Cascode | I_D | 0.566 mA (0.56 mA used) | Hand calc | R3 |
| Cascode | gm | 7.54 mS | Hand calc | R3 |
| Cascode | gm/Id | 13.34 V⁻¹ | Hand calc | R3 |
| Cascode | W (M2 / M1) | 46.5 µm / 46.8 µm | Hand calc | R3 |
| Cascode | Cascode gate bias | 1.078 V | Schematic | [schematic](../amplifiers/cascode/cascode-amplifier-schematic.png) |
| Cascode | Max gain (as reported) | 17.7657 dB | Reported / marker | [AC plot](../amplifiers/cascode/cascode-ac-response.png), [reading](cascode-amplifier.md#reading-the-ac-plot) |
| Cascode | f−3dB | 20.1298 MHz | Simulated (marker) | [AC plot](../amplifiers/cascode/cascode-ac-response.png) |
| Cascode | Power | Not measured | — | — |

## Active-Load Amplifier

| Block | Metric | Value | Type | Evidence |
|---|---|---:|---|---|
| Active load | UGB target | 100 MHz | Target | R6 aim |
| Active load | Power target | 1 mW | Target | R6 aim |
| Active load | C_L | 5 pF | Target | R6 aim |
| Active load | Overdrive target | 200 mV | Target | R6 aim |
| Active load | I_D | 0.555 mA | Hand calc | R6 |
| Active load | gm | 3.14 mS | Hand calc | R6 |
| Active load | gm/Id | 5.658 V⁻¹ | Hand calc | R6 |
| Active load | NMOS W | 9.7588 µm | Hand calc | R6 |
| Active load | PMOS W | 35.44349 µm | Hand calc | R6 |
| Active load | Max gain | 18.966 dB | Reported (handwritten) | R6 results page |
| Active load | −3 dB gain level | 15.9665 dB | Reported (handwritten) | R6 results page |
| Active load | f−3dB | 11.9539 MHz | Reported (handwritten) | R6 results page |
| Active load | Gain at 100 MHz | 475.455 mdB | Reported (handwritten) | R6 results page |
| Active load | 0 dB frequency | ≈ 105.71 MHz | Reported (handwritten) | R6 results page |
| Active load | Gain × f−3dB | ≈ 106.1 MHz | Calculated | — |

## Target vs Achieved

| Design | Metric | Target | Result | Result type | Verdict |
|---|---|---:|---:|---|---|
| CS | Gain | 4 V/V | 3.886 V/V | Simulated | 2.9 % below target |
| CS | GBW | 100 MHz | ≈ 100.9 MHz | Calculated from simulated gain and pole | Met |
| Cascode | Gain | 20 dB | 17.7657 dB (as reported) | Reported | **Not claimed**; plot suggests the value is the −3 dB level |
| Cascode | f−3dB | 20 MHz | 20.1298 MHz | Simulated | Met |
| Cascode | Power | 1 mW | — | — | Not measured |
| Active load | UGB | 100 MHz | ≈ 105.7 MHz | Reported (handwritten) | Met, per report |
| Active load | Power | 1 mW | — | — | Not measured |
| Mirrors | I_OUT | 100 / 500 µA | ≈ 100 / ≈ 505 µA (cascode, at 1.8 V) | Plot reading | Cascode tracks I_REF; simple does not |

## Not measured anywhere

Output resistance, mirror matching error, power, noise, slew rate, output swing, linearity, PSRR, CMRR, phase margin, area, corners (PVT), Monte Carlo, DRC, LVS, post-layout results.
