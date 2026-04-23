import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ── Color palette ──────────────────────────────────────────────
BG_DARK    = "#1a1a2e"
BG_PANEL   = "#16213e"
BG_CARD    = "#0f3460"
ACCENT     = "#e94560"
ACCENT2    = "#f5a623"
TEXT_WHITE = "#ffffff"
TEXT_GRAY  = "#a0aec0"
GREEN      = "#48bb78"
RED        = "#fc8181"
BTN_HOVER  = "#c73652"

# ── Mock data ───────────────────────────────────────────────────
PRODUCTS = [
    {"code": "A1", "name": "Lays Chips",      "price": 1.50, "count": 8,  "max": 10},
    {"code": "A2", "name": "Doritos",          "price": 1.75, "count": 5,  "max": 10},
    {"code": "A3", "name": "Snickers",         "price": 1.25, "count": 3,  "max": 10},
    {"code": "A4", "name": "Kit Kat",          "price": 1.25, "count": 0,  "max": 10},
    {"code": "B1", "name": "Coca-Cola",        "price": 2.00, "count": 7,  "max": 12},
    {"code": "B2", "name": "Sprite",           "price": 2.00, "count": 4,  "max": 12},
    {"code": "B3", "name": "Water",            "price": 1.00, "count": 10, "max": 12},
    {"code": "B4", "name": "Orange Juice",     "price": 2.50, "count": 2,  "max": 12},
    {"code": "C1", "name": "Granola Bar",      "price": 1.50, "count": 6,  "max": 10},
    {"code": "C2", "name": "Trail Mix",        "price": 2.00, "count": 1,  "max": 10},
    {"code": "C3", "name": "Peanuts",          "price": 1.00, "count": 9,  "max": 10},
    {"code": "C4", "name": "Protein Bar",      "price": 3.00, "count": 0,  "max": 10},
]

WORKER_ID = "W-1042"


