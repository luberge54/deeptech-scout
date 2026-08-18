# Physical AI in Switzerland and Europe — an opinionated market map

Generated 2026-08-18 from 5 scored companies.

This ranks companies building robots and autonomous machines that perceive and act
in the physical world. The criteria and their weights are the argument; the scores
are its consequence. Both are stated in
[`00-scoping.md`](00-scoping.md) and were fixed before any company was scored.

The weighting takes two positions worth disagreeing with: traction is redefined as
units deployed at paying customers rather than money raised, and timing is capped at
10 because the "why now" of Physical AI is identical for every company here.

## 1. The ranking

| # | Company | Score | Hand-score | Gap | Lowest-confidence criterion |
|---|---------|-------|------------|-----|------------------------------|
| 1 | **ANYbotics** | **86/100** | 93/100 | -7 | Market (MEDIUM) |
| 2 | **Verity** | **85/100** | 92/100 | -7 | none below HIGH |
| 3 | **Gravis Robotics** | **70/100** | 85/100 | -15 | none below HIGH |
| 4 | **Humanoid** | **59/100** | 77/100 | -18 | none below HIGH |
| 5 | **mimic robotics** | **54/100** | 60/100 | -6 | Market (MEDIUM) |

## 2. Calibration — the model against a blind hand-score

Five companies were scored by hand before any pipeline code existed. The model
never saw those scores. The comparison is the point of this project: a ranking
nobody has checked is an opinion with extra steps.

Disagreement per criterion, in notches out of 5. A negative number means the
model scored lower than the hand-score.

| Company | Field traction | Team / execution | Technology | Market | Timing | Total gap |
|---------|---|---|---|---|---|---|
| ANYbotics | — | — | -1 | -1 | — | **-7** |
| Verity | — | — | -1 | -1 | — | **-7** |
| Gravis Robotics | -1 | — | -2 | -1 | +1 | **-15** |
| Humanoid | -2 | — | — | -2 | — | **-18** |
| mimic robotics | — | -1 | -1 | +1 | — | **-6** |
| **Sum** | **-3** | **-1** | **-5** | **-4** | **+1** | |

**Agreement: 12 of 25 criterion scores identical, 22 of 25 within one notch.**

**Rank order: identical on both sides.**

Hand: ANYbotics > Verity > Gravis Robotics > Humanoid > mimic robotics

Model: ANYbotics > Verity > Gravis Robotics > Humanoid > mimic robotics

