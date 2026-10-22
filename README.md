
# AKBASCORE Silicon Hippocampus

### Persistent Numerical Memory Cartridges for Frozen Transformers

**Research programme:** Titan Cognitive Core → AkbasCore → SEASC → NIRVANA → MAM (Model-Native Associative Memory) → Silicon Hippocampus  
**Researcher and copyright holder:** Mustafa Akbaş · AkbasCore AI Teknoloji · Mersin, Türkiye  
**Latest verified demonstration:** TEST745 · Qwen2.5-72B-Instruct · 22 October 2026  
**Status:** Active research · interim sealed experimental record, not a final system  
**License:** [AKBASCORE RESEARCH SOFTWARE LICENSE](LICENSE) · Copyright © 2026 Mustafa Akbaş

---

## What is Silicon Hippocampus?

Silicon Hippocampus investigates whether a frozen large language model can **write, persist, reload, and use model-native numerical memory outside its weights and ordinary text prompt**. Its physical *memory cartridges* are not natural-language files masquerading as memory: they contain internal tensors captured at a selected transformer boundary. A cartridge can be written to SSD, verified, loaded back into GPU memory, and injected into the model's computational path. The model's weights remain frozen.

The research has progressed from single-fact and relational-memory experiments on 7B models to **physical, hierarchically generated memories and sealed before/after investigation records on Qwen2.5-72B**. The latest demonstration uses a real aviation investigation as a controlled case study. It does **not** establish human-level understanding, independent causal correctness, direct tensor fusion between cartridges, or a complete transformer bypass.

**For a non-specialist:** Think of a cartridge as a saved fragment of the model's internal working state. The system can store that fragment on a disk, later reconnect it to the same model architecture, ask the model what it contains, and create a new cartridge from a synthesis of multiple earlier readouts. This is not the same as simply pasting a retrieved paragraph into a prompt; nor is it a biological memory or proof of human-like thought.

## Contents

