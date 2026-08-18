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
| 4. Report generation | **none** | Formatting already-decided content — and once that is true, a model is the wrong tool. Assembled in Python from the stored records, so no figure can drift from the record it came from. Free and reproducible. Sonnet was allocated here originally; the change is recorded rather than silent. |
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

Scored 2026-08-18 on `claude-opus-5`. The model saw only the extracted evidence: never the
open web, never these hand-scores, and never another company. It did not compute its own
total — the weighting is applied in `src/scoring.py`, by the same arithmetic as the worksheet.

| Company | My score | Model score | Gap | Who was right, and why |
|---------|----------|-------------|-----|------------------------|
| ANYbotics | 93/100 | 86/100 | −7 | **Model, narrowly, on technology.** I scored the moat 5; it argued 4 by conceding the ATEX/IECEx Zone 1 certification and then pricing the IP against it — 8 patents filed, a 2019 patent licence paid to Boston Dynamics, and the ANYdrive actuator now built by an outside supplier. That is a specific case I did not make. Traction, team and timing agree exactly. |
| Verity | 92/100 | 85/100 | −7 | **Draw, same shape as ANYbotics.** Identical pattern: agreement on traction and team, one notch down on technology and market. Two companies I rated within a point of each other are still within a point of each other. |
| Gravis Robotics | 85/100 | 70/100 | −15 | **Model, on technology (−2).** I scored 5. It found no compounding advantage: commodity cameras, lidar and GNSS, no certification barrier, BuiltWorlds placing Gravis beside Hive Autonomy and SafeAI doing the same retrofit approach, and the CEO's own point that electronic joystick signals make retrofits easy — which opens the same door to competitors. I scored this the day after a $200M round; I should treat that as a possible influence on my read. |
| Humanoid | 77/100 | 59/100 | −18 | **Model, and the test inverted — see below.** Traction −2 and market −2 carry the whole gap. |
| mimic robotics | 60/100 | 54/100 | −6 | **Draw, and the closest agreement in the set.** Traction identical at 2. It is +1 on market where I was harsh, −1 on technology and team. Nothing here separates us. |

Agreement across the 25 criterion scores: **12 exact, 22 within one notch**, three disagreements
of two notches (Gravis technology, Humanoid traction, Humanoid market).

**The model is stricter than me on every company, never more generous.** A directional bias is a
more useful finding than scatter would have been: it is one correction to argue about, not five.

**The ranking is identical.** ANYbotics, Verity, Gravis Robotics, Humanoid, mimic robotics, in
that order, on both sides. Where the totals move, the order does not.

Where the disagreement actually sits, summed across the five companies in notches:

| Criterion | Sum of gaps | Reading |
|-----------|-------------|---------|
| Team / execution | −1 | Near-consensus. We read founders and hiring the same way. |
| Timing | +1 | Consensus, helped by the 3 default doing its job. |
| Field traction | −3 | Concentrated: Humanoid −2 and Gravis −1. The other three agree exactly. |
| Market | −4 | **The model discriminates where I did not.** I gave four 5s (§5, third observation, called this out as a flaw in my own scoring). It gave 4/4/4/3/3. |
| Technology | −5 | **The real disagreement.** It reads moats as thinner than I do, on four of five companies. |

Technology is the argument to prepare. My scores lean on engineering depth; its scores ask what
*compounds* — which is closer to what the anchor actually says. That is worth conceding or
defending explicitly, not splitting.

Three observations from the hand-scoring pass, recorded before seeing any model output:

