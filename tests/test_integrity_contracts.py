import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.integrity_contracts import WallThicknessTelemetry
from run_integrity_pipeline import (
    calculate_de_waard_corrosion_rate,
    compute_remaining_useful_life,
)


def test_valid_telemetry_payload():
    payload = {
        "asset_tag": "PL-FL-1042A",
        "inspection_timestamp": datetime.now(),
        "nominal_thickness_mm": 12.50,
        "measured_thickness_mm": 11.20,
        "t_min_allowable_mm": 8.00,
        "corrosion_inhibitor_dosing_l_per_day": 40.0,
    }
    model = WallThicknessTelemetry(**payload)
    assert model.measured_thickness_mm == 11.20
    assert model.asset_tag == "PL-FL-1042A"


def test_physical_anomaly_rejection():
    invalid_payload = {
        "asset_tag": "PL-FL-1042A",
        "inspection_timestamp": datetime.now(),
        "nominal_thickness_mm": 12.50,
        "measured_thickness_mm": 15.00,
        "t_min_allowable_mm": 8.00,
        "corrosion_inhibitor_dosing_l_per_day": 40.0,
    }
    with pytest.raises(ValidationError):
        WallThicknessTelemetry(**invalid_payload)


def test_t_min_exceeds_nominal_rejection():
    invalid_payload = {
        "asset_tag": "PL-FL-1042A",
        "inspection_timestamp": datetime.now(),
        "nominal_thickness_mm": 10.00,
        "measured_thickness_mm": 9.50,
        "t_min_allowable_mm": 10.50,
        "corrosion_inhibitor_dosing_l_per_day": 30.0,
    }
    with pytest.raises(ValidationError):
        WallThicknessTelemetry(**invalid_payload)


def test_deterministic_de_waard_calculation():
    rate = calculate_de_waard_corrosion_rate(temp_c=55.0, co2_partial_press_bar=2.5, ph=5.8)
    assert 1.80 <= rate <= 1.90
    metrics = compute_remaining_useful_life(
        current_thickness_mm=11.2,
        t_min_allowable_mm=8.2,
        active_corrosion_rate_mm_yr=rate,
        inhibitor_efficiency=0.92,
    )
    assert metrics["rul_years"] > 15.0
    assert metrics["effective_loss_mm_yr"] > 0.0
