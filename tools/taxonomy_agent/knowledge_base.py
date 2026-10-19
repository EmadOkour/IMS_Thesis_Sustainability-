"""
EU Taxonomy Knowledge Base — SE-Relevant Activities
Siemens Energy FY2025 thesis, IMS Masters, Hochschule Zittau/Görlitz

Covers all activities where SE has taxonomy-eligible revenue, CapEx, or OpEx.
Data sources: EU Delegated Regulation 2021/2139 + SE Annual Report FY2025.
"""

# ─── Activity Registry ────────────────────────────────────────────────────────

ACTIVITIES = {
    "3.1": {
        "name": "Manufacture of renewable energy technologies",
        "objective": "Climate change mitigation",
        "business_area": "Siemens Gamesa (Wind)",
        "se_status": {
            "revenue_eligible": True,
            "revenue_aligned": True,   # One of SE's aligned activities
            "note": "Onshore and offshore wind turbine manufacturing"
        },
        "tsc": {
            "description": "Manufacturing of equipment exclusively for renewable energy generation",
            "threshold": "Equipment must serve only renewable energy sources",
            "key_dnsh": {
                "E1_climate_adaptation": "Climate risk assessment required",
                "E3_water": "No significant water impacts",
                "E4_biodiversity": "No significant biodiversity impacts",
                "rare_earths": "Annex I A3.1 DNSH — no specific rare earth traceability requirement in current text",
            }
        },
        "gaps": ["G2"],
        "gap_notes": "Rare earth traceability (neodymium/dysprosium) absent from upstream scope despite DNSH obligations on manufacturers",
        "eurlex_ref": "Annex I, Section 3.1, Commission Delegated Regulation (EU) 2021/2139",
        "amendments": []
    },

    "3.20": {
        "name": "Manufacture, installation and servicing of high and medium-voltage electrical equipment",
        "objective": "Climate change mitigation",
        "business_area": "Gas Services / Grid Technologies",
        "se_status": {
            "revenue_eligible": True,
            "revenue_aligned": False,
            "note": "SE's core switchgear and transformer manufacturing"
        },
        "tsc": {
            "description": "High/medium voltage electrical equipment meeting specific EN standards",
            "threshold": "Must comply with EN 62271-200 (AC metal-enclosed switchgear) and EN 62271-203 (gas-insulated switchgear)",
            "key_dnsh": {
                "SF6": "Leak rate requirements — SF6 is a potent GHG (GWP ~23,900)",
                "F_gases": "F-gas Regulation 517/2014 compliance",
                "EcoDesign": "Ecodesign Regulation requirements",
            }
        },
        "gaps": ["G3"],
        "gap_notes": [
            "Air-insulated switchgear (AIS) is environmentally superior (no SF6) but EN standards not referenced in A3.20 — regulation-dependent gap",
            "SF6-based equipment faces transformation requirement to SF6-free alternatives",
            "EcoDesign documentation gap — process-fixable"
        ],
        "eurlex_ref": "Annex I, Section 3.20, Commission Delegated Regulation (EU) 2021/2139",
        "amendments": [],
        "monitoring_flag": "HIGH — EU Commission reviewing SF6 regulation (F-gas revision). Changes here directly affect this activity's criteria."
    },

    "4.9": {
        "name": "Transmission and distribution of electricity",
        "objective": "Climate change mitigation",
        "business_area": "Grid Technologies",
        "se_status": {
            "revenue_eligible": True,
            "revenue_aligned": False,
            "note": "Grid infrastructure projects, transmission equipment"
        },
        "tsc": {
            "description": "Infrastructure for electricity transmission and distribution",
            "threshold": "Geographic criterion: EU grid or grid achieving equivalent GHG intensity reduction",
            "key_dnsh": {
                "geographic_scope": "Non-EU exports excluded under geographic eligibility criterion",
            }
        },
        "gaps": ["G5"],
        "gap_notes": "Non-EU exports (Middle East, APAC, Americas) excluded under geographic criterion — process-fixable via project boundary documentation",
        "eurlex_ref": "Annex I, Section 4.9, Commission Delegated Regulation (EU) 2021/2139",
        "amendments": []
    },

    "4.29": {
        "name": "Manufacture of gas-fired power generation equipment",
        "objective": "Climate change mitigation (transitional)",
        "business_area": "Gas Services",
        "se_status": {
            "revenue_eligible": True,
            "revenue_aligned": False,
            "note": "Gas turbine manufacturing"
        },
        "tsc": {
            "description": "Gas turbines and combined-cycle gas turbines for power generation",
            "threshold": "Life-cycle GHG emissions below 100 gCO2eq/kWh",
            "key_dnsh": {
                "ghg_threshold": "100 gCO2eq/kWh — unachievable for fossil gas combustion turbines",
                "hydrogen_ready": "Must be capable of running on 100% hydrogen or other low-carbon fuels",
            }
        },
        "gaps": ["G4"],
        "gap_notes": "GHG threshold of 100gCO2eq/kWh is structurally unachievable with fossil gas combustion — transformation-required gap (H2-ready retrofit or fuel switch required)",
        "eurlex_ref": "Annex I, Section 4.29, Commission Delegated Regulation (EU) 2021/2139",
        "amendments": [],
        "monitoring_flag": "CRITICAL — EU Commission reviewing whether to extend transitional status of gas turbines post-2030. Changes directly affect SE's largest revenue gap."
    },
}


# ─── SE Taxonomy Summary (FY2025) ─────────────────────────────────────────────

SE_TAXONOMY_FY2025 = {
    "revenue": {"eligible_pct": 73.6, "aligned_pct": 41.1, "gap_pp": 32.5},
    "capex":   {"eligible_pct": 78.8, "aligned_pct": 54.7, "gap_pp": 24.1},
    "opex":    {"eligible_pct": 83.0, "aligned_pct": 44.3, "gap_pp": 38.7},
    "source":  "SE Annual Report FY2025, s.2.10.2.3, p.86 and p.91",
    "verified": True,
}


# ─── Amendment Tracker ────────────────────────────────────────────────────────

KNOWN_AMENDMENTS = [
    {
        "regulation": "2021/2139",
        "amendment": "Commission Delegated Regulation (EU) 2022/1214",
        "date": "2022-07-09",
        "summary": "Added gas and nuclear transitional activities. Added Activity 4.29 (gas turbines). Key for SE.",
        "activities_affected": ["4.29", "new nuclear activities"],
        "eurlex_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32022R1214"
    },
    {
        "regulation": "2021/2139",
        "amendment": "Commission Delegated Regulation (EU) 2023/2485",
        "date": "2023-11-27",
        "summary": "Additional mitigation activities added. Review of existing TSC thresholds.",
        "activities_affected": ["Various — check full text"],
        "eurlex_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32023R2485"
    },
]

BASE_REGULATION_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32021R2139"
EURLEX_SEARCH_URL = "https://eur-lex.europa.eu/search.html?query=2021%2F2139&qid=&type=quick&lang=en"
