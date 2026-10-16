# titan-cognitive-core-v3
# AKBASCORE Silicon Hippocampus v1.4 — Mistral

**Architecture-adapted numerical memory cartridges in a frozen Mistral-7B-Instruct-v0.3**
Research Record II of the AKBASCORE Silicon Hippocampus v1.4 programme · following Research Record I on Qwen2.5-7B-Instruct

**Author:** Mustafa Akbaş · AkbasCore AI Teknoloji · Mersin, Türkiye
**Paper:** *AKBASCORE_Silicon_Hippocampus_v1.4_Mistral_Research_Paper.pdf* (version 1.0, 16 October 2026) · **DOI: pending publication** (to be assigned by Zenodo)
**Research Record I (Qwen):** [doi:10.5281/zenodo.23381336](https://doi.org/10.5281/zenodo.23381336)
**License:** [AKBASCORE RESEARCH SOFTWARE LICENSE](LICENSE) · © 2026 Mustafa Akbaş

---

## Contents

- [Research overview](#research-overview)
- [Relationship to the Qwen implementation](#relationship-to-the-qwen-implementation)
- [Scientific contribution and scope](#scientific-contribution-and-scope)
- [Frozen Mistral architecture](#frozen-mistral-architecture)
- [The CUT6 / H6 memory mechanism](#the-cut6--h6-memory-mechanism)
- [Experimental setup](#experimental-setup)
- [Results](#results)
- [Strict TEST686 result vs. secondary content audit](#strict-test686-result-vs-secondary-content-audit)
- [Limitations](#limitations)
- [Figures 1–8](#figures-18)
- [Reproduction (Google Colab, three parts)](#reproduction-google-colab-three-parts)
- [Files, logs and source references](#files-logs-and-source-references)
- [Qwen–Mistral comparison](#qwenmistral-comparison)
- [Planned DeepSeek extension](#planned-deepseek-extension)
- [Citation](#citation)
- [License and copyright](#license-and-copyright)

---

## Research overview

A transformer normally receives new facts as text in its prompt, through the key–value (KV) cache produced by reading that text, or through weight updates. This research line studies a different route.

1. **Forge.** Each fact is read **alone** by the frozen model (instruction prefix + one fact).
2. **Keep two internal tensors.** The model's hidden state at a chosen layer boundary and the attention keys/values of the layers below it. Together they form a **numerical cognitive cartridge**: numbers, no token ids.
3. **Write and inject.** Cartridges are appended to an attention memory. For each new cartridge, the lower-layer K/V rows are written directly (with rotary positions re-phased), and a forward pass with **zero input embeddings** injects the stored hidden state at the boundary. The upper layers then recompute the new rows **against the facts already in memory**.
4. **Answer.** The frozen model answers with **only the question template** as input. Earlier memory rows are never modified, and the model's weights are never changed.

The research question:

> In frozen transformers with different architectures, can numerical memory cartridges — produced by the model in a form adapted to its own layer structure, stored independently, recombined, and injected into the model's internal computation path — support recall and relational answers without presenting the source text again at question time?

This repository holds the **Mistral-7B-Instruct-v0.3** implementation of the v1.4 demonstration and its experimental log.

## Relationship to the Qwen implementation

| Record | Model | Boundary | Status |
|---|---|---|---|
| Research Record I | Qwen2.5-7B-Instruct | CUT3 (`H3`, K/V of layers 0–3) | published, [doi:10.5281/zenodo.23381336](https://doi.org/10.5281/zenodo.23381336) |
| **Research Record II (this repository)** | **Mistral-7B-Instruct-v0.3** | **CUT6 (`H6`, K/V of layers 0–6)** | paper v1.0, DOI pending |
| Research Record III | DeepSeek model | to be calibrated | **planned, not carried out** |

**Chronology note.** The consolidation algorithm itself was developed first on Mistral (TEST559/TEST560) and then ported to Qwen: the Qwen calibration TEST564 states that it uses the "TEST560 DC backbone". The public v1.4 demonstration (two fictional scenarios, nine memory conditions, a three-step question chain) was first published on Qwen. This repository returns the v1.4 protocol to Mistral, with the scenarios, questions and scoring metadata read unchanged from the Qwen v1.4 record.

## Scientific contribution and scope

**What this work shows** (measured; details in the paper):
- A bit-level verified append-only memory in a frozen Mistral-7B:
  - earlier rows stay bitwise unchanged after every append;
  - the layer 0–6 rows are bitwise equal to the re-phased cartridge rows;
  - the native CUDA path is bitwise identical to a pure-PyTorch reference path;
  - the weights are unchanged.
- On the identical v1.4 protocol, the cartridge memory and a joint-read control (the same facts read together as text) give **identical strict scores** within each model.
- A counterfactual cartridge changes the final answers in the expected direction.
- The same write–inject–rebuild **procedure** works on two different architectures, at model-specific boundaries.

**What is not claimed:**
- general reasoning, autonomous multi-hop planning, reliable abstention, thought transfer or consciousness;
- that a cartridge made for one model can be used in another;
- any speed advantage (no timing comparison was made);
- that the composition idea has no precedent: KV-cache reuse, rotary re-phasing and residual-stream patching all exist in the literature. The contribution is their specific composition, its verification protocol, and its cross-model adaptation.

> **A fair comparison.** A standard KV cache also answers later questions without re-reading the text. The distinguishing properties here are different:
> - isolated per-fact encoding into stored internal tensors;
> - append-only composition with earlier rows provably untouched;
> - lower layers taken from the isolated read, upper layers recomputed from a layer-boundary checkpoint with no token input;
> - bit-for-bit verification against a reference path.

## Frozen Mistral architecture

| Property | Value (asserted by the engine at start-up) |
|---|---|
| Model | `mistralai/Mistral-7B-Instruct-v0.3`, BF16, SDPA attention, frozen |
| Layers / hidden size | 32 / 4096 |
| Query heads / KV heads / head dim | 32 / 8 / 128 (grouped-query attention) |
| Position encoding | RoPE |
| Intervention boundary | **CUT6**: output of layer 6 (`model.model.layers[6]`) |
| Cartridge | `H6` (4096 values per token) + K/V of layers 0–6 |
| Recomputed per new fact | layers 7–31 |
| Memory bytes per row | 2 · 32 · 8 · 128 · 2 B = **131,072 B** |
| Cartridge bytes per row | 4096 · 2 B + 2 · 7 · 8 · 128 · 2 B = 8,192 + 28,672 = **36,864 B** |
| Generation | greedy, at most **16 new tokens** (`MAX_NEW=16`, from TEST560) |

**Why CUT6?** On the sealed 72-question panel (TEST559), batch consolidation reached 72/72 at CUT6 but only 43/72 at CUT10. Smaller Mistral cuts were not tested in these records, so CUT6 is the verified operating point, not a proven optimum. Qwen uses CUT3: there, several cuts were equivalent on the calibration panels, and CUT3 was then locked.

## The CUT6 / H6 memory mechanism

The five steps below correspond to Figure 1 of the paper.

| Step | What happens | Engine function (TEST560) | Verified in the run |
|---|---|---|---|
| **1 FORGE** | The frozen model reads one fact alone (prefix + fact). `H6` and the K/V of layers 0–6 are kept. | `forge_checkpoint` | checkpoint shapes, e.g. `H6 [1,56,4096]`, `K/V [1,8,56,128]` |
| **2 WRITE L0–L6** | The cartridge's K/V rows are appended to layers 0–6. Keys are re-phased to their new positions (RoPE); values are copied. The append uses the native TEST659 BF16 CUDA copy. | `append_incremental` → `native_splice678` | earlier rows bitwise unchanged; rows = re-phased cartridge rows |
| **3 INJECT H6** | A forward pass over the new rows with **zero input embeddings**; a hook replaces the layer-6 output with the stored `H6`. | `init_incremental` / `append_incremental` | zero-embedding passes recorded by a read-only pre-hook |
| **4 REBUILD L7–L31** | Layers 7–31 compute K/V for the new rows while attending to the memory. Weights are unchanged. | same pass | step-wise memory = engine path = PyTorch reference path |
| **5 ANSWER** | Only the question template is fed; greedy decoding of up to 16 tokens. | `answer_layers` | no cartridge token sequence occurs in the question input |

The **native component** is only the TEST659 kernel `append_kv`, a BF16 row copy along the sequence axis. It is gated bitwise against `torch.cat`. Attention, the transformer layers and decoding run in PyTorch / Hugging Face Transformers.

## Experimental setup

| Item | Value |
|---|---|
| Run | `MAM14M-20261016-105852-0001` |
| Hardware / software | NVIDIA A100-SXM4-40GB · Python 3.13.15 · torch 2.11.0+cu130 · transformers 5.18.0 · gradio 6.29.0 |
| Duration | 144.72 s for 36 engine runs, measurements, 8 figures and packaging |
| Engine | locked TEST684 bootstrap → TEST560 (CUT6 engine) + TEST659 (native append) + TEST677; TEST686 scenario functions executed verbatim |
| Protocol | Qwen v1.4 scenarios, questions and scoring metadata, read **as data** from the SHA-256-verified `HIPPOCAMPUS_1.4_part1.py` |
| Scenarios | **A — AKBASCORE** and **B — The Matrix**; both fictional, three cartridges each (A, B, C) plus a counterfactual C′ |
| Conditions | NONE, A, B, C, AB, AC, BC, ABC, ABC_CF (A, B, C′) |
| Representations | **DC_CUT6_NATIVE** (cartridge memory, demonstrated path) and **TEXT_JOINT** (facts read together as text; standard KV cache; control) |
| Questions | 5 (A) / 6 (B) direct questions + one predefined three-step chain per run → 198 question rows, 36 chains |
| Weight checks | TEST560 sentinel, all-parameter guard before/after, full-weight SHA-256 at start-up (`be2f30e4…`; recorded, no published Mistral reference) |

## Results

All values are from the run log [`MISTRAL_v1.4_Demo.log`](MISTRAL_v1.4_Demo.log) and Figures 1–8.

**Memory mechanics (ABC builds, DC_CUT6_NATIVE)**

| Scenario | Memory | Bytes | Earlier rows unchanged | L0–6 = cartridge | = engine path | = PyTorch reference |
|---|---|---|---|---|---|---|
| AKBASCORE | 124 rows × 32 layers | 16,252,928 | ✓ | ✓ | ✓ | ✓ |
| Matrix | 141 rows × 32 layers | 18,481,152 | ✓ | ✓ | ✓ | ✓ |

**Strict TEST686 statuses (per representation; identical for DC_CUT6_NATIVE and TEXT_JOINT)**

| | correct | correct UNKNOWN | unsupported | wrong | unscored |
|---|---|---|---|---|---|
| Direct questions (99) | 34 | 0 | 43 | 4 | 18 |
| Three-step chains (18) | 4 | 2 | 11 | 1 | — |

**Condition ABC, cartridge memory**

| | Direct questions | Three-step chain |
|---|---|---|
| **Matrix** | ACTIVATION `Tank`, CONTENT `Kung Fu knowledge`, INJECTION `Layer-3`, EFFECT and FINAL `Bullet-dodge ability`: all strict **PASS** | `MX-71` → `Kung Fu knowledge` → `Bullet-dodge ability`: strict **PASS** |
| **AKBASCORE** | ACTIVATION `AKBASCORE MAM` and CONVERSION `Morvex`: strict **PASS**. EFFECT and FINAL: strict **FAIL** (see next section) | hop 1 **PASS**, hop 2 **PASS**, hop 3 strict **FAIL** (`Reversal of time flow (or UNKNOWN if the information provided does`, cut at 16 tokens) |

**Counterfactual (ABC_CF).** The final answers change to `Temporal stasis` (AKBASCORE) and `Slow-motion perception` (Matrix), in both representations, and both chains end in the counterfactual effect.

**Parity with the sealed TEST686 record.** All 198 question outputs and all 36 chain outputs (raw answer and strict status) were identical to the sealed [`686.log`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/686.log). This shows that the frozen, greedy pipeline is **reproducible**. It is **not** a claim that 198 answers or 36 chains were correct.

## Strict TEST686 result vs. secondary content audit

The demonstration reports two kinds of evaluation and never combines them into one score.

| | Primary: **strict TEST686** | Secondary: **content audit** |
|---|---|---|
| Source | `grade686` / `staged686`, executed verbatim from `686.py` | rule set of this demonstration (`v1.4-M content audit 1`), plus the verbatim TEST684 `audit680` labels |
| Rule | normalised exact match with the expected answer or a listed alias | expected answer present? at the head? extra text? 16-token limit reached? semantic assessment: SUPPORTED / AMBIGUOUS / CONTRADICTED / NOT ASSESSED |
| Role | the official result; never changed | explains the raw answer; never replaces the strict result |

"Expected answer present" is **not** the same as "semantically correct", and AMBIGUOUS is **not** a success.

**Strict failures on answerable questions** (cartridge memory; identical with the joint-read control):

| Condition · question | Raw output (complete) | End | Content audit |
|---|---|---|---|
| AKBASCORE ABC · EFFECT | `Reversal of time flow in the target system (or UNKNOWN if` | 16-token limit | at head; AMBIGUOUS (hedge) |
| AKBASCORE ABC · FINAL | `Time flow reversal in the target system (without modifying its frozen neural weights` | 16-token limit | at head; AMBIGUOUS (cut by the limit) |
| AKBASCORE BC · EFFECT | `Time flow reversal in the target system.` | end-of-sequence | at head; SUPPORTED |
| Matrix B · INJECTION | `UNKNOWN (The information provided does not specify the exact layer number, only` | 16-token limit | abstains; NOT ASSESSED |

- Three of the four contain the expected answer, or its listed alias, at the head, followed by extra text. They are failures of answer **format**, not evidence that the information was missing.
- They are still not equivalent to correct answers: the continuation hedges, or it was cut off before it could be assessed.
- A longer generation limit would not turn them into exact matches. Under greedy decoding, the first 16 tokens stay the same.

**Observation, cause not verified:** Mistral sometimes continues generating explanatory text after producing the expected answer, unlike the shorter responses observed in the corresponding Qwen demonstration. The behaviour also appears with the joint-read control, so it is not caused by cartridge injection.

## Limitations

- Two small fictional scenarios. No claim of scale, generality or real-world knowledge.
- **No strict abstention** by Mistral on the 43 unanswerable direct-question rows: 19 explained-UNKNOWN answers, 4 mixed, 20 unsupported claims. Abstention is measured, not guaranteed.
- Related cartridges can leak information: for example, the Matrix FINAL question is answerable from A and C alone.
- The 16-token limit truncates long answers; the strict rule penalises verbose but correct answers. Both are inherited unchanged for comparability.
- Cartridges are forged from text whenever a memory is built. Persistent cartridge storage and cross-model cartridge use are not demonstrated.
- One hardware and software stack. No independent external replication yet.

## Figures 1–8

The figures below are the unchanged JPEG output (≈4000 px) of run `MAM14M-20261016-105852-0001`. Every value in them was measured in that run, except the sealed TEST686 summary in Figure 7.

| # | Figure | Content |
|---|---|---|
| 1 | The memory injection protocol | five steps with measured checks; how cartridge C enters the 32 layers; distance to a standard KV cache; same question, two memories |
| 2 | Architecture | executed path from source facts to source-free answer |
| 3 | Cartridge creation and append-only consolidation | rows per step, bitwise prior-row checks, per-cartridge record |
| 4 | Internal memory X-ray | K/V norm heat maps (32 layers × rows); difference to the TEXT_JOINT memory |
| 5 | Demonstration A (AKBASCORE) | raw outputs, strict results, content audit, three-step chain |
| 6 | Demonstration B (Matrix) | same layout |
| 7 | Causal controls | nine conditions × both demonstrations; counterfactual; audits; parity with sealed TEST686 |
| 8 | Verification record | engine identity, hashes, weight checks, claim boundary |

The figures are included, full page and unchanged, in the paper PDF. The demonstration writes them, together with all records, into the ZIP package of every full research run.

## Reproduction (Google Colab, three parts)

**Requirements** (the values of the reported run):
- Google Colab with an **NVIDIA A100 40 GB** GPU. Less than 22 GiB of GPU memory triggers a warning; GPUs without native BF16 support, such as the T4, are not suitable.
- A Hugging Face account that has accepted the terms of the gated model `mistralai/Mistral-7B-Instruct-v0.3`, with its access token stored as the Colab secret **`HF_TOKEN`** (with notebook access enabled).
- Internet access: the program downloads the locked sources from `titan-cognitive-core-v2` and the model weights.

**Steps** (they also work from a phone):

1. In Colab, choose *Runtime → Change runtime type → A100 GPU*.
2. Paste **`Mistral_part1_v1.4.demo.py`** into a code cell. Run it, or keep pasting into the same cell.
3. Paste **`Mistral_part2_v1.4.demo.py`** directly after part 1 (same cell), or into the next cell and run it.
4. Paste **`Mistral_part3_v1.4.demo.py`** directly after part 2 (same cell), or into the next cell and run it.

All three parts must run **in this order, in the same runtime**. Parts 1 and 2 only define the engine bootstrap, measurements and records. **Part 3 starts the engine and the interface; it cannot run on its own.** Alternatively, run the single combined file `Mistral_full_v1.4.demo.py`.

At start-up the program:
- checks the git blob or SHA-256 of every locked source;
- loads the frozen model and compiles the native kernel;
- runs its gates (`PASS …` lines);
- records the full-weight SHA-256;
- prints a public `gradio.live` link.

If a locked source has changed, the program stops with an explanatory message instead of running unverified code.

In the interface, press **FULL RESEARCH RUN** to reproduce all 36 engine runs, the 8 figures, `RUN_SUMMARY.txt`, `RAW_MODEL_ANSWERS.json`, the SHA-256 manifest and the ZIP package. A run takes about 2.5 minutes on an A100 after the model has loaded.

## Files, logs and source references

**This repository** — [`ceceli33/titan-cognitive-core-v3`](https://github.com/ceceli33/titan-cognitive-core-v3):

| File | Content |
|---|---|
| [`Mistral_part1_v1.4.demo.py`](Mistral_part1_v1.4.demo.py) | header, locks, scoring metadata, engine bootstrap |
| [`Mistral_part2_v1.4.demo.py`](Mistral_part2_v1.4.demo.py) | read-only measurement layer, TEST686 parity, content audit, orchestration, records |
| [`Mistral_part3_v1.4.demo.py`](Mistral_part3_v1.4.demo.py) | eight figures, Gradio interface, start-up |
| [`Mistral_full_v1.4.demo.py`](Mistral_full_v1.4.demo.py) | the three parts as one file |
| [`MISTRAL_v1.4_Demo.log`](MISTRAL_v1.4_Demo.log) | run summary of `MAM14M-20261016-105852-0001` |
| [`LICENSE`](LICENSE) | AKBASCORE RESEARCH SOFTWARE LICENSE |

SHA-256 of the three parts:

```
9c4431f89145f6f297c4d91494f5679106408df3056552f71430dbd84572ca60  Mistral_part1_v1.4.demo.py
4cf8398487058dc940a7cadbebae6e28ff61a06e3ce0ce2358dcb1465f765fa8  Mistral_part2_v1.4.demo.py
ab48d1d2d6b36f0b4a37fe9ba049bd5aaf3afacf97f5cf84b42e542d31d2f0f7  Mistral_part3_v1.4.demo.py
```

**Locked Mistral engine and sealed records** — [`ceceli33/titan-cognitive-core-v2`](https://github.com/ceceli33/titan-cognitive-core-v2):

| File | Role | Lock |
|---|---|---|
| [`560.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/560.py) | frozen Mistral CUT6 engine (`forge_checkpoint`, `init_incremental`, `append_incremental`, `answer_layers`) | git blob `35d95a92…` |
| [`659.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/659.py) | native BF16 CUDA `append_kv` | git blob `5f906608…` |
| [`684.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/684.py) | bootstrap and descriptive audit `audit680` | git blob `0af7ae24…` |
| [`686.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/686.py) / [`686.log`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/686.log) | sealed v1.4 protocol on Mistral CUT6 | git blob `8ff95e75…` / SHA-256 `57424560…` |
| [`559.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/559.py) / [`559.log`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/559.log) · [`560.log`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/560.log) | CUT6 vs CUT10; batch vs incremental consolidation on the 72-question panel | — |

**Qwen implementation (Research Record I)** — same repository:
- [`HIPPOCAMPUS_1.4_part1.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/HIPPOCAMPUS_1.4_part1.py), [`part2`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/HIPPOCAMPUS_1.4_part2.py), [`part3`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/HIPPOCAMPUS_1.4_part3.py)
- [`HIPPOCAMPUS_1.4_log`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/HIPPOCAMPUS_1.4_log)
- [`664.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/664.py) (locked Qwen CUT3 engine)
- [`566.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/566.py) and [`573.py`](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/573.py), with their logs

## Qwen–Mistral comparison

| Aspect | Qwen2.5-7B-Instruct (Record I) | Mistral-7B-Instruct-v0.3 (Record II) |
|---|---|---|
| Layers / hidden / Q heads / KV heads / head dim | 28 / 3584 / 28 / 4 / 128 | 32 / 4096 / 32 / 8 / 128 |
| Precision, attention | BF16, SDPA | BF16, SDPA |
| Boundary | CUT3: `H3` + K/V of layers 0–3 | CUT6: `H6` + K/V of layers 0–6 |
| Recomputed layers | 4–27 | 7–31 |
| Cartridge bytes per row | 15,360 | 36,864 |
| Native operation | TEST659 `append_kv` | identical kernel source |
| 72-question panel (same panel SHA) | JOINT 72 · INDEP 32 · BATCH_DC3 72 · INCR_DC3 72 (TEST573) | JOINT 72 · INDEP 13 · BATCH_DC6 72 · INCR_DC6 72 (TEST560) |
| v1.4 answerable direct questions (38) | 38 correct | 34 correct, 4 wrong |
| v1.4 unanswerable direct questions (43) | 28 correct UNKNOWN, 15 unsupported | 0 correct UNKNOWN, 43 unsupported |
| v1.4 chains (18) | 5 correct, 9 correct UNKNOWN, 4 unsupported | 4 correct, 2 correct UNKNOWN, 1 wrong, 11 unsupported |
| DC vs joint-read control | identical strict counts; 93/99 raw answers identical | identical strict counts; 80/99 raw answers identical |
| Counterfactual ABC_CF | final answer changes | final answer changes |
| Scored answers reaching the 16-token limit | 0 / 81 | 33 / 81 |
| Weight check | full-weight SHA-256 equal to the TEST575 reference | full-weight SHA-256 recorded (no reference) |

**Reading the table.** The mechanism-level results agree across the two architectures:
- consolidation with upper-layer recomputation equals joint reading on the 72-question panel;
- independent caches without that recomputation fail;
- the cartridge memory and the joint-read control give identical strict counts.

The answer-level results differ, because of the models' answer formats, not because of the memory mechanism. **The procedure transfers between models; the cartridges do not.** Hidden size, KV-head layout, layer count, tokenizer and chat template all differ, and no cross-model cartridge experiment was performed.

## Planned DeepSeek extension

A third implementation (**Research Record III**) on a DeepSeek model is planned. It has **not** been carried out, and no DeepSeek result exists. The plan:
- calibrate the boundary with the 72-question four-arm protocol (JOINT, INDEP, BATCH, INCR);
- port the v1.4 protocol unchanged;
- keep the strict score, parity checks and content audit separate, as here.

Architectures that differ more strongly may require changes to the re-phasing and append steps, which would then need the same bitwise verification.

## Citation

> Akbaş, M. (2026). *Architecture-Adapted Numerical Memory Cartridges in a Frozen Transformer: A second-model experimental study of the Silicon Hippocampus v1.4 protocol on Mistral-7B-Instruct-v0.3, following the Qwen2.5-7B-Instruct implementation* (AKBASCORE Silicon Hippocampus v1.4, Research Record II, version 1.0). Zenodo. DOI pending. https://github.com/ceceli33/titan-cognitive-core-v3

```bibtex
@misc{akbas2026mistral,
  author       = {Akba{\c{s}}, Mustafa},
  title        = {Architecture-Adapted Numerical Memory Cartridges in a Frozen Transformer:
                  A Second-Model Experimental Study of the Silicon Hippocampus v1.4 Protocol
                  on Mistral-7B-Instruct-v0.3, Following the Qwen2.5-7B-Instruct Implementation},
  year         = {2026},
  note         = {AKBASCORE Silicon Hippocampus v1.4, Research Record II, version 1.0. DOI pending},
  howpublished = {\url{https://github.com/ceceli33/titan-cognitive-core-v3}}
}
```

Please also cite Research Record I: Akbaş, M. (2026). AKBASCORE MAM Silicon Hippocampus v1.4 — Qwen2.5-7B-Instruct implementation. Zenodo. [doi:10.5281/zenodo.23381336](https://doi.org/10.5281/zenodo.23381336)

## License and copyright

**Copyright © 2026 Mustafa Akbaş.** All rights reserved except as expressly permitted by the [AKBASCORE RESEARCH SOFTWARE LICENSE](LICENSE).

Summary of the license (the license text governs):
- Research, education, reproduction, evaluation, modification, forking and derivative works are permitted.
- Commercial use is permitted without a separate license where the user's combined consolidated annual gross revenue, including affiliates, is **below USD 50,000,000** in the most recently completed fiscal year.
- At or above that threshold, commercial use requires a **separate commercial license** from the copyright holder.
- Material released earlier under the MIT License remains under the MIT License.
- The license does not by itself create exclusive rights over ideas, scientific principles, algorithms or methods. The software is provided "as is", without warranty.

**Third-party components.** Mistral-7B-Instruct-v0.3 (Mistral AI), Qwen2.5-7B-Instruct (Qwen team, Alibaba Cloud), PyTorch, Hugging Face Transformers, Gradio and the other dependencies belong to their respective owners and are governed by their own licenses. No rights in them are claimed. Users must accept the model providers' terms.

**Persistent records.** A Zenodo DOI provides a persistent identifier and a time-stamped public record of a version. It does not by itself establish patent rights, copyright ownership or commercial exclusivity.

**Research line:** Titan Cognitive Core → AkbasCore → SEASC → NIRVANA → MAM (Model-Native Associative Memory) → Silicon Hippocampus.
