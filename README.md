# ChemData Asset Integrity Engine

An industrial-grade, type-safe asset integrity evaluation engine for upstream and midstream pipeline infrastructure. Built with **Python 3.12**, **Pydantic v2**, and deterministic electrochemical degradation modeling (**calibrated de Waard-Lotz kinetics**).

---

## Architectural Highlights

* **Strict Type Safety & Contract Boundaries**: Pydantic v2 schemas enforce physical boundaries on wall thickness, corrosion inhibitor dosing, and allowable minimum structural tolerances (`t_min`).
* **Self-Healing Ingestion Gateway**: Catches physical anomalies (e.g., ultrasonic wall-thickness readings exceeding nominal pipe design) and routes structured feedback for payload remediation.
* **Electrochemical Degradation Engine**: Deterministic implementation of calibrated de Waard-Lotz (1993) CO2 corrosion kinetics factoring in:
  * System temperature (`T_K`)
  * CO2 partial pressure (`P_CO2`)
  * In-situ brine pH passivation factors (`F_pH`)
  * High-temperature protective scale formation
* **Dynamic Prognostics**: Calculates Net Effective Loss Rate and Remaining Useful Life (RUL) under active chemical inhibitor dosing regimes.

## Project Structure

```text
chemdata-asset-integrity-engine/
|-- analytics/
|   |-- __init__.py
|   |-- corrosion_kinetics.py       # Electrochemical kinetics & RUL models
|-- schemas/
|   |-- __init__.py
|   |-- integrity_contracts.py     # Pydantic v2 data models & validators
|-- tests/
|   |-- __init__.py
|   |-- test_integrity_contracts.py # Automated test suite
|-- .gitignore                      # Environment and cache rules
|-- pytest.ini                      # Test runner configuration
|-- requirements.txt                # Pinned production dependencies
|-- run_integrity_pipeline.py       # End-to-end self-healing demonstration
`-- README.md
```

## Technical Specifications & Kinetics

The deterministic baseline degradation rate `V_corr` (mm/year) is modeled via the calibrated de Waard-Lotz (1993) relationship:

log10(V_corr) = 5.71 - (1119 / T_K) + 0.67 * log10(P_CO2) - F_pH

Where:
* **T_K**: Pipe operating temperature in Kelvin (`T_C + 273.15`).
* **P_CO2**: CO2 partial pressure in bar (`P_system * y_CO2`).
* **F_pH**: Scale-passivation correction factor applied when in-situ brine pH > 5.0.

### Prognostics & Remaining Useful Life (RUL) Formulation

Accounting for active chemical corrosion inhibitor dosing efficiency (`eta_inhib`), the net effective metal loss rate and remaining structural life are determined by:

V_eff = V_corr * (1 - eta_inhib)

RUL (years) = (t_measured - t_min) / V_eff

Where:
* **t_measured**: Current ultrasonic wall-thickness measurement (mm).
* **t_min**: Minimum structural allowable limit under API 570 hoop-stress design thresholds (mm).
* **V_eff**: Net effective degradation rate (mm/year).
* **eta_inhib**: Active inhibitor efficiency (e.g., `0.92` for 92% dosing efficiency).

---

## Quickstart

### 1. Environment Initialization

Clone and activate a local virtual environment:

```bash
git clone [https://github.com/JesusAs2019/chemdata-asset-integrity-engine.git](https://github.com/JesusAs2019/chemdata-asset-integrity-engine.git)
cd chemdata-asset-integrity-engine
python -m venv .venv

Activate the environment:

Windows (PowerShell):

.\.venv\Scripts\Activate.ps1

Linux / macOS:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

2. Run the Integrity Pipeline
Execute the self-healing demonstration:

python run_integrity_pipeline.py

3. Pipeline Execution Output

===================================================
  CHEMDATA ASSET INTEGRITY ENGINE | PIPELINE INGESTION & DEGRADATION SUITE
===================================================

[STEP 1] Ingesting Raw Inspection Telemetry (Payload 1)...
 -> Status: CONTRACT CONTRAVENTION DETECTED [REJECTED]
 -> Validation Feedback: "Physical anomaly: Measured wall thickness (14.8mm) exceeds nominal design (12.5mm) beyond tolerance."

[STEP 2] Corrective Feedback Loop -> Reprocessing Rectified Sensor Payload...

 -> Status: CONTRACT VERIFIED [ACCEPTED]

[STEP 3] Running Deterministic Degradation Engine...
---------------------------------------------------

Asset Segment Tag:          PL-FL-1042A
Nominal Wall Thickness:     12.50 mm
Current Verified Wall:      11.20 mm
Minimum Structural Limit:   8.20 mm
Baseline Corrosion Rate:    1.844 mm/year
Net Effective Loss Rate:    0.1475 mm/year (@ 92% Dosing Eff.)
Remaining Useful Life (RUL):20.34 Years
===================================================

4. Automated Test Suite
Run the full PyTest suite to verify edge boundaries and numerical stability:

pytest -v

## Standards Alignment Matrix

===================================================
Parameter/Layer:	Governing Standard	        :Implementation Module
Parameter/Layer:	API 570/ASME B31G	schemas   : integrity_contracts.py
Parameter/Layer:	de Waard-Lotz/NORSOK M-506  :  analytics:  corrosion_kinetics.py
Parameter/Layer:	Automated verification      :tests/test_integrity_contracts.py
===================================================

## License

License Distributed under the MIT License.
Developed and maintained by ChemData AI Solutions.
