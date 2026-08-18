# Step 0 — Scoping

This document is the actual deliverable of the project. Everything downstream is execution.
Nothing gets coded until every section below is filled in and defensible out loud.

---

## 1. Sub-sector definition

**Sector: Physical AI.** Companies whose core product is a machine that perceives and acts in
the physical world, and whose value comes primarily from onboard autonomy rather than from the
mechanics. Mobile robots, drones, autonomous industrial machines, manipulation, humanoids.

**Geography: Switzerland and Europe** (EU + UK + Norway), by headquarters.

**In scope — a company qualifies if all four hold:**
- Its main commercial product is a physical system, and the differentiator is the AI on board
- It is independently financed — a startup or scale-up, not a division of a listed group
- Headquarters in Switzerland or Europe
- At least one disclosed funding round, or public evidence of revenue

**Out of scope — explicitly excluded, with the reason:**
- **Pure software, simulation or foundation-model companies** — no physical product, so the
  same criteria would not measure the same thing
- **Industrial automation incumbents** (ABB, KUKA, Stäubli) — mature and orders of magnitude
  larger; including them compresses every startup into the bottom of the scale
- **Swiss and European R&D sites of foreign tech groups** (Google Zurich, Apple, NVIDIA,
  Meta, Disney Research) — scoring Alphabet on "amount raised" is meaningless. Listed
  unscored in the annex, section 7
- **Academic labs and unincorporated spin-off projects** — no company to score yet

**Edge case rulings, decided in advance:**
- *Founded in Europe, HQ later moved to the US* → out of the main ranking, listed in the
  annex and flagged. The migration is itself a finding worth discussing in the thesis.
- *European HQ, manufacturing in Asia* → in scope. Where it builds does not change what it is.
- *Acquired by a larger group but still operating as a distinct product line* → out of the
  ranking, noted in the annex. Its funding trajectory stopped being a signal on acquisition.

> Why the boundary matters: an interviewer will test it with an edge case. This definition is
> built to survive "what about company X?" — every exclusion above has a stated reason, and
> the reason is always the same one: the criteria must measure comparable things.

---

## 2. Company list

26 companies. Funding figures are deliberately absent here — collecting and sourcing them is
the job of steps 1 and 2. This list is names, geography and segment only.

Sources used to build it: the Swiss Robotics Startups ecosystem map (~100 entries, filtered
against the section 1 criteria), Greater Zurich Area's robotics selection, Top100 Startups
Switzerland, and EU-Startups / Tech.eu funding coverage from 2025–2026.

| # | Company | Country | Sub-segment | How I found it |
|---|---------|---------|-------------|----------------|
| 1 | ANYbotics | CH — Zurich | Legged robots, industrial inspection | Known ETH spin-off |
| 2 | Verity | CH — Zurich | Autonomous warehouse inventory drones | Ecosystem map |
| 3 | Voliro | CH — Zurich | Contact-inspection drones | Ecosystem map |
| 4 | Flyability | CH — Lausanne | Confined-space inspection drones | Known EPFL spin-off |
| 5 | Wingtra | CH — Zurich | VTOL mapping and survey drones | Ecosystem map |
| 6 | mimic robotics | CH — Zurich | Dexterous manipulation | EU-Startups, Nov 2025 |
| 7 | Ascento | CH — Zurich | Wheeled-legged security patrol robots | Ecosystem map |
| 8 | Gravis Robotics | CH — Zurich | Autonomous heavy construction machinery | Greater Zurich selection |
| 9 | LOXO | CH — Bern | Autonomous delivery vehicles | Ecosystem map |
| 10 | Ecorobotix | CH — Yverdon | Precision agriculture, smart spraying | Ecosystem map |
| 11 | Tethys Robotics | CH — Zurich | Autonomous underwater robots | Greater Zurich selection |
| 12 | Saeki | CH — Zurich | Robotic fabrication for construction | Ecosystem map |
| 13 | NEURA Robotics | DE — Metzingen | Cognitive robots and humanoids | Largest EU round, 2026 |
| 14 | Agile Robots | DE — Munich | Force-controlled manipulation | Sector coverage |
| 15 | Sereact | DE — Stuttgart | Embodied AI for robotic picking | EU funding coverage 2026 |
| 16 | Robco | DE — Munich | Modular industrial robots for SMEs | Sector coverage |
| 17 | Fernride | DE — Munich | Autonomous yard and port logistics | Sector coverage |
| 18 | Humanoid | UK — London | Industrial humanoid robots | Tech.eu, Jul 2026 |
| 19 | Dexory | UK — Oxford | Warehouse inventory robots | Sector coverage |
| 20 | Wayve | UK — London | Embodied AI for driving — see edge case | Sector coverage |
| 21 | Exotec | FR — Lille | Warehouse goods-to-person robotics | Sector coverage |
| 22 | Donecle | FR — Toulouse | Automated aircraft inspection drones | EU-Startups, Apr 2026 |
| 23 | AgreenCulture | FR — Toulouse | Autonomous agricultural robots | Sector coverage |
| 24 | PAL Robotics | ES — Barcelona | Humanoid and service robots | Sector coverage |
| 25 | THEKER | ES — Barcelona | Humanoid manipulation | EU funding coverage 2026 |
| 26 | Oversonic Robotics | IT — Besana Brianza | Humanoid robots for industry | Sector coverage |

