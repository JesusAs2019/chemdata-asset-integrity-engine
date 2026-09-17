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
