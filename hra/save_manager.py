import json
from business import Business, Market
class SaveManager:
    FILENAME = "save.json"
 
    def save(self, business: Business, market: Market) -> str:
        try:
            data = {
                "money": business.money, "stock": business.stock,
                "sell_price": business.sell_price,
                "resources": business.resources,
                "employees": business.employees,
                "last_profit": business.last_profit,
                "history": business.history, "turn": business.turn,
                "credit": business.credit,
                "marketing_boost": business.marketing_boost,
                "marketing_demand_bonus": business.marketing_demand_bonus,
                "rent": business.rent,
                "market_tax": market.tax, "market_base_demand": market.base_demand,
                "market_inflation": market.inflation, "market_economy": market.economy,
                "market_season_idx": market.season_idx,
                "market_comp_price": market.comp_price,
                "product_name": business.product.name,
            }
            with open(self.FILENAME, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return "Hra ulozena!"
        except Exception as e:
            return f"Chyba ulozeni: {e}"
 
    def load(self, business: Business, market: Market) -> str:
        try:
            with open(self.FILENAME, "r", encoding="utf-8") as f:
                data = json.load(f)
            business.money               = data["money"]
            business.stock               = data["stock"]
            business.sell_price          = data["sell_price"]
            business.resources           = data["resources"]
            business.employees           = data["employees"]
            business.last_profit         = data["last_profit"]
            business.history             = data["history"]
            business.turn                = data["turn"]
            business.credit              = data["credit"]
            business.marketing_boost     = data["marketing_boost"]
            business.marketing_demand_bonus = data["marketing_demand_bonus"]
            business.rent                = data["rent"]
            market.tax                   = data["market_tax"]
            market.base_demand           = data["market_base_demand"]
            market.inflation             = data["market_inflation"]
            market.economy               = data["market_economy"]
            market.season_idx            = data["market_season_idx"]
            market.comp_price            = data["market_comp_price"]
            return "Hra nactena!"
        except FileNotFoundError:
            return "Soubor save.json nenalezen."
        except Exception as e:
            return f"Chyba nacteni: {e}"