import importlib.util

from pyroll.core import RollPass, ThreeRollPass, Hook, root_hooks, Unit

VERSION = "2.0.0"
PILLAR_MODEL_INSTALLED = bool(importlib.util.find_spec("pyroll.pillar_model"))

RollPass.wusatowski_temperature_coefficient = Hook[float]()
"""Temperature correction factor a for Wusatowski's spread equation."""

RollPass.wusatowski_velocity_coefficient = Hook[float]()
"""Velocity correction factor c for Wusatowski's spread equation."""

RollPass.wusatowski_material_coefficient = Hook[float]()
"""Material correction factor d for Wusatowski's spread equation."""

RollPass.wusatowski_friction_coefficient = Hook[float]()
"""Friction correction factor f for Wusatowski's spread equation."""

RollPass.wusatowski_exponent = Hook[float]()
"""Exponent w for Wusatowski's spread equation."""


@RollPass.wusatowski_temperature_coefficient
def wusatowski_temperature_coefficient(self: RollPass):
    return 1


@RollPass.wusatowski_velocity_coefficient
def wusatowski_velocity_coefficient(self: RollPass):
    return (-0.002958 + 0.00341 * self.draught) * self.velocity + 1.07168 - 0.10431 * self.draught


@RollPass.wusatowski_material_coefficient
def wusatowski_material_coefficient(self: RollPass):
    return 1


@RollPass.wusatowski_friction_coefficient
def wusatowski_friction_coefficient(self: RollPass):
    return 1


@RollPass.wusatowski_exponent
def wusatowski_exponent_low_strain(self: RollPass):
    if self.draught >= 0.5:
        in_equivalent_height = self.in_profile.equivalent_height
        in_equivalent_width = self.in_profile.equivalent_width

        return 10 ** (
                -1.269 * (in_equivalent_height / (2 * self.roll.working_radius)) ** 0.556
                * in_equivalent_width / in_equivalent_height
        )


@RollPass.wusatowski_exponent
def wusatowski_exponent_high_strain(self: RollPass):
    if self.draught < 0.5:
        in_equivalent_height = self.in_profile.equivalent_height
        in_equivalent_width = self.in_profile.equivalent_width

        return 10 ** (
                -3.457 * (in_equivalent_height / (2 * self.roll.working_radius)) ** 0.968
                * in_equivalent_width / in_equivalent_height
        )


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not (PILLAR_MODEL_INSTALLED and rp.disk_elements):
        if not self.has_set_or_cached("width"):
            return None

        return (
                rp.wusatowski_temperature_coefficient
                * rp.wusatowski_velocity_coefficient
                * rp.wusatowski_material_coefficient
                * rp.wusatowski_friction_coefficient
                * rp.draught ** (-rp.wusatowski_exponent)
        ) * rp.in_profile.width


@ThreeRollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    rp = self.roll_pass

    if not (PILLAR_MODEL_INSTALLED and rp.disk_elements):
        if not self.has_set_or_cached("width"):
            return None

        return (
                rp.wusatowski_temperature_coefficient
                * rp.wusatowski_velocity_coefficient
                * rp.wusatowski_material_coefficient
                * rp.wusatowski_friction_coefficient
                * rp.draught ** (-rp.wusatowski_exponent)
        ) * rp.in_profile.width


if PILLAR_MODEL_INSTALLED:
    import pyroll.pillar_model


    # noinspection PyUnresolvedReferences
    @RollPass.DiskElement.pillar_spreads
    def pillar_spreads(self: RollPass.DiskElement):
        rp = self.roll_pass
        return (
                rp.wusatowski_temperature_coefficient
                # * rp.wusatowski_velocity_coefficient
                * rp.wusatowski_material_coefficient
                * rp.wusatowski_friction_coefficient
                * self.pillar_draughts ** (-rp.wusatowski_exponent)
        )
