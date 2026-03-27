import random
from constants import EMPLOYEE_TYPES, SEASONS, SEASON_DEMAND_MOD

class Resource:
    def __init__(self, name: str, price: float):
        self.name       = name
        self.base_price = price
        self.price      = price
 
 
class Product:
    def __init__(self, name: str, recipe: dict, base_price: float,
                 start_money: float, prod_cost: float):
        self.name        = name
        self.recipe      = recipe
        self.base_price  = base_price
        self.price       = base_price
        self.start_money = start_money
        self.prod_cost   = prod_cost
 
 
class Business:
    def __init__(self, product: Product):
        self.money        = product.start_money
        self.product      = product
        self.stock        = 0
        self.sell_price   = product.price
        self.resources: dict = {}
        self.employees    = {k: 0 for k in EMPLOYEE_TYPES}
        self.last_profit  = 0
        self.history: list = []
        self.turn         = 0
        self.credit       = 0.0
        self.credit_rate  = 0.08
        self.marketing_boost = 0
        self.marketing_demand_bonus = 0
        self.rent         = 150
 
    def buy_resource(self, resource: Resource, amount: int, tax: float, inflation: float):
        mod  = 1 + inflation + tax * 0.3
        cost = round(resource.base_price * mod * amount, 2)
        if self.money >= cost:
            self.money -= cost
            self.resources[resource.name] = self.resources.get(resource.name, 0) + amount
            return True
        return False
 
    def _effective_prod_cost(self, tax: float, inflation: float) -> float:
        inz = self.employees["Inzenyr"]
        cost_reduction = 1 - min(inz * 0.05, 0.40)
        return self.product.prod_cost * (1 + inflation + tax * 0.2) * cost_reduction
 
    def produce(self, tax: float, inflation: float, amount: int = 1):
        prod_cost = self._effective_prod_cost(tax, inflation)
        produced  = 0
        for _ in range(amount):
            if self.money < prod_cost:
                break
            ok = all(self.resources.get(r, 0) >= q
                     for r, q in self.product.recipe.items())
            if not ok:
                break
            for r, q in self.product.recipe.items():
                self.resources[r] -= q
            self.money -= prod_cost
            self.stock += 1
            produced += 1
        return produced
 
    def hire(self, emp_type: str):
        if self.money >= 200 and emp_type in self.employees:
            self.money -= 200
            self.employees[emp_type] += 1
            return True
        return False
 
    def fire(self, emp_type: str):
        if self.employees.get(emp_type, 0) > 0:
            self.employees[emp_type] -= 1
            return True
        return False
 
    def total_salary(self) -> float:
        return sum(EMPLOYEE_TYPES[t]["salary"] * c for t, c in self.employees.items())
 
    def take_credit(self, amount: float):
        self.money  += amount
        self.credit += amount
 
    def _pay_credit_interest(self):
        if self.credit > 0:
            interest  = round(self.credit * self.credit_rate, 2)
            repayment = round(self.credit * 0.10, 2)
            total     = min(interest + repayment, self.money)
            self.money -= total
            self.credit = max(0, self.credit - repayment)
            return interest + repayment
        return 0.0
 
    def buy_marketing(self, cost: float, demand_bonus: int, duration: int):
        if self.money >= cost:
            self.money -= cost
            self.marketing_boost        = duration
            self.marketing_demand_bonus = demand_bonus
            return True
        return False
 
    def change_sell_price(self, delta: int):
        self.sell_price = max(1, self.sell_price + delta)
 
    def end_quarter(self, market, resources: list):
        pracovnici = self.employees["Pracovnik"]
        if pracovnici > 0:
            self.produce(market.tax, market.inflation, pracovnici)
 
        eff_demand = market.effective_demand(self)
        comp_share = market.competitor_market_share(self.sell_price)
        eff_demand = max(0, int(eff_demand * (1 - comp_share)))
 
        sold     = min(self.stock, eff_demand)
        revenue  = sold * self.sell_price
        tax_amt  = revenue * market.tax
        salaries = self.total_salary()
        credit_p = self._pay_credit_interest()
        penalty  = 500.0 if (self.stock > 0 and self.employees["Pracovnik"] == 0) else 0.0
 
        profit = revenue - tax_amt - salaries - self.rent - penalty - credit_p
        self.money += profit
        self.stock -= sold
        self.last_profit = profit
        self.history.append(profit)
        self.turn += 1
 
        if self.marketing_boost > 0:
            self.marketing_boost -= 1
            if self.marketing_boost == 0:
                self.marketing_demand_bonus = 0
 
        market.next_quarter()
        return {"sold": sold, "revenue": revenue, "tax": tax_amt,
                "salaries": salaries, "credit": credit_p,
                "penalty": penalty, "profit": profit}
 
 
