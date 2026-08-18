# Interview notes — DeepTech Scout

Every design decision in this project, with the argument behind it, written as the questions
an interviewer is likely to ask.

Keep this file updated as the project progresses. The reasoning is the deliverable; the code
is the evidence that the reasoning was applied.

---

## The 30-second version

> I built a market map of Physical AI in Switzerland and Europe. A Python pipeline collects
> public sources, extracts structured and sourced data, and scores each company against five
> weighted criteria I defined up front. The interesting part is not the pipeline —
> an engineer writes that in an afternoon. It is the weighting, and the fact that I measured
> where the model's scores disagree with my own.
>
> I ran it end to end on the five companies I had hand-scored blind, first. The model put them
> in exactly the same order I did, while scoring every one of them lower. Twelve of 25
> criterion scores were identical, 22 within one notch. On the largest disagreement I now
> think the model was right and I was wrong.

Scope note, and say it before being asked: the pipeline was run end to end on **five**
companies, not 26. Those five are the ones with a blind hand-score to compare against, so they
carry the evidence. The remaining 21 are a cost decision, not a technical one — steps 2 to 5 run
on code that is already written and tested.

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

## What the run actually produced

| Company | My score | Model | Gap |
|---------|---------:|------:|----:|
| ANYbotics | 93 | 86 | −7 |
| Verity | 92 | 85 | −7 |
| Gravis Robotics | 85 | 70 | −15 |
| Humanoid | 77 | 59 | −18 |
| mimic robotics | 60 | 54 | −6 |

**The ranking is identical on both sides.** The totals all move down and the order does not.

**The model is stricter than me on all five, never more generous.** That is a more useful
result than scatter would have been: it is one correction to argue about rather than five
unrelated ones.

**The disagreement is concentrated.** Summed across the five, in notches: team −1, timing +1,
traction −3, market −4, **technology −5**. Team and timing are near-consensus. Technology is the
argument to prepare — my scores credited engineering depth, the model asked what *compounds*,
which is closer to what my own anchor actually says.

### The one to volunteer: Humanoid

I designed that test to check whether **the model** would confuse funding with traction. It
resolved in the opposite direction. I scored its traction 4 on the strength of a binding
Schaeffler agreement. The model scored 2 — crediting the same agreement for clearing a 1, then
refusing 3 because there are no paying installs at three to ten customers, and flagging the
"nine industrial deployments with Fortune 500 customers" as single-sourced and internally
inconsistent.

On the evidence in front of it, its reading of my own anchor is better than mine. I let a
binding future commitment stand in for present deployment. That single disagreement is −12 of
the −18 point gap on Humanoid.

Being able to say "my tool corrected me, here is the evidence, and I updated the document" is
worth more than a ranking nobody has challenged.

### What the model wrote, that I had not seen

The thesis step flagged that **ANYbotics' ATEX Zone 1 certification is credited twice** in my
own rubric — once as a technology moat, once as a dated timing unlock — which inflates the
single most important fact in the set. That is a flaw in the criteria, found by the pipeline,
and it is now recorded rather than quietly fixed.

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

**Measured result:** 12 of 25 criterion scores identical, 22 of 25 within one notch, rank order
identical, and a systematic downward bias on the model's side. The three two-notch disagreements
are Gravis technology, Humanoid traction and Humanoid market — all argued out in scoping §5
rather than averaged away.

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

**What happened when it was tested, and the honest version of the answer.** mimic robotics was
the company chosen to exercise this rule. Extraction labelled its field traction `found` at HIGH
confidence — on one item out of seven, and that item turned out to be a product announcement,
not a deployment. The cap never engaged.

The scoring step was not fooled: it scored that criterion 2, the same value I gave it by hand,
and its reasoning names exactly what the flag missed — every customer claim unnamed and
company-sourced, no paying deployment, no unit count, no repeat order.

So the correct statement is narrower than the one I first wrote down: **a HIGH confidence flag
says the evidence *class* is strong, not that the evidence is strong.** It is computed in Python
from the type of source, deliberately, so that it cannot drift between runs — and the accepted
cost of that is that one independent source and six both return HIGH. The scores are unaffected,
but anyone reading the report needs to know what the flag does and does not mean.

**Three states, not two.** Evidence is recorded as `found`, `searched_not_found`, or
`not_searched`. Only the middle one triggers the cap. A coverage gap — the research ran out of
budget, an area was skipped — is excluded from scoring entirely, because penalising a company
for a limit of my own search would be measuring the wrong thing.

### How is the underlying data traceable?

Every extracted field carries its source URL and a confidence level. A market map whose numbers
cannot be traced back to a source collapses at the first factual challenge.

