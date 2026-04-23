import pygame
from buttons import Button
from render import Renderer
from save_manager import SaveManager
from business import Business, Market, Resource, Event, Product
from hra.products import PRODUCTS

class Game:
    WIDTH  = 1000
    HEIGHT = 700    # увеличена высота для панелей + кнопок без перекрытий
    FPS    = 60
 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Simulátor podnikání")
 
        fonts = {
            "small": pygame.font.SysFont(None, 21),
            "big":   pygame.font.SysFont(None, 46),
            "med":   pygame.font.SysFont(None, 30),
        }
        self.font      = fonts["small"]
        self.renderer  = Renderer(self.screen, fonts)
        self.save_mgr  = SaveManager()
        self.clock     = pygame.time.Clock()
        self.state     = "menu"
        self.last_report: dict = {}
        self.event_obj = Event()
 
        self.metal    = Resource("Kov",   50)
        self.plastic  = Resource("Plast", 30)
        self.glass    = Resource("Sklo",  40)
        self.resources = [self.metal, self.plastic, self.glass]
 
        self.products         = PRODUCTS
        self.selected_product = self.products[0]
        self.business: Business = Business(self.selected_product)
        self.market:   Market   = Market()
 
        self._all_repeatable_buttons: list = []
        self._build_menu_buttons()
        self._build_product_buttons()
        self._build_game_buttons()
 
    # ── state helpers ───────────────────────────────────────────
    def _set_state(self, s: str):
        self.state = s
 
    def _select_product(self, p: Product):
        self.selected_product = p
        self._start_game()
 
    def _start_game(self):
        self.business    = Business(self.selected_product)
        self.market      = Market()
        self.event_obj   = Event()
        self.last_report = {}
        self.state       = "game"
        self._build_game_buttons()
 
    def _next_turn(self):
        self.last_report = self.business.end_quarter(self.market, self.resources)
        self.market.update_resources(self.resources)
        self.event_obj.trigger(self.market)
 
    def _save(self):
        self.event_obj.text = self.save_mgr.save(self.business, self.market)
 
    def _load(self):
        self.event_obj.text = self.save_mgr.load(self.business, self.market)
        self.state = "game"
 
    def _buy_res(self, resource: Resource, amt: int):
        self.business.buy_resource(resource, amt, self.market.tax, self.market.inflation)
 
    def _produce(self, amt: int = 1):
        self.business.produce(self.market.tax, self.market.inflation, amt)
 
    def _take_credit(self, amount: float):
        self.business.take_credit(amount)
        self.event_obj.text = f"Kredit {int(amount)} Kc prijat. Splatte vcas!"
 
    def _buy_marketing(self):
        ok = self.business.buy_marketing(cost=500, demand_bonus=5, duration=3)
        self.event_obj.text = ("Marketing: +5 poptavky na 3 kv."
                               if ok else "Nedostatek penez na marketing.")
 
    # ── button builders ─────────────────────────────────────────
    def _build_menu_buttons(self):
        self.menu_buttons = [
            Button(350, 265, 300, 50, "Nova hra",
                   lambda: self._set_state("product_select"), (100, 200, 120)),
            Button(350, 330, 300, 50, "Nacist hru", self._load,      (100, 170, 220)),
            Button(350, 395, 300, 50, "Ukoncit",    pygame.quit,     (220, 100, 100)),
        ]
 
    def _build_product_buttons(self):
        self.product_buttons = [
            Button(350, 200 + i * 90, 300, 55, f"Hrat jako: {p.name}",
                   lambda _p=p: self._select_product(_p), (100, 190, 160))
            for i, p in enumerate(self.products)
        ]
        self.product_buttons.append(
            Button(430, 470, 140, 38, "<- Zpet",
                   lambda: self._set_state("menu"), (200, 200, 200))
        )
 
    def _build_game_buttons(self):
        R  = Renderer
        BH = R.BH
 
        def res_btn(x, label, res, amt):
            w = 95 if amt == 2 else 100
            return Button(x, R.R1, w, BH, label,
                          lambda r=res, a=amt: self._buy_res(r, a),
                          (200, 220, 255), repeatable=True)
 
        self.game_buttons = [
            # ── ROW 1: resources + next-turn ───────────────────
            res_btn(  5, "Kov +2",    self.metal,    2),
            res_btn(105, "Kov +10",   self.metal,   10),
            res_btn(210, "Plast +2",  self.plastic,  2),
            res_btn(315, "Plast +10", self.plastic, 10),
            res_btn(420, "Sklo +2",   self.glass,    2),
            res_btn(520, "Sklo +10",  self.glass,   10),
            Button(625, R.R1, 370, BH, "Dalsi tah >> (1 kvartal)",
                   self._next_turn, (255, 210, 50)),
 
            # ── ROW 2: produce / price / employees ─────────────
            Button(  5, R.R2,  95, BH, "Vyrobit x1",
                   lambda: self._produce(1), (120, 220, 120), repeatable=True),
            Button(105, R.R2,  95, BH, "Vyrobit x5",
                   lambda: self._produce(5), (120, 220, 120), repeatable=True),
            Button(210, R.R2,  95, BH, "Cena +10",
                   lambda: self.business.change_sell_price(+10),
                   (180, 255, 180), repeatable=True),
            Button(310, R.R2,  95, BH, "Cena -10",
                   lambda: self.business.change_sell_price(-10),
                   (255, 180, 180), repeatable=True),
            Button(415, R.R2, 100, BH, "Najit Prac.",
                   lambda: self.business.hire("Pracovnik"), (170, 210, 255)),
            Button(520, R.R2, 100, BH, "Prop. Prac.",
                   lambda: self.business.fire("Pracovnik"), (255, 200, 170)),
            Button(625, R.R2, 115, BH, "Kredit 1000",
                   lambda: self._take_credit(1000), (255, 200, 140)),
            Button(745, R.R2, 115, BH, "Kredit 5000",
                   lambda: self._take_credit(5000), (255, 180, 100)),
            Button(865, R.R2,  80, BH, "Ulozit",
                   self._save, (200, 200, 200)),
            Button(950, R.R2,  45, BH, "Load",
                   self._load, (200, 200, 200)),
 
            # ── ROW 3: engineer / marketolog / marketing ────────
            Button(  5, R.R3, 100, BH, "Najit Inz.",
                   lambda: self.business.hire("Inzenyr"), (170, 230, 200)),
            Button(110, R.R3, 100, BH, "Prop. Inz.",
                   lambda: self.business.fire("Inzenyr"), (255, 210, 180)),
            Button(215, R.R3, 115, BH, "Najit Market.",
                   lambda: self.business.hire("Marketolog"), (220, 190, 255)),
            Button(335, R.R3, 115, BH, "Prop. Market.",
                   lambda: self.business.fire("Marketolog"), (255, 190, 220)),
            Button(455, R.R3, 120, BH, "Reklama (500)",
                   self._buy_marketing, (255, 230, 100)),
        ]
 
        BW, BH2 = 118, 28
        self.back_btn = Button(
            self.WIDTH - BW - 6, self.HEIGHT - BH2 - 4,
            BW, BH2, "<- Menu",
            lambda: self._set_state("menu"), (200, 200, 200)
        )
        self.restart_btn = Button(
            370, 390, 260, 50, "Nova hra",
            lambda: self._set_state("product_select"), (100, 200, 120)
        )
        self._all_repeatable_buttons = [b for b in self.game_buttons if b.repeatable]
 
    # ── input ──────────────────────────────────────────────────
    def _handle_events(self) -> bool:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "menu":
                    for b in self.menu_buttons:    b.click(e.pos)
                elif self.state == "product_select":
                    for b in self.product_buttons: b.click(e.pos)
                elif self.state == "game":
                    for b in self.game_buttons:    b.on_mouse_down(e.pos)
                    self.back_btn.click(e.pos)
                elif self.state == "gameover":
                    self.restart_btn.click(e.pos)
                    self.back_btn.click(e.pos)
            if e.type == pygame.MOUSEBUTTONUP and self.state == "game":
                for b in self._all_repeatable_buttons:
                    b.on_mouse_up(e.pos)
        return True
 
    def _update_hover(self, mp):
        mapping = {
            "menu":           self.menu_buttons,
            "product_select": self.product_buttons,
            "game":           self.game_buttons + [self.back_btn],
            "gameover":       [self.restart_btn, self.back_btn],
        }
        for b in mapping.get(self.state, []):
            b.update(mp)
 
    # ── main loop ───────────────────────────────────────────────
    def run(self):
        running = True
        while running:
            mp = pygame.mouse.get_pos()
            self.screen.fill(Renderer.C_BG)
            self._update_hover(mp)
 
            if self.state == "game":
                for b in self._all_repeatable_buttons:
                    b.tick()
 
            if self.state == "menu":
                self.renderer.draw_menu(self.menu_buttons)
            elif self.state == "product_select":
                self.renderer.draw_product_select(self.products, self.product_buttons)
            elif self.state == "gameover":
                self.renderer.draw_gameover(
                    self.business.turn, [self.restart_btn, self.back_btn])
            elif self.state == "game":
                if self.business.money < -500:
                    self.state = "gameover"
                else:
                    self.renderer.draw_game(
                        self.business, self.market, self.event_obj,
                        self.resources, self.last_report,
                        self.game_buttons + [self.back_btn],
                    )
 
            running = self._handle_events()
            pygame.display.flip()
            self.clock.tick(self.FPS)
 
        pygame.quit()