### 2b. Edge cases — ruled on before scoring

Applying section 1 to the grey zone. Each ruling is stated so it can be defended.

| Company | Ruling | Reason |
|---------|--------|--------|
| Auterion (CH) | **Out** | Drone autonomy software running on third-party airframes. No own physical product. |
| Energy Robotics (DE) | **Out** | Inspection software layered on other vendors' robots. Same reason as Auterion. |
| Bota Systems (CH) | **Out** | Force-torque sensor supplier — a component, not a system that perceives and acts. |
| Distalmotion (CH) | **Out** | Surgical robotics. Strong Swiss player, but medtech regulation and sales cycles make it incomparable to industrial Physical AI. |
| Wayve (UK) | **In, flagged** | Does not build the vehicle, which strains the "physical product" test. Kept because the autonomy stack *is* the product and it is deployed on real roads. Reversible if the flag proves distorting. |

> The Wayve ruling is the one to expect a question on. The honest answer is that it sits on the
> boundary, the boundary was drawn before the company was considered, and the decision is
> documented rather than silent.

---

## 3. Scoring criteria and weights

Weights must sum to 100. The justification column is what gets discussed in an interview —
it is more important than the number itself.

| Criterion | Weight | What it measures | Why this weight |
|-----------|--------|------------------|-----------------|
| Field traction | **30** | Units deployed at paying industrial customers. Funding is a secondary indicator only. | In Physical AI the binding constraint is deployment, not modelling. Anyone can demo; almost nobody survives contact with a real site. |
| Team / execution | **25** | Founder background, hardware iteration speed, ability to hire scarce robotics talent | Hardware punishes slow teams. Iteration speed is the single best predictor of who is still standing in three years. |
| Technology / product | **20** | Maturity, technical moat, defensibility | Weighted below traction on purpose: robotics moats erode fast because everyone reads the same papers. What defends is accumulated real-world data, which shows up under traction. |
| Market | **15** | Addressable size, segment growth rate | Discriminates weakly here — most of the panel targets comparable industrial segments, so it separates few companies. |
| Timing | **10** | Why now — what changed that makes this possible today | Deliberately low. See section 3b. |
| **Total** | **100** | | |

### 3b. Two positions this weighting takes

**Traction is not the amount raised.** It is redefined as units deployed at paying industrial
customers, with funding demoted to a secondary indicator. Dollars raised is a lagging, noisy
signal: a €100M round reports what a group of investors believed eighteen months ago. Robots
running on a customer site report what works now.

**Timing is capped at 10 on purpose.** The "why now" of Physical AI — cheap sensors, vision-
language-action models, industrial labour shortage — is identical for every company in the
panel. A criterion that awards everyone the same score does not rank anything; it only
inflates the totals. Keeping it at 10 acknowledges that it matters to the sector without
pretending it separates companies within it.

---

## 4. Scoring scale

A 1–5 scale with written anchors for every criterion, so that two runs of the pipeline produce
comparable scores. Without anchors the model drifts between runs and the ranking means nothing.

Scores 2 and 4 are intermediate positions between the anchors below.

### Field traction — weight 30

| Score | Anchor |
|-------|--------|
| 1 | Demos, pilots and letters of intent only. No customer paying for a deployment, or deployments only at investor and partner sites. |
| 3 | Paying deployments at roughly 3–10 customers, still sold project by project, each installation substantially custom. |
| 5 | Repeat orders from several industrial customers, tens of units in routine daily service, and at least one customer that has moved past an initial pilot into a fleet. |

> The discriminator is the **pilot-to-fleet transition**, not the number of pilots. Robotics is
> full of companies with fifty pilots and no second order — that is "pilot purgatory", and it
> scores a 2, not a 4. A single customer that scaled from three units to thirty is worth more
> evidence than twenty logos on a website.

### Team / execution — weight 25

