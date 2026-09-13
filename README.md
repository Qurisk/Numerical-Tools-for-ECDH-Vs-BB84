# Numerical Tools for ECDH vs. BB84

Numerical companion to our paper **A Unified Channel-Error Framework for Comparative Performance and Security Analysis
of Classical and Quantum Key Establishment**.
Reproduces the two figures reported in the paper and provides break-even solvers for the key-provisioning comparison.


## Motivation

ECDH and BB84 quantum key distribution both
establish shared key material; they are usually compared solely on the basis of their security guarantees. But another interesting factor to compare is how they degrade differently as a *communication channel* gets noisier.

This repo provides numerical tools that make the comparison concrete through a shared channel-error coordinate `eps_ch`, along two axes:

1. **Reliability:** ECDH must deliver a public key intact; a single flipped bit invalidates the exchange, so the failure probability grows with the key length `npk` unless a forward error-correcting code absorbs the errors. BB84 instead aborts when the observed QBER exceeds its security threshold. Figure 1 compares P-256, P-384, and P-521 without coding, together with two BCH-coded P-256 operating points.

2. **Key-Provisioning Behaviour:** Figure 2 compares the effective key-provisioning index
   `R_KP` of the two schemes: for ECDH, the security strength delivered per
   transported public-key bit, scaled by the channel capacity; for BB84, the
   asymptotic secret-key fraction scaled by the sifted detection yield, over a
   range of fibre lengths. Their crossing identifies where the two provisioning
   indices are equal under the adopted normalization.


## Requirements

Python 3.10 or newer with NumPy, SciPy and Matplotlib.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

`requirements.txt` pins the exact versions used to produce the published
figures (NumPy 2.5.3, SciPy 1.18.1, Matplotlib 3.11.1 on Python 3.14.4).


## Usage

```bash
.venv/bin/python ECDHvsQKD_perf_chan.py                       # Figure 1 of section 5
.venv/bin/python effective_key_material_provisioning_rate.py  # Figure 2 of section 5
.venv/bin/python solver.py                                    # break-even solvers
```

Each numerical script writes its vector output(s) to `figures/`:

| Script | Figure(s) written | Also printed |
| --- | --- | --- |
| `ECDHvsQKD_perf_chan.py` | `figures/failure_probability.pdf` | expected number of sifted detections |
| `effective_key_material_provisioning_rate.py` | `figures/provisioning_rate.pdf` | — |
| `solver.py` | `figures/break_even_distance.pdf`, `figures/break_even_channel_error.pdf` | break-even distance and break-even channel-error coordinate |

`figures/` is regenerated on every run and is not tracked by git; drop the
entry from `.gitignore` to version the output alongside the source.


## Repository map

![Repository architecture](docs/architecture.png)

*All numerical scripts use the shared configuration and model modules; the analytical formulas remain centralized in `model.py`.*

| File | Role |
| --- | --- |
| `config.py` | **Every adjustable quantity.** Physical parameters, curve and code tables, sweep grids, figure selections, and break-even solver inputs. Start here. |
| `model.py` | Closed-form model: one function per analytical expression, no configuration and no plotting. |
| `ECDHvsQKD_perf_chan.py` | Figure 1: protocol-level failure probability vs. channel-error coordinate. |
| `effective_key_material_provisioning_rate.py` | Figure 2: key-provisioning index vs. channel-error coordinate. |
| `solver.py` | Solves the RKP break-even condition either for fibre distance at fixed `eps_ch` or for `eps_ch` at fixed distance, and plots both intersections. |
| `requirements.txt` | Pinned dependency versions. |
| `docs/` | Repository architecture diagram and its generation script. |

The numerical scripts do not duplicate the analytical model: they select parameters from `config.py`, call the functions in `model.py`, and assemble the requested figures or break-even calculation. Changes to operating parameters, curve selections, or solver brackets belong in `config.py`; changes to the analytical model belong in `model.py`.


## Configuring a run

All edits happen in `config.py`, which is divided into commented sections.

- **Physical parameters**: `ETA_DET`, `PD`, `P_B`, `ALPHA`. These are the
  values behind the published figures.
- **Curves and codes**: `CURVES` maps a curve name to its security strength
  and uncompressed public-key length; `CODES` maps a (curve, code) pair to its
  `(n, k, t, number of codewords)`. Adding a row makes it available to both
  figures.
- **Curve selection**: `FIG1_UNCODED`, `FIG1_CODED`, `FIG2_CURVES`,
  `FIG2_DISTANCES_KM` list what each figure draws. Removing an entry drops the
  curve; no plotting code needs editing.
