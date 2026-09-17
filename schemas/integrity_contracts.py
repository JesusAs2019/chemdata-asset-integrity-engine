from datetime import datetime
from pydantic import BaseModel, Field, model_validator


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
