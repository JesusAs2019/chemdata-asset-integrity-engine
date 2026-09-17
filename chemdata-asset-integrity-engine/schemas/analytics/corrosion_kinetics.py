from typing import Dict
import numpy as np


def calculate_de_waard_corrosion_rate(
    temp_c: float, 
    co2_partial_press_bar: float, 
    ph: float
) -> float:
    """
    Computes bare-metal CO2 corrosion rate (mm/year) using de Waard-Lotz (1993) kinetics
    with temperature scaling and pH passivation corrections.
    """
    temp_k = temp_c + 273.15
    # Calibrated de Waard-Lotz equation
    log_v_corr = 4.93 - (1119.0 / temp_k) + (0.58 * np.log10(co2_partial_press_bar))
    v_bare = 10 ** log_v_corr

    # pH passivation factor (F_pH)
    f_ph = max(0.1, 1.0 - (0.32 * (ph - 5.0))) if ph > 5.0 else 1.0

    # High-temperature scale protective factor (>65°C)
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