- **Break-even solver operating point**:
  `SOLVER_CURVE` selects the ECDH reference curve.
  `ETA_DET_CUSTOM`, `PD_CUSTOM`, `P_B_CUSTOM`, and `ALPHA_CUSTOM`
  define the BB84 operating point used by both solver modes.
  With the current defaults, only `ETA_DET_CUSTOM = 0.70` differs from
  the parameters used for the published Figure 2.
- **Distance solver**:
  `ECH_TARGET` fixes the channel-error coordinate and
  `D_BRACKET_KM` defines the distance interval searched by Brent's method.
- **Channel-error solver**:
  `D_TARGET_KM` fixes the fibre distance and
  `ECH_BRACKET` defines the channel-error interval searched by Brent's method.
- **Solver plotting**:
  `SOLVER_PLOT_POINTS` controls only the smoothness of the two solver figures;
  it does not control the numerical accuracy of Brent's root finder.

The Brent intervals are numerical search brackets, not physical limits of the model. A root is guaranteed to be bracketed when the RKP difference changes sign between the two endpoints. If both endpoints have the same sign, the solver reports that no sign change is bracketed; this statement alone does not prove that no root exists elsewhere or that no multiple crossings exist inside an arbitrary interval. Inspect or adjust the bracket when this occurs.

## Break-even solver

The solver uses the difference

`g(eps_ch, d) = R_KP^BB84(eps_ch, d) - R_KP^ECDH(eps_ch)`,

so a root of `g` is exactly the break-even condition

`R_KP^BB84 = R_KP^ECDH`.

The two solver modes answer different link-planning questions.

### 1. Known channel-error level: solve for fibre distance

If a channel-error coordinate `eps_ch` can be guaranteed, the distance solver
keeps `eps_ch` fixed and solves

`R_KP^BB84(eps_ch, d*) = R_KP^ECDH(eps_ch)`.

The resulting `d*` is the distance at which the two provisioning indices are equal. Under the adopted model and when BB84 has the larger index on the lower-distance side of the crossing, `d*` acts as the maximum fibre distance for which that ordering is retained.

This mode is useful when several candidate BB84 links are evaluated under the same assumed channel-error level. Rather than entering every link distance individually, the user can solve once for `d*` and compare each candidate distance against the resulting boundary.

The generated figure `figures/break_even_distance.pdf` plots both provisioning indices against fibre distance and marks the numerical intersection.

### 2. Known fibre distance: solve for channel-error level

If the fibre distance is already known, the channel-error solver keeps that distance fixed and solves

`R_KP^BB84(eps_ch*, d) = R_KP^ECDH(eps_ch*)`.

The resulting `eps_ch*` is the channel-error coordinate at which the two provisioning indices are equal. When BB84 has the larger index on the lower-error side of the crossing, `eps_ch*` is the maximum admissible channel-error level for retaining that ordering under the selected model parameters.

This mode is useful for a specific BB84 link whose physical length is fixed:
instead of manually sweeping candidate error levels, the solver returns the break-even channel-error target directly.

The generated figure `figures/break_even_channel_error.pdf` plots both provisioning indices against `eps_ch` and marks the numerical intersection.



With the default solver configuration (`ETA_DET_CUSTOM = 0.70`, `SOLVER_CURVE = "P-256"`), the current examples give approximately

- `d* = 11.553583 km` for `eps_ch = 0.05`;
- `eps_ch* = 0.02389293` for `d = 18 km`.

These values belong to the custom solver operating point and should not be confused with the approximately 25 km low-error crossover discussed for the different parameter set used in Figure 2 of the paper.


## Model

Implemented in `model.py`, one function per equation:

| Quantity | Function |
| --- | --- |
| Fibre transmittance `10^(-alpha d / 10)` | `transmittance` |
| Basis-match probability `p_B^2 + (1-p_B)^2` | `basis_match` |
| Sifted yield `p_BS (eta + (1-eta) p_d)` | `sifted_yield` |
| QBER `(eta e + (1-eta) p_d / 2) / (eta + (1-eta) p_d)` | `qber` |
| Binary entropy `H2` | `binary_entropy` |
| Secret-key fraction `max(0, 1 - 2 H2(Q))` | `secret_fraction` |
| BB84 rate | `rate_bb84` |
| ECDH rate `St / (2 npk) * (1 - H2(e))` | `rate_ecdh` |
| BB84 abort probability | `p_abort_bb84` |
| Uncoded public-key failure `1 - (1-e)^npk` | `p_fail_uncoded` |
| Coded public-key failure | `p_fail_coded` |
| Two-way exchange failure `1 - (1-p)^2` | `p_fail_exchange` |
