import param as pm
from ltfqia.interest_rate import InterestRate
"""
2.0 Net Present Value and Internal Rate of Return
There are three chief areas of financial decision-making in most businesses. 
Capital Budgeting is the allocation of funds to relatively long-range projects
or investements. 
From the perspective of capital budgeting, a company is a portfolio of projects
and investments. 
Capital structure is the choice of long-term financing for the investments the
company wants to make.
Working Capital Management is the management of the company's short-term assets
(such as inventory) and short-term liabilities (such as money owed to
suppliers).
2.1 Net Present Value and the Net Present Value Rule
Net present value (NPV) describes a way to characterize the value of an
investment, and the net present value rule is a method for choosing among
alternative investments. 
The net present value of an investment is the present value of its cash inflows
minus the present value of its cash outflows. The word "net" in an NPV refers
to subtracting the present value of the investments outflows (costs) from the
present value of its inflows (benefits) to arrive at the net benefit.
The steps in computing NPV and applying the NPV rule are as follows:
1. Identify all cash flows associated with the investment - all inflows and outflows.
2. Determine the appropriate discount rate or opportunity cost, r, for the investment project
3. Using that discount rate, find the present value of each cash flow. (Inflows are positive, outflows are negative.)
4. Sum all present values. The sum of the present values of all cash flows (inflows and outflows) is the investments net present value.
5. Apply the NPV rule: if the investment's NPV is positive, an investor should undertake it; if the NPV is negative, the investor should not undertake it. If an investor must choose one project over another, they will choose the one with higher NPV.
"""


class NetPresentValue(pm.Parameterized):
    cashflows = pm.ListSelector(default=[], objects=[])

    def __init__(self, discount_rate: InterestRate, cash_flows: list, **params):
        self.discount_rate = discount_rate
        self.cash_flows = cash_flows
        super(NetPresentValue, self).__init__(**params)
