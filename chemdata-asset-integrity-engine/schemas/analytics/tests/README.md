# IntegrityData AI: Deterministic Pipeline Degradation & Chemical Dosing Optimizer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Pydantic v2](https://img.shields.io/badge/data_contracts-Pydantic_v2-e92063.svg)](https://docs.pydantic.dev/)
[![Compliance](https://img.shields.io/badge/standards-API_570%20%7C%20NACE_MR0175-green.svg)]()

### Engineered by ChemData & AI Consulting Ltd
**Practice:** [chemdataai.com](https://www.chemdataai.com)  
**Lead Architect:** Jean Pierre Assiana (BSc Oil & Gas Management, MSc Applied Chemistry)

---

## Executive Summary

Mid-tier upstream operators manage topside piping and flowline networks using fragmented data: ultrasonic wall-thickness certificates (trapped in PDFs), laboratory water chemistry (Fe/Mn counts), and SCADA chemical injection skids. 

This architectural disconnect leads to:
1. **Chemical Over-Dosing:** Offshore operators routinely over-inject specialty corrosion inhibitors by 25–40% to compensate for blind spots, spending excess OPEX annually.
2. **Catastrophic Failure Risk:** Localized CO₂/H₂S sweet-corrosion under-dosing causing pinhole leaks and unscheduled shutdowns.

**IntegrityData AI** replaces manual, error-prone workflows with a **type-safe, deterministic analytical mesh**:
- Enforces strict thermodynamic and physical validation at the boundary using **Pydantic v2 data contracts**.
- Implements self-healing agentic extraction for unstructured inspection logs.
- Executes non-linear electrochemical degradation kinetics via verified **de Waard-Milliams equations**—eliminating LLM hallucinations from safety-critical engineering calculations.

---

## Architecture Flow

[ Ultrasonic NDT Reports (PDFs) ]       [ SCADA / ER Probes ]       [ Water Chemistry (LIMS) ]
│                                │                              │
└────────────────────────────────┼──────────────────────────────┘
▼
[ Pydantic v2 Type-Safe Gateway ]
├── FAILS: Semantic Feedback Loop to Ingestion Agent
└── PASSES: Write to Normalized PostgreSQL Schema
│
▼
[ Deterministic Electrochemical Engine ]
├── de Waard-Milliams CO₂ Degradation Modeling
└── Dynamic Remaining Useful Life (RUL) Calculation
│
▼
[ Optimized Chemical Dosing Setpoint ]


---

## Quickstart & Verification

```bash
# 1. Clone repository
git clone [https://github.com/JesusAs2019/chemdata-asset-integrity-engine.git](https://github.com/JesusAs2019/chemdata-asset-integrity-engine.git)
cd chemdata-asset-integrity-engine

# 2. Set up virtual environment & dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run automated unit & boundary test suite
pytest tests/ -v

# 4. Run the live pipeline simulation
python run_integrity_pipeline.py

---

### Phase 3: Run and Test Locally

Execute these commands in your editor terminal to confirm everything works before committing:

1. **Run the automated unit tests:**
   ```bash
   pytest tests/ -v
Expected result: 3 passed in < 0.2 seconds.


