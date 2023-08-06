import numpy as np
from pyroll.core import RollPass, Hook

VERSION = "2.0.0"

RollPass.roll_gap_ratio = Hook[float]()
"""Calculate cross-section ratio used in Hensel-Poluchin master curves."""

RollPass.rolling_efficiency = Hook[float]()
"""Calculate rolling efficiency according to Hensel-Poluchin master curve."""

RollPass.deformation_resistance = Hook[float]()
"""Calculate deformation resistance according to Hensel-Poluchin master curve."""

RollPass.lever_arm_coefficient = Hook[float]()
"""Calculate lever coefficient according to Hensel-Poluchin master curve."""


@RollPass.roll_gap_ratio
def roll_gap_ratio(self: RollPass):
    mean_cross_section = (self.in_profile.cross_section.area + 2 * self.out_profile.cross_section.area) / 3
    return self.roll.contact_area / mean_cross_section


@RollPass.rolling_efficiency
def rolling_efficiency(self: RollPass):
    inverse_efficiency = (0.9901 + 0.106 * self.roll_gap_ratio + 0.0283 * self.roll_gap_ratio ** 2
                          + 1.5718 * np.exp(-2.4609 * self.roll_gap_ratio)
                          + 0.3117 * np.exp(-15.625 * self.roll_gap_ratio ** 2))
    return inverse_efficiency ** -1


@RollPass.deformation_resistance
def deformation_resistance(self: RollPass):
    mean_flow_stress = (self.in_profile.flow_stress + 2 * self.out_profile.flow_stress) / 3
    return mean_flow_stress / self.rolling_efficiency


@RollPass.lever_arm_coefficient
def lever_arm_coefficient(self: RollPass):
    mean_temperature = (self.in_profile.temperature + self.out_profile.temperature) / 2
    return ((np.exp(-0.6 * self.roll_gap_ratio) + 0.076 * self.roll_gap_ratio)
            * self.velocity ** 0.005 * np.exp(
                -0.0003 * (mean_temperature - 273.15 - 900)))


@RollPass.roll_force
def roll_force(self: RollPass):
    return self.deformation_resistance * self.roll.contact_area


@RollPass.Roll.roll_torque
def roll_torque(self: RollPass.Roll):
    return self.roll_pass.roll_force * self.contact_length * self.roll_pass.lever_arm_coefficient
