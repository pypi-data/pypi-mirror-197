import holoviews as hv
import pandas as pd
import numpy as np
import param as pm

class PureCurve(pm.Parameterized):
    reserve_ratio = pm.Number(0.5, bounds=(0.01,2), step=0.01)
    price = pm.Number(1, bounds=(0.01,10), step=0.01)
    supply = pm.Number(0.5, bounds=(0.01,0.99), step=0.01)
    
    @pm.depends("r", "price", "supply")
    def update(self):
        self.slope = self.slope()
        self.exponent = self.exponent()
    
    def exponent(self):
        return (1 / self.reserve_ratio) - 1
    
    def slope(self):
        return self.price / self.supply ** self.exponent()
    
    def exponential(self, x):
        return self.slope() * x ** self.exponent()
    
    #For drawing the bonding curve. Range shows how many times the initial supply you make the graph for, steps how many subdivisions
    def curve_over_supply(self, supply_range=1, steps=1000):
        x = np.linspace(self.param['supply'].bounds[0]/2, self.param['supply'].bounds[1], steps)
        y = self.exponential(x)

        return pd.DataFrame(zip(x, y), columns=["Supply", "Price"])
    
    def initial_point(self):
        points = hv.Points((self.supply,self.price))
        return points.opts(color='k', size=10)
    
    def view_curve_over_supply(self):
        hv.extension('bokeh')
        curve = self.curve_over_supply()
        return curve.hvplot.line(x='Supply', y='Price', line_width=8) * self.initial_point()
    
    def info(self):
        return f"Slope: {self.slope():.2} Exponent: {self.exponent():.2}"

class BondingCurveInitializer(pm.Parameterized):

    initial_price = pm.Number(3, bounds=(0.1,10), step=0.01)
    initial_supply = pm.Number(100, bounds=(1,1000), step=1)
    initial_balance = pm.Number(100, bounds=(1,1000), step=1)

    def reserve_ratio(self):
        return self.initial_balance / (self.initial_price * self.initial_supply)
    
    #Returns the token price given a specific supply
    def get_price(self, supply):
        return (supply ** ((1 / self.reserve_ratio()) - 1) * self.initial_price) / (
            self.initial_supply ** ((1 / self.reserve_ratio()) - 1)
        )

    #Returns the collateral balance price given a specific supply
    def get_balance(self, supply):
        return (
            self.reserve_ratio() * self.get_price(supply) * supply
        )
    
    #For drawing the bonding curve. Range shows how many times the initial supply you make the graph for, steps how many subdivisions
    def curve_over_supply(self, range=6, steps=1000):
        x = np.linspace(0, self.initial_supply*range, steps)
        y = self.get_price(x)

        return pd.DataFrame(zip(x, y), columns=["Supply (in thousands)", "Price"])
    
    def curve_over_balance(self, range=6, steps=1000):
        supply_list = np.linspace(0, self.initial_supply*range, steps)
        x = self.get_balance(supply_list)
        y = self.get_price(supply_list)

        return pd.DataFrame(zip(x, y), columns=["Balance (in thousands)", "Price"])
    
    def initial_point(self):
        points = hv.Points((self.initial_supply,self.initial_price))
        return points.opts(color='k', size=10)
    
    def outputs(self):
        return "Reserve Ratio: {0:.2f}".format(self.reserve_ratio())
    
    def view(self):
        hv.extension('bokeh')
        curve = self.curve_over_supply()
        return curve.hvplot.line(x='Supply (in thousands)', y='Price', line_width=8) * self.initial_point()



class BondingCurve(BondingCurveInitializer):
    
    current_supply = pm.Number(100, bounds=(1,1000), step=1)

    #Returns how much wxDai you get from selling TEC
    def sale_return(self, bonded):
        return self.get_balance(self.current_supply) * (
            (bonded / self.current_supply + 1) ** (1 / self.reserve_ratio()) - 1
        )

    #Returns how much TEC you get from purchasing with wxDai
    def purchase_return(self, collateral):
        return self.current_supply * (
            (collateral / self.get_balance(self.current_supply) + 1) ** (self.reserve_ratio()) - 1
        )
    
    def current_point(self):
        points = hv.Points((self.current_supply,self.get_price(self.current_supply)))
        return points.opts(color='red', size=10)

    def outputs(self):
        return "Initial price: {0:.2f}\n\rCurrent price: {1:.2f}".format(self.initial_price, self.get_price(self.current_supply))

    def view(self):
        hv.extension('bokeh')
        curve = self.curve_over_supply()
        return curve.hvplot.line(x='Supply (in thousands)', y='Price', line_width=8) * self.initial_point() * self.current_point()


class BondingCurveCalculator(BondingCurve):
    amount = pm.Number(0, bounds=(-100, 100))
    
    def new_supply(self):
        return max(0, min(self.current_supply + self.purchase_return(self.sale_return(self.amount)), 1000))

    def new_point(self):
        new_supply = self.new_supply()
        points = hv.Points((new_supply, self.get_price(new_supply)))
        return points.opts(color='green', size=10)
    
    def outputs(self):
        return "Initial price: {0:.2f}\n\rCurrent price: {0:.2f}\n\rNew price: {1:.2f}\n\rNew Supply: {2:.2f}".format(self.get_price(self.current_supply), self.get_price(self.new_supply()), self.new_supply())

    def view(self):
        hv.extension('bokeh')
        curve = self.curve_over_supply()
        return curve.hvplot.line(x='Supply (in thousands)', y='Price', line_width=8) * self.current_point() * self.new_point()