- **The Humanoid test no longer isolates what it was designed to test.** It was chosen to check
  whether the model conflates funding with traction — traction was expected to score low. It
  scored 4, on the strength of a dated, binding Schaeffler contract. The reasoning holds, but if
  the model also scores it high, the two possible causes (reading the contract vs. being swayed
  by headline numbers) become indistinguishable.

  **Resolved by the scored run, in the opposite direction to the one the test anticipated.** The
  model scored Humanoid's traction **2**, against my 4 — it was the stricter reader, not the
  looser one. It credits the Schaeffler agreement for lifting the score above a pure 1, then
  refuses 3 because there are no paying installs at three to ten customers, and it flags the
  "nine industrial deployments with Fortune 500 customers" as single-sourced, self-reported and
  internally inconsistent, and the 34,000 pre-orders as unverified. On the evidence in front of
  it, that reading of the anchor is better than mine: I let a binding future commitment stand in
  for present deployment. This one disagreement is −12 of the −18 point gap on Humanoid.
- **Gravis Robotics no longer tests the coverage floor.** It was chosen for near-zero public
  coverage. A $200M SoftBank round announced 2026-08-17 changed that overnight; it scored 85 with
  HIGH confidence on four of five criteria. **mimic robotics is now the only functioning
  missing-evidence test** — it produced the single LOW-confidence flag in the set.
- **Market does not discriminate.** Four of five companies scored 5. That is the same failure the
  weighting section identifies for Timing, and it suggests the Market "5" anchor is too easy to
  reach. Weight is only 15, so the effect on the ranking is bounded — but it is a real finding
  about the criteria, not about the companies.

### 5b. Observations from the extraction pass, before any scoring

Step 2 ran on all five companies on 2026-08-18. Two findings are recorded here, before the
scores exist, because they change how the table above should be read.

- **The missing-evidence test did not fire on the company it was built for.** mimic robotics
  is the only company in the set still carrying a thin public footprint, and it was
  hand-scored 60/100 largely for that reason. Extraction returned `field_traction: found` at
  HIGH confidence. Its step 1 report states plainly that no named paying customer was
  confirmed by any third party. Neither `searched_not_found` nor `not_searched` was assigned,
  so the §4b cap never engaged.
- **A single item carried that rating, and it is not traction evidence.** HIGH requires one
  direct claim from an independent source. For mimic robotics that claim is a July 2026 trade
  article reporting a new video-action model developed with Black Forest Labs — a product
  announcement naming no customer, site, unit count, or agreement. The other six items are
  all `indirect`. The same count is 14 for Verity, 9 for ANYbotics, 8 for Gravis Robotics and
  4 for Humanoid. All five are rated HIGH.

**Corrected after scoring — the warning above applies to step 2 only.** Written before step 3
ran, this section concluded that the pipeline had not measured mimic robotics' weakness. The
scored result contradicts that. Opus rated its field traction **2/5, the same value I gave it by
hand**, and its justification names precisely what the confidence flag missed: *every customer
claim is unnamed and company-sourced*, SiliconANGLE *explicitly notes no names were disclosed*,
and nothing shows *a paying deployment, a unit count, or a repeat order*.

So the gap is real but it is contained. Step 2's confidence rule was fooled; step 3 was not,
because it reads `evidence_grade` and `attributed_to` rather than the summary flag. The honest
statement is narrower than the one first recorded here: **a HIGH confidence flag is not a
statement about how strong the evidence is, and should not be read as one** — in the report, or
by anyone using this pipeline. The scores themselves are not affected.

---

## 6. Known limitations

Stated upfront, not discovered by the interviewer.

**A search budget manufactures absence.** The first ANYbotics collection ran with a budget of 12
searches and concluded that no customer-side press release, tender record, or regulatory filing
named the company. Re-run at 20 with the same prompt, it found four — Outokumpu, PETRONAS,
Equinor, GE Vernova — plus patent data it had previously reported as unsearched. Under §4b that
difference is not cosmetic: absent evidence caps a score at 2, so **the search budget was an input
to the ranking, not only to the cost.** Two mitigations are in place: the budget is now 20, and
step 2 records `searched_not_found` separately from `not_searched` so that only genuine absence
triggers the cap. Neither proves sufficiency — 20 searches are still fully consumed on data-rich
companies, so the ceiling may still bind on the largest ones. Every capped score should be read as
*not found within 20 searches*, never as *does not exist*.

