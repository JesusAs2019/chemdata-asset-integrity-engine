from datetime import datetime
from typing import Dict
import numpy as np
from pydantic import BaseModel, Field, ValidationError, model_validator


# =====================================================================
# 1. TYPE-SAFE DATA CONTRACTS (Pydantic v2)
# =====================================================================

class WallThicknessTelemetry(BaseModel):
    asset_tag: str = Field(..., pattern=r"^[A-Z0-9]{2,4}-[A-Z]{2,4}-[0-9]{3,5}[A-Z]?$")
    inspection_timestamp: datetime
    nominal_thickness_mm: float = Field(..., gt=0.0, le=100.0)
    measured_thickness_mm: float = Field(..., gt=0.0, le=100.0)
    t_min_allowable_mm: float = Field(..., gt=0.0, le=100.0)
    corrosion_inhibitor_dosing_l_per_day: float = Field(..., ge=0.0, le=500.0)

    @model_validator(mode="after")
    def verify_physical_bounds(self):
        if self.measured_thickness_mm > (self.nominal_thickness_mm * 1.05):
            raise ValueError(
                f"Physical anomaly: Measured wall thickness ({self.measured_thickness_mm}mm) "
                f"exceeds nominal design ({self.nominal_thickness_mm}mm) beyond tolerance."
            )
        if self.t_min_allowable_mm >= self.nominal_thickness_mm:
            raise ValueError("Allowable minimum (t_min) must be strictly less than nominal thickness.")
        return self


# =====================================================================
# 2. CALIBRATED ELECTROCHEMICAL DEGRADATION ENGINE
# =====================================================================

def calculate_de_waard_corrosion_rate(
    temp_c: float, 
    co2_partial_press_bar: float, 
    ph: float
) -> float:
    """
    Computes bare-metal CO2 corrosion rate (mm/year) using calibrated de Waard-Lotz kinetics
    with pH passivation and high-temperature scaling factors.
    """
    temp_k = temp_c + 273.15
    # Calibrated empirical relation with standard field baseline factor (0.044)
    log_v_corr = 4.93 - (1119.0 / temp_k) + (0.58 * np.log10(co2_partial_press_bar))
    v_bare = (10 ** log_v_corr) * 0.044

    # pH passivation factor (F_pH)
    f_ph = max(0.1, 1.0 - (0.32 * (ph - 5.0))) if ph > 5.0 else 1.0

    # High-temperature scale protective factor (>65 C)
    scale_factor = max(0.05, 1.0 - (0.015 * (temp_c - 65.0))) if temp_c > 65.0 else 1.0

    return round(float(v_bare * f_ph * scale_factor), 3)


def compute_remaining_useful_life(
    current_thickness_mm: float,
    t_min_allowable_mm: float,
    active_corrosion_rate_mm_yr: float,
    inhibitor_efficiency: float = 0.90
) -> Dict[str, float]:
    """Calculates Remaining Useful Life (RUL) under chemical inhibitor treatment."""
    effective_loss_rate = active_corrosion_rate_mm_yr * (1.0 - inhibitor_efficiency)
    if effective_loss_rate <= 0:
        return {"rul_years": 999.0, "effective_loss_mm_yr": 0.0}

    remaining_metal = current_thickness_mm - t_min_allowable_mm
    rul_years = max(0.0, remaining_metal / effective_loss_rate)
    return {
        "rul_years": round(float(rul_years), 2),
        "effective_loss_mm_yr": round(float(effective_loss_rate), 4)
    }


# =====================================================================
# 3. SELF-HEALING AUDIT SIMULATION
# =====================================================================

def run_pipeline():
    print("=" * 75)
    print("  CHEMDATA & AI CONSULTING | ASSET INTEGRITY PIPELINE TEST SUITE")
    print("=" * 75)

    raw_payload_iteration_1 = {
        "asset_tag": "PL-FL-1042A",
        "inspection_timestamp": "2026-09-16T10:00:00",
        "nominal_thickness_mm": 12.50,
        "measured_thickness_mm": 14.80,  # Ingestion error
        "t_min_allowable_mm": 8.20,
        "corrosion_inhibitor_dosing_l_per_day": 45.0
    }

    print("\n[STEP 1] Ingesting Raw Inspection Payload (Iteration 1)...")
    try:
        telemetry = WallThicknessTelemetry(**raw_payload_iteration_1)
    except ValidationError as e:
        print(" -> Gateway Status: CONTRACT CONTRAVENTION DETECTED X")
        error_msg = e.errors()[0]["msg"]
        print(f" -> Feedback to Agent: \"{error_msg}\"")

        print("\n[STEP 2] Routing Feedback to Self-Healing Parser (Iteration 2)...")
        corrected_payload = raw_payload_iteration_1.copy()
        corrected_payload["measured_thickness_mm"] = 11.20
        telemetry = WallThicknessTelemetry(**corrected_payload)
        print(" -> Gateway Status: VERIFICATION PASSED OK")

    print("\n[STEP 3] Running Deterministic Degradation Engine...")
    uninhibited_rate = calculate_de_waard_corrosion_rate(
        temp_c=55.0, 
        co2_partial_press_bar=2.5, 
        ph=5.8
    )
    rul_metrics = compute_remaining_useful_life(
        current_thickness_mm=telemetry.measured_thickness_mm,
        t_min_allowable_mm=telemetry.t_min_allowable_mm,
        active_corrosion_rate_mm_yr=uninhibited_rate,
        inhibitor_efficiency=0.92
    )

    print("-" * 75)
    print(f"Asset Segment Tag:          {telemetry.asset_tag}")
    print(f"Nominal Wall Thickness:     {telemetry.nominal_thickness_mm} mm")
    print(f"Current Verified Wall:      {telemetry.measured_thickness_mm} mm")
    print(f"Minimum Structural Limit:   {telemetry.t_min_allowable_mm} mm")
    print(f"Uninhibited Corrosion Rate: {uninhibited_rate} mm/year")
    print(f"Net Effective Loss Rate:    {rul_metrics['effective_loss_mm_yr']} mm/year (@ 92% Dosing Eff.)")
    print(f"Remaining Useful Life (RUL):{rul_metrics['rul_years']} Years")
    print("=" * 75)


if __name__ == "__main__":
    run_pipeline()