| Score | Anchor |
|-------|--------|
| 1 | First-time founders with no record of shipping hardware, no visible iteration, flat or shrinking team. |
| 3 | Credible technical founders with a strong research pedigree, one product generation shipped, steady hiring. |
| 5 | Founders who have shipped hardware at scale before, or two-plus product generations shipped at this company with visibly shortening cycles, and the pull to hire senior robotics people away from big tech. |

> **An ETH or EPFL pedigree caps at 3 in this panel.** Nearly every Swiss company on the list
> has one, so it is table stakes, not a differentiator. Anything that everyone shares cannot
> separate anyone — the same logic that caps the timing criterion at 10.

### Technology / product — weight 20

| Score | Anchor |
|-------|--------|
| 1 | The capability is demonstrated in published research by others and the demo could be reproduced with off-the-shelf components. |
| 3 | Real engineering depth — hard integration work, reliability in the field — but the underlying approach is broadly available to competitors. |
| 5 | An advantage that compounds: a proprietary real-world data flywheel, a hardware component competitors cannot buy, or a certification that takes years to replicate. |

> A 5 requires something that **gets stronger with use**. A clever architecture does not qualify;
> everyone reads the same papers. This is the criterion where the weighting argument from
> section 3b cashes out.

### Market — weight 15

| Score | Anchor |
|-------|--------|
| 1 | Narrow niche with few buyers, or a segment where no budget line exists for this category of spend. |
| 3 | Genuinely sizeable segment, but crowded, or with procurement cycles long enough to starve a startup. |
| 5 | Large segment with an urgent and already-budgeted pain — labour shortage, regulatory inspection mandate — where the buyer purchases in this category today. |

> Judge the **existing budget line**, not the headline market size. A TAM is easy to inflate and
> nobody can check it. A buyer who already has a line item for inspection is a buyer who can sign.

### Timing — weight 10

| Score | Anchor |
|-------|--------|
| 1 | Could have been built five years ago and was not, with no external change explaining why now. |
| 3 | Rides the general Physical AI wave — the same "why now" as every other company in the panel. **This is the default score here.** |
| 5 | A specific, dateable unlock the company is positioned for: a regulation entering into force, a component crossing a price threshold, a customer-side mandate. |

> Because the generic wave scores a 3 for everyone, only a *specific* unlock earns a 5. This is
> what keeps a low-weight criterion from quietly inflating every total.

### 4b. Handling missing evidence

The pipeline will not find complete data for all 26 companies. Younger and less publicised
companies will have thinner public footprints, and that must not be silently rewarded or
punished by guesswork.

**Rule: where evidence for a criterion is absent, the score is capped at 2 and flagged as low
confidence. The model must never infer a score from what is plausible for a company of that
type.**

Absence of evidence is recorded as absence, not averaged away into a middling score. Every
low-confidence flag is listed in the final report so a reader can see exactly which parts of
the ranking rest on thin data.

### 4c. Sourcing the traction criterion

There is a real tension in this design, and it is better stated than discovered: field traction
carries the highest weight (30) and is the hardest evidence to obtain publicly. Industrial
buyers rarely disclose deployment volumes. Left alone, the most important criterion would carry
the most low-confidence flags.

The weight is not lowered — the argument for it holds. Instead, step 1 searches for traction
evidence deliberately and beyond the company's own marketing:

| Source | What it reveals |
|--------|-----------------|
| Customer-side press releases | The buyer announcing a rollout is stronger evidence than the vendor announcing a win |
| Published case studies | Usually name a site and sometimes a unit count |
| Job postings | A company hiring ten field deployment engineers has deployments. Hiring only researchers does not. |
| Trade and industry press | Covers installations that never reach the startup press |
| Regulatory and tender records | Public-sector deployments leave a paper trail |

Job postings are an **indirect indicator** and are labelled as such in the extracted data. They
support a score, they never establish one on their own.

### 4d. Model allocation across the pipeline

Two models, assigned per step rather than one model for the whole pipeline. The principle:
**spend capability where judgment happens, not uniformly.**

| Step | Model | Reasoning |
|------|-------|-----------|
| 1. Source collection | `claude-sonnet-5` | High input volume (search results), low judgment. Finding and returning pages is not where model capability separates. |
| 2. Structured extraction | `claude-sonnet-5` | Reading a page and filling a schema field with its source URL. Mechanical once the schema is fixed. |
| 3. Weighted scoring | `claude-opus-5` | The only step that is pure judgment: arbitrating between the 1/3/5 anchors, applying the missing-evidence cap, and writing a justification that survives challenge. This is the step the project is actually about. |
| 4. Report generation | `claude-sonnet-5` | Formatting already-decided content. |
| 5. Thesis and executive summary | `claude-opus-5` | Synthesis across 26 scored companies — pattern-finding, not transcription. |

