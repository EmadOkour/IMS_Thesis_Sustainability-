# EU Taxonomy Agent — 2021/2139 Monitor & Query Tool

Built alongside the IMS Masters thesis on translating EU Taxonomy / CSRD obligations into operational practice.

## What it does

1. **Monitors** EUR-Lex for amendments to Commission Delegated Regulation (EU) 2021/2139
2. **Stores** SE-relevant taxonomy activity knowledge base (activities 3.1, 3.20, 4.9, 4.29)
3. **Reports** SE FY2025 taxonomy gap (73.6% eligible → 41.1% aligned, 32.5pp gap)
4. **Flags** high-priority regulatory changes (SF6 ban, gas turbine transitional status review)

## Install

```bash
pip install -r requirements.txt --break-system-packages
```

## Usage

```bash
# Check for EUR-Lex updates + print report
python monitor.py

# Offline mode — knowledge base only, no network call
python monitor.py --offline

# Full verbose report with all activity detail
python monitor.py --verbose

# Query a specific activity
python monitor.py --activity 4.29
python monitor.py --activity 3.20
python monitor.py --activity 4.9
python monitor.py --activity 3.1

# Save report to reports/ directory
python monitor.py --save
```

## SE-Relevant Activities Tracked

| Activity | Name | SE BA | Aligned? | Gap Type |
|----------|------|-------|----------|----------|
| 3.1 | Manufacture of renewable energy technologies | Siemens Gamesa | ✅ Yes | G2: rare earth DNSH |
| 3.20 | Manufacture of HV/MV electrical equipment | GT / GS | ❌ No | G3: regulation-dependent |
| 4.9 | Transmission and distribution of electricity | Grid Technologies | ❌ No | G5: process-fixable |
| 4.29 | Manufacture of gas-fired power generation equipment | Gas Services | ❌ No | G4: transformation-required |

## Amendment History

| Date | Regulation | Key change |
|------|-----------|------------|
| 2022-07-09 | 2022/1214 | Added gas + nuclear transitional activities (incl. Activity 4.29) |
| 2023-11-27 | 2023/2485 | Additional mitigation activities; TSC reviews |

## Monitoring Priorities

**Activity 4.29** — EU Commission reviewing gas turbine transitional status post-2030. Critical for SE's largest revenue gap.

**Activity 3.20** — SF6 phase-out regulation (F-gas Regulation revision) directly affects switchgear taxonomy alignment criteria.

## Files

- `knowledge_base.py` — SE-relevant activities, TSC thresholds, gap notes, amendment history
- `monitor.py` — EUR-Lex monitoring, activity query CLI, report generation
- `reports/` — saved monitoring reports (auto-created)
