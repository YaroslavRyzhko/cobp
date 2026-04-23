import pygame
from constants import EMPLOYEE_TYPES
from business import Business, Market, Event

class Renderer:
    # ── colours ────────────────────────────────────────────────
    C_BG     = (245, 245, 250)
    C_PANEL  = (233, 233, 244)
    C_BORDER = (180, 180, 200)
    C_TEXT   = (20,  20,  40)
    C_LABEL  = (80,  80, 100)
    C_ACCENT = (40,  40, 120)
    C_GREEN  = (0,  155,   0)
    C_RED    = (195,  0,   0)
 
    # ── layout constants (all in pixels, screen 1000×700) ──────
    # Left stats panel
    SP_X, SP_Y, SP_W, SP_H = 5,   5, 260, 450   # stats
    RP_X, RP_Y, RP_W, RP_H = 5, 460, 260,  76   # resources
 
    # Right block (graph + employees + recipe + report)
    GP_X, GP_Y, GP_W, GP_H = 270,  5, 435, 205  # graph
    EP_X, EP_Y, EP_W, EP_H = 270, 215, 200, 115  # employees
    RP2_X,RP2_Y,RP2_W,RP2_H= 270, 335, 200,  76  # recipe
    LR_X, LR_Y, LR_W, LR_H = 475, 215, 225, 196  # last-report
 
    # Bottom info strip
    EV_X,  EV_Y,  EV_W,  EV_H  = 5, 540,  988, 26   # event box
    TIP_X, TIP_Y                = 5, 572              # tip text
 
    # Button rows – start well below all panels
    R1 = 592   # row 1
    R2 = 626   # row 2
    R3 = 658   # row 3
    BH = 30    # button height
 
    def __init__(self, screen, fonts: dict):
        self.screen   = screen
        self.font     = fonts["small"]
        self.font_big = fonts["big"]
        self.font_med = fonts["med"]
        self.W = screen.get_width()
        self.H = screen.get_height()
 
    # ── helpers ────────────────────────────────────────────────
    def _panel(self, rect, bg=None):
        bg = bg or self.C_PANEL
        pygame.draw.rect(self.screen, bg, rect, border_radius=7)
        pygame.draw.rect(self.screen, self.C_BORDER, rect, 1, border_radius=7)
 
    def _txt(self, text, x, y, color=None, font=None):
        self.screen.blit(
            (font or self.font).render(text, True, color or self.C_TEXT),
            (x, y))
 
    # ── graph ──────────────────────────────────────────────────
    def draw_graph(self, history: list):
        GX, GY = self.GP_X + 4, self.GP_Y + 4
        GW, GH = self.GP_W - 8, self.GP_H - 8
        self._panel((GX, GY, GW, GH), (238, 238, 248))
        lbl = self.font.render("Graf zisku (Kc)", True, self.C_ACCENT)
        self.screen.blit(lbl, (GX + GW // 2 - lbl.get_width() // 2, GY + 4))
 
        if len(history) < 2:
            self._txt("Zatim zadna data...", GX + 10, GY + GH // 2 - 6, (160, 160, 160))
            return
 
        max_v = max(history); min_v = min(history)
        span  = max_v - min_v if max_v != min_v else 1
        pad   = 18
        # leave 52px right margin for value labels
        draw_w = GW - pad - 52
        step   = draw_w / max(len(history) - 1, 1)
 
        pts = [(GX + pad + i * step,
                GY + GH - pad - ((v - min_v) / span) * (GH - 2 * pad))
               for i, v in enumerate(history)]
 
        z = GY + GH - pad - ((0 - min_v) / span) * (GH - 2 * pad)
        z = max(GY + pad, min(GY + GH - pad, z))
        pygame.draw.line(self.screen, (200, 80, 80),
                         (GX + pad, z), (GX + pad + draw_w, z), 1)
 
        for i in range(1, len(pts)):
            c = self.C_GREEN if history[i] >= 0 else self.C_RED
            pygame.draw.line(self.screen, c, pts[i-1], pts[i], 2)
 
        lx = GX + pad + draw_w + 4
        self._txt(str(int(max_v)), lx, GY + pad)
        self._txt(str(int(min_v)), lx, GY + GH - pad - 10)
 
    # ── menu ───────────────────────────────────────────────────
    def draw_menu(self, buttons: list):
        t = self.font_big.render("Simulator podnikani", True, (30, 30, 80))
        self.screen.blit(t, (self.W // 2 - t.get_width() // 2, 110))
        s = self.font_med.render(
            "Obchodni informacni systemy – OOP simulace", True, (100, 100, 150))
        self.screen.blit(s, (self.W // 2 - s.get_width() // 2, 170))
        for b in buttons:
            b.draw(self.screen, self.font)
 
    # ── product select ─────────────────────────────────────────
    def draw_product_select(self, products: list, buttons: list):
        t = self.font_med.render("Vyber produkt pro novou hru:", True, self.C_ACCENT)
        self.screen.blit(t, (self.W // 2 - t.get_width() // 2, 110))
        for i, p in enumerate(products):
            info = (f"{p.name}  |  Cena: {p.base_price} Kc  |  "
                    f"Start: {int(p.start_money)} Kc  |  Recept: " +
                    ", ".join(f"{k} x{v}" for k, v in p.recipe.items()))
            self._txt(info, 80, 175 + i * 90, self.C_LABEL)
        for b in buttons:
            b.draw(self.screen, self.font)
 
    # ── game over ──────────────────────────────────────────────
    def draw_gameover(self, turn: int, buttons: list):
        msg = self.font_big.render("KONEC HRY – Firma zkrachovala!", True, self.C_RED)
        self.screen.blit(msg, (self.W // 2 - msg.get_width() // 2, 240))
        sub = self.font_med.render(f"Prezili jste {turn} kvartalu.", True, self.C_LABEL)
        self.screen.blit(sub, (self.W // 2 - sub.get_width() // 2, 310))
        for b in buttons:
            b.draw(self.screen, self.font)
 
    # ── main game ──────────────────────────────────────────────
    def draw_game(self, business: Business, market: Market,
                  event: Event, resources: list,
                  last_report: dict, buttons: list):
 
        # ── Stats panel (left, narrow) ──────────────────────────
        self._panel((self.SP_X, self.SP_Y, self.SP_W, self.SP_H))
        V = 185   # value column x
        stats = [
            ("Penize:",         f"{int(business.money)} Kc",
             self.C_GREEN if business.money > 0 else self.C_RED),
            ("Sklad:",          f"{business.stock} ks",           self.C_TEXT),
            ("Prodejni cena:",  f"{business.sell_price} Kc",      self.C_TEXT),
            ("Produkt:",        business.product.name,             self.C_ACCENT),
            ("Sezona:",         market.season,                     self.C_ACCENT),
            ("Kvartal:",        str(business.turn),                self.C_TEXT),
            ("Dan:",            f"{int(market.tax * 100)} %",      self.C_TEXT),
            ("Inflace:",        f"{round(market.inflation*100,1)} %", self.C_TEXT),
            ("Poptavka:",       str(market.effective_demand(business)), self.C_TEXT),
            ("Konk. cena:",
             f"{business.sell_price} / {int(market.comp_price)} Kc",
             self.C_GREEN if business.sell_price <= market.comp_price else self.C_RED),
            ("Kredit:",         f"{int(business.credit)} Kc",
             self.C_RED if business.credit > 0 else self.C_TEXT),
            ("Marketing:",      f"{business.marketing_boost} kv.",
             self.C_ACCENT if business.marketing_boost > 0 else self.C_LABEL),
            ("Zisk min. kv.:",  f"{int(business.last_profit)} Kc",
             self.C_GREEN if business.last_profit >= 0 else self.C_RED),
        ]
        for i, (lbl, val, vc) in enumerate(stats):
            self._txt(lbl, self.SP_X + 8,   self.SP_Y + 10 + i * 32, self.C_LABEL)
            self._txt(val, self.SP_X + V,    self.SP_Y + 10 + i * 32, vc)
 
        # ── Resources panel ─────────────────────────────────────
        self._panel((self.RP_X, self.RP_Y, self.RP_W, self.RP_H))
        self._txt("Zasoby:", self.RP_X + 8, self.RP_Y + 6, self.C_ACCENT)
        for ri, r in enumerate(resources):
            qty = business.resources.get(r.name, 0)
            self._txt(f"  {r.name}: {qty} ks  (nakup ~{int(r.price)} Kc)",
                      self.RP_X + 8, self.RP_Y + 24 + ri * 22)
 
        # ── Graph ───────────────────────────────────────────────
        self.draw_graph(business.history)
 
        # ── Employees panel ─────────────────────────────────────
        self._panel((self.EP_X, self.EP_Y, self.EP_W, self.EP_H))
        self._txt("Zamestnanci (najeti: 200):", self.EP_X + 8, self.EP_Y + 6, self.C_ACCENT)
        for ei, (etype, edata) in enumerate(EMPLOYEE_TYPES.items()):
            cnt = business.employees[etype]
            self._txt(f"  {etype}: {cnt}  (plat {edata['salary']} Kc)",
                      self.EP_X + 8, self.EP_Y + 24 + ei * 28)
 
        # ── Recipe panel ────────────────────────────────────────
        self._panel((self.RP2_X, self.RP2_Y, self.RP2_W, self.RP2_H))
        self._txt(f"Recept ({business.product.name}):",
                  self.RP2_X + 8, self.RP2_Y + 6, self.C_ACCENT)
        prod_cost = business._effective_prod_cost(market.tax, market.inflation)
        self._txt(f"  Vyr. naklady: ~{int(prod_cost)} Kc",
                  self.RP2_X + 8, self.RP2_Y + 24)
        for ri, (rn, qty) in enumerate(business.product.recipe.items()):
            self._txt(f"  {rn} x{qty}",
                      self.RP2_X + 8, self.RP2_Y + 44 + ri * 18, self.C_LABEL)
 
        # ── Last-quarter report ─────────────────────────────────
        if last_report:
            self._panel((self.LR_X, self.LR_Y, self.LR_W, self.LR_H))
            self._txt("Minuly kvartal:", self.LR_X + 8, self.LR_Y + 6, self.C_ACCENT)
            rows = [
                f"  Prodano:   {last_report.get('sold', 0)} ks",
                f"  Trzby:     {int(last_report.get('revenue', 0))} Kc",
                f"  Dane:     -{int(last_report.get('tax', 0))} Kc",
                f"  Mzdy:     -{int(last_report.get('salaries', 0))} Kc",
            ]
            if last_report.get("penalty", 0) > 0:
                rows.append(f"  Pokuta:   -{int(last_report['penalty'])} Kc")
            if last_report.get("credit", 0) > 0:
                rows.append(f"  Kredit:   -{int(last_report['credit'])} Kc")
            rows.append(f"  Zisk:      {int(last_report.get('profit', 0))} Kc")
            for ri, row in enumerate(rows):
                color = self.C_RED if "Pokuta" in row or "Kredit" in row else self.C_TEXT
                if "Zisk" in row:
                    color = self.C_GREEN if last_report.get("profit", 0) >= 0 else self.C_RED
                self._txt(row, self.LR_X + 8, self.LR_Y + 24 + ri * 22, color)
 
        # ── Event box ───────────────────────────────────────────
        self._panel((self.EV_X, self.EV_Y, self.EV_W, self.EV_H), (224, 224, 255))
        self._txt(f"Udalost: {event.text}", self.EV_X + 8, self.EV_Y + 5, (40, 0, 120))
 
        # ── Tip ─────────────────────────────────────────────────
        self._txt(
            "Tip: Drzet tlacitko = rychle nakupy.  Kazdy tah = 1 kvartal.",
            self.TIP_X, self.TIP_Y, (120, 120, 140))
 
        # ── Buttons ─────────────────────────────────────────────
        for b in buttons:
            b.draw(self.screen, self.font)