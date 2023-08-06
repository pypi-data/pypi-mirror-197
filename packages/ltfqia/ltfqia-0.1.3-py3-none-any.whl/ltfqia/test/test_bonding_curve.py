import panel as pn

from ltfqia import BondingCurveInitializer, BondingCurve, BondingCurveCalculator


def test_bonding_curve():
    r = BondingCurveInitializer()
    r_display = pn.Row(pn.Column(r, r.outputs), r.view)

    bc = BondingCurve()
    bc_display = pn.Row(pn.Column(bc, bc.outputs), bc.view)


    c = BondingCurveCalculator()
    c_display = pn.Row(pn.Column(c, c.outputs), c.view)

    return pn.Column(r_display, bc_display, c_display)