The argued verdict on each disagreement is in
[`00-scoping.md` §5](00-scoping.md#5-calibration-set).

## 3. The companies

### 1. ANYbotics — 86/100

Switzerland · legged robots for industrial inspection

| Criterion | Score | Weight | Points | Confidence | Hand-score |
|-----------|-------|--------|--------|------------|------------|
| Field traction | 5/5 | 30 | 30.0 | HIGH | 5/5 (M) |
| Team / execution | 4/5 | 25 | 20.0 | HIGH | 4/5 (H) |
| Technology | 4/5 | 20 | 16.0 | HIGH | 5/5 (H) |
| Market | 4/5 | 15 | 12.0 | MEDIUM | 5/5 (H) |
| Timing | 4/5 | 10 | 8.0 | HIGH | 4/5 (H) |

**Why these scores**

*Field traction.* This clears the top anchor on customer-side evidence, not just company claims. Outokumpu's own newsroom confirms three named ANYmal robots in daily service across three plants in Germany, Sweden and Finland, with a 2023 deal expanded in 2024 — that is one customer past pilot into a multi-site fleet with a repeat order. PETRONAS' own press release confirms a 2019 co-development moving to a signed commercial agreement in March 2022 to scale deployment. GE Vernova's own site describes a two-week PoC converting into deployment at a customer site in Ireland, and Equinor put an ANYmal D into the Northern Lights CCS facility integrated into its own Flotilla fleet software. Vendor/investor claims of ~200 units shipped and thousands of weekly inspections are company-sourced and discounted, but even without them the customer-side accounts alone establish repeat orders and units in daily service across multiple named industrials. A 3 would require each install to be custom with only 3-10 customers; the named roster (BP, Equinor, Novelis, Outokumpu, Equans, BASF, DSM-Firmenich, Grace) plus SLB as channel partner and RaaS commercial packaging exceeds that.
Sources: [1](https://www.outokumpu.com/en/news/2024/outokumpu-to-expand-the-use-of-robotics-in-safety-management-%E2%80%93-first-anymal-robot-%E2%80%9Cjokkeri%E2%80%9D-started-operating-at-the-company%E2%80%99s-site-in-tornio,-finland-3460793), [2](https://www.petronas.com/media/media-releases/petronas-partners-anybotics-ag-commercialise-anymal-x), [3](https://www.gevernova.com/news/articles/power-couple-how-ge-vernova-anybotics-are-transforming), [4](https://www.roboticstomorrow.com/article/2026/03/anymal-deployed-at-northern-lights-ccs-facility/26213), [5](https://www.businesswire.com/news/home/20241212175922/en/TDK-Ventures-Invests-in-ANYbotics-a-World-Leader-in-Industrial-Inspection-Autonomous-Robots), [6](https://www.climateinvestment.com/news/climate-investment-ci-joins-investment-in-anybotics-to-transform-oil-gas-inspection-through-autonomous-robotics)

*Team / execution.* The scale explicitly caps ETH/EPFL pedigree at 3, and this is the archetypal ETH RSL spin-off (Fankhauser, Hutter, Fässler). What pushes above 3 is the multi-generation shipping record rather than the pedigree: ALoF (2009) to StarlETH (2012) to ANYmal Alpha (2015) to commercial ANYmal C deliveries from 2020, ANYmal D as fourth generation, and the separately certified ANYmal X unveiled 2022 with commercial orders in 2023 — that is well past 'one generation shipped.' Hiring has scaled from ~100 to ~200-260 across sources, and it has pulled a Chief Product Officer with May Mobility, Intel and Qualcomm background, evidencing senior big-tech draw. It does not reach 5 because no founder has shipped hardware at scale before, generation cycles are long (2015 prototype to 2020 first deliveries, ANYmal X commercial launch still targeted for 2026 four years after unveiling) rather than shortening, and headcount figures are irreconcilable. Funding (~$150M cumulative) counts here only as resourcing, and it is substantial.
Sources: [1](https://rsl.ethz.ch/partnership/spinoff/anybotics.html), [2](https://www.anybotics.com/about-us/company/), [3](https://baike.baidu.com/en/item/ANYmal/2406921), [4](https://www.anybotics.com/robotics/anymal/), [5](https://www.chemengonline.com/anybotics-robotic-deployment-at-northern-lights-carbon-capture-and-storage/), [6](https://theaiinsider.tech/2025/09/23/anybotics-total-funding-at-150-million-after-climate-investments-joins-to-scale-autonomous-inspection-in-hazardous-sites/)

*Technology.* The decisive item for above-3 is the ATEX/IECEx Zone 1 IIB certification on ANYmal X — a multi-year certification path (co-development from 2019, unveiled 2022, commercial launch targeted 2026) that is exactly the 'multi-year certification' moat named in the 5 anchor, and it is a hard barrier competitors cannot shortcut. Supporting depth: the proprietary ANYdrive actuator (frameless motor, harmonic reducer, planar spiral spring) now industrialized with maxon, IP67 rating, and an AWS-based fleet backend deploying identical containers across sites, with a Data Navigator analytics layer that processed 2,500+ inspections in two weeks across Grace, Outokumpu and DSM-Firmenich — the beginnings of a data flywheel. It stops short of 5 because the IP position is thin and partly borrowed: only 8 patents filed per CB Insights, and a reported patent licensing fee paid to Boston Dynamics in 2019; the actuator is now produced by an external supplier, and the inspection-data asset is only described in pilot terms rather than demonstrated to compound into model performance. Above 3 because the certification is not 'broadly available.'
Sources: [1](https://www.anybotics.com/robotics/anymal-x/), [2](https://baike.baidu.com/en/item/ANYmal/2406921), [3](https://www.therobotreport.com/maxon-anybotics-partner-drives-anymal-legged-inspection-robot/), [4](https://www.cbinsights.com/company/anybotics-patents), [5](https://www.historytools.org/companies/boston-dynamics-guide), [6](https://www.therobotreport.com/anybotics-launches-data-navigator-unlock-value-inspection-data/), [7](https://aws.amazon.com/blogs/robotics/anybotics-uses-aws-to-deploy-a-global-robot-workforce-for-industrial-inspections/)

*Market.* The buyers are named and they are already purchasing in this category: BP, Equinor, Petrobras, ENI, PETRONAS, Shell, SLB in oil & gas; BASF, Borealis, DSM-Firmenich, Grace in chemicals; Outokumpu and Novelis in metals; GE Vernova, Siemens Energy and Swiss nuclear KKL/Axpo in power. Inspection and asset-integrity is an existing, budgeted line item at these operators — Outokumpu framed it under safety management, and GE Vernova folded it into its own APM software, evidence of an established procurement slot rather than a speculative new one. SLB as 'preferred ground robotics supplier' gives a channel into that budget, and RaaS lowers capex friction. It falls short of 5 because the segment is visibly crowded — ANYbotics itself markets against Boston Dynamics' Spot, and Unitree and others are listed as competitors — and heavy-industry/oil-major procurement cycles are long (PETRONAS 2019 engagement to 2026 full commercial launch), which is precisely the starving-cycle risk in the 3 anchor. Above 3 because the pain (Ex-zone human inspection) is urgent and safety-driven with buyers already spending.
Sources: [1](https://www.anybotics.com/news/anybotics-establishes-platform-to-accelerate-industrial-robotic-inspection/), [2](https://www.anybotics.com/news/anybotics-partners-with-slb-to-advance-autonomous-robotics-operations-in-oil-gas/), [3](https://roboticsandautomationnews.com/2023/04/06/anybotics-to-provide-steelmaker-outokumpu-with-its-canine-inspection-robot/66462/), [4](https://www.anybotics.com/news/how-to-hire-an-industrial-inspection-robot-part-2/), [5](https://tracxn.com/d/companies/anybotics/__Vn7BHz9bBT8R2cLQ_B1B3hHf-47uVwxrlBrVPLPTLUc), [6](https://www.gevernova.com/news/articles/power-couple-how-ge-vernova-anybotics-are-transforming)

*Timing.* There is a dateable unlock, but it is one ANYbotics manufactured rather than one handed to it by the outside world. The ATEX/IECEx Zone 1 certification of ANYmal X — co-development from 2019, public unveiling 22 March 2022 at OTC Asia, Early Adopter Program 2022, commercial ordering 2023 — is a specific, dated regulatory threshold that opens Zone 1 hazardous areas that were previously closed to any legged robot, and it is what makes the oil & gas and chemicals pipeline addressable now. The Climate Investment round of September 2025, from a fund owned by OGCI members (Aramco, BP, Chevron, Equinor, ExxonMobil, Shell), also points to a customer-side decarbonization/emissions-monitoring mandate driving demand at a datable moment. It is not a 5 because the certification is the company's own achievement on a schedule it set, with full commercial launch still pushed to 2026, and no external regulation or component price threshold is shown compelling buyers to act by a given date; the 2022 anti-weaponization pledge is explicitly not a regulation. It is above the default 3 because the evidence names a concrete, dated gating event rather than merely riding the general Physical AI wave.
Sources: [1](https://www.anybotics.com/news/anymal-x-the-worlds-first-ex-proof-legged-robot/), [2](https://www.anybotics.com/robotics/anymal-x/), [3](https://www.climateinvestment.com/news/climate-investment-ci-joins-investment-in-anybotics-to-transform-oil-gas-inspection-through-autonomous-robotics), [4](https://www.greaterzuricharea.com/en/news/anybotics-sends-inspection-robots-explosive-environments)

**Contradictions in the sources, left unresolved**

- Headcount figures are inconsistent across sources and dates, ranging from 'more than 100' (older LinkedIn copy) to 'more than 190' (2025 job posting) to 'over 200 experts' (Dec 2024 release) to 251 (Tracxn, March 2026) to 260 (RocketReach) to Wikipedia's static '150'; these are not reconcilable without knowing each source's snapshot date.
- Unit-count and reservation figures are muddled: '500 ANYmal X quadrupeds reserved' (2023, a pre-order figure) versus 'over 200 units... shipped' and 'approximately 200 ANYmal robots... deployed' (2024-2025 releases); unclear whether the ~200 figure includes only ANYmal/ANYmal D or also ANYmal X, and whether 'shipped' equals 'actively deployed.'
- Funding totals vary by currency and rounding: reports cite '$130 million,' 'over $150 million,' and 'over €127 million' as the cumulative total at different points in 2024-2025, without a single reconciled ledger.
- All specific unit/fleet figures trace back to ANYbotics or its investors' own statements, even when repeated by trade press; the strongest independent confirmations found are the Outokumpu, PETRONAS, Equinor, and GE Vernova customer-side accounts, but none of these publish a company-wide fleet total.
- Patent depth is thin: only '8 patents' filed per CB Insights, and one historical account notes ANYbotics paid Boston Dynamics a patent licensing fee in 2019, suggesting partial reliance on external IP; no primary patent filings were reviewed directly to confirm scope or currency of this.

### 2. Verity — 85/100

Switzerland · autonomous indoor drones for warehouse inventory tracking

| Criterion | Score | Weight | Points | Confidence | Hand-score |
|-----------|-------|--------|--------|------------|------------|
| Field traction | 5/5 | 30 | 30.0 | HIGH | 5/5 (H) |
| Team / execution | 5/5 | 25 | 25.0 | HIGH | 5/5 (H) |
| Technology | 3/5 | 20 | 12.0 | HIGH | 4/5 (M) |
| Market | 4/5 | 15 | 12.0 | HIGH | 5/5 (H) |
| Timing | 3/5 | 10 | 6.0 | HIGH | 3/5 (M) |

**Why these scores**

*Field traction.* This goes well past the 3-anchor of "3-10 customers, each install custom." IKEA/Ingka deploying 100 drones across 16 European locations, KeHE starting at one Arizona site in summer 2023 and then rolling out across US distribution centers (the Portland site being cited as the 100th installation) is a textbook repeat order and pilot-to-fleet expansion; DSV runs Verity across multiple sites including a 10,000+ pallet-location facility, and On has a fleet scanning daily at a US plant. Named, customer-attributed quotes exist from DSV, KeHE and On, not just Verity's own count. It falls short of nothing in the anchor; the counts (30 sites 2023 → 100+ 2024 → 150+ 2025) are company-sourced and one Maersk pilot site is confirmed dead, which is why this is a 5 on the strength of the customer-confirmed fleet expansions rather than on the headline numbers alone.
Sources: [1](https://www.automatedwarehouseonline.com/verity-inventory-drones-surpass-100-warehouse-sites/), [2](https://supplychaindigital.com/technology/ups-dsv-maersk-trust-verity-for-operational-visibility), [3](https://www.boringbusinessnerd.com/startups/verity), [4](https://www.robotics247.com/article/case_study_haleon_strengthens_supply_chain_performance_with_verity_drones), [5](https://www.greaterzuricharea.com/en/news/deploys-inventory-drones-verity), [6](https://thenewwarehouse.com/2025/09/03/622-warehouse-inventory-accuracy-takes-off-with-verity/), [7](https://www.supplychaindive.com/news/Maersk-verity-drones-warehouse-management/628296/)

*Team / execution.* The ETH/EPFL spinout pedigree alone would cap at 3, but co-founder Raffaello D'Andrea also co-founded Kiva Systems, which shipped warehouse robots at scale and was acquired by Amazon in 2012 — prior hardware shipped at scale, which is exactly the 5 anchor. Beyond that there is generational evidence: a live-events drone business (30,000+ autonomous flights over people, 7,000 incident-free at Cirque du Soleil) preceded the warehouse product launched in 2020, and the FCC filing shows the company now on a Series 4 indoor system. Hiring is not flat or purely academic — field, manufacturing, test, refurbishment and contract-manufacturing quality roles are open, and senior hires include an ex-Covariant business development head; ~80-100+ staff. This exceeds 4 because both conditions of the top anchor (prior at-scale hardware and multiple shipped generations) are evidenced, not just one.
Sources: [1](https://www.einpresswire.com/article/621916511), [2](https://ethz.ch/en/news-and-events/eth-news/news/2021/08/verity-drones-warehouse.html), [3](https://insidetowers.com/more-drones-granted-exemptions-from-fcc-covered-list/), [4](https://www.prnewswire.com/news-releases/verity-studios-drones-dance-with-drake-in-songs-elevate-and-look-alive-300699191.html), [5](https://www.ziprecruiter.com/Jobs/Drone-Engineer), [6](https://www.boringbusinessnerd.com/startups/verity)

*Technology.* Above 1 clearly: the drones are purpose-built rather than commodity hardware (The Robot Report explicitly contrasts Verity's custom airframes with Gather AI's off-the-shelf approach), GPS-denied SLAM navigation runs unattended ceiling-to-floor scans off-hours at claimed 99.9% accuracy, and there is genuine control-theory depth (learned quadcopter control from Hehn's ETH doctorate; a propulsion-failure safe-landing algorithm). But it does not reach 4-5 because the approach is demonstrably available to others — the same market contains Gather AI, Corvus, EyeSee Drones, B Garage and inventAIRy XL doing indoor inventory drones, and the safe-landing algorithm is described as something that "can be integrated in all quadrotors," i.e. portable rather than unbuyable. No evidence of a proprietary data flywheel that compounds with each scan, and the only certification cited (FCC Covered List conditional approval) is time-limited to end-2026 rather than a multi-year moat. The RFID noise-rejection add-on is a differentiator but is described only by Verity's own CRO.
Sources: [1](https://www.therobotreport.com/gather-ai-acquires-assets-of-ware-robotics-to-consolidate-drone-based-inventory-market/), [2](https://insidetowers.com/more-drones-granted-exemptions-from-fcc-covered-list/), [3](https://www.cello-square.com/en/blog/view-1845.do), [4](https://www.greaterzuricharea.com/en/drone-technology), [5](https://thenewwarehouse.com/2025/09/03/622-warehouse-inventory-accuracy-takes-off-with-verity/)

*Market.* Better than the 3 anchor because the pain is already budgeted and bought: DSV's operations manager frames the drones against contractual SLA requirements for specific order types, i.e. an operational necessity, and the buyer set spans 3PL (DSV, UPS SCS, Maersk/Performance Team), retail (Ingka/IKEA), food distribution (KeHE), CPG (Haleon) and footwear manufacturing (On) — these are firms that purchase inventory-accuracy tooling today, and KeHE's multi-DC rollout shows procurement cycles that are not startup-starving. Held back from 5 by crowding that the evidence itself documents: at least five direct competitors (Gather AI, Corvus, EyeSee, B Garage, inventAIRy XL) and an ongoing consolidation event in which Gather AI absorbed Ware Robotics — a sign the category is contested and possibly not yet large enough to support all entrants.
Sources: [1](https://supplychaindigital.com/technology/ups-dsv-maersk-trust-verity-for-operational-visibility), [2](https://www.automatedwarehouseonline.com/verity-inventory-drones-surpass-100-warehouse-sites/), [3](https://www.therobotreport.com/gather-ai-acquires-assets-of-ware-robotics-to-consolidate-drone-based-inventory-market/), [4](https://www.cello-square.com/en/blog/view-1845.do), [5](https://robotics.press/news/corvus-robotics-company-profile/)

*Timing.* No specific dateable unlock explains why now. The one regulatory fact that is genuinely permissive — FAA Part 107 not applying to indoor-only operations — has been true throughout and is a standing condition, not a change; indeed the company was founded in 2014 and launched the warehouse product in 2020, so the enabling environment long predates the present. The dated FCC/Pentagon Covered List item is a conditional import/marketing approval expiring 31 December 2026, which is a compliance hurdle Verity had to clear as a non-US manufacturer rather than a market-opening mandate. The cited "since 2019 indoor inventory drones reshaped industrial drone use" is exactly the general Physical AI/warehouse-automation wave that the default anchor covers. Above 1 because the company did not sit on an obvious opportunity — the 2019-2020 emergence of the indoor inventory-survey category is real and Verity launched into it — but nothing here earns 4 or 5.
Sources: [1](https://www.faa.gov/faq/do-faa-rules-and-regulations-apply-commercial-uas-or-drone-operations-conducted-indoors-only), [2](https://insidetowers.com/more-drones-granted-exemptions-from-fcc-covered-list/), [3](https://www.cello-square.com/en/blog/view-1845.do)

**Contradictions in the sources, left unresolved**

- LinkedIn's own company page states 'more than 100' employees, while a third-party startup profile states 'approximately 80 people.' Neither figure is independently audited.
- Deployment figures cited over time (30 sites in March 2023, 80 warehouses in 2023/2024, 100 customer warehouses/sites in Aug-Sept 2024, 150 global deployments in Sept 2025) all trace back to Verity's own statements, even when repeated by trade press; no independent third party has published its own unit count.
- Tracxn lists the March 2023 Series B tranche as '$38.8M' while Verity's own press release and multiple wire outlets state '$32M' (30M CHF) for that same tranche, with an additional $11M in July 2023 — a discrepancy of roughly $7M.
- Verity/trade press cite Maersk as a flagship logo, but Supply Chain Dive's independent reporting is the only source noting that the original Miami pilot site is confirmed by Maersk to be 'no longer operational'; later Maersk references (e.g., in RFID pilot news, 2025 podcast) do not clarify whether these are new/different sites.

### 3. Gravis Robotics — 70/100

Switzerland · autonomy retrofit kits for heavy construction machinery

| Criterion | Score | Weight | Points | Confidence | Hand-score |
|-----------|-------|--------|--------|------------|------------|
| Field traction | 3/5 | 30 | 18.0 | HIGH | 4/5 (H) |
| Team / execution | 4/5 | 25 | 20.0 | HIGH | 4/5 (H) |
| Technology | 3/5 | 20 | 12.0 | HIGH | 5/5 (H) |
| Market | 4/5 | 15 | 12.0 | HIGH | 5/5 (H) |
| Timing | 4/5 | 10 | 8.0 | HIGH | 3/5 (H) |

**Why these scores**

*Field traction.* The evidence reaches named, multi-country counterparties beyond pure demos: Holcim invested and expanded Gravis from construction into quarry work explicitly 'following a successful UK pilot', Kibag in Switzerland is running Gravis kit on Develon machines, and Flannery Plant Hire has a distribution-style arrangement plus the $8M CAM Pathfinder project. That is more than the 1-anchor (demos/pilots/LOIs). But it does not reach 5: there is no evidence of repeat orders, no unit counts, no customer described as past pilot into a fleet. The most concrete recent items are still framed as trials and shows — a 'UK-first trial' of an autonomous excavator at Manchester Airport (Oct 2025), Bauma 2025 live demonstrations, and a planned CONEXPO 2026 Hitachi demo. The 'seven countries / four continents' and 'dozens of brands' claims are company statements relayed by press, not third-party confirmation, and no paying-customer count or revenue is confirmed by a primary source (only an aggregator's unverified $10.1M). Roughly 3-10 named accounts, each install custom per machine brand, is exactly the 3 anchor.
Sources: [1](https://www.holcim.com/media/company-news/holcim-invests-in-gravis-robotics), [2](https://www.newcivilengineer.com/innovative-thinking/gravis-robotics-secures-17-4m-in-funding-to-roll-out-automated-excavators-globally-01-12-2025/), [3](https://www.gravisrobotics.com/news), [4](https://www.therobotreport.com/gravis-robotics-raises-200m-autonomous-construction/), [5](https://www.equipmentworld.com/technology/article/15746115/video-gravis-robotics-unveils-earthmoving-autonomy-platform), [6](https://www.hitachicm.com/us/en/news/2026/hitachi-construction-machinery-to-demonstrate-augmented-machine-/), [7](https://roboticsandautomationnews.com/2026/08/17/gravis-robotics-raises-200-million-to-scale-its-construction-robotics-business/104199/)

*Team / execution.* This is an ETH Zurich spin-off, which the rubric caps at 3 on pedigree alone — Johns and Jud come out of the HEAP walking-excavator programme, with Marco Hutter (DARPA SubT winner) on the board. What lifts it above 3 is shipped product iteration plus extraordinary resources: the Rack retrofit kit went from first work with Menzi Muck to OEM-revealed integrations with CASE, Develon, Hitachi, Menzi Muck, Sumitomo and Yanmar at Bauma April 2025, followed by a second-generation 'Copilot' system debuted at CONEXPO March 2026 — two generations inside about eighteen months. Capital went from a $23m round (Nov) to a $200m SoftBank Series A at $1bn post-money (Aug 2026), a statement about resources to hire and scale. It does not reach 5: no founder has shipped hardware at volume before, the founders are academics and an architect by background, headcount is unconfirmed (26 vs 55 across two aggregators), and there is no evidence of pulling senior talent out of big tech.
Sources: [1](https://dfab.ch/de/news/foundation-of-the-eth-spin-off-gravis-robotics), [2](https://techfundingnews.com/gravis-robotics-ai-autonomy-construction-machinery/), [3](https://roboticsbusinessnews.com/news/38/1078/gravis-robotics-debuts-autonomous-earthmoving-platform-at-bauma-2025-turning-heavy-equipment-into-smarter-teammates.html), [4](https://www.gravisrobotics.com/news), [5](https://sifted.eu/articles/gravis-robotics-1bn-valuation-200m-softbank), [6](https://www.enr.com/articles/63517-200m-funding-round-set-for-automated-equipment-startup-gravis-robotics)

*Technology.* The Rack is a genuinely engineered retrofit stack — five surround cameras, lidar, onboard compute, GNSS, plus the Slate 3D tablet interface — backed by nearly a decade of ETH heavy-machinery autonomy research, and the learning-based controller that infers soil state from hydraulic pressure, vibration and engine strain is more than a bolt-on perception kit. That places it well above 1. It does not reach 5 because nothing in the evidence shows compounding: no proprietary data flywheel is documented (only a company description of the control approach), no unbuyable component (cameras, lidar, GNSS are commodity), and no multi-year certification barrier. BuiltWorlds explicitly places Gravis alongside Hive Autonomy and SafeAI doing retrofittable autonomy on heavy machinery, i.e. the approach is broadly available. The CEO's own framing — that OEMs' move to electronic joystick signals makes it easy to plug in a retrofit computer — cuts against defensibility, since the same door opens for competitors.
Sources: [1](https://www.ivtinternational.com/features/case-study-gravis-robotics-drives-intelligent-automation-for-kteg-battery-powered-excavator.html), [2](https://www.gravisrobotics.com/press-release), [3](https://www.forbes.com/sites/johnkoetsier/2026/08/17/excavators-meet-ai-gravis-nabs-200-million-from-softbank-to-give-construction-equipment-brains/), [4](https://rsl.ethz.ch/partnership/spinoff/gravisrobotics.html), [5](https://builtworlds.com/insights/2025-robotics-top-50-list/)

*Market.* The buyers named are organisations that already purchase in this category: Holcim (quarrying), Taylor Woodrow and Morgan Sindall (contractors), and Flannery Plant Hire, the UK's largest equipment rental provider, whose entire business is putting machines on sites — retrofit autonomy sits on an existing plant-hire budget line rather than requiring a new one. The autonomous construction equipment market is independently sized at $8.8bn in 2023 growing >7.5% annually (Global Market Insights via Fortune), and the UK's $716bn infrastructure pipeline is a real demand backdrop. It falls short of 5 because the segment is contested by comparable retrofit players (SafeAI, Hive Autonomy per BuiltWorlds) and because construction/quarry procurement runs through slow contractor and rental-fleet cycles; the $1.6 trillion 'earthmoving industry' figure is a company TAM claim, not a served market. Above 3 because the pain is budgeted and the buyers are already named and transacting, not merely addressable.
Sources: [1](https://www.newcivilengineer.com/innovative-thinking/gravis-robotics-secures-17-4m-in-funding-to-roll-out-automated-excavators-globally-01-12-2025/), [2](https://www.holcim.com/media/company-news/holcim-invests-in-gravis-robotics), [3](https://fortune.com/2025/11/28/gravis-robotics-fundraise-23m-construction-labor-shortage-ai-automation-equipment/), [4](https://www.therobotreport.com/gravis-robotics-raises-200m-autonomous-construction/), [5](https://builtworlds.com/insights/2025-robotics-top-50-list/), [6](https://www.gravisrobotics.com/series-a)

*Timing.* Above the default 3 because two concrete, company-specific unlocks are documented rather than the generic Physical AI wave. First, the CEO identifies a technical threshold: OEMs' industry-wide switch from hydraulic pilot-stage joysticks to electronic joystick signals, which is what makes a plug-in retrofit computer able to command the machine directly — Gravis's entire retrofit business model depends on that transition having happened. Second, an $8m UK government-backed CAM Pathfinder award for construction automation with Flannery, reported around August 2026, is a dated public-funding event that pulls demand forward. Not a 5 because neither is a hard mandate or a regulatory deadline with a fixed date — the joystick transition is gradual and undated in the evidence, and the Pathfinder grant is a funding programme rather than a customer mandate. The labour-shortage and infrastructure-boom arguments are the generic sector tailwind and carry no weight here.
Sources: [1](https://www.ivtinternational.com/features/case-study-gravis-robotics-drives-intelligent-automation-for-kteg-battery-powered-excavator.html), [2](https://www.therobotreport.com/gravis-robotics-raises-200m-autonomous-construction/), [3](https://rsl.ethz.ch/partnership/spinoff/gravisrobotics.html)

**Contradictions in the sources, left unresolved**

- fundz.net's acquisitions tracker states SoftBank Group acquired Gravis Robotics on July 26, 2026, in a deal potentially exceeding a $500 million valuation. Every other financial-press source (ENR, Sifted, Forbes, The Robot Report, EU-Startups) describes the same capital event as a $200M Series A investment (not an acquisition) valuing the company at $1bn post-money.
- RocketReach lists 55 employees for Gravis Robotics, while Growjo states 26 employees plus a claimed $10.1M in annual revenue. Neither source is a primary company disclosure, and no company-confirmed headcount was found.
- Most press (TechFundingNews, EU-Startups, ENR, Forbes) names Ryan Luke Johns (CEO) and Dominic Jud (CTO) as co-founders with Marco Hutter as a board member/co-founder. A Chinese-language innovation listing (36kr) adds Marco Tranzatto and Burak Çizmeci as additional co-founders. CB Insights' people page states Gravis Robotics has 1 executive and that its founder is Marco Hutter, which does not corroborate the fuller founder list.

### 4. Humanoid — 59/100

United Kingdom · humanoid robots for industrial and manufacturing work

| Criterion | Score | Weight | Points | Confidence | Hand-score |
|-----------|-------|--------|--------|------------|------------|
| Field traction | 2/5 | 30 | 12.0 | HIGH | 4/5 (H) |
| Team / execution | 4/5 | 25 | 20.0 | HIGH | 4/5 (H) |
| Technology | 3/5 | 20 | 12.0 | HIGH | 3/5 (M) |
| Market | 3/5 | 15 | 9.0 | HIGH | 5/5 (H) |
| Timing | 3/5 | 10 | 6.0 | HIGH | 3/5 (M) |

**Why these scores**

*Field traction.* The confirmed activity is all proof-of-concept: a Siemens Erlangen trial (60 totes/hour), a six-week Ford Cologne trial (97% reliability, 83 picks/hour), and a Bosch intralogistics POC completed March 2026. Company evidence explicitly states no revenue-generating, non-POC deployment exists and that Beta robots only reach customer sites in Q4 2026. That would be a 1 on the anchor, but it is lifted above pure pilots/LOIs by Schaeffler's own press office confirming a *binding*, phased deployment and supply agreement for a four-digit unit count by 2032 with first systems live in Germany before end-2026 — a customer-side commitment stronger than an LOI, from a partner that also invested. It cannot reach 3 because there are no paying installs at 3-10 customers: the claimed 'nine industrial deployments with Fortune 500 customers' is single-sourced, self-reported and internally inconsistent (NVIDIA appears elsewhere only as a compute partner), and the 34,000 pre-orders/$2.4B is flagged unverified by multiple outlets.
Sources: [1](https://press.siemens.com/global/en/pressrelease/siemens-and-humanoid-bring-physical-ai-factory-floor-deploying-humanoids-industrial), [2](https://www.euronews.com/next/2026/01/20/can-humanoid-ai-robots-really-handle-arduous-factory-work-a-new-ford-factory-trial-exceeds), [3](https://www.schaeffler.com/en/media/press-releases/press-releases-detail.jsp?id=88159744), [4](https://www.therobotreport.com/humanoid-partners-with-bosch-schaeffler-scale-robot-production/), [5](https://thehumanoid.ai/humanoid-raises-152-million-at-1-35-billion-post-money-valuation-becoming-europes-first-pure-play-humanoid-robotics-unicorn/), [6](https://techfundingnews.com/humanoid-152m-europe-first-humanoid-robotics-unicorn/), [7](https://theroboticsmedia.com/article/humanoid-152-million-series-a-135-billion-prime-movers-lab-schaeffler-bosch-july-21-2026)

*Team / execution.* Above a 3 because the senior bench is not merely credible-technical: CTO Jarad Cannon was CTO at Brain Corp through growth from 5 to over 40,000 deployed robots and spent six years at iRobot — i.e. someone who has shipped robots at fleet scale — and the founder previously scaled and sold a ~$1B-revenue manufacturing business, seeding this one with ~$30M of his own capital. Two hardware generations were unveiled inside 15 months (wheeled Alpha Sept 2025, bipedal Alpha Dec 2025) with shortening build cycles (7 months then 5 months), ~200 staff across London, Boston and Vancouver, and $270M raised including strategic money from Schaeffler and Bosch. It stops short of 5 because the generation timelines and the '48 hours to walking' claim are company-reported and explicitly flagged unverified by TheNextWeb, and neither generation has yet shipped in volume — the shipping-at-scale record belongs to a hired executive's prior employer, not to this team's own output.
Sources: [1](https://thehumanoid.ai/humanoid-appoints-jarad-cannon-as-chief-technology-officer-to-lead-innovation-in-human-robot-collaboration/), [2](https://thenextweb.com/news/humanoid-152m-series-a-robotics-unicorn-bosch), [3](https://thehumanoid.ai/humanoid-unveils-the-uks-first-humanoid-robot-for-industrial-use/), [4](https://thehumanoid.ai/humanoid-unveils-record-breaking-bipedal-robot-walking-48-hours-after-assembly/), [5](https://www.businesswire.com/news/home/20260723238282/en/Humanoid-Raises-$152-Million-at-$1.35-Billion-Post-Money-Valuation-Becoming-Europes-First-Pure-Play-Humanoid-Robotics-Unicorn), [6](https://techfundingnews.com/humanoid-152m-europe-first-humanoid-robotics-unicorn/)

*Technology.* There is genuine engineering depth — a 41-DoF, 70kg wheeled platform with 15kg payload, and the KinetIQ four-layer stack with a trial-and-error learning variant and fleet orchestration — so this is above a 1. But the autonomy substrate is the standard purchasable one: Siemens' own release confirms Humanoid has integrated NVIDIA's full physical AI stack (Jetson Thor, Isaac Sim, Isaac Lab), which is available to every competitor. It falls short of 4-5 because nothing in the evidence compounds or is unbuyable: the actuators come from Schaeffler as external preferred supplier (>50% of demand), manufacturing is outsourced to Robert Bosch Robotics, KinetIQ's proprietary claim is company-attributed with no technical corroboration, and there is no certification moat or accumulating proprietary operating dataset described.
Sources: [1](https://www.therobotreport.com/uk-based-humanoid-secures-152m-in-series-a-funding/), [2](https://press.siemens.com/global/en/pressrelease/siemens-and-humanoid-bring-physical-ai-factory-floor-deploying-humanoids-industrial), [3](https://drivesncontrols.com/uk-start-up-says-its-modular-humanoid-robots-will-cut-costs/), [4](https://www.schaeffler.com/en/media/press-releases/press-releases-detail.jsp?id=88159744), [5](https://thenextweb.com/news/humanoid-152m-series-a-robotics-unicorn-bosch)

*Market.* Sizeable but demonstrably crowded and slow, which is exactly the 3 anchor. The founder himself names Tesla, Agility and Figure AI as competitors, and press notes Neura Robotics closed over $1B in Europe at a higher valuation — this is the most contested category in the sector. The cited market figure (~$38B by 2035, Goldman Sachs) is a future projection rather than an existing budget line, and the one binding commitment stretches procurement out to 2032, the kind of cycle that starves a startup. It is above a 1 because the targets — warehouse picking, kitting, machine feeding, load/unload at automotive and electronics plants — are large industrial segments where buyers like Schaeffler have signed for a RaaS structure, showing real willingness to spend; it does not reach 4-5 because no evidence shows buyers today making volume purchases in the humanoid category at scale.
Sources: [1](https://thehumanoid.ai/humanoid-unveils-the-uks-first-humanoid-robot-for-industrial-use/), [2](https://thehumanoid.ai/humanoid-secures-landmark-deal-with-schaeffler-to-deploy-thousands-of-humanoid-robots/), [3](https://www.unite.ai/artem-sokolov-founder-of-humanoid-interview-series/), [4](https://thenextweb.com/news/humanoid-152m-series-a-robotics-unicorn-bosch), [5](https://techfundingnews.com/humanoid-152m-europe-first-humanoid-robotics-unicorn/)

*Timing.* The timing evidence is the sector-wide wave rather than a company-specific unlock. The strongest item — the roadmap being framed around the newly released NVIDIA Jetson Thor — is a component availability event equally available to every humanoid competitor, and it is a company-authored framing rather than an external mandate. The Siemens/NVIDIA CES partnership is a customer-side dateable event but it is Siemens' programme, not a mandate to buy from Humanoid. The remaining items ($18.8B robotics funding in 2026, $55.8B per Dealroom) are pure macro capital context, which is the definition of the default. Not a 1, because a concrete component release and a named customer AI-factory programme do anchor the 'why now'; not a 4-5, because no regulation, cost threshold crossing, or customer purchase mandate specific to this company is documented.
Sources: [1](https://thehumanoid.ai/humanoid-leads-uk-innovation-with-nvidia/), [2](https://press.siemens.com/global/en/pressrelease/siemens-and-humanoid-bring-physical-ai-factory-floor-deploying-humanoids-industrial), [3](https://theroboticsmedia.com/article/humanoid-152-million-series-a-135-billion-prime-movers-lab-schaeffler-bosch-july-21-2026), [4](https://startupfortune.com/london-startup-humanoid-becomes-europes-first-humanoid-robotics-unicorn/)

**Contradictions in the sources, left unresolved**

- One trade outlet reports Humanoid claims nine industrial deployments with Fortune 500 customers including NVIDIA, SAP, and Siemens; this is not corroborated elsewhere, and NVIDIA's role is otherwise described as a compute/technology partner rather than a deployment customer, and no other source mentions an SAP deployment.
- Widely repeated company claim of 34,000 pre-orders worth $2.4 billion is explicitly flagged as self-reported and unverified by multiple outlets.
- Humanoid's claim to be Europe's first pure-play humanoid robotics unicorn is contested by TheNextWeb, which notes Germany's Neura Robotics closed a round exceeding $1 billion in June 2026 at a reportedly higher valuation.
- Company timelines (seven months for wheeled Alpha, five months for bipedal, 48 hours to stable walking) are self-reported and explicitly noted by TheNextWeb as unverified.

### 5. mimic robotics — 54/100

Switzerland · dexterous robotic manipulation using imitation learning

| Criterion | Score | Weight | Points | Confidence | Hand-score |
|-----------|-------|--------|--------|------------|------------|
| Field traction | 2/5 | 30 | 12.0 | HIGH | 2/5 (H) |
| Team / execution | 3/5 | 25 | 15.0 | HIGH | 4/5 (H) |
| Technology | 3/5 | 20 | 12.0 | HIGH | 4/5 (M) |
| Market | 3/5 | 15 | 9.0 | MEDIUM | 2/5 (L) |
| Timing | 3/5 | 10 | 6.0 | MEDIUM | 3/5 (M) |

**Why these scores**

*Field traction.* Every customer claim is unnamed and company-sourced: the November 2025 release asserts pilots with "Fortune 500 companies and global automotive brands" and logistics partners, and SiliconANGLE explicitly notes no names were disclosed. The ETH AI Center framing is "deepen pilot collaborations," i.e. still pilots. What lifts this above a pure 1 is one concrete, journalist-stated placement — FLUX-mimic taken "to the factory floor at Audi" in July 2026 — plus hiring for a Forward Deployed Robotics Engineer and Field Engineer, which implies real on-site work. But nothing shows a paying deployment, a unit count, or a repeat order, so it cannot reach the 3 anchor of paying deployments at ~3-10 customers; the only price point ($90k stations) is an unsourced Sacra estimate.
Sources: [1](https://www.globenewswire.com/news-release/2025/11/03/3179052/0/en/mimic-robotics-raises-16-million-to-deploy-frontier-physical-AI-across-industries.html), [2](https://siliconangle.com/2025/11/04/mimic-raises-16m-build-ai-models-human-like-robotic-hands/), [3](https://roboticsandautomationnews.com/2026/07/29/mimic-robotics-introduces-frontier-video-action-models-to-the-factory-floor-at-audi/103705/), [4](https://www.mimicrobotics.com/careers), [5](https://ai.ethz.ch/news-and-events/ai-center-news/2025/09/mimic_Robotics_Seed_Round_2025.html), [6](https://sacra.com/c/mimic-robotics/)

*Team / execution.* This is the ETH spinout profile the anchor caps at 3: incorporated April 2024 out of the ETH Soft Robotics Lab, with Robert Katzschmann as scientific advisor and four founders drawn from the original research project — no evidence any of them has shipped hardware at scale before. Execution is credible and moving: pre-seed May 2024, a $16M seed in November 2025, the M1 hand and U1 exoskeleton launched, a peer-reviewable mimic-one paper, and the FLUX-mimic model with Black Forest Labs — essentially one shipped product generation plus a model release, not 2+ generations with shortening cycles. The About page claim of 50+ people with DeepMind and Tesla Optimus leadership would push toward 4, but it is company-stated, undated, and contradicted by press reports of 25 people at the seed, so it cannot carry the higher score.
Sources: [1](https://www.venturekick.ch/mimic-robotics), [2](https://www.forbes.com/sites/davidprosser/2024/05/07/meet-the-swiss-start-up-taking-on-the-tech-giants-in-robotics-and-ai/), [3](https://ai.ethz.ch/news-and-events/ai-center-news/2025/09/mimic_Robotics_Seed_Round_2025.html), [4](https://www.eu-startups.com/2025/11/swiss-startup-mimic-lands-e13-8-million-to-deliver-robots-that-can-finally-do-what-people-do/), [5](https://roboticsandautomationnews.com/2025/11/05/mimic-robotics-raises-16-million-to-deploy-frontier-physical-ai-across-industries/96263/), [6](https://www.mimicrobotics.com/about), [7](https://www.techbriefs.com/component/content/article/55534-mimic-robotics-launches-m1-hand-and-u1-exoskeleton-to-bring-human-level-dexterity-to-factory-robots), [8](https://arxiv.org/html/2506.11916v1)

*Technology.* Real engineering depth: a tendon-driven M1 hand with 15 actuated DoF across 21 joints, forearm-mounted motors, and >25 kg cylindrical power grasp is not an off-the-shelf part, so this is above a 1. But the architecture is deliberately non-proprietary where it matters commercially — both the CTO and CPO say mimic buys widely-sold robot arms rather than building them — and the learning approach (diffusion policy for dexterous hand control) was published openly on arXiv, i.e. broadly available. The U1 passive exoskeleton for recording human hand demonstrations is the one element that could compound into a data flywheel, and FLUX-mimic is built with an external partner (Black Forest Labs) rather than on unbuyable internal assets; there is no evidence of proprietary data scale, an unbuyable component, or certification moat that a 5 requires.
Sources: [1](https://roboticsandautomationnews.com/2026/07/18/mimic-robotics-unveils-full-stack-platform-for-dexterous-robot-manipulation/103473/), [2](https://sifted.eu/articles/mimic-ai-robotic-arm), [3](https://www.eu-startups.com/2025/11/swiss-startup-mimic-lands-e13-8-million-to-deliver-robots-that-can-finally-do-what-people-do/), [4](https://www.techbriefs.com/component/content/article/55534-mimic-robotics-launches-m1-hand-and-u1-exoskeleton-to-bring-human-level-dexterity-to-factory-robots), [5](https://arxiv.org/html/2506.11916v1)

*Market.* The target segments — automotive, manufacturing, logistics, retail — are large and already buy automation, and the German shortage of 5 million manufacturing workers by 2030 gives a real pain signal, which keeps this well above a 1 with no budget line. But the evidence also shows an unusually crowded field on both flanks: Sacra names Covariant (already earning subscription revenue), Skild AI ($300M) and FieldAI ($405M) as direct foundation-model manipulation comparables, Tracxn adds Agile Robots, Flexiv and Teradyne in dexterous industrial hardware, and Forbes situates mimic against Figure, Sanctuary and 1X. There is no evidence of a buyer today purchasing dexterous-hand stations at a specific budgeted line item — the only market sizing is a company-cited analyst projection to 2035 — so it does not reach the 5 anchor of urgent, already-budgeted spend.
Sources: [1](https://sifted.eu/articles/eth-robotics-spinout-mimic-raises-16m-seed), [2](https://sacra.com/c/mimic-robotics/), [3](https://tracxn.com/d/companies/mimicrobotics/__Olg6fxMKBM7JOp_XzNVPUiqMvh4Uri0_g-K3Yg8hkW4), [4](https://www.forbes.com/sites/davidprosser/2024/05/07/meet-the-swiss-start-up-taking-on-the-tech-giants-in-robotics-and-ai/), [5](https://www.globenewswire.com/news-release/2025/11/03/3179052/0/en/mimic-robotics-raises-16-million-to-deploy-frontier-physical-AI-across-industries.html), [6](https://www.mimicrobotics.com/about)

*Timing.* The timing case rests entirely on generic wave arguments: a projected 2030 German labor shortage (a slow demographic trend, not a dateable unlock), and mimic's own website framing that better models, data and cheap hardware are converging into a European robotics "gold rush" — a quote whose source and date the research could not even confirm. No regulation, no crossed component price threshold, no customer mandate is documented. The AWS Generative AI Accelerator selection and Innosuisse grant are company milestones, not external market unlocks, so nothing here lifts it above the default; equally, the labor-shortage pressure is real enough that it is not a 1 with no external change at all.
Sources: [1](https://sifted.eu/articles/eth-robotics-spinout-mimic-raises-16m-seed), [2](https://www.mimicrobotics.com/about), [3](https://roboticsandautomationnews.com/2025/11/05/mimic-robotics-raises-16-million-to-deploy-frontier-physical-ai-across-industries/96263/)

**Contradictions in the sources, left unresolved**

- Press coverage of the November 2025 seed round consistently reports a 25-person team, while mimic's own About page (undated, referencing later product launches) claims a larger team of 50+ people; the two figures cannot be reconciled to a specific date from the sources found.
- The Tracxn company profile states mimic robotics was a seed company based in West Palm Beach (United States), founded in 2009, which contradicts every other source placing the company in Zurich and founded in 2024; this is treated as a data error rather than usable evidence.

## 4. What this rests on

| Company | Sources retrieved | Evidence items kept | Searches | Budget spent? |
|---------|-------------------|---------------------|----------|---------------|
| ANYbotics | 135 | 52 | 20/20 | yes |
| Verity | 133 | 47 | 20/20 | yes |
| Gravis Robotics | 81 | 52 | 20/20 | yes |
| Humanoid | 148 | 36 | 19/20 | no |
| mimic robotics | 125 | 38 | 20/20 | yes |

Every evidence item behind these scores carries a URL that was checked against the
pages the research actually retrieved; a claim citing anything else was discarded
before scoring. A `yes` in the last column means the research spent its whole search
budget, so a gap in that company's evidence may be a limit of the search rather than
an absence in the world.

The limitations of this method are stated in
[`00-scoping.md` §6](00-scoping.md#6-known-limitations). They are worth reading before
the ranking is used for anything.

## 5. Provenance

- Collection and extraction: `claude-sonnet-5`
- Scoring: `claude-opus-5`
- Report assembly: no model. Every figure above is computed from the stored
  records, and every justification is quoted verbatim from the scoring step.
- Total API cost of the run behind this report: **$9.59**

Regenerate with `.venv\Scripts\python.exe src\report.py`.
