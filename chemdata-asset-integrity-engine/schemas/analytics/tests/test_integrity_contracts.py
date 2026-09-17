import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas.integrity_contracts import WallThicknessTelemetry
from analytics.corrosion_kinetics import (
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


def test_physical_anomaly_rejection():
    # Measured thickness greater than design nominal + tolerance
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


def test_deterministic_de_waard_math():
    rate = calculate_de_waard_corrosion_rate(temp_c=55.0, co2_partial_press_bar=2.5, ph=5.8)
    assert rate > 0.0
    rul = compute_remaining_useful_life(11.2, 8.0, rate, inhibitor_efficiency=0.90)
    assert rul["rul_years"] > 0.0
    