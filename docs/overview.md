# Overview

## What this repository is

A set of transistor-level analog design studies, carried out in Cadence Virtuoso with Spectre during a CMOS analog IC design course (Jan–Apr 2026). They are organized here by design topic rather than by lab number. The studies build on one another:

```
MOSFET characterization        (PMOS study; NMOS sweeps inside each design)
        ↓
gm/Id design methodology       (gm/Id → V_GS, I_D/W → W)
        ↓
Bias selection                 (output at VDD/2; current from power or R_D)
        ↓
Current mirrors                (simple vs cascode at 100 µA and 500 µA)
        ↓
Common-source amplifier        (resistive load, gain 3.886 V/V, pole 25.97 MHz)
        ↓
Cascode techniques             (cascode mirror; cascode amplifier at 20 MHz)
        ↓
Active loads                   (CS with PMOS mirror load)
        ↓
Gain / bandwidth analysis      (GBW ≈ gm / 2πC_L holds across the CS stages)
        ↓
Design trade-offs              (headroom vs R_out; gain vs bandwidth; W vs C)
```

## Scope

| In scope | Out of scope |
|---|---|
| Device characterization (PMOS full set, NMOS gm/Id) | PLL design, which lives in [pll-cadence-virtuoso](https://github.com/Tanisha110705/pll-cadence-virtuoso) |
| gm/Id sizing | Layout, DRC, LVS, extraction |
| Current mirrors | Corners, Monte Carlo, noise |
| CS, cascode and active-load amplifiers | Multi-stage / op-amp design |

## Technologies

| Technology | Devices | Studies |
|---|---|---|
| UMC 180 nm (`umc_18`) | N_18_MM, P_18_MM | PMOS characterization, CS amplifier, current mirrors, cascode amplifier |
| n18/p18 devices in a `*_scl` library (PDK not named) | n18, p18 | Active-load amplifier |

All devices use L = 180 nm; VDD = 1.8 V; simulation temperature 27 °C.

## Reading order

1. [mos-characterization.md](mos-characterization.md): device data and λ, γ
2. [gm-id-methodology.md](gm-id-methodology.md): how device data becomes W and V_GS
3. [current-mirrors.md](current-mirrors.md)
4. [common-source.md](common-source.md)
5. [cascode-amplifier.md](cascode-amplifier.md)
6. [active-load.md](active-load.md)
7. [analysis-methods.md](analysis-methods.md): DC / AC / transient / operating regions
8. [results.md](results.md): every number with its evidence
9. [evidence-audit.md](evidence-audit.md): sources, gaps, inconsistencies
10. [reproduction.md](reproduction.md), [repository-guide.md](repository-guide.md)

## Questions this repository answers

| Question | Where |
|---|---|
| What devices were characterized, in what technology? | [mos-characterization.md](mos-characterization.md) |
| How was gm/Id used, and how were sizes chosen? | [gm-id-methodology.md](gm-id-methodology.md) |
| How were the mirrors designed, and how do simple and cascode differ? | [current-mirrors.md](current-mirrors.md) |
| How was the CS amplifier designed, and what gain did it get? | [common-source.md](common-source.md) |
| How was the cascode amplifier designed, and what were gain and bandwidth? | [cascode-amplifier.md](cascode-amplifier.md) |
| How was the active-load amplifier implemented? | [active-load.md](active-load.md) |
| What were the main trade-offs? | [README](../README.md#design-tradeoffs) |
| What simulation evidence exists? | [repository-guide.md](repository-guide.md) |
| What was not characterized, and what comes next? | [evidence-audit.md](evidence-audit.md#missing-evidence), [README](../README.md#future-work) |