**This nearly failed silently, and how it was caught is the part worth telling.** The first
extraction run produced 50 pieces of evidence for ANYbotics, every one of them with a
confident-looking source: `outokumpu.com`, `petronas.com`, `anybotics.com`. All five criteria
came out `found` at HIGH confidence. Every single URL was fabricated.

The cause was a gap between two steps rather than a bad model. Collection names its sources in
prose and keeps the real URLs in a separate list; extraction was only ever sent the prose. Asked
for a URL per claim with none in front of it, the model produced something URL-shaped. My rule
*"drop any claim without a URL"* never fired — because a fabricated domain is not a missing one.

The fix is the interesting part. The source list is now sent to the extraction step, and an
evidence item whose URL is not among the pages the research actually retrieved is **deleted in
Python**, not merely discouraged in the prompt. A criterion left with nothing falls back to
`searched_not_found` and LOW.

Verified before spending anything further: replaying the broken record through the new rule
rejects 50 of 50 fabricated sources, while five genuine URLs pass. The five records that ship
carry **225 evidence items and 225 verifiable URLs**.

The general point, and the one I would actually make: *a rule that cannot fire is not a rule.*
It is worth checking that a safeguard can distinguish the failure it was written for from a
plausible imitation of success.

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

### What the scored data actually said

The five-company run does not test the acquisition hypothesis — it is too small, and both
acquired companies sit in the annex by construction. What it did produce is a different and
narrower argument, stated in `04-thesis.md`:

> European Physical AI value over the next three years accrues to narrow machines with regulated
> or contractual access to a site, not to general-purpose platforms — and the 2026 humanoid
> valuations in Europe are the mispricing this creates.

Three findings behind it, all traceable to the scores:

- **Only one criterion used its full range.** Technology scored 3–4 for everyone, team 3–4
  except Verity, timing 3–4 by design. Field traction ran 5, 5, 3, 2, 2 — and it is what
  produces the 86-to-54 spread. These companies are not separated by what they can build.
- **Capital and traction point in opposite directions in the middle of the table.** Verity
  reached 100+ confirmed sites on roughly $40–50M. Gravis holds a $1bn valuation with no
  confirmed repeat order; Humanoid raised $270M with no revenue-generating deployment before
  Q4 2026, by its own statement.
- **ETH supplies founders, not advantage.** Four of the five are ETH-linked and none reached a 5
  on technology. What moved team scores was an imported operator who had shipped fleets before —
  D'Andrea's Kiva lineage at Verity, Brain Corp at Humanoid. The scarce hire is not the PhD.

The thesis document also lists six named, dated conditions that would falsify it — including
Gravis publishing a fleet with unit counts before CONEXPO 2027, and Humanoid converting the
Schaeffler agreement into confirmed paid units by end-2027. Volunteer those: a thesis nobody can
disagree with is not a thesis.

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

Measured rather than anticipated, after the run:

- **A search budget manufactures absence.** The first ANYbotics collection ran 12 searches and
  concluded that no customer-side or regulatory source named the company. Re-run at 20, it found
  four — Outokumpu, PETRONAS, Equinor, GE Vernova. Since absent evidence caps a score, **the
  search budget was an input to the ranking, not only to the cost.** The budget is now 20, and
  four of the five reports still spent all of it, so a gap may still be truncation. Every capped
  score reads as *not found within 20 searches*, never as *does not exist*.
- **Nothing checks that evidence belongs to the criterion it was filed under.** A product
  announcement filed under field traction lifted mimic robotics' weakest criterion to HIGH on
  its own.
- **My rubric double-counts one fact.** ATEX certification scores under both technology and
  timing for ANYbotics. Found by the pipeline, not by me.
- **The scoring model never sees the web.** It scores the document collection produced, so a
  source that was missed propagates silently. The audit trail exists; auditing it is manual.
- **The step 1 prompt never asks for German-, French- or Italian-language sources**, which
  matters for a panel centred on Switzerland. Whether it changes coverage has not been measured.
- **Five companies cannot describe a sector.** No agriculture, surgical, defence, last-mile or
  fixed-infrastructure AMR company is in the set — an Exotec- or AutoStore-class business would
  very likely outrank ANYbotics on field traction.

---

## If asked what you would do next

- Widen field traction sourcing beyond public web data — customer case studies, job postings as
  a proxy for deployment engineering, trade press
- Re-run the pipeline quarterly and track score movement, since momentum is more informative
  than a single snapshot
- Expand the calibration set from 5 to 10 companies to tighten the agreement measurement
- Run step 1 on the remaining 21 companies — the only expensive part left, and the only thing
  standing between this and the full map
- Make confidence reflect how much evidence there is, not only what kind, now that mimic
  robotics has shown the two come apart
- Have the scoring step check that an item belongs to the criterion it was filed under, or
  separate technology evidence from traction evidence before it reaches the model
- Split the ATEX-style double count: one fact should not score under two criteria
