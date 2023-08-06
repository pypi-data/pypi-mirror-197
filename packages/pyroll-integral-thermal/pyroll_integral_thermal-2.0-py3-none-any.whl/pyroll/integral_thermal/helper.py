from pyroll.core import Unit


def mean_temperature(unit: Unit):
    return (unit.in_profile.temperature + unit.out_profile.temperature) / 2


def mean_density(unit: Unit):
    return (unit.in_profile.density + unit.out_profile.density) / 2


def mean_thermal_capacity(unit: Unit):
    return (unit.in_profile.thermal_capacity + unit.out_profile.thermal_capacity) / 2
