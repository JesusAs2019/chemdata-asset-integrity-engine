# ChemData Asset Integrity Engine

An industrial-grade, type-safe asset integrity evaluation engine for upstream and midstream pipeline infrastructure. Built with **Python 3.12**, **Pydantic v2**, and deterministic electrochemical degradation modeling (**calibrated de Waard-Lotz kinetics**).

---

## Architectural Highlights

- **Strict Type Safety & Contract Boundaries**: Pydantic v2 schemas enforce physical boundaries on wall thickness, corrosion inhibitor dosing, and allowable minimum structural tolerances (t_min).
- **Self-Healing Ingestion Gateway**: Catches physical anomalies (e.g., ultrasonic wall-thickness readings exceeding nominal pipe design) and routes structured feedback for payload remediation.
- **Electrochemical Degradation Engine**: Deterministic implementation of calibrated de Waard-Lotz (1993) CO2 corrosion kinetics factoring in:
  - System temperature (T_K)
  - CO2 partial pressure (P_CO2)
  - In-situ brine pH passivation factors (F_pH)
  - High-temperature protective scale formation
- **Dynamic Prognostics**: Calculates Net Effective Loss Rate and Remaining Useful Life (RUL) under active chemical inhibitor dosing regimes.

---

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

Technical Specifications & KineticsThe deterministic baseline degradation rate $V_{corr}$ (mm/year) is modeled via de Waard-Lotz:$$\log_{10}(V_{corr}) = 5.71 - \frac{1119}{T_K} + 0.67 \log_{10}(P_{CO_2}) - F_{pH}$$Where:$T_K$: Pipe operating temperature in Kelvin.$P_{CO_2}$: Partial pressure of $CO_2$ in bar ($P_{system} \times y_{CO_2}$).$F_{pH}$: Empirical pH passivation correction factor when brine $pH > 5.0$.Prognostics FormulationGiven an inhibitor availability/efficiency factor $\eta_{inhib}$, the effective degradation rate and remaining structural life are determined by:$$V_{eff} = V_{corr} \times (1 - \eta_{inhib})$$$$RUL = \frac{t_{measured} - t_{min}}{V_{eff}}$$Quickstart1. Environment InitializationClone and activate a local virtual environment:Bashgit clone [https://github.com/JesusAs2019/chemdata-asset-integrity-engine.git](https://github.com/JesusAs2019/chemdata-asset-integrity-engine.git)
cd chemdata-asset-integrity-engine
python -m venv .venv
Activate the environment:Windows (PowerShell): .\.venv\Scripts\Activate.ps1Linux / macOS: source .venv/bin/activateInstall dependencies:Bashpip install -r requirements.txt
2. Run the Integrity PipelineExecute the self-healing demonstration:Bashpython run_integrity_pipeline.py
Pipeline Execution

 Output:Plaintext
                                                                                  ===========================================================================
  CHEMDATA ASSET INTEGRITY ENGINE | PIPELINE INGESTION & DEGRADATION SUITE
===========================================================================

[STEP 1] Ingesting Raw Inspection Telemetry (Payload 1)...
 -> Status: CONTRACT CONTRAVENTION DETECTED [REJECTED]
 -> Validation Feedback: "Physical anomaly: Measured wall thickness (14.8mm) exceeds nominal design (12.5mm) beyond tolerance."

[STEP 2] Corrective Feedback Loop -> Reprocessing Rectified Sensor Payload...
 -> Status: CONTRACT VERIFIED [ACCEPTED]

[STEP 3] Running Deterministic Degradation Engine...
---------------------------------------------------------------------------
Asset Segment Tag:          PL-FL-1042A
Nominal Wall Thickness:     12.50 mm
Current Verified Wall:      11.20 mm
Minimum Structural Limit:   8.20 mm
Baseline Corrosion Rate:    1.844 mm/year
Net Effective Loss Rate:    0.1475 mm/year (@ 92% Dosing Eff.)
Remaining Useful Life (RUL):20.34 Years
===========================================================================
3. Automated Test Suite
Run the full PyTest suite to verify edge boundaries and numerical stability:Bashpytest -v
All 4 boundary and mathematical verification tests will pass.Standards Alignment MatrixParameter / LayerGoverning StandardImplementation ModuleIngestion & Thickness ThresholdsAPI 570 / ASME B31Gschemas/integrity_contracts.pyInternal CO2 Kineticsde Waard-Lotz / NORSOK M-506analytics/corrosion_kinetics.pyUnit & Integration TestingAutomated verificationtests/test_integrity_contracts.py

License Distributed under the MIT License.
Developed and maintained by ChemData AI Solutions.