Cost at August 2026 list prices: Opus is 2.5× Sonnet per token on both input and output. Running
the whole pipeline on Opus would roughly double the project cost for a quality gain confined to
steps 3 and 5.

**Consequence to respect on any rerun:** step 3 stays on Opus. A scoring pass run on a different
model is not comparable to the existing one, and the calibration in §5 would have to be redone.

---

## 5. Calibration set

Five companies scored **by hand, before running the pipeline**. The gap between these scores
and the model's output is measured and discussed in the final report.

This is the section that makes the project credible. Do not skip it.

Hand-scoring completed 2026-08-18, blind, before any pipeline code was written. Full
per-criterion scores, confidence levels, and justifications are in
[`calibration-worksheet.md`](calibration-worksheet.md).

| Company | My score | Model score | Gap | Who was right, and why |
|---------|----------|-------------|-----|------------------------|
| ANYbotics | 93/100 | | | |
| Verity | 92/100 | | | |
| Gravis Robotics | 85/100 | | | |
| Humanoid | 77/100 | | | |
| mimic robotics | 60/100 | | | |

Three observations from the hand-scoring pass, recorded before seeing any model output:

- **The Humanoid test no longer isolates what it was designed to test.** It was chosen to check
  whether the model conflates funding with traction — traction was expected to score low. It
  scored 4, on the strength of a dated, binding Schaeffler contract. The reasoning holds, but if
  the model also scores it high, the two possible causes (reading the contract vs. being swayed
  by headline numbers) become indistinguishable.
- **Gravis Robotics no longer tests the coverage floor.** It was chosen for near-zero public
  coverage. A $200M SoftBank round announced 2026-08-17 changed that overnight; it scored 85 with
  HIGH confidence on four of five criteria. **mimic robotics is now the only functioning
  missing-evidence test** — it produced the single LOW-confidence flag in the set.
- **Market does not discriminate.** Four of five companies scored 5. That is the same failure the
  weighting section identifies for Timing, and it suggests the Market "5" anchor is too easy to
  reach. Weight is only 15, so the effect on the ranking is bounded — but it is a real finding
  about the criteria, not about the companies.

---

## 6. Known limitations

Stated upfront, not discovered by the interviewer.

- TBD

---

## 7. Annex — ecosystem players, not scored

Excluded from the ranking because the scoring criteria do not apply to them, but they shape
the sector and belong in the picture.

### Foreign corporate R&D sites in Switzerland

Not scored — the criteria are built for independently financed companies. Listed because they
compete for the same talent pool as every company in the ranking, and because they are where
a share of Swiss robotics and computer-vision work actually happens.

| Group | Site | Relevance to Physical AI |
|-------|------|--------------------------|
| Google / DeepMind | Zurich | Largest Google R&D centre outside the US; robotics and computer vision |
| Amazon | Zurich | Reinforced by the RIVR acquisition, see below |
| Apple | Zurich | AI and computer vision lab |
| Meta | Zurich | Computer vision |
| Microsoft | Zurich | Mixed reality and AI |
| NVIDIA | Zurich | Robotics and simulation |
| Disney Research | Zurich | Character robotics, long-standing ETH partnership |
| IBM Research | Rüschlikon | Long-standing European research site |
| ABB | Zurich region | Not foreign, but a listed incumbent — excluded from the ranking for scale |

*To verify and complete in step 1 — headcount and current robotics activity per site.*

### Acquired companies

The most interesting rows in this document. Both were ETH-originated, both were acquired
before reaching independent scale.

| Company | Acquirer | Year | Signal |
|---------|----------|------|--------|
| RIVR (ex Swiss-Mile) | Amazon (US) | March 2026 | Wheeled quadrupeds for last-mile delivery. Raised ~$25M incl. Bezos Expeditions before exit. |
| Sevensense Robotics | ABB (CH/SE) | 2024 | Visual navigation for mobile robots. Absorbed into an incumbent's product line. |

### European companies that relocated their HQ abroad

| Company | Founded in | Moved to | Year |
|---------|-----------|----------|------|
| *To investigate in step 1* | | | |

### Working hypothesis for the thesis

Emerging from the annex, **to be tested against the scored data, not assumed**: Switzerland
generates world-class Physical AI technology through ETH and EPFL spin-offs, but value capture
migrates abroad — through acquisition by foreign strategics — before those companies reach
independent scale. If the scored data supports it, the interesting question becomes which of
the 26 has the field traction to break that pattern.