class Market:
    def __init__(self):
        self.tax         = 0.15
        self.base_demand = 12
        self.inflation   = 0.02
        self.economy     = 1.0
        self.season_idx  = 0
        self.comp_price  = 210.0
        self.comp_base   = 210.0
 
    @property
    def season(self) -> str:
        return SEASONS[self.season_idx % 4]
 
    def effective_demand(self, business: Business) -> int:
        s_mod  = SEASON_DEMAND_MOD[self.season]
        m_mod  = 1 + business.employees["Marketolog"] * 0.05
        bonus  = business.marketing_demand_bonus
        return max(1, int(self.base_demand * self.economy * s_mod * m_mod) + bonus)
 
    def competitor_market_share(self, player_price: float) -> float:
        if self.comp_price <= 0:
            return 0.0
        return max(0.0, min(0.5, (player_price / self.comp_price - 1) * 0.3))
 
    def update_resources(self, resources: list):
        for r in resources:
            r.price = round(r.base_price * (1 + self.inflation), 2)
 
    def next_quarter(self):
        self.season_idx += 1
        self.comp_price = round(
            self.comp_base * (1 + self.inflation) * random.uniform(0.92, 1.08), 2)
 
    def apply_event(self, ev: str):
        actions = {
            "krize":       lambda: setattr(self, "economy",   0.8),
            "boom":        lambda: setattr(self, "economy",   1.2),
            "tax_up":      lambda: setattr(self, "tax",       round(min(self.tax + 0.05, 0.60), 2)),
            "tax_down":    lambda: setattr(self, "tax",       round(max(self.tax - 0.05, 0.05), 2)),
            "inflace_up":  lambda: setattr(self, "inflation", round(min(self.inflation + 0.01, 0.20), 3)),
            "inflace_down":lambda: setattr(self, "inflation", round(max(self.inflation - 0.01, 0.00), 3)),
            "comp_dump":   lambda: setattr(self, "comp_price",round(self.comp_base * 0.75, 2)),
            "res_boom":    lambda: setattr(self, "inflation", round(min(self.inflation + 0.03, 0.20), 3)),
        }
        if ev in actions:
            actions[ev]()
 
 
class Event:
    def __init__(self):
        self.text  = "Zadna udalost"
        self._pool = [
            ("krize",       "Ekonomicka krize. Lide mene nakupuji."),
            ("boom",        "Ekonomicky rust. Vyssi poptavka!"),
            ("tax_up",      "Vlada zvysila dane."),
            ("tax_down",    "Vlada snizila dane. Lepsi podminky!"),
            ("inflace_up",  "Roste inflace. Material zdrazuje."),
            ("inflace_down","Inflace klesla. Naklady se snizuji!"),
            ("comp_dump",   "Konkurent drasticky snizil ceny!"),
            ("res_boom",    "Celosvetovy nedostatek surovin!"),
            ("none",        "Ekonomika stabilni."),
            ("none",        "Ekonomika stabilni."),
            ("none",        "Ekonomika stabilni."),
        ]
 
    def trigger(self, market: Market) -> str:
        ev, text = random.choice(self._pool)
        self.text = text
        market.apply_event(ev)
        return ev