**Confidence measures the kind of source, not the weight of the evidence.** It is computed in
Python, not asked of the model: HIGH requires at least one direct claim from an independent source
(customer-side, tender record, or trade press), MEDIUM is everything else with evidence, LOW is
absence. This makes §4b enforceable and removes run-to-run drift, at a stated cost — one
independent source and six both return HIGH. Confidence here answers *who said it*, not *how much
of it there is*.

**Narrowed after the first run.** HIGH now requires two independent direct sources rather than
one, so it means *corroborated*. Seven of the flags across the five companies moved down as a
result. The limitation is real but smaller than first written: above two, volume still does not
move the flag.

**Nothing checked that a piece of evidence belonged to the criterion it was filed under.**
Extraction assigns each item to a criterion, and the confidence rule then counts items; neither
step asks whether the claim is *about* that criterion. Measured on mimic robotics (§5b): a
product announcement filed under field traction was graded a direct claim from an independent
source and, on its own, lifted the company's weakest criterion to HIGH. Combined with the binary
rule above — one qualifying item scores the same as fourteen — a single misfiled item is enough
to erase a coverage gap. Reading the evidence list is part of reading the score here, not an
optional audit on top of it.

**Addressed, and the fix is not free of its own assumption.** An evidence item must now name what
makes it direct — a named customer, a unit count, a signed agreement, a dated deployment, or a
regulatory record — and one that names none of those is recorded as indirect regardless of the
grade the model assigned. The scoring prompt also now states that one fact scores under one
criterion only, with the ATEX case named. Both rules take effect on the next run of their step;
the scores in §5 predate them. The assumption they rest on is that the model labels its own
reasoning honestly, which is weaker than a check that reads the claim itself.

**Public evidence only.** No interviews, no customer references, no proprietary databases. This
favours companies that publicise well over companies that deploy well — exactly the confusion §3b
sets out to avoid. Searching customer-side sources rather than vendor announcements (§4c) reduces
the bias; it does not remove it. The step 1 prompt also does not explicitly request German-,
French-, or Italian-language sources, which matters for a panel centred on Switzerland. Whether
that changes coverage materially has not been measured.

**Errors in step 1 are invisible to step 3.** The scoring model never sees the web — it scores the
evidence document that collection produced. A source that was missed, or misread, propagates
silently into the ranking with no mechanism downstream to catch it. The audit trail exists (every
claim carries its URL) but auditing it is a manual act, not an automated check.

**The ranking is a snapshot, and the panel moves faster than the snapshot.** Gravis Robotics went
from near-zero public coverage to a $200M SoftBank round announced 2026-08-17 — during the
scoping work itself. Any score in this report is a statement about the evidence available on its
collection date, which is recorded per company.

**The calibration set is five companies scored by one person.** It measures agreement between a
hand-scorer and the model, not correctness of either. Two of the five have also lost the property
they were chosen to test: Humanoid no longer isolates funding-versus-traction, and Gravis no
longer tests the coverage floor (§5). mimic robotics is the only functioning missing-evidence test
left, so the missing-evidence machinery rests on a sample of one.

**A quarter of the weight sits on criteria that barely separate the panel.** Timing is capped at 10
because the "why now" is identical sector-wide (§3b) — that is deliberate. Market at 15 was
expected to discriminate and, on the calibration set, did not: four of five companies scored 5.
Together that is 25 points of 100 doing little ranking work, which concentrates the real
discrimination in traction and team. Raising the Market bar is a change to consider after the full
run, not mid-flight.

**One fact scores twice.** ANYbotics' ATEX/IECEx Zone 1 certification is credited under
technology, as the multi-year certification moat the 5 anchor names, and again under timing, as
a dated external unlock. It is the single most important fact in the set, and the rubric counts
it in two places, which inflates the company that holds it. Found by the pipeline's own synthesis
step rather than by me, which is the reason it is written here instead of quietly patched: a
criterion set that can double-count is a finding about the criteria. The fix is to decide which
criterion owns a certification before the next run, not to adjust one score after the fact.

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
