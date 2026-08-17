# Interview notes — DeepTech Scout

Every design decision in this project, with the argument behind it, written as the questions
an interviewer is likely to ask.

Keep this file updated as the project progresses. The reasoning is the deliverable; the code
is the evidence that the reasoning was applied.

---

## The 30-second version

> I built a market map of Physical AI in Switzerland and Europe. A Python pipeline collects
> public sources on 26 companies, extracts structured and sourced data, and scores each one
> against five weighted criteria I defined up front. The interesting part is not the pipeline —
> an engineer writes that in an afternoon. It is the weighting, and the fact that I measured
> where the model's scores disagree with my own.

Three things this is meant to demonstrate, in order of importance:

1. **Product judgment** — the criteria and their weights
2. **Ability to ship** — a working end-to-end pipeline
3. **Awareness of limits** — a calibration set that measures where the output is wrong

---

## Scoping decisions

### Why Physical AI, and why Switzerland and Europe rather than worldwide?

A worldwide map competes with published VC research and adds nothing. A Swiss and European
map covers ground that is genuinely less well documented, and it produces a document that can
be sent directly to the companies it analyses. Same effort, far more useful output.

### Why did you define the criteria before listing the companies?

If the company list comes first, the criteria get shaped — unconsciously — to favour the
companies already liked. That is detectable in an interview. Defining criteria blind and then
applying them is the honest sequence, and it is worth saying out loud.

### How did you set the weights?

| Criterion | Weight |
|-----------|--------|
| Field traction | 30 |
| Team / execution | 25 |
| Technology / product | 20 |
| Market | 15 |
| Timing | 10 |

The weighting takes a position: in Physical AI the binding constraint is deployment, not
modelling. Anyone can produce a demo; very few companies survive contact with a real
industrial site. So traction leads, and technology is deliberately weighted below it, because
robotics moats erode fast — everyone reads the same papers.

### Why is traction not measured by funding?

Traction is defined as **units deployed at paying industrial customers**, with funding demoted
to a secondary indicator.

Money raised is a lagging and noisy signal: a €100M round reports what a group of investors
believed roughly eighteen months earlier. Robots running on a customer site report what works
now. In a sector where capital is currently abundant, funding measures investor enthusiasm
more than it measures product-market fit.

### Why is timing weighted at only 10?

The "why now" of Physical AI — cheap sensors, vision-language-action models, industrial labour
shortage — is identical for every company in the panel. A criterion that awards everyone the
same score does not rank anything; it only inflates the totals.

Keeping it at 10, and setting the generic wave as a 3 in the scale, acknowledges that timing
matters to the sector without pretending it separates companies within it.

The same logic caps an ETH or EPFL pedigree at 3 on the team criterion: almost every Swiss
company on the list has one, so it is table stakes rather than a differentiator.

---

## Method decisions

### How do you know the model's scores are right?

This is the question the whole project has to survive, and the honest answer is that a language
model scoring "market size" from web search results produces plausible-sounding numbers that
may carry little signal.

So five companies are scored **by hand, before the pipeline runs**. The gap between those
scores and the model's output is measured, and the disagreements are analysed in the final
report. The deliverable includes a section on where the tool is wrong and why.

Knowing the limits of the product is the point, not a caveat.

### What stops the scores drifting between runs?

Written anchors for 1, 3 and 5 on every criterion (section 4 of the scoping document). Without
them the model scores by mood and two runs produce different rankings, which makes the whole
exercise meaningless.

### What happens when the data is not there?

Where evidence for a criterion is absent, the score is capped at 2 and flagged as low
confidence. The model is explicitly forbidden from inferring a score from what is plausible for
a company of that type.

Absence of evidence is recorded as absence rather than averaged away into a middling score, and
every low-confidence flag is surfaced in the report. Otherwise the ranking quietly rewards
companies with better PR.

### How is the underlying data traceable?

Every extracted field carries its source URL and a confidence level. A market map whose numbers
cannot be traced back to a source collapses at the first factual challenge.

---

## Edge cases — expect one of these

The boundary was drawn in section 1 before any company was considered, and every exclusion has
a stated reason. The reason is always the same one: **the criteria must measure comparable
things.**

| Case | Ruling | One-line answer |
|------|--------|-----------------|
| Google Zurich, Apple, NVIDIA and other foreign R&D sites | Annex, unscored | Scoring Alphabet on "amount raised" is meaningless and would compress every startup into the bottom of the scale. They are listed because they compete for the same talent. |
| ABB, KUKA, Stäubli | Out | Mature incumbents, orders of magnitude larger. Same scale-compression problem. |
| Auterion, Energy Robotics | Out | Software running on third-party hardware. No physical product of their own. |
| Bota Systems | Out | Component supplier — a sensor, not a system that perceives and acts. |
| Distalmotion | Out | Surgical robotics. Medtech regulation and sales cycles make it incomparable to industrial Physical AI. |
| **Wayve** | **In, flagged** | The weakest ruling. They do not build the vehicle. Kept because the autonomy stack *is* the product and it is deployed on public roads. Documented rather than hidden, and reversible if it distorts the ranking. |

If pressed on Wayve: the point is not that the call is obviously right, it is that the boundary
existed before the company was examined and the tension is written down.

---

## The thesis

**Working hypothesis, to be tested against the scored data rather than assumed:**

> Switzerland generates world-class Physical AI technology through ETH and EPFL spin-offs, but
> value capture migrates abroad — through acquisition by foreign strategics — before those
> companies reach independent scale.

Evidence that prompted it, both surfaced while building the company list:

- **RIVR** (formerly Swiss-Mile, ETH spin-off, backed by Bezos Expeditions, ~$25M raised)
  acquired by **Amazon** in March 2026
- **Sevensense Robotics** (ETH spin-off, visual navigation) acquired by **ABB** in 2024

Note the sequence: the exclusion rules that sent both companies to the annex were written
*before* either acquisition was known. The finding came out of applying the method, not out of
looking for a story.

If the scored data supports the hypothesis, the question that follows is which of the 26 has
the field traction to break the pattern. If the data does not support it, that is reported too.

---

## Known weaknesses — raise these before the interviewer does

- **LLM scoring is soft on the market criterion.** Market size judgments from web search are the
  least reliable output of the pipeline. This is why market carries the second-lowest weight and
  why the calibration set exists.
- **Public data favours companies with good PR.** A quiet company with strong deployments can
  score below a loud one. The low-confidence flags make this visible but do not fix it.
- **Field traction is the hardest thing to source publicly.** Deployment numbers are rarely
  disclosed. Expect this criterion — the highest weighted — to carry the most low-confidence
  flags, which is an uncomfortable but honest tension in the design.
- **26 companies is a sample, not the sector.** The list was filtered from a ~100-entry
  ecosystem map plus funding coverage; companies with no public footprint at all are invisible
  to it.

---

## If asked what you would do next

- Widen field traction sourcing beyond public web data — customer case studies, job postings as
  a proxy for deployment engineering, trade press
- Re-run the pipeline quarterly and track score movement, since momentum is more informative
  than a single snapshot
- Expand the calibration set from 5 to 10 companies to tighten the agreement measurement