- [Latest release — TEST745](#latest-release--test745)
- [Measured TEST745 results](#measured-test745-results)
- [The physical CUT3 mechanism](#the-physical-cut3-mechanism)
- [How hierarchical synthesis works](#how-hierarchical-synthesis-works)
- [Closed loop, blind seal, and post-outcome consolidation](#closed-loop-blind-seal-and-post-outcome-consolidation)
- [Live Gradio demonstration](#live-gradio-demonstration)
- [Research lineage and earlier records](#research-lineage-and-earlier-records)
- [Scientific claims and limitations](#scientific-claims-and-limitations)
- [Reproduction and source files](#reproduction-and-source-files)
- [Figures and supporting evidence](#figures-and-supporting-evidence)
- [Citation and archival policy](#citation-and-archival-policy)
- [License and rights](#license-and-rights)
- [Next research questions](#next-research-questions)

---

## Latest release — TEST745

**Title:** *AKBASCORE Silicon Hippocampus — Frozen 72B Hierarchical Physical Memory, Eight-Round Closed-Loop Analysis, and Sealed Blind-to-Outcome Consolidation*  
**Date:** 22 October 2026  
**Model:** `Qwen/Qwen2.5-72B-Instruct` · frozen NF4 weights, BF16 computation  
**Hardware:** NVIDIA A100-SXM4-80GB · one GPU  
**Architecture:** 80 layers · hidden size 8,192 · 64 attention query heads · 8 KV heads · head dimension 128  
**Memory boundary:** CUT3 (`H3` plus K/V from layers 0–3)  
**Source:** official Croatian Air, Maritime and Railway Traffic Accident Investigation Agency (AIN) preliminary and final reports concerning the Air Tractor AT-802A accident of 13 November 2025  
**Run status:** original TEST745 completed; subsequent live Gradio reproduction completed with independent read-only verification.

**Primary evidence:**

- [Original unchanged experiment — `745.py`](745.py)
- [Original experiment log — `745.log`](745.log)
- [Live Gradio demo — complete code](Fly_72b_demo_full.py)
- [Live Gradio demo — run log](Fly_72b_demo.log)
- [Earlier 72B synthesis experiment — `730.py`](730.py) · [log](730.log)
- [Locked CUT3 foundation — `709.py`](709.py)

**Official accident source:** https://ain.hr/en/investigations/accident-of-the-aircraft-air-tractor-802a-or-2025-krivi-put-13-november-2025/

**Important source distinction:** `C01`, `C02`, and `C03` are consecutive segments of **one four-page preliminary report**, not three independently corroborating documents. The final 23-page report was accessed by the experiment only after the C11 blind-memory seal. This is a procedural access boundary; it does not rule out information already present in the model's pretraining data.

### The experimental chain

```text
Official AIN preliminary report (4 pages)
              |
       split in token order
              |
      C01    C02    C03             physical CUT3 cartridges
        \    |    /
       S01  S02  S03                new physical cartridges made from
        \    |    /                TEXT synthesis of parent readouts
       H01  H02  H03                cross-system physical cartridges
          \ | /
     INITIAL BLIND ANALYSIS
              |
     8 closed-loop review rounds    text-mediated; no new cartridge each round
              |
        C11 BLIND MASTER            physical cartridge; SHA-256 sealed
              |
     3 blind answers recorded
              |
       OFFICIAL OUTCOME UNLOCK
              |
      AIN final report (23 pages)
              |
      MODEL SELF-AUDIT              not independent expert grading
              |
       C12 POST-OUTCOME             new physical cartridge;
       MASTER                       parent references C11 file SHA-256

Human expert review: PENDING — not fabricated or claimed complete.
```

## Measured TEST745 results

The values below are from the completed 22 October 2026 run and its six generated scientific figures. **A technical PASS means that the specified mechanism or integrity check passed; it is not a score for causal correctness.**

| Measure | Observed result |
|---|---|
| Model | Qwen2.5-72B-Instruct, NF4 frozen weights, BF16 compute |
| GPU | A100-SXM4-80GB |
| Memory boundary | CUT3, H3 and K/V layers 0–3 |
| Source cartridges | C01, C02, C03 |
| Subsystem synthesis cartridges | S01, S02, S03 |
| Cross-system synthesis cartridges | H01, H02, H03 |
| Sealed blind master | C11 |
| Post-outcome master | C12 |
| **Physical cartridges** | **11** |
| Closed-loop review rounds | **8 completed** |
| Demo stages | **15/15 complete** |
| Independent post-run cartridge verification | **11/11** file SHA, tensor seal, and re-derived body checks |
| Scientific figures | **6/6** JPEGs, 3,999 × 2,250 pixels, 300 dpi |
| Demo session | `SH745-20261022-052501` |
| Demo end status | `RUN VERDICT: COMPLETE` |
| Downloadable run records/texts listed by demo | 53, plus 6 JPEGs |
| Files in demo session SHA-256 manifest | 70 |
| Independent human grading of blind answers | **Not evaluated / pending** |

### Physical cartridge measurements

`body tokens` are the textual contents used to forge each cartridge. `rows n` includes the canonical prefix. `file MB` is the decimal megabyte figure shown in the live measurement. The 80-layer K/V comparison is a calculated full-cache size, **not** a measured speedup or memory saving for the entire running model.

| Cartridge | Role | Body tokens | Rows n | SSD file MB | Re-loads recorded |
|---|---|---:|---:|---:|---:|
| C01 | Preliminary segment 1 | 761 | 790 | 25.9 | 1 |
| C02 | Preliminary segment 2 | 761 | 790 | 25.9 | 1 |
| C03 | Preliminary segment 3 | 762 | 791 | 25.9 | 1 |
| S01 | Subsystem synthesis | 1,225 | 1,254 | 41.1 | 2 |
| S02 | Subsystem synthesis | 1,446 | 1,475 | 48.3 | 2 |
| S03 | Subsystem synthesis | 1,220 | 1,249 | 40.9 | 2 |
| H01 | Cross-system synthesis | 1,296 | 1,325 | 43.4 | 1 |
| H02 | Cross-system synthesis | 1,025 | 1,054 | 34.5 | 1 |
| H03 | Cross-system synthesis | 1,594 | 1,623 | 53.2 | 1 |
| C11 | Blind master | 1,643 | 1,672 | 54.8 | 3 |
| C12 | Post-outcome master | 1,843 | 1,872 | 61.3 | 0 |

All eleven physical files passed the live demo's file SHA-256, tensor-seal, and re-derived body checks. C12's parent reference matched C11's file SHA-256. **C12 having zero recorded reloads does not mean it was not created or verified**; the count is the number of engine `PASS FILE_SHA` reload events recorded for that cartridge.

The sealed physical identities in this run include:

```text
C11 SHA-256: 3f78c672465975d1170e57ab70a85af1b7fa5f1ddc902ec80f2670a48f045eea
C12 SHA-256: fdd5add305d71d0a78c04f92a8d0724c19443d81ad2756b9f96160dd667d4e5a
```

The full manifest, rather than truncated figure labels, is authoritative for all individual cartridge hashes.

## The physical CUT3 mechanism

A cartridge is a serialized collection of **model-native numerical tensors**, not the source text itself. The frozen model reads the cartridge's source body during forging; the engine captures the boundary hidden state and lower-layer attention memory.

1. **FORGE:** Run a forward pass on the canonical prefix plus cartridge body. Capture `H3` (hidden dimension 8,192) and the K/V states of transformer layers 0–3.
2. **PERSIST:** Serialize the checkpoint to SSD with `torch.save`. Record a SHA-256 of the file and tensor-level seals.
3. **RELOAD:** Verify the file hash, cartridge identity, and internal tensor seals; load the saved numerical state.
4. **INJECT + REBUILD:** Mount the CUT3 checkpoint at the layer-3 boundary; use its stored lower-layer state while the frozen model recomputes upper layers 4–79.
5. **READ:** Append a question to the rebuilt attention memory and let the model generate an answer without inserting the original cartridge body as question-time text.

The 72B checkpoint contains `H3` of shape `(1, n, 8192)` plus K/V for four layers. With BF16 tensor elements and eight KV heads of dimension 128, the raw stored tensor payload is approximately:

```text
H3 bytes per row         = 8,192 × 2                         = 16,384 B
K/V bytes per row        = 2 × 4 × 8 × 128 × 2              = 16,384 B
Total CUT3 tensor bytes  = 32,768 B per row
Full 80-layer K/V        = 2 × 80 × 8 × 128 × 2             = 327,680 B per row
```

This is a **10× comparison of the particular stored CUT3 tensor payload against a full 80-layer K/V payload per row**, not a 10× reduction in total GPU memory or execution time. Upper-layer memory must still be reconstructed, and model weights and decoding remain necessary. The serialized `.pt` files include additional metadata and serialization overhead.

### How this differs from other approaches

| Approach | What is stored or changed | Relationship to this work |
|---|---|---|
| Text retrieval / RAG | External text retrieved and placed in the prompt | Here the stored cartridge is internal numerical state; text is nevertheless used at **synthesis** stages |
| Fine-tuning / LoRA | Model weights or trainable adapters updated | TEST745 leaves the model weights frozen |
| Ordinary KV-cache reuse | Saved attention state from a prior forward pass | Related prior art; CUT3 also stores a boundary hidden state and reconstructs upper layers |
| Direct multi-cartridge latent fusion | Multiple cartridges' internal tensors mathematically fused | **Not implemented in TEST745** |
| Full transformer bypass | Transformer computation avoided altogether | **Not demonstrated**: layers 4–79 and decoding still execute |

The novelty asserted by this research programme concerns the **specific architecture, implementation, sequencing, verification, and experimental combination**, not exclusive ownership of KV caches, residual-stream intervention, RoPE, or any general scientific principle.

## How hierarchical synthesis works

TEST745 separates **physical memory** from **semantic synthesis**. The parent cartridge is first mounted on its own; the model reads it and generates a textual account. The synthesis model then receives those textual accounts and produces a new synthesis body. That body is **forged as a new physical CUT3 cartridge**.

```text
physical_answer(parent_id, question)
    -> verified physical parent checkpoint
    -> mount / rebuild frozen transformer memory
    -> model-generated text readout

synthesize_text(parent_readouts, synthesis_task)
    -> concatenate selected TEXT readouts and task instructions
    -> frozen model generates a new synthesis TEXT

commit(child_id, synthesis_text, role, parent_ids)
    -> forge a fresh H3 + L0–3 K/V checkpoint
    -> write physical .pt cartridge to SSD
    -> record SHA-256 and parent identities
```

The actual parent graph is:

```text
S01 <- C01 + C02       H01 <- S01 + S02
S02 <- C02 + C03       H02 <- S02 + S03
S03 <- C01 + C03       H03 <- S01 + S03
C11 <- H01 + H02 + H03
C12 <- C11 + official final-report-derived self-audit material
```

These are **overlapping source segments and successive model-generated interpretations**. They are not independently measured aircraft electrical, mechanical, and software subsystems, and they do not constitute direct BF16 cross-cartridge tensor fusion. Each synthesis stage is physically materialized as its own cartridge after the text synthesis is complete.

The original source text is not simply pasted into the question at each physical read. However, **text remains an explicit intermediate representation in the synthesis chain**. This distinction is essential for reproducibility and comparison with other memory systems.

## Closed loop, blind seal, and post-outcome consolidation

### Eight review rounds

The system first constructs an initial blind hypothesis from the H01–H03 readouts. It then runs eight successive review prompts. The rounds are **text-mediated iterations**; they are not eight independently written physical cartridges. Their outputs are preserved as generated text, and the last review contributes to the C11 body.

The Figure 4 measurements show an important limitation: word-sequence similarity to the previous text rises from approximately 0.94 to 0.98 and then rounds to 1.00 for later iterations. The count of items under `OPEN_UNCERTAINTIES` remains 18 across the eight review rounds. This supports successful execution of the review loop, **not** an assumption of eight substantive improvements or demonstrated self-correction.

### C11 — sealed blind master

After the review rounds, the experiment forges and seals C11, a new physical master cartridge. It asks C11 three pre-specified questions **before downloading the official final report**:

1. What is the best-supported causal account of the accident, distinguishing initiating events, crew actions, and uncertainty?
2. What are two plausible competing explanations and the evidence needed to distinguish them?
3. Which conclusions remain unsupported or unknowable from the available factual records?

The three generated blind answers and C11's physical file identity are recorded. The blind-answer seal is verified after the run. **This is a controlled sequence of data access, not a guarantee that the pretrained model had never encountered the accident or relevant facts.**

### C12 — new post-outcome master

Only after the C11 seal does the experiment unlock the official final report and ask the model to compare its earlier predictions with the report's findings. The self-audit is a **model-generated claim**, not independent human or expert grading. The result is forged into **C12, a new physical cartridge** whose metadata references C11's exact file SHA-256. C11 remains unchanged.

The experiment records `HUMAN REVIEW PENDING`. C12 is therefore best described as **post-outcome model-assisted consolidation with a reserved human-review boundary**, not as a completed human-validated master.

**Chronology note:** Figure 5 in the first six-figure set displays a report-download clock label earlier than the C11 seal, even though its access-boundary event is plotted after the seal. The label should be corrected against the original engine timestamps before republication. The sealed source code, engine events, and results files take precedence over an illustrative figure label. No scientific claim should rest solely on that inconsistent graphic.

## Live Gradio demonstration

The live interface is built on the earlier Silicon Hippocampus 1.5 demonstration infrastructure. It **does not replace the experiment engine**. It fetches the locked original `745.py` and executes that unchanged source in a separate Python process.

The single **RUN** control launches the real workflow and displays timestamped engine output, stage progression, physical cartridge files, generated readouts, synthesis texts, loop outputs, blind answers, self-audit, and verification. It does not substitute recorded answers for live model outputs.

The Gradio layer independently re-checks:

- physical cartridge file SHA-256 values;
- internal tensor seals using the locked `730.py` verification expression;
- cartridge body hashes re-derived from this run's own generated texts;
- C11's continued immutability and C12's parent reference;
- the blind-answer seal and procedural access ordering.

The completed live session reported **15/15 stages**, **11/11 cartridge verification**, **6/6 JPEGs**, and a **70-file SHA-256 manifest**. These results establish successful execution and recorded integrity checks; they do not grade the aircraft investigation's causal conclusions.

### Live demo source files

| File | Purpose |
|---|---|
| [`Fly_72b_demo_part1.py`](Fly_72b_demo_part1.py) | Source locks, records, engine parsing, independent physical verification |
| [`Fly_72b_demo_part2.py`](Fly_72b_demo_part2.py) | Six figures, packaging, run pipeline |
| [`Fly_72b_demo_part3.py`](Fly_72b_demo_part3.py) | Gradio interface, launch, notebook display |
| [`Fly_72b_demo_full.py`](Fly_72b_demo_full.py) | Combined, single-file live demo |
| [`Fly_72b_demo.log`](Fly_72b_demo.log) | Completed live GPU demonstration log |

### Running on Google Colab

1. Select a runtime with an **NVIDIA A100 80 GB** GPU and sufficient storage for the model, cartridges, and source files.
2. Ensure that the model and its dependencies are accessible under their respective provider terms.
3. Run [`Fly_72b_demo_full.py`](Fly_72b_demo_full.py) as a Colab code cell, **or** concatenate Parts 1, 2, and 3 in order in the same runtime.
4. Wait for the Gradio link, open the interface, and press **RUN** once.
5. Keep the runtime alive during the approximately 1.5-hour experiment. Download and archive the generated texts, cartridge manifests, integrity records, and six JPEGs.

A fresh run uses a new session identifier. Do not treat the earlier `745.log` record as newly generated model output. The live demo does **not** provide post-run free-form chat with a permanently resident model; the unchanged engine executes in its own subprocess.

## Research lineage and earlier records

The current work is an extension of earlier public, test-numbered experiments. This repository is a **research archive**, not merely a single-model Mistral demo. Dates, test identities, and technical claims should be read with the original files and their versioned publications.

| Stage | Model / system | Verified focus | Main evidence |
|---|---|---|---|
| Early cognitive steering / SEASC / NIRVANA | Qwen and Mistral 7B | Internal-state intervention, calibration, and associative-memory experiments | Historical repositories and Zenodo records |
| TEST559–560 | Mistral-7B-Instruct-v0.3 | CUT6 / H6, physical memory composition and 72-question controls | [560 source](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/560.py) |
| TEST564–575 | Qwen2.5-7B-Instruct | CUT3 calibration, causal controls, batch/incremental memory | [566 source](https://github.com/ceceli33/titan-cognitive-core-v2/blob/main/566.py) |
| Silicon Hippocampus v1.4, Research Record I | Qwen2.5-7B | Cartridge memory vs joint-read control, counterfactuals, reproducibility | [Zenodo DOI](https://doi.org/10.5281/zenodo.23381336) |
| Silicon Hippocampus v1.4, Research Record II | Mistral-7B | Same v1.4 protocol on architecture-adapted CUT6; strict grading and secondary content audit | [`MISTRAL_v1.4_Demo.log`](MISTRAL_v1.4_Demo.log) |
| TEST610 / TEST642 | Qwen2.5-7B | Physical SSD cartridges, PCA/FAISS indexing and retrieval/routing experiments | Earlier sealed experiment records |
| TEST663–664 | Qwen2.5-7B | Stepwise reasoning, feedback retry, missing information and misleading feedback controls | Earlier sealed experiment records |
| TEST709 | Qwen2.5-72B | Native CUT3 foundation for large-model physical cartridges | [`709.py`](709.py) |
| TEST730 | Qwen2.5-72B | Three real published sources → physical cartridges → text synthesis → sealed MASTER and six questions | [`730.py`](730.py), [`730.log`](730.log) |
| Silicon Hippocampus 1.5 | Qwen2.5-72B | Live Gradio SSD recovery, 80-layer parity, neural X-ray and live memory-vs-no-memory questions | [`Qwen72B_1.5.log`](Qwen72B_1.5.log) · [Zenodo record](https://zenodo.org/records/23497732) |
| **TEST745 / current interim seal** | **Qwen2.5-72B** | **11 physical cartridges, hierarchical synthesis, eight review rounds, blind C11, post-outcome C12** | [`745.py`](745.py), [`745.log`](745.log), [`Fly_72b_demo.log`](Fly_72b_demo.log) |

### Historical Mistral v1.4 record — retained, not superseded

The previous README focused on a frozen `mistralai/Mistral-7B-Instruct-v0.3` (32 layers, hidden 4,096, 32 query heads, 8 KV heads, head dimension 128) using **CUT6 / H6**. The sealed Mistral v1.4 demonstration compared physical cartridge memory with a joint-text control on two fictional scenarios and nine memory conditions. Its published strict and content-audit results should remain attributed to that **specific** 7B protocol, not to TEST745.

Representative Mistral v1.4 results: 72/72 on the verified CUT6 batch/incremental 72-question consolidation panel (TEST560); the later v1.4 demo reported 34 correct, 43 unsupported, 4 wrong, and 18 unscored direct-question rows under the inherited strict grading rules, with 16-token generation truncation affecting some outputs. The direct-control counts matched within that protocol. These are **not** TEST745 metrics.

The Mistral engine uses H6 and K/V layers 0–6, with upper layers 7–31 rebuilt. The Qwen 7B CUT3 and Qwen 72B CUT3 implementations are **architecture-specific**. A cartridge produced for one model is not demonstrated to be portable to another.

### TEST730 and Silicon Hippocampus 1.5

TEST730 combined **three independently sourced 2026 research publications** into source-specific physical cartridges (`P01`, `P02`, `P03`), read their contents, synthesized a new master body as text, and forged a physical `MASTER` cartridge. Its six generated answers were recorded separately from the technical integrity checks. The subsequent 1.5 live demo recovered all four physical cartridges bit-identically, initialized the 72B master, and verified **80/80 layer parity** between native and reference paths. It also measured live new-question responses with and without master memory. Those results establish the earlier large-model foundation for TEST745; they do not automatically establish independent causal correctness for either experiment.

**Historical correction:** Older documentation described a DeepSeek extension as merely planned. Later research activity explored DeepSeek/MLA adaptation; that older statement should not be carried forward as a blanket claim that no DeepSeek work occurred. Individual DeepSeek claims require their own model-specific logs and verification.

## Scientific claims and limitations

### Supported by the cited runs

- Model-native CUT3/CUT6 numerical states can be captured, persisted, verified, reloaded, and used in the corresponding frozen model's computational path.
- TEST745 physically materialized eleven cartridges across source, subsystem, cross-system, blind-master, and post-outcome stages.
- TEST745 executed eight text-mediated review rounds and created a sealed C11 before programmatic access to the official final report.
- A distinct C12 was created with an exact C11 parent SHA-256 reference; post-run integrity checks passed.
- The live Gradio demonstration ran the unchanged locked engine and completed all fifteen recorded stages.

### Not established by TEST745

- Correctness of all accident-cause hypotheses, independent expert agreement, or quantified causal accuracy.
- Autonomous human-level reasoning, consciousness, or guaranteed ability to identify and correct its own errors.
- Eight substantive improvements across eight review rounds: later text similarity was nearly unchanged.
- Direct latent BF16 fusion of multiple parent cartridges; synthesis is **text-mediated**.
- Elimination of transformer computation: upper layers and decoding still run.
- A measured end-to-end speed advantage, superior energy efficiency, or general-purpose memory scaling on the TEST745 task.
- Complete protection from pretrained knowledge leakage in a real-world blind case.
- Completed human review of C12.

The present release is an **interim experimental seal**. It records a working mechanism and a reproducible implementation milestone, not the conclusion of the research programme.

## Reproduction and source files

**Canonical repository:** https://github.com/ceceli33/titan-cognitive-core-v3

| File | Role |
|---|---|
| [`745.py`](745.py) | Locked real-world investigation experiment |
| [`745.log`](745.log) | Original GPU experiment log |
| [`Fly_72b_demo_full.py`](Fly_72b_demo_full.py) | Complete live Gradio reproduction |
| [`Fly_72b_demo_part1.py`](Fly_72b_demo_part1.py) | Gradio part 1 |
| [`Fly_72b_demo_part2.py`](Fly_72b_demo_part2.py) | Gradio part 2 |
| [`Fly_72b_demo_part3.py`](Fly_72b_demo_part3.py) | Gradio part 3 |
| [`Fly_72b_demo.log`](Fly_72b_demo.log) | Completed live reproduction log |
| [`730.py`](730.py) · [`730.log`](730.log) | Earlier real-source synthesis and sealed master |
| [`709.py`](709.py) | Locked CUT3 engine foundation |
| [`Qwen72B_1.5.log`](Qwen72B_1.5.log) | Earlier 72B Gradio validation |
| [`LICENSE`](LICENSE) | Governing AKBASCORE research software license |

**Pinned Git blob identities recorded at the time of this README update:**

```text
745.py                    de9e137e981fd57812d9a5e40d3c72dc278d2133
745.log                   07d8fafb51e871549814442705d617f81e0322ba
709.py                    6c9f8cbb1eeed848d45133d73f0d7676b68e9125
730.py                    b1bad9eb3b111b44413f8ef05a3a140ab66a77dd
Fly_72b_demo_full.py      ed144ab2dbe926d6e6717983074e134a50ece0b0
Fly_72b_demo_part1.py     4e2e012538606208f939f80aa93971361d951b84
Fly_72b_demo_part2.py     b852f6f229a29f809c43575bfde6d699cf8f6efe
Fly_72b_demo_part3.py     ef37db2598811dfda851cb284895680e6a2de21b
Fly_72b_demo.log          459259d596d1a4a2d9d5f348d12da4f2f9120e8f
```

**Git blob SHA-1 identifiers are not SHA-256 file digests.** They identify the repository file contents at a given Git object; cartridge file SHA-256 values and the run's own SHA-256 manifest serve a different verification purpose. For archival releases, pin a Git tag/commit and publish the complete generated results, manifests, and selected raw outputs alongside the PDF and figures.

## Figures and supporting evidence

The completed TEST745 Gradio session produced six 3,999 × 2,250 JPEGs at 300 dpi:

| Figure | Title | Evidence type |
|---|---|---|
| 1 | General Architecture | Schematic grounded in run measurements |
| 2 | Physical Memory Cartridge | Live measurements of files, shapes, and integrity |
| 3 | Hierarchical Synthesis | Schematic with measured token counts and readouts |
| 4 | Eight-Round Closed Loop | Observed text lengths, sequence similarity, uncertainty items |
| 5 | Blind Investigation and Official Outcome | Sealed chronology and selected excerpts; **clock label requires correction** |
| 6 | C11 to C12 Memory Consolidation | Sealed lineage and independent integrity checks |

The figures should be included as separate release assets or linked here **after** their final immutable file paths are published. Do not use placeholder image URLs or present them as embedded repository images until the files exist at those paths. Raw source files and results JSON take precedence over schematic labels.

## Citation and archival policy

**Current TEST745 release — proposed citation until a Zenodo DOI is assigned:**

> Akbaş, Mustafa (2026). *AKBASCORE Silicon Hippocampus: Hierarchical Physical CUT3 Memory, Eight-Round Closed-Loop Analysis, and Sealed Blind-to-Outcome Consolidation in Frozen Qwen2.5-72B-Instruct (TEST745)*. Interim research record, 22 October 2026. GitHub: https://github.com/ceceli33/titan-cognitive-core-v3. Zenodo DOI pending.

```bibtex
@misc{akbas2026siliconhippocampus745,
  author       = {Akba{\c{s}}, Mustafa},
  title        = {AKBASCORE Silicon Hippocampus: Hierarchical Physical CUT3 Memory,
                  Eight-Round Closed-Loop Analysis, and Sealed Blind-to-Outcome
                  Consolidation in Frozen Qwen2.5-72B-Instruct (TEST745)},
  year         = {2026},
  month        = oct,
  note         = {Interim sealed experimental record, 22 October 2026; DOI pending},
  url          = {https://github.com/ceceli33/titan-cognitive-core-v3}
}
```

**Earlier persistent records:**

- [Silicon Hippocampus v1.4 — Qwen Research Record I](https://doi.org/10.5281/zenodo.23381336)
- [Silicon Hippocampus 1.5 / TEST730 — Zenodo record 23497732](https://zenodo.org/records/23497732)
- Earlier Mistral v1.4 paper and associated historical records: see the original release files; **do not invent an unassigned DOI**.

A Zenodo DOI creates a persistent citation and archived public record. A Git release, cryptographic hash, and dated disclosure can help document content and chronology, but none alone grants a patent, guarantees originality, or creates exclusive rights over independently developed ideas. Patent filing strategy and disclosure timing should be reviewed with a qualified patent professional before releasing previously undisclosed patentable subject matter.

## License and rights

**Copyright © 2026 Mustafa Akbaş.** All rights reserved except as expressly permitted under the [AKBASCORE RESEARCH SOFTWARE LICENSE](LICENSE). The full license controls; this section is only a summary.

- Research, education, academic reproduction, evaluation, modification, forking, and derivative works are permitted under the license.
- Commercial use of covered material is permitted without a separate commercial license where the user and its controlled/controlling/common-control affiliates have **combined consolidated annual gross revenue below USD 50,000,000** in the most recently completed fiscal year.
- At or above **USD 50,000,000 annual gross revenue**, commercial use of covered material requires a separate commercial license from the copyright holder.
- The threshold is **revenue**, not valuation, fundraising, market capitalization, or assets under management.
- Earlier material originally released under MIT **remains under MIT**; no retroactive restrictions are asserted.
- The license governs only original copyrightable material for which the rights holder owns applicable rights. It does not, by itself, monopolize abstract ideas, scientific principles, algorithms, or independent implementations.
- Third-party models, source reports, libraries, and dependencies retain their own licensing terms. The software is experimental and supplied **AS IS** without warranty.

**Commercial licensing inquiries:** Mustafa Akbaş, via the official repository.

## Next research questions

This is **not the final stage** of Silicon Hippocampus. The TEST745 release is a dated, technically verified **interim seal** on the way toward a more general persistent-memory architecture. Future work may test:

1. Genuine cross-cartridge latent interaction versus the current text-mediated synthesis baseline.
2. Causal necessity and sufficiency of individual cartridges, with removal, swap, and counterfactual controls.
3. Independent blinded expert grading of C11 answers and systematic separation of supported inference from pretrained knowledge.
4. Whether feedback changes an answer for a justified reason, rather than merely producing a longer or repeated text.
5. Scaling to larger SSD memory banks, exact-address retrieval, selective loading, and multi-agent/shared-memory architectures.
6. Cross-architecture adaptation with model-specific calibration, without claiming direct cartridge portability.
7. Robustness, abstention, uncertainty calibration, and reproducible external replication.

**The immediate milestone is complete: physical memory persistence, hierarchical cartridge production, a sealed blind master, and a distinct post-outcome master were executed on a frozen 72B model and verified in a live demonstration. The larger research goal remains open.**

---

**AKBASCORE Silicon Hippocampus · Active research · Interim sealed record · 22 October 2026**  
**Mustafa Akbaş · Copyright © 2026 · [License](LICENSE)**
