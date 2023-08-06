import sys

import numpy as np
from pyroll.core import RollPass, Hook

VERSION = "2.0"

RollPass.zouhar_contact_c1 = Hook[float]()
"""Get the value of the Zouhar C1 constant for the given roll pass."""

RollPass.zouhar_contact_c2 = Hook[float]()
"""Get the value of the Zouhar C2 constant for the given roll pass."""

RollPass.zouhar_contact_c3 = Hook[float]()
"""Get the value of the Zouhar C3 constant for the given roll pass."""

RollPass.zouhar_contact_in_width = Hook[float]()
"""Get the value of the incoming profile width for the given roll pass."""


@RollPass.zouhar_contact_c1
def default_c1(self: RollPass):
    return 1


@RollPass.zouhar_contact_c2
def default_c2(self: RollPass):
    return 0


@RollPass.zouhar_contact_c3
def default_c3(self: RollPass):
    return 1


@RollPass.zouhar_contact_in_width
def default_in_width(self: RollPass):
    return self.in_profile.width


@RollPass.Roll.contact_area
def contact_area(self: RollPass.Roll):
    rp = self.roll_pass
    if (
            rp.zouhar_contact_c1 is not None
            and
            rp.zouhar_contact_c2 is not None
            and
            rp.zouhar_contact_c3 is not None
            and
            rp.zouhar_contact_in_width is not None
    ):
        rp.logger.debug(f"Used Zouhar contact model for roll pass {rp.label}.")
        return (
                       rp.out_profile.width * rp.zouhar_contact_c2
                       + 0.5 * (
                               rp.out_profile.width
                               + rp.zouhar_contact_in_width * rp.zouhar_contact_c1
                       )
                       * (1 - rp.zouhar_contact_c2)
               ) * rp.zouhar_contact_c3 * rp.roll.contact_length


@RollPass.zouhar_contact_c2
def diamond_diamond_c2(self: RollPass):
    if "diamond" in self.in_profile.classifiers and "diamond" in self.classifiers:
        return 0.3


@RollPass.zouhar_contact_c2
def diamond_square_c2(self: RollPass):
    if "diamond" in self.in_profile.classifiers and "square" in self.classifiers:
        return 0.28


@RollPass.zouhar_contact_in_width
def diamond_square_in_width(self: RollPass):
    if "diamond" in self.in_profile.classifiers and "square" in self.classifiers:
        return self.in_profile.local_width(self.in_profile.height / 2)


@RollPass.zouhar_contact_c2
def oval_square_c2(self: RollPass):
    if "oval" in self.in_profile.classifiers and "square" in self.classifiers:
        return 0.1


@RollPass.zouhar_contact_in_width
def oval_square_in_width(self: RollPass):
    if "oval" in self.in_profile.classifiers and "square" in self.classifiers:
        return self.in_profile.local_width(self.in_profile.height / 2)


@RollPass.zouhar_contact_c1
def round_oval_c1(self: RollPass):
    if "round" in self.in_profile.classifiers and "oval" in self.classifiers:
        return 0.45


@RollPass.zouhar_contact_c2
def round_oval_c2(self: RollPass):
    if "round" in self.in_profile.classifiers and "oval" in self.classifiers:
        return 0.18


@RollPass.zouhar_contact_c1
def square_oval_c1(self: RollPass):
    if "square" in self.in_profile.classifiers and "oval" in self.classifiers:
        return 0.82


@RollPass.zouhar_contact_c2
def square_oval_c2(self: RollPass):
    if "square" in self.in_profile.classifiers and "oval" in self.classifiers:
        return 0.2


@RollPass.zouhar_contact_c3
def square_oval_c3(self: RollPass):
    if "square" in self.in_profile.classifiers and "oval" in self.classifiers:
        return 1.02


try:
    from pyroll.report import hookimpl, plugin_manager


    @hookimpl(specname="property_format")
    def ratio_format(name: str, value: object):
        if name.startswith("zouhar_contact_c"):
            return np.format_float_positional(value, precision=2)

    plugin_manager.register(sys.modules[__name__])

except ImportError:
    pass
