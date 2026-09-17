from datetime import datetime
from pydantic import ValidationError
from schemas.integrity_contracts import WallThicknessTelemetry
from analytics.corrosion_kinetics import (
    calculate_de_waard_corrosion_rate,
    compute_remaining_useful_life,
)


def run_pipeline():
    print("=" * 75)
    print("  CHEMDATA & AI CONSULTING | ASSET INTEGRITY PIPELINE TEST SUITE")
    print("=" * 75)

    # Ingestion Payload with intentional data error (measured > nominal)
    raw_payload_iteration_1 = {
        "asset_tag": "PL-FL-1042A",
        "inspection_timestamp": "2026-09-16T10:00:00",
        "nominal_thickness_mm": 12.50,
        "measured_thickness_mm": 14.80,  # <-- Ingestion error
        "t_min_allowable_mm": 8.20,
        "corrosion_inhibitor_dosing_l_per_day": 45.0
    }

    print("\n[STEP 1] Ingesting Raw Inspection Payload (Iteration 1)...")
    try:
        telemetry = WallThicknessTelemetry(**raw_payload_iteration_1)
    except ValidationError as e:
        print(" -> Gateway Status: CONTRACT CONTRAVENTION DETECTED ✗")
        error_msg = e.errors()[0]["msg"]
        print(f" -> Feedback to Agent: \"{error_msg}\"")

        print("\n[STEP 2] Routing Feedback to Self-Healing Parser (Iteration 2)...")
        corrected_payload = raw_payload_iteration_1.copy()
        corrected_payload["measured_thickness_mm"] = 11.20  # Corrected reading
        telemetry = WallThicknessTelemetry(**corrected_payload)
        print(" -> Gateway Status: VERIFICATION PASSED ✓")

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
    