# ═══════════════════════════════════════════════════════════════
class VendingMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine System")
        self.geometry("900x680")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)

        self.current_frame = None
        self.show_home()

    # ── Navigation ──────────────────────────────────────────────
    def switch_frame(self, FrameClass, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = FrameClass(self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_home(self):       self.switch_frame(HomeScreen)
    def show_record_sale(self): self.switch_frame(RecordSaleScreen)
    def show_inventory(self):  self.switch_frame(UpdateInventoryScreen)


# ═══════════════════════════════════════════════════════════════
class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self._build()

    def _build(self):
        # Header
        hdr = tk.Frame(self, bg=BG_PANEL, height=80)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏪  VENDING MACHINE SYSTEM",
                 font=("Courier", 20, "bold"), fg=ACCENT, bg=BG_PANEL
                 ).pack(side="left", padx=24, pady=20)
        tk.Label(hdr, text=f"Machine ID: VM-001  |  {datetime.now().strftime('%Y-%m-%d')}",
                 font=("Courier", 10), fg=TEXT_GRAY, bg=BG_PANEL
                 ).pack(side="right", padx=24)

        # Body
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(expand=True)

        tk.Label(body, text="Select an Action",
                 font=("Courier", 16), fg=TEXT_WHITE, bg=BG_DARK
                 ).pack(pady=(60, 40))

        self._big_btn(body, "💳  Record Sale",
                      "Customer purchases a product",
                      self.master.show_record_sale)
        tk.Frame(body, height=20, bg=BG_DARK).pack()
        self._big_btn(body, "📦  Update Inventory",
                      "Restocker updates machine slots",
                      self.master.show_inventory)

    def _big_btn(self, parent, title, subtitle, cmd):
        card = tk.Frame(parent, bg=BG_CARD, cursor="hand2", width=420, height=90)
        card.pack_propagate(False)
        card.pack()
        tk.Label(card, text=title, font=("Courier", 14, "bold"),
                 fg=TEXT_WHITE, bg=BG_CARD).pack(anchor="w", padx=20, pady=(18, 2))
        tk.Label(card, text=subtitle, font=("Courier", 10),
                 fg=TEXT_GRAY, bg=BG_CARD).pack(anchor="w", padx=20)
        card.bind("<Button-1>", lambda e: cmd())
        for w in card.winfo_children():
            w.bind("<Button-1>", lambda e: cmd())
        card.bind("<Enter>", lambda e: card.configure(bg=ACCENT))
        card.bind("<Leave>", lambda e: card.configure(bg=BG_CARD))


# ═══════════════════════════════════════════════════════════════
class RecordSaleScreen(tk.Frame):
    """Use Case 1 – Record Sale"""

    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self.selected   = None   # product dict
        self.payment    = tk.StringVar(value="cash")
        self.input_code = tk.StringVar()
        self.cash_given = tk.DoubleVar()
        self._build()

    # ── Layout ──────────────────────────────────────────────────
    def _build(self):
        self._header()
        main = tk.Frame(self, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=16, pady=10)

        left  = tk.Frame(main, bg=BG_DARK)
        right = tk.Frame(main, bg=BG_DARK, width=300)
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="y", padx=(10, 0))

        self._product_grid(left)
        self._sale_panel(right)

    def _header(self):
        hdr = tk.Frame(self, bg=BG_PANEL)
        hdr.pack(fill="x")
        tk.Button(hdr, text="← Back", font=("Courier", 10),
                  bg=BG_PANEL, fg=TEXT_GRAY, bd=0, cursor="hand2",
                  command=self.master.show_home).pack(side="left", padx=14, pady=14)
        tk.Label(hdr, text="💳  RECORD SALE",
                 font=("Courier", 16, "bold"), fg=ACCENT, bg=BG_PANEL
                 ).pack(side="left", padx=4, pady=14)

    # ── Product grid ────────────────────────────────────────────
    def _product_grid(self, parent):
        tk.Label(parent, text="Select Product", font=("Courier", 11, "bold"),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w", pady=(4, 6))

        grid_frame = tk.Frame(parent, bg=BG_DARK)
        grid_frame.pack(fill="both", expand=True)

        for i, p in enumerate(PRODUCTS):
            r, c = divmod(i, 4)
            self._product_tile(grid_frame, p, r, c)

    def _product_tile(self, parent, p, row, col):
        is_empty = p["count"] == 0
        bg = "#2d3748" if is_empty else BG_CARD

        tile = tk.Frame(parent, bg=bg, width=130, height=100,
                        highlightbackground=BG_DARK, highlightthickness=2)
        tile.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        tile.grid_propagate(False)
        parent.grid_columnconfigure(col, weight=1)

        tk.Label(tile, text=p["code"], font=("Courier", 10, "bold"),
                 fg=ACCENT2, bg=bg).place(x=6, y=4)
        tk.Label(tile, text=p["name"], font=("Courier", 9, "bold"),
                 fg=TEXT_WHITE if not is_empty else TEXT_GRAY,
                 bg=bg, wraplength=110, justify="center"
                 ).place(relx=0.5, rely=0.42, anchor="center")
        tk.Label(tile, text=f"${p['price']:.2f}", font=("Courier", 10),
                 fg=GREEN if not is_empty else TEXT_GRAY, bg=bg
                 ).place(relx=0.5, rely=0.75, anchor="center")

        if is_empty:
            tk.Label(tile, text="SOLD OUT", font=("Courier", 7, "bold"),
                     fg=RED, bg=bg).place(relx=0.5, rely=0.9, anchor="center")
        else:
            tk.Label(tile, text=f"Qty: {p['count']}", font=("Courier", 7),
                     fg=TEXT_GRAY, bg=bg).place(relx=0.95, rely=0.96, anchor="se")
            tile.bind("<Button-1>", lambda e, prod=p: self._select(prod))
            for w in tile.winfo_children():
                w.bind("<Button-1>", lambda e, prod=p: self._select(prod))
            tile.bind("<Enter>", lambda e, t=tile, b=bg: t.configure(bg=ACCENT) if not is_empty else None)
            tile.bind("<Leave>", lambda e, t=tile, b=bg: t.configure(bg=b))

    # ── Sale panel (right side) ──────────────────────────────────
    def _sale_panel(self, parent):
        # Selected item display
        tk.Label(parent, text="Order Summary", font=("Courier", 11, "bold"),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w")

        self.summary_frame = tk.Frame(parent, bg=BG_PANEL, width=280, height=110)
        self.summary_frame.pack(fill="x", pady=(4, 12))
        self.summary_frame.pack_propagate(False)
        self._refresh_summary()

        # Payment method
        tk.Label(parent, text="Payment Method", font=("Courier", 11, "bold"),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w")
        pf = tk.Frame(parent, bg=BG_DARK)
        pf.pack(fill="x", pady=(4, 12))
        for val, label in [("cash", "💵 Cash"), ("card", "💳 Card")]:
            rb = tk.Radiobutton(pf, text=label, variable=self.payment,
                                value=val, font=("Courier", 10),
                                fg=TEXT_WHITE, bg=BG_DARK, selectcolor=BG_CARD,
                                activebackground=BG_DARK, activeforeground=TEXT_WHITE,
                                command=self._refresh_payment)
            rb.pack(side="left", padx=8)

        # Cash entry (shown when cash selected)
        self.cash_frame = tk.Frame(parent, bg=BG_DARK)
        self.cash_frame.pack(fill="x", pady=(0, 8))
        tk.Label(self.cash_frame, text="Cash Given ($)", font=("Courier", 10),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w")
        self.cash_entry = tk.Entry(self.cash_frame, textvariable=self.cash_given,
                                   font=("Courier", 12), bg=BG_CARD,
                                   fg=TEXT_WHITE, insertbackground=TEXT_WHITE, bd=0)
        self.cash_entry.pack(fill="x", ipady=6, pady=2)

        # Card number (shown when card selected)
        self.card_frame = tk.Frame(parent, bg=BG_DARK)
        tk.Label(self.card_frame, text="Card Number (last 4)", font=("Courier", 10),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w")
        self.card_entry = tk.Entry(self.card_frame, font=("Courier", 12),
                                   bg=BG_CARD, fg=TEXT_WHITE,
                                   insertbackground=TEXT_WHITE, bd=0)
        self.card_entry.pack(fill="x", ipady=6, pady=2)
        self._refresh_payment()

        # Process button
        self.process_btn = tk.Button(parent, text="PROCESS SALE ▶",
                                     font=("Courier", 12, "bold"),
                                     bg=ACCENT, fg=TEXT_WHITE, bd=0,
                                     activebackground=BTN_HOVER,
                                     cursor="hand2", pady=12,
                                     command=self._process_sale)
        self.process_btn.pack(fill="x", pady=(10, 0))

        # Receipt area
        self.receipt_label = tk.Label(parent, text="", font=("Courier", 9),
                                      fg=GREEN, bg=BG_DARK, justify="left",
                                      wraplength=270)
        self.receipt_label.pack(anchor="w", pady=(10, 0))

    def _refresh_summary(self):
        for w in self.summary_frame.winfo_children():
            w.destroy()
        if not self.selected:
            tk.Label(self.summary_frame, text="No product selected",
                     font=("Courier", 10), fg=TEXT_GRAY, bg=BG_PANEL
                     ).pack(expand=True)
        else:
            p = self.selected
            tax = round(p["price"] * 0.095, 2)
            total = round(p["price"] + tax, 2)
            for label, val in [
                ("Product:", p["name"]),
                ("Code:",    p["code"]),
                ("Price:",   f"${p['price']:.2f}"),
                ("Tax:",     f"${tax:.2f}"),
                ("TOTAL:",   f"${total:.2f}"),
            ]:
                row = tk.Frame(self.summary_frame, bg=BG_PANEL)
                row.pack(fill="x", padx=10, pady=1)
                tk.Label(row, text=label, font=("Courier", 9), fg=TEXT_GRAY,
                         bg=BG_PANEL, width=10, anchor="w").pack(side="left")
                tk.Label(row, text=val,
                         font=("Courier", 9, "bold" if label == "TOTAL:" else "normal"),
                         fg=ACCENT2 if label == "TOTAL:" else TEXT_WHITE,
                         bg=BG_PANEL).pack(side="left")

    def _refresh_payment(self):
        if self.payment.get() == "cash":
            self.cash_frame.pack(fill="x", pady=(0, 8))
            self.card_frame.pack_forget()
        else:
            self.card_frame.pack(fill="x", pady=(0, 8))
            self.cash_frame.pack_forget()

    def _select(self, prod):
        self.selected = prod
        self.receipt_label.configure(text="")
        self._refresh_summary()

    def _process_sale(self):
        if not self.selected:
            messagebox.showwarning("No Selection", "Please select a product first.")
            return
        p = self.selected
        tax   = round(p["price"] * 0.095, 2)
        total = round(p["price"] + tax, 2)

        if self.payment.get() == "cash":
            given = self.cash_given.get()
            if given < total:
                messagebox.showerror("Insufficient Funds",
                                     f"Cash given ${given:.2f} is less than total ${total:.2f}.")
                return
            change = round(given - total, 2)
            receipt_extra = f"Cash Given:  ${given:.2f}\nChange:      ${change:.2f}"
        else:
            last4 = self.card_entry.get().strip()
            if not last4.isdigit() or len(last4) != 4:
                messagebox.showerror("Card Error", "Enter valid last 4 digits of card.")
                return
            receipt_extra = f"Card:        xxxx-{last4}\nCard Fee:    $0.00"

        # Deduct stock
        p["count"] -= 1

        sale_num = f"TXN-{datetime.now().strftime('%H%M%S')}"
        receipt = (
            f"✅ SALE APPROVED\n"
            f"{'─'*32}\n"
            f"Sale #:      {sale_num}\n"
            f"Product:     {p['name']} ({p['code']})\n"
            f"Price:       ${p['price']:.2f}\n"
            f"Tax:         ${tax:.2f}\n"
            f"Total:       ${total:.2f}\n"
            f"{receipt_extra}\n"
            f"{'─'*32}\n"
            f"Time: {datetime.now().strftime('%H:%M:%S')}\n"
            f"Thank you!"
        )
        self.receipt_label.configure(text=receipt)
        self.selected = None
        self._refresh_summary()


# ═══════════════════════════════════════════════════════════════
class UpdateInventoryScreen(tk.Frame):
    """Use Case 2 – Update Inventory"""

    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self.restock_vars = {}
        self._build()

    def _build(self):
        self._header()
        self._worker_bar()
        self._table()
        self._footer()

    def _header(self):
        hdr = tk.Frame(self, bg=BG_PANEL)
        hdr.pack(fill="x")
        tk.Button(hdr, text="← Back", font=("Courier", 10),
                  bg=BG_PANEL, fg=TEXT_GRAY, bd=0, cursor="hand2",
                  command=self.master.show_home).pack(side="left", padx=14, pady=14)
        tk.Label(hdr, text="📦  UPDATE INVENTORY",
                 font=("Courier", 16, "bold"), fg=ACCENT, bg=BG_PANEL
                 ).pack(side="left", padx=4, pady=14)
        tk.Label(hdr, text=f"Machine: VM-001",
                 font=("Courier", 10), fg=TEXT_GRAY, bg=BG_PANEL
                 ).pack(side="right", padx=20)

    def _worker_bar(self):
        bar = tk.Frame(self, bg=BG_CARD, height=36)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Label(bar, text=f"👷 Restocker: {WORKER_ID}   |   "
                            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                 font=("Courier", 10), fg=ACCENT2, bg=BG_CARD
                 ).pack(side="left", padx=16, pady=8)

    def _table(self):
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True, padx=16, pady=10)

        # Column headers
        headers = ["Slot", "Product Name", "Current", "Max", "Add Qty", "Status"]
        widths   = [6, 20, 9, 6, 9, 10]
        hdr_row = tk.Frame(container, bg=BG_CARD, height=32)
        hdr_row.pack(fill="x")
        hdr_row.pack_propagate(False)
        for h, w in zip(headers, widths):
            tk.Label(hdr_row, text=h, font=("Courier", 9, "bold"),
                     fg=ACCENT2, bg=BG_CARD, width=w, anchor="w"
                     ).pack(side="left", padx=6, pady=6)

        # Simple frame rows (no canvas)
        for i, p in enumerate(PRODUCTS):
            self._table_row(container, p, i)

    def _table_row(self, parent, p, idx):
        bg = BG_PANEL if idx % 2 == 0 else BG_DARK
        pct = p["count"] / p["max"]
        status_color = GREEN if pct > 0.4 else (ACCENT2 if pct > 0 else RED)
        status_text  = "OK" if pct > 0.4 else ("LOW" if pct > 0 else "EMPTY")

        row = tk.Frame(parent, bg=bg, height=40)
        row.pack(fill="x")
        row.pack_propagate(False)

        # Bar background inside row
        bar_w = int(pct * 60)
        if bar_w > 0:
            bar = tk.Frame(row, bg=status_color, width=bar_w, height=2)
            bar.place(x=0, y=38)

        data = [p["code"], p["name"], str(p["count"]), str(p["max"])]
        widths = [6, 20, 9, 6]
        for val, w in zip(data, widths):
            tk.Label(row, text=val, font=("Courier", 10),
                     fg=TEXT_WHITE, bg=bg, width=w, anchor="w"
                     ).pack(side="left", padx=6)

        # Qty entry
        var = tk.IntVar(value=0)
        self.restock_vars[p["code"]] = var
        entry = tk.Entry(row, textvariable=var, font=("Courier", 10),
                         bg=BG_CARD, fg=TEXT_WHITE, insertbackground=TEXT_WHITE,
                         bd=0, width=5)
        entry.pack(side="left", padx=6, ipady=3)

        tk.Label(row, text=status_text, font=("Courier", 9, "bold"),
                 fg=status_color, bg=bg, width=10, anchor="w"
                 ).pack(side="left", padx=6)

    def _footer(self):
        footer = tk.Frame(self, bg=BG_PANEL, height=60)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        tk.Button(footer, text="APPLY RESTOCK ▶",
                  font=("Courier", 12, "bold"),
                  bg=ACCENT, fg=TEXT_WHITE, bd=0, cursor="hand2",
                  activebackground=BTN_HOVER, padx=20,
                  command=self._apply_restock
                  ).pack(side="right", padx=20, pady=12)

        self.status_label = tk.Label(footer, text="", font=("Courier", 10),
                                     fg=GREEN, bg=BG_PANEL)
        self.status_label.pack(side="left", padx=20, pady=12)

    def _apply_restock(self):
        updated = []
        errors  = []
        for p in PRODUCTS:
            add = self.restock_vars[p["code"]].get()
            if add < 0:
                errors.append(f"{p['code']}: negative quantity")
                continue
            if add == 0:
                continue
            new_count = p["count"] + add
            if new_count > p["max"]:
                errors.append(f"{p['code']}: exceeds max ({p['max']})")
                continue
            p["count"] = new_count
            updated.append(f"{p['code']} → {new_count}/{p['max']}")
            self.restock_vars[p["code"]].set(0)

        if errors:
            messagebox.showerror("Restock Errors", "\n".join(errors))
            return

        if not updated:
            self.status_label.configure(text="No changes made.", fg=TEXT_GRAY)
            return

        log_id = f"RST-{datetime.now().strftime('%H%M%S')}"
        self.status_label.configure(
            text=f"✅ Restock {log_id} applied: {len(updated)} slot(s) updated.", fg=GREEN)

        # Refresh table
        self.destroy()
        self.master.show_inventory()


# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = VendingMachineApp()
    app.mainloop()
