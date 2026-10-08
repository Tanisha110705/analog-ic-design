# Analysis Methods: DC, AC, Transient, Sizing and Operating Regions

This page describes what each analysis type was used for in these studies and how far the evidence goes.

## DC analysis

| Use | Where | Evidence |
|---|---|---|
| Device characteristics (I_D–V_GS, I_D–V_DS families) | PMOS; NMOS testbenches | [PMOS plots](../device-characterization/pmos), [NMOS plots](../device-characterization/nmos-gm-id) |
| Op-point outputs swept vs V_GS (gm, gmoverid, cgs, vdsat, vth) | PMOS, NMOS | Same |
| Derived lookup curves (I_D/W vs gm/Id, fT vs gm/Id) via the Calculator | PMOS, all NMOS designs | Same |
| Bias current vs input DC level | CS amplifier | [right panel](../amplifiers/common-source/cs-ac-current-and-dc-transfer.png) |
| Output compliance (I_OUT vs V_OUT, 0 → 1.8 V) | Simple and cascode mirrors | [simple](../current-mirrors/simple/simple-mirror-iout-vs-vout.png), [cascode](../current-mirrors/cascode/cascode-mirror-iout-vs-vout.png) |

What DC analysis established here: the V_GS for each target gm/Id, the current density for sizing, the CS bias point on its transfer curve, and the headroom at which each mirror starts to behave as a current source.

What it did not establish: the bias stability across corners or temperature (only 27 °C was simulated), or the printed operating region of each device.

## AC analysis

| Use | Where | Evidence |
|---|---|---|
| Pole-zero analysis (`pz`) of V(Vout)/V1 | CS amplifier | [Spectre log](../amplifiers/common-source/cs-spectre-pz-log.png) |
| Small-signal drain current vs frequency | CS amplifier | [left panel](../amplifiers/common-source/cs-ac-current-and-dc-transfer.png) |
| V_OUT magnitude (dB20) with −3 dB marker | Cascode amplifier | [AC plot](../amplifiers/cascode/cascode-ac-response.png) |
| Gain, f−3dB, unity-gain frequency | Active-load amplifier | Handwritten only |

Midband gain and f−3dB are reported only where a simulator output or marker exists. No poles were calculated beyond the Spectre `pz` output, and no phase margin applies (these are open-loop single stages, not feedback amplifiers).

## Transient analysis

**No transient results exist for any block in this repository.** The CS input source defines a 10 mV sine amplitude, and the CS notebook lists "transient analysis" as a planned step, but no waveform appears in the report. The only transient waveforms in the source material belong to the PLL and are not used here.

## Transistor sizing

```
spec (gain, GBW or f-3dB, C_L, power or output bias)
      │
      ├─► I_D      from power (I = P/VDD) or output bias (I = (VDD − V_OUT)/R_D)
      ├─► gm       from GBW (2π·C_L·GBW) or from gain and f-3dB
      ▼
  gm/Id = gm / I_D
      │
      ├─► V_GS     marker on gm/Id–V_GS   (W = 1 µm testbench, circuit-like V_DS)
      ├─► I_D/W    marker on I_D/W–gm/Id
      ▼
  W = I_D / (I_D/W),  L = 180 nm throughout
```

Every sized device and its source values are tabulated in [gm-id-methodology.md](gm-id-methodology.md#worked-values-from-each-design). Only widths that appear on a schematic or in a hand calculation are published. Unsupported dimensions (e.g. the active-load Mp1 width and I_REF) are listed as missing.

## Operating region verification

A device is in saturation when V_GS > V_th and V_DS ≥ V_GS − V_th ≈ Vdsat (magnitudes for PMOS), in triode when V_DS < Vdsat, and in cutoff (or sub-threshold) when V_GS < V_th.

What the evidence supports, per circuit:

| Circuit | Check available | Conclusion |
|---|---|---|
| CS amplifier | Output designed at 0.9 V with V_GS ≈ 0.77 V; I_D–V_IN curve | V_DS (≈ 0.9 V by design) exceeds V_GS − V_th for any V_th above ≈ 0 V, so saturation is very likely. Not confirmed by a printed op-point. |
| Simple mirror | I_OUT–V_OUT plot | M0 is in triode below the knee (≈ 0.1–0.25 V) and saturated above it. M2 is always saturated (diode connection). |
| Cascode mirror | I_OUT–V_OUT plot | Both output devices saturated only above ≈ 0.6 V (100 µA) / ≈ 0.75–0.8 V (500 µA), where I_OUT flattens. |
| Cascode amplifier | Design allots 0.45 V V_DS per device | Not confirmed. No op-point shown. |
| Active-load amplifier | None | Not confirmed. No op-point shown. |

The Spectre `region` op-point output appears in the signal browser of several screenshots, but it was never plotted or printed. **This repository does not claim that every transistor was verified in saturation.**
