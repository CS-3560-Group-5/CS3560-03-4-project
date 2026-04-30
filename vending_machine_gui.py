import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Connect to database
import db_connection
# ----

# ── Color palette ──────────────────────────────────────────────
# Clean, modern light theme — neutral tones with a blue accent
BG_MAIN    = "#f5f6fa"   # Main background — off-white
BG_WHITE   = "#ffffff"   # Pure white for cards and panels
BG_SIDEBAR = "#f0f2f8"   # Slightly tinted background for sidebars/rows
ACCENT     = "#3b5bdb"   # Primary blue accent — buttons, headers
ACCENT_HOV = "#2f4ac0"   # Darker blue on hover
ACCENT_LT  = "#dbe4ff"   # Light blue tint for selected/highlighted states
TEXT_DARK  = "#1a1a2e"   # Primary text — near black
TEXT_MID   = "#4a5568"   # Secondary text — medium gray
TEXT_LIGHT = "#a0aec0"   # Muted/placeholder text
GREEN      = "#2f9e44"   # Success green
GREEN_BG   = "#ebfbee"   # Light green background for success banners
RED        = "#c92a2a"   # Error/sold-out red
RED_BG     = "#fff5f5"   # Light red background
ORANGE     = "#e67700"   # Warning orange for LOW status
ORANGE_BG  = "#fff9db"   # Light orange background
BORDER     = "#dee2f0"   # Subtle border color for cards and separators


# ── Helper: standard labeled input field ───────────────────────
def labeled_entry(parent, label_text, var=None, height=None, bg=BG_WHITE):
    """Creates a label + entry pair. If height is given, returns a Text widget."""
    tk.Label(parent, text=label_text, font=("Segoe UI", 10, "bold"),
             fg=TEXT_MID, bg=bg).pack(anchor="w", pady=(10, 2))
    if height:
        widget = tk.Text(parent, font=("Segoe UI", 10), bg=BG_SIDEBAR,
                         fg=TEXT_DARK, insertbackground=TEXT_DARK,
                         relief="flat", bd=0, height=height, wrap="word",
                         highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=ACCENT)
        widget.pack(fill="x", ipady=6)
        return widget
    else:
        entry = tk.Entry(parent, textvariable=var, font=("Segoe UI", 11),
                         bg=BG_SIDEBAR, fg=TEXT_DARK, insertbackground=TEXT_DARK,
                         relief="flat", bd=0,
                         highlightthickness=1, highlightbackground=BORDER,
                         highlightcolor=ACCENT)
        entry.pack(fill="x", ipady=7)
        return entry


# ── Helper: primary action button ──────────────────────────────
def action_button(parent, text, command):
    """Creates a styled full-width primary button with hover effect."""
    btn = tk.Button(parent, text=text, font=("Segoe UI", 11, "bold"),
                    bg=ACCENT, fg=BG_WHITE, activebackground=ACCENT_HOV,
                    activeforeground=BG_WHITE, relief="flat", bd=0,
                    cursor="hand2", pady=11, command=command)
    btn.pack(fill="x", pady=(16, 0))
    btn.bind("<Enter>", lambda e: btn.configure(bg=ACCENT_HOV))
    btn.bind("<Leave>", lambda e: btn.configure(bg=ACCENT))
    return btn


# ── Helper: standard screen header bar ─────────────────────────
def screen_header(parent, title, back_cmd, machine_info=None):
    """Builds a consistent white top header bar for all non-home screens."""
    hdr = tk.Frame(parent, bg=BG_WHITE, height=64)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")

    back = tk.Button(hdr, text="←  Back", font=("Segoe UI", 10),
                     bg=BG_WHITE, fg=ACCENT, activebackground=ACCENT_LT,
                     activeforeground=ACCENT, relief="flat", bd=0,
                     cursor="hand2", padx=10, command=back_cmd)
    back.pack(side="left", padx=16, pady=14)

    tk.Label(hdr, text=title, font=("Segoe UI", 14, "bold"),
             fg=TEXT_DARK, bg=BG_WHITE).pack(side="left", padx=8, pady=14)

    if machine_info:
        model = machine_info.get("ModelNumber", "N/A")
        tk.Label(hdr, text=f"Machine: {model}", font=("Segoe UI", 9),
                 fg=TEXT_LIGHT, bg=BG_WHITE).pack(side="right", padx=20)


# ═══════════════════════════════════════════════════════════════
# Main application class — manages the window and screen navigation
# ═══════════════════════════════════════════════════════════════
class VendingMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine System")
        self.geometry("940x700")
        self.resizable(False, False)
        self.configure(bg=BG_MAIN)
        self.current_frame = None

        # Load machine info from the database on startup
        try:
            self.machine_info = db_connection.get_machine_info()
            self.machine_id   = self.machine_info["MachineID"]
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not connect to database:\n{e}")
            self.machine_info = None
            self.machine_id   = 1
        # ----

        self.show_home()

    def switch_frame(self, FrameClass, **kwargs):
        """Destroys the current screen and replaces it with a new one."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = FrameClass(self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    # Navigation methods — called by buttons throughout the UI
    def show_home(self):                self.switch_frame(HomeScreen)
    def show_record_sale(self):         self.switch_frame(RecordSaleScreen)
    def show_inventory(self):           self.switch_frame(UpdateInventoryScreen)
    def show_maintenance_request(self): self.switch_frame(MaintenanceRequestScreen)
    def show_maintenance_tickets(self): self.switch_frame(MaintenanceTicketsScreen)
    def show_cash_level(self):          self.switch_frame(UpdateCashLevelScreen)
    def show_machine_info(self):        self.switch_frame(UpdateMachineInfoScreen)


# ═══════════════════════════════════════════════════════════════
# Home Screen — main menu with grouped action cards
# ═══════════════════════════════════════════════════════════════
class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self._build()

    def _build(self):
        # Top header bar
        hdr = tk.Frame(self, bg=BG_WHITE, height=72)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        tk.Label(hdr, text="🏪  Vending Machine System",
                 font=("Segoe UI", 18, "bold"), fg=TEXT_DARK, bg=BG_WHITE
                 ).pack(side="left", padx=28, pady=18)

        machine   = self.master.machine_info
        info_text = (f"{machine['ModelNumber']}  ·  {datetime.now().strftime('%B %d, %Y')}"
                     if machine else datetime.now().strftime('%B %d, %Y'))
        tk.Label(hdr, text=info_text, font=("Segoe UI", 10),
                 fg=TEXT_LIGHT, bg=BG_WHITE).pack(side="right", padx=28)

        # Body
        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(expand=True)

        tk.Label(body, text="What would you like to do?",
                 font=("Segoe UI", 13), fg=TEXT_MID, bg=BG_MAIN
                 ).pack(pady=(32, 18))

        # Customer section
        self._section(body, "Customer")
        self._card(body, "💳", "Record Sale",
                   "Customer purchases a product",
                   self.master.show_record_sale)

        # Restocker section
        self._section(body, "Restocker")
        self._card(body, "📦", "Update Inventory",
                   "View and restock machine slots",
                   self.master.show_inventory)
        self._card(body, "💵", "Update Cash Level",
                   "Collect cash or refill coins",
                   self.master.show_cash_level)

        # Technician / Admin section
        self._section(body, "Technician / Admin")
        self._card(body, "🔧", "Report Maintenance Issue",
                   "Log a malfunction or request service",
                   self.master.show_maintenance_request)
        self._card(body, "✅", "Close Maintenance Ticket",
                   "Technician marks a repair as complete",
                   self.master.show_maintenance_tickets)
        self._card(body, "⚙️", "Machine Information",
                   "Admin updates the machine profile",
                   self.master.show_machine_info)

    def _section(self, parent, label):
        """Small uppercase section label with a horizontal divider line."""
        row = tk.Frame(parent, bg=BG_MAIN)
        row.pack(fill="x", padx=60, pady=(14, 4))
        tk.Label(row, text=label.upper(), font=("Segoe UI", 8, "bold"),
                 fg=TEXT_LIGHT, bg=BG_MAIN).pack(side="left")
        tk.Frame(row, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(10, 0), pady=6)

    def _card(self, parent, icon, title, subtitle, cmd):
        """White card button with icon badge, title, subtitle, and hover highlight."""
        card = tk.Frame(parent, bg=BG_WHITE, cursor="hand2",
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", padx=60, pady=3, ipady=4)

        # Icon badge
        icon_lbl = tk.Label(card, text=icon, font=("Segoe UI", 15),
                             bg=ACCENT_LT, width=3, pady=6)
        icon_lbl.pack(side="left", padx=(14, 12), pady=8)

        # Text block
        text_blk = tk.Frame(card, bg=BG_WHITE)
        text_blk.pack(side="left", fill="x", expand=True, pady=8)
        tk.Label(text_blk, text=title, font=("Segoe UI", 11, "bold"),
                 fg=TEXT_DARK, bg=BG_WHITE, anchor="w").pack(fill="x")
        tk.Label(text_blk, text=subtitle, font=("Segoe UI", 9),
                 fg=TEXT_LIGHT, bg=BG_WHITE, anchor="w").pack(fill="x")

        # Chevron
        chev = tk.Label(card, text="›", font=("Segoe UI", 18),
                        fg=TEXT_LIGHT, bg=BG_WHITE)
        chev.pack(side="right", padx=16)

        # Hover effect — highlights entire card blue-tinted
        def on_enter(e):
            card.configure(bg=ACCENT_LT, highlightbackground=ACCENT)
            icon_lbl.configure(bg=ACCENT_LT)
            text_blk.configure(bg=ACCENT_LT)
            chev.configure(bg=ACCENT_LT, fg=ACCENT)
            for w in text_blk.winfo_children():
                w.configure(bg=ACCENT_LT)

        def on_leave(e):
            card.configure(bg=BG_WHITE, highlightbackground=BORDER)
            icon_lbl.configure(bg=ACCENT_LT)
            text_blk.configure(bg=BG_WHITE)
            chev.configure(bg=BG_WHITE, fg=TEXT_LIGHT)
            for w in text_blk.winfo_children():
                w.configure(bg=BG_WHITE)

        for w in [card, icon_lbl, text_blk, chev] + text_blk.winfo_children():
            w.bind("<Button-1>", lambda e: cmd())
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)


# ═══════════════════════════════════════════════════════════════
# Use Case 1: Record Sale Screen
# Customer selects a product and completes a cash or card payment.
# System side effects: inventory is decremented; a restock request
# is auto-generated if the slot falls below its threshold.
# ═══════════════════════════════════════════════════════════════
class RecordSaleScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self.selected   = None
        self.payment    = tk.StringVar(value="cash")
        self.cash_given = tk.DoubleVar()

        # Load all slot and product data from the database
        try:
            self.products = db_connection.get_all_products_with_slots()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load products:\n{e}")
            self.products = []

        self._build()

    def _build(self):
        screen_header(self, "💳  Record Sale",
                      self.master.show_home, self.master.machine_info)

        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=16)

        # Left: product grid  |  Right: order + payment panel
        left = tk.Frame(main, bg=BG_MAIN)
        right = tk.Frame(main, bg=BG_WHITE, width=290,
                         highlightthickness=1, highlightbackground=BORDER)
        left.pack(side="left", fill="both", expand=True, padx=(0, 16))
        right.pack(side="right", fill="y")

        self._product_grid(left)
        self._sale_panel(right)

    def _product_grid(self, parent):
        tk.Label(parent, text="Select a product",
                 font=("Segoe UI", 11, "bold"), fg=TEXT_MID, bg=BG_MAIN
                 ).pack(anchor="w", pady=(0, 10))

        grid = tk.Frame(parent, bg=BG_MAIN)
        grid.pack(fill="both", expand=True)

        for i, p in enumerate(self.products):
            r, c = divmod(i, 4)
            self._product_tile(grid, p, r, c)
        for c in range(4):
            grid.grid_columnconfigure(c, weight=1)

    def _product_tile(self, parent, p, row, col):
        """White tile showing slot code, name, price, and stock. Muted if sold out."""
        is_empty = p["count"] == 0 or p["name"] == "Empty"

        tile = tk.Frame(parent, bg=BG_WHITE, width=140, height=108,
                        highlightthickness=1,
                        highlightbackground=BORDER if not is_empty else "#e2e8f0")
        tile.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        tile.grid_propagate(False)

        # Slot code badge
        tk.Label(tile, text=p["code"], font=("Segoe UI", 8, "bold"),
                 fg=ACCENT if not is_empty else TEXT_LIGHT,
                 bg=ACCENT_LT if not is_empty else BG_SIDEBAR,
                 padx=6, pady=2).place(x=6, y=6)

        # Product name
        tk.Label(tile, text=p["name"], font=("Segoe UI", 9, "bold"),
                 fg=TEXT_DARK if not is_empty else TEXT_LIGHT,
                 bg=BG_WHITE, wraplength=118, justify="center"
                 ).place(relx=0.5, rely=0.46, anchor="center")

        if is_empty:
            label = "EMPTY" if p["name"] == "Empty" else "SOLD OUT"
            tk.Label(tile, text=label, font=("Segoe UI", 7, "bold"),
                     fg=RED, bg=BG_WHITE).place(relx=0.5, rely=0.85, anchor="center")
        else:
            # Price and quantity
            tk.Label(tile, text=f"${p['price']:.2f}", font=("Segoe UI", 10, "bold"),
                     fg=GREEN, bg=BG_WHITE).place(relx=0.5, rely=0.72, anchor="center")
            tk.Label(tile, text=f"Qty: {p['count']}", font=("Segoe UI", 7),
                     fg=TEXT_LIGHT, bg=BG_WHITE).place(relx=0.95, rely=0.95, anchor="se")

            # Hover and click bindings for selectable tiles
            def on_enter(e, t=tile):
                t.configure(highlightbackground=ACCENT, bg=ACCENT_LT)
                for w in t.winfo_children():
                    w.configure(bg=ACCENT_LT)
            def on_leave(e, t=tile):
                t.configure(highlightbackground=BORDER, bg=BG_WHITE)
                for w in t.winfo_children():
                    w.configure(bg=BG_WHITE)

            tile.bind("<Enter>",    on_enter)
            tile.bind("<Leave>",    on_leave)
            tile.bind("<Button-1>", lambda e, prod=p: self._select(prod))
            for w in tile.winfo_children():
                w.bind("<Enter>",    on_enter)
                w.bind("<Leave>",    on_leave)
                w.bind("<Button-1>", lambda e, prod=p: self._select(prod))

    def _sale_panel(self, parent):
        """Right panel: order summary, payment method selector, and process button."""
        pad = tk.Frame(parent, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=20, pady=20)

        # Order summary
        tk.Label(pad, text="Order Summary", font=("Segoe UI", 11, "bold"),
                 fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(4, 10))

        self.summary_frame = tk.Frame(pad, bg=BG_SIDEBAR,
                                      highlightthickness=1, highlightbackground=BORDER)
        self.summary_frame.pack(fill="x", pady=(0, 16))
        self._refresh_summary()

        # Payment method radio buttons
        tk.Label(pad, text="Payment Method", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w")
        pf = tk.Frame(pad, bg=BG_WHITE)
        pf.pack(fill="x", pady=(6, 12))
        for val, label in [("cash", "💵  Cash"), ("card", "💳  Card")]:
            tk.Radiobutton(pf, text=label, variable=self.payment, value=val,
                           font=("Segoe UI", 10), fg=TEXT_DARK, bg=BG_WHITE,
                           selectcolor=ACCENT_LT, activebackground=BG_WHITE,
                           command=self._refresh_payment).pack(side="left", padx=(0, 16))

        # Cash input field
        self.cash_frame = tk.Frame(pad, bg=BG_WHITE)
        self.cash_frame.pack(fill="x")
        tk.Label(self.cash_frame, text="Cash Given ($)", font=("Segoe UI", 9),
                 fg=TEXT_LIGHT, bg=BG_WHITE).pack(anchor="w")
        self.cash_entry = tk.Entry(self.cash_frame, textvariable=self.cash_given,
                                   font=("Segoe UI", 11), bg=BG_SIDEBAR, fg=TEXT_DARK,
                                   insertbackground=TEXT_DARK, relief="flat", bd=0,
                                   highlightthickness=1, highlightbackground=BORDER,
                                   highlightcolor=ACCENT)
        self.cash_entry.pack(fill="x", ipady=7, pady=(2, 0))

        # Card input field
        self.card_frame = tk.Frame(pad, bg=BG_WHITE)
        tk.Label(self.card_frame, text="Card Number (last 4)", font=("Segoe UI", 9),
                 fg=TEXT_LIGHT, bg=BG_WHITE).pack(anchor="w")
        self.card_entry = tk.Entry(self.card_frame, font=("Segoe UI", 11),
                                   bg=BG_SIDEBAR, fg=TEXT_DARK,
                                   insertbackground=TEXT_DARK, relief="flat", bd=0,
                                   highlightthickness=1, highlightbackground=BORDER,
                                   highlightcolor=ACCENT)
        self.card_entry.pack(fill="x", ipady=7, pady=(2, 0))
        self._refresh_payment()

        action_button(pad, "Process Sale  ▶", self._process_sale)

        # Receipt area — shown after a successful sale
        self.receipt_frame = tk.Frame(pad, bg=GREEN_BG,
                                      highlightthickness=1, highlightbackground=GREEN)
        self.receipt_label = tk.Label(self.receipt_frame, text="",
                                      font=("Segoe UI", 9), fg=GREEN,
                                      bg=GREEN_BG, justify="left", wraplength=240)
        self.receipt_label.pack(padx=12, pady=10, anchor="w")

    def _refresh_summary(self):
        """Rebuilds the order summary panel based on the currently selected product."""
        for w in self.summary_frame.winfo_children():
            w.destroy()

        if not self.selected:
            tk.Label(self.summary_frame, text="No product selected",
                     font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_SIDEBAR
                     ).pack(pady=14)
        else:
            p     = self.selected
            tax   = round(p["price"] * 0.095, 2)
            total = round(p["price"] + tax, 2)
            for label, val, bold in [
                ("Product", p["name"],           False),
                ("Code",    p["code"],            False),
                ("Price",   f"${p['price']:.2f}", False),
                ("Tax",     f"${tax:.2f}",         False),
                ("Total",   f"${total:.2f}",       True),
            ]:
                row = tk.Frame(self.summary_frame, bg=BG_SIDEBAR)
                row.pack(fill="x", padx=12, pady=2)
                tk.Label(row, text=label, font=("Segoe UI", 9),
                         fg=TEXT_LIGHT, bg=BG_SIDEBAR, width=8, anchor="w").pack(side="left")
                tk.Label(row, text=val,
                         font=("Segoe UI", 10, "bold" if bold else "normal"),
                         fg=ACCENT if bold else TEXT_DARK,
                         bg=BG_SIDEBAR).pack(side="left")
            tk.Frame(self.summary_frame, bg=BG_SIDEBAR, height=6).pack()

    def _refresh_payment(self):
        """Swaps between the cash and card input field based on the selected method."""
        if self.payment.get() == "cash":
            self.cash_frame.pack(fill="x", pady=(8, 0))
            self.card_frame.pack_forget()
        else:
            self.card_frame.pack(fill="x", pady=(8, 0))
            self.cash_frame.pack_forget()

    def _select(self, prod):
        """Stores the selected product and refreshes the order summary."""
        self.selected = prod
        self.receipt_frame.pack_forget()
        self.receipt_label.configure(text="")
        self._refresh_summary()

    def _process_sale(self):
        """Validates payment and processes the sale. Shows a receipt on success.
        System side effects: slot count is decremented; a restock request is
        auto-generated if stock falls at or below the slot's restock threshold."""
        if not self.selected:
            messagebox.showwarning("No Selection", "Please select a product first.")
            return

        p     = self.selected
        tax   = round(p["price"] * 0.095, 2)
        total = round(p["price"] + tax, 2)

        if self.payment.get() == "cash":
            given = self.cash_given.get()
            if given < total:
                messagebox.showerror("Insufficient Funds",
                                     f"Cash ${given:.2f} is less than total ${total:.2f}.")
                return
            change        = round(given - total, 2)
            receipt_extra = f"Cash Given:   ${given:.2f}\nChange:       ${change:.2f}"
        else:
            last4 = self.card_entry.get().strip()
            if not last4.isdigit() or len(last4) != 4:
                messagebox.showerror("Card Error", "Please enter valid last 4 digits.")
                return
            receipt_extra = f"Card:         xxxx-{last4}\nCard Fee:     $0.00"

        # Record transaction and update inventory in the database
        try:
            if self.payment.get() == "cash":
                sale_num = db_connection.record_cash_sale(
                    product_id=p["product_id"], machine_id=self.master.machine_id,
                    tax=tax, cash_given=self.cash_given.get())
            else:
                sale_num = db_connection.record_card_sale(
                    product_id=p["product_id"], machine_id=self.master.machine_id,
                    tax=tax, card_fee=0.00, account_charged=f"xxxx-{last4}")

            new_count = p["count"] - 1
            db_connection.update_slot_count(p["code"], new_count)
            # System-triggered: auto-generate restock request if stock is low
            db_connection.check_and_create_restock_request(p["code"])

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not record sale:\n{e}")
            return

        p["count"] = new_count

        # Display receipt in the green banner
        self.receipt_label.configure(text=(
            f"✅  Sale Approved\n{'─'*28}\n"
            f"Sale #:       TXN-{sale_num}\n"
            f"Product:      {p['name']} ({p['code']})\n"
            f"Price:        ${p['price']:.2f}\n"
            f"Tax:          ${tax:.2f}\n"
            f"Total:        ${total:.2f}\n"
            f"{receipt_extra}\n{'─'*28}\n"
            f"Time: {datetime.now().strftime('%H:%M:%S')}\nThank you!"))
        self.receipt_frame.pack(fill="x", pady=(14, 0))

        self.selected = None
        self._refresh_summary()


# ═══════════════════════════════════════════════════════════════
# Use Case 2: Update Inventory Screen
# Restocker views slot stock levels and enters quantities to add.
# System side effect: resolves any open restock requests after
# a slot is successfully restocked.
# ═══════════════════════════════════════════════════════════════
class UpdateInventoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self.restock_vars = {}  # Maps slot code → IntVar for Add Qty input

        # Load all slot data from the database
        try:
            self.products = db_connection.get_all_products_with_slots()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load inventory:\n{e}")
            self.products = []

        self._build()

    def _build(self):
        screen_header(self, "📦  Update Inventory",
                      self.master.show_home, self.master.machine_info)
        self._worker_bar()
        self._table()
        self._footer()

    def _worker_bar(self):
        """Thin blue banner showing the logged-in restocker and current date/time."""
        bar = tk.Frame(self, bg=ACCENT_LT, height=38)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        try:
            workers     = db_connection.get_service_workers()
            worker_name = workers[0]["Name"]     if workers else "Unknown"
            worker_id   = workers[0]["WorkerID"] if workers else "N/A"
        except Exception:
            worker_name = "Unknown"
            worker_id   = "N/A"

        tk.Label(bar,
                 text=f"👷  {worker_name}  (ID: {worker_id})     {datetime.now().strftime('%A, %B %d  %H:%M')}",
                 font=("Segoe UI", 9), fg=ACCENT, bg=ACCENT_LT
                 ).pack(side="left", padx=20, pady=10)

    def _table(self):
        """Scrollable inventory table with a colored header row and alternating rows."""
        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=20, pady=14)

        # Header row
        hdr = tk.Frame(container, bg=ACCENT, height=34)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        for h, w in zip(["Slot", "Product", "Current", "Max", "Add Qty", "Status"],
                        [6,       22,         9,         7,     9,          10]):
            tk.Label(hdr, text=h, font=("Segoe UI", 9, "bold"),
                     fg=BG_WHITE, bg=ACCENT, width=w, anchor="w"
                     ).pack(side="left", padx=10, pady=8)

        # One row per slot
        for i, p in enumerate(self.products):
            self._table_row(container, p, i)

    def _table_row(self, parent, p, idx):
        """Single inventory row with alternating background and color-coded status badge."""
        bg = BG_WHITE if idx % 2 == 0 else BG_SIDEBAR

        max_amt = p["max"] if p["max"] else 1
        pct     = p["count"] / max_amt if max_amt > 0 else 0

        # Determine status color and text based on fill percentage
        if pct > 0.4:
            status_text, fg_s, bg_s = "OK",    GREEN,  GREEN_BG
        elif pct > 0:
            status_text, fg_s, bg_s = "LOW",   ORANGE, ORANGE_BG
        else:
            status_text, fg_s, bg_s = "EMPTY", RED,    RED_BG

        row = tk.Frame(parent, bg=bg, height=38)
        row.pack(fill="x")
        row.pack_propagate(False)

        # Static columns: slot code, name, current count, max capacity
        for val, w in zip([p["code"], p["name"], str(p["count"]), str(p["max"])],
                          [6,         22,         9,               7]):
            tk.Label(row, text=val, font=("Segoe UI", 10),
                     fg=TEXT_DARK, bg=bg, width=w, anchor="w"
                     ).pack(side="left", padx=10)

        # Add Qty entry field — restocker types how many to add
        var = tk.IntVar(value=0)
        self.restock_vars[p["code"]] = var
        tk.Entry(row, textvariable=var, font=("Segoe UI", 10),
                 bg=BG_MAIN, fg=TEXT_DARK, insertbackground=TEXT_DARK,
                 relief="flat", bd=0, width=5,
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT).pack(side="left", padx=10, ipady=3)

        # Color-coded status badge
        tk.Label(row, text=f"  {status_text}  ",
                 font=("Segoe UI", 8, "bold"),
                 fg=fg_s, bg=bg_s, padx=4, pady=2).pack(side="left", padx=6)

    def _footer(self):
        """Bottom action bar with Apply Restock button and status message."""
        footer = tk.Frame(self, bg=BG_WHITE, height=62,
                          highlightthickness=1, highlightbackground=BORDER)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        btn = tk.Button(footer, text="Apply Restock  ▶",
                        font=("Segoe UI", 11, "bold"),
                        bg=ACCENT, fg=BG_WHITE, activebackground=ACCENT_HOV,
                        activeforeground=BG_WHITE, relief="flat", bd=0,
                        cursor="hand2", padx=24, command=self._apply_restock)
        btn.pack(side="right", padx=20, pady=12)
        btn.bind("<Enter>", lambda e: btn.configure(bg=ACCENT_HOV))
        btn.bind("<Leave>", lambda e: btn.configure(bg=ACCENT))

        self.status_label = tk.Label(footer, text="", font=("Segoe UI", 10),
                                     fg=GREEN, bg=BG_WHITE)
        self.status_label.pack(side="left", padx=20)

    def _apply_restock(self):
        """Validates all Add Qty inputs and writes valid updates to the database.
        System side effect: resolves open restock requests for restocked slots."""
        updated, errors = [], []

        for p in self.products:
            add = self.restock_vars[p["code"]].get()
            if add == 0:
                continue
            if add < 0:
                errors.append(f"{p['code']}: negative quantity not allowed")
                continue
            new_count = p["count"] + add
            if new_count > p["max"]:
                errors.append(f"{p['code']}: exceeds max capacity ({p['max']})")
                continue
            try:
                db_connection.update_slot_count(p["code"], new_count)
                db_connection.resolve_restock_request(p["code"])
                updated.append(p["code"])
                self.restock_vars[p["code"]].set(0)
            except Exception as e:
                errors.append(f"{p['code']}: database error — {e}")

        if errors:
            messagebox.showerror("Restock Errors", "\n".join(errors))
            return
        if not updated:
            self.status_label.configure(text="No changes entered.", fg=TEXT_LIGHT)
            return

        self.status_label.configure(
            text=f"✅  {len(updated)} slot(s) updated successfully.", fg=GREEN)
        self.destroy()
        self.master.show_inventory()


# ═══════════════════════════════════════════════════════════════
# Use Case 3: Maintenance Request Screen
# Technician or admin reports a malfunction or schedules service.
# System side effect: machine status is set to ERROR or SCHEDULED.
# ═══════════════════════════════════════════════════════════════
class MaintenanceRequestScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self._build()

    def _build(self):
        screen_header(self, "🔧  Report Maintenance Issue",
                      self.master.show_home, self.master.machine_info)

        outer = tk.Frame(self, bg=BG_MAIN)
        outer.pack(expand=True, fill="both")
        card = tk.Frame(outer, bg=BG_WHITE,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(padx=80, pady=24, fill="both", expand=True)
        pad = tk.Frame(card, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=36, pady=28)

        tk.Label(pad, text="Submit a Maintenance Request",
                 font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Label(pad, text="Report a malfunction or schedule preventive service for this machine.",
                 font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_WHITE
                 ).pack(anchor="w", pady=(2, 20))

        # Request type selector
        tk.Label(pad, text="Request Type", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w")
        self.request_type = tk.StringVar(value="malfunction")
        rf = tk.Frame(pad, bg=BG_WHITE)
        rf.pack(anchor="w", pady=(4, 18))
        for val, label in [("malfunction", "🔴  Malfunction / Emergency"),
                            ("preventive",  "🟡  Scheduled Preventive Maintenance")]:
            tk.Radiobutton(rf, text=label, variable=self.request_type, value=val,
                           font=("Segoe UI", 10), fg=TEXT_DARK, bg=BG_WHITE,
                           selectcolor=ACCENT_LT, activebackground=BG_WHITE
                           ).pack(anchor="w", pady=3)

        # Reason text area and worker ID field
        self.reason_entry  = labeled_entry(pad, "Reason for Request", height=4, bg=BG_WHITE)
        self.worker_id_var = tk.StringVar()
        labeled_entry(pad, "Your Worker ID", var=self.worker_id_var, bg=BG_WHITE)

        action_button(pad, "Submit Request  ▶", self._submit)

        self.confirm_label = tk.Label(pad, text="", font=("Segoe UI", 9),
                                      fg=GREEN, bg=BG_WHITE,
                                      wraplength=600, justify="left")
        self.confirm_label.pack(anchor="w", pady=(14, 0))

    def _submit(self):
        """Validates form and writes a new maintenance request to the database."""
        reason    = self.reason_entry.get("1.0", "end").strip()
        worker_id = self.worker_id_var.get().strip()

        if not reason:
            messagebox.showwarning("Missing Info", "Please describe the reason for the request.")
            return
        if not worker_id:
            messagebox.showwarning("Missing Info", "Please enter your Worker ID.")
            return

        try:
            req_id = db_connection.create_maintenance_request(
                machine_id=self.master.machine_id, worker_id=worker_id,
                reason=reason,
                date_requested=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # System-triggered: update machine status based on request type
            new_status = "ERROR" if self.request_type.get() == "malfunction" else "SCHEDULED"
            db_connection.update_machine_status(self.master.machine_id, new_status)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not submit request:\n{e}")
            return

        type_label = ("Malfunction" if self.request_type.get() == "malfunction"
                      else "Preventive Maintenance")
        self.confirm_label.configure(
            text=(f"✅  Request submitted\n{'─'*34}\n"
                  f"Request ID:  MR-{req_id}\n"
                  f"Type:        {type_label}\n"
                  f"Worker ID:   {worker_id}\n"
                  f"Time:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"Status:      Pending — a technician will be assigned shortly."))
        self.reason_entry.delete("1.0", "end")
        self.worker_id_var.set("")


# ═══════════════════════════════════════════════════════════════
# Use Case 4: Close Maintenance Ticket Screen
# Technician selects an open ticket, logs service notes, and closes it.
# System side effect: machine status is restored to ONLINE.
# ═══════════════════════════════════════════════════════════════
class MaintenanceTicketsScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self.selected_ticket = None

        # Load all open (unresolved) maintenance requests for this machine
        try:
            self.tickets = db_connection.get_open_maintenance_requests(self.master.machine_id)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load tickets:\n{e}")
            self.tickets = []

        self._build()

    def _build(self):
        screen_header(self, "✅  Close Maintenance Ticket",
                      self.master.show_home, self.master.machine_info)

        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=16)

        # Left: list of open tickets  |  Right: resolution form
        left = tk.Frame(main, bg=BG_MAIN)
        right = tk.Frame(main, bg=BG_WHITE, width=320,
                         highlightthickness=1, highlightbackground=BORDER)
        left.pack(side="left", fill="both", expand=True, padx=(0, 16))
        right.pack(side="right", fill="y")

        self._ticket_list(left)
        self._resolution_form(right)

    def _ticket_list(self, parent):
        """Renders all open tickets as clickable white cards."""
        tk.Label(parent, text="Open Tickets",
                 font=("Segoe UI", 11, "bold"), fg=TEXT_MID, bg=BG_MAIN
                 ).pack(anchor="w", pady=(0, 10))

        if not self.tickets:
            ok = tk.Frame(parent, bg=GREEN_BG,
                          highlightthickness=1, highlightbackground=GREEN)
            ok.pack(fill="x")
            tk.Label(ok,
                     text="✅  No open maintenance tickets — machine is running normally.",
                     font=("Segoe UI", 10), fg=GREEN, bg=GREEN_BG
                     ).pack(padx=16, pady=14)
            return

        for t in self.tickets:
            self._ticket_card(parent, t)

    def _ticket_card(self, parent, t):
        """Single clickable ticket card showing request ID, date, and reason."""
        card = tk.Frame(parent, bg=BG_WHITE, cursor="hand2",
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", pady=4, ipady=2)

        top = tk.Frame(card, bg=BG_WHITE)
        top.pack(fill="x", padx=14, pady=(10, 2))
        tk.Label(top, text=f"MR-{t['MaintenanceRequestID']}",
                 font=("Segoe UI", 10, "bold"), fg=ACCENT, bg=BG_WHITE).pack(side="left")
        tk.Label(top, text=str(t["DateRequested"]),
                 font=("Segoe UI", 9), fg=TEXT_LIGHT, bg=BG_WHITE).pack(side="right")

        tk.Label(card, text=t["ReasonForRequest"],
                 font=("Segoe UI", 9), fg=TEXT_MID, bg=BG_WHITE,
                 wraplength=360, justify="left", anchor="w"
                 ).pack(fill="x", padx=14, pady=(0, 10))

        # Hover highlight for the entire card
        def on_enter(e, c=card):
            c.configure(bg=ACCENT_LT, highlightbackground=ACCENT)
            for w in c.winfo_children():
                w.configure(bg=ACCENT_LT)
                for ww in w.winfo_children():
                    ww.configure(bg=ACCENT_LT)

        def on_leave(e, c=card):
            c.configure(bg=BG_WHITE, highlightbackground=BORDER)
            for w in c.winfo_children():
                w.configure(bg=BG_WHITE)
                for ww in w.winfo_children():
                    ww.configure(bg=BG_WHITE)

        for w in [card] + card.winfo_children():
            w.bind("<Button-1>", lambda e, ticket=t: self._select_ticket(ticket))
            w.bind("<Enter>",    on_enter)
            w.bind("<Leave>",    on_leave)

    def _resolution_form(self, parent):
        """Right-side form where the technician logs notes and closes the ticket."""
        pad = tk.Frame(parent, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(pad, text="Close Selected Ticket",
                 font=("Segoe UI", 11, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(4, 14))

        self.selected_label = tk.Label(pad, text="No ticket selected.",
                                       font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_WHITE)
        self.selected_label.pack(anchor="w", pady=(0, 14))

        self.notes_entry = labeled_entry(pad, "Service Notes", height=4, bg=BG_WHITE)
        self.tech_id_var = tk.StringVar()
        labeled_entry(pad, "Technician ID", var=self.tech_id_var, bg=BG_WHITE)

        action_button(pad, "Close Ticket  ▶", self._close_ticket)

        self.confirm_label = tk.Label(pad, text="", font=("Segoe UI", 9),
                                      fg=GREEN, bg=BG_WHITE,
                                      wraplength=260, justify="left")
        self.confirm_label.pack(anchor="w", pady=(12, 0))

    def _select_ticket(self, ticket):
        """Stores the clicked ticket and highlights its ID in the form."""
        self.selected_ticket = ticket
        self.selected_label.configure(
            text=f"Selected: MR-{ticket['MaintenanceRequestID']}", fg=ACCENT)
        self.confirm_label.configure(text="")

    def _close_ticket(self):
        """Marks the selected ticket as resolved and restores machine status to ONLINE."""
        if not self.selected_ticket:
            messagebox.showwarning("No Ticket", "Please select a ticket to close.")
            return

        notes   = self.notes_entry.get("1.0", "end").strip()
        tech_id = self.tech_id_var.get().strip()

        if not notes:
            messagebox.showwarning("Missing Info", "Please enter service notes.")
            return
        if not tech_id:
            messagebox.showwarning("Missing Info", "Please enter your Technician ID.")
            return

        date_resolved = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            db_connection.close_maintenance_request(
                request_id=self.selected_ticket["MaintenanceRequestID"],
                date_resolved=date_resolved, notes=notes)
            # System-triggered: restore machine to ONLINE after repair is complete
            db_connection.update_machine_status(self.master.machine_id, "ONLINE")
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not close ticket:\n{e}")
            return

        self.confirm_label.configure(
            text=(f"✅  Ticket closed\n{'─'*28}\n"
                  f"Request ID:  MR-{self.selected_ticket['MaintenanceRequestID']}\n"
                  f"Technician:  {tech_id}\n"
                  f"Resolved:    {date_resolved}\n"
                  f"Machine status → ONLINE"))

        self.selected_ticket = None
        self.selected_label.configure(text="No ticket selected.", fg=TEXT_LIGHT)
        self.notes_entry.delete("1.0", "end")
        self.tech_id_var.set("")
        self.destroy()
        self.master.show_maintenance_tickets()


# ═══════════════════════════════════════════════════════════════
# Use Case 5: Update Cash Level Screen
# Restocker logs a cash collection or a coin change refill.
# System side effects: resolves open cash or change alerts.
# ═══════════════════════════════════════════════════════════════
class UpdateCashLevelScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)

        # Load money handler data from the database
        try:
            self.money_info = db_connection.get_money_handler(self.master.machine_id)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load cash data:\n{e}")
            self.money_info = None

        self._build()

    def _build(self):
        screen_header(self, "💵  Update Cash Level",
                      self.master.show_home, self.master.machine_info)

        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=16)

        # Left: current cash status  |  Right: action form
        left = tk.Frame(main, bg=BG_WHITE,
                        highlightthickness=1, highlightbackground=BORDER)
        left.pack(side="left", fill="both", expand=True, padx=(0, 16))

        right = tk.Frame(main, bg=BG_WHITE, width=340,
                         highlightthickness=1, highlightbackground=BORDER)
        right.pack(side="right", fill="y")

        self._status_panel(left)
        self._action_form(right)

    def _status_panel(self, parent):
        """Displays current MoneyHandler thresholds loaded from the database."""
        pad = tk.Frame(parent, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=28, pady=24)

        tk.Label(pad, text="Current Cash Status",
                 font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Label(pad, text="Thresholds and limits configured for this machine.",
                 font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_WHITE
                 ).pack(anchor="w", pady=(2, 18))
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(0, 16))

        if self.money_info:
            m = self.money_info
            for label, val in [
                ("Bill Max Amount",            f"${m.get('BillMaxAmount', 'N/A')}"),
                ("Bill Restock Max Threshold", f"{m.get('BillRestockMaxThreshold', 'N/A')}%"),
                ("Coin Restock Min Threshold", f"{m.get('CoinRestockMinThreshold', 'N/A')}%"),
                ("Coin Restock Max Threshold", f"{m.get('CoinRestockMaxThreshold', 'N/A')}%"),
            ]:
                row = tk.Frame(pad, bg=BG_SIDEBAR,
                               highlightthickness=1, highlightbackground=BORDER)
                row.pack(fill="x", pady=4)
                tk.Label(row, text=label, font=("Segoe UI", 10),
                         fg=TEXT_MID, bg=BG_SIDEBAR, width=28, anchor="w"
                         ).pack(side="left", padx=14, pady=10)
                tk.Label(row, text=val, font=("Segoe UI", 10, "bold"),
                         fg=TEXT_DARK, bg=BG_SIDEBAR).pack(side="right", padx=14)
        else:
            tk.Label(pad, text="Could not load cash data from database.",
                     font=("Segoe UI", 10), fg=RED, bg=BG_WHITE).pack(anchor="w")

    def _action_form(self, parent):
        """Right-side form for logging a cash collection or change refill."""
        pad = tk.Frame(parent, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(pad, text="Log an Action",
                 font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(4, 16))

        # Action type selector
        tk.Label(pad, text="Action Type", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w")
        self.action_type = tk.StringVar(value="collect")
        af = tk.Frame(pad, bg=BG_WHITE)
        af.pack(anchor="w", pady=(4, 16))
        for val, label in [("collect", "💰  Collect Cash (Bills)"),
                            ("refill",  "🪙  Refill Change (Coins)")]:
            tk.Radiobutton(af, text=label, variable=self.action_type, value=val,
                           font=("Segoe UI", 10), fg=TEXT_DARK, bg=BG_WHITE,
                           selectcolor=ACCENT_LT, activebackground=BG_WHITE
                           ).pack(anchor="w", pady=3)

        self.amount_var    = tk.DoubleVar()
        self.worker_id_var = tk.StringVar()
        labeled_entry(pad, "Amount ($)",     var=self.amount_var,    bg=BG_WHITE)
        labeled_entry(pad, "Your Worker ID", var=self.worker_id_var, bg=BG_WHITE)

        action_button(pad, "Apply Cash Update  ▶", self._apply)

        self.confirm_label = tk.Label(pad, text="", font=("Segoe UI", 9),
                                      fg=GREEN, bg=BG_WHITE,
                                      wraplength=280, justify="left")
        self.confirm_label.pack(anchor="w", pady=(12, 0))

    def _apply(self):
        """Validates input and writes the cash collection or refill to the database."""
        amount    = self.amount_var.get()
        worker_id = self.worker_id_var.get().strip()
        action    = self.action_type.get()

        if amount <= 0:
            messagebox.showwarning("Invalid Amount", "Please enter an amount greater than $0.")
            return
        if not worker_id:
            messagebox.showwarning("Missing Info", "Please enter your Worker ID.")
            return

        try:
            if action == "collect":
                db_connection.record_cash_collection(
                    machine_id=self.master.machine_id, worker_id=worker_id,
                    amount_collected=amount,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # System-triggered: resolve any active cash collection alert
                db_connection.resolve_cash_collection_alert(self.master.machine_id)
                action_label = "Cash Collected"
            else:
                db_connection.record_change_refill(
                    machine_id=self.master.machine_id, worker_id=worker_id,
                    amount_added=amount,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                # System-triggered: resolve any active change refill alert
                db_connection.resolve_change_refill_alert(self.master.machine_id)
                action_label = "Change Refilled"
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not update cash level:\n{e}")
            return

        self.confirm_label.configure(
            text=(f"✅  {action_label}\n{'─'*30}\n"
                  f"Amount:      ${amount:.2f}\n"
                  f"Worker ID:   {worker_id}\n"
                  f"Time:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
        self.amount_var.set(0.0)
        self.worker_id_var.set("")


# ═══════════════════════════════════════════════════════════════
# Use Case 6: Update Machine Information Screen
# Admin edits the machine's stored profile (address, model, etc.)
# ═══════════════════════════════════════════════════════════════
class UpdateMachineInfoScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self.machine = self.master.machine_info
        self._build()

    def _build(self):
        screen_header(self, "⚙️  Update Machine Information",
                      self.master.show_home, self.master.machine_info)

        outer = tk.Frame(self, bg=BG_MAIN)
        outer.pack(expand=True, fill="both")
        card = tk.Frame(outer, bg=BG_WHITE,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(padx=80, pady=24, fill="both", expand=True)
        pad = tk.Frame(card, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=36, pady=28)

        tk.Label(pad, text="Edit Machine Profile",
                 font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Label(pad, text="Changes are saved directly to the database.",
                 font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_WHITE
                 ).pack(anchor="w", pady=(2, 18))
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(0, 12))

        # Two-column layout for the editable fields
        cols     = tk.Frame(pad, bg=BG_WHITE)
        cols.pack(fill="x")
        left_col  = tk.Frame(cols, bg=BG_WHITE)
        right_col = tk.Frame(cols, bg=BG_WHITE)
        left_col.pack(side="left",  fill="both", expand=True, padx=(0, 20))
        right_col.pack(side="right", fill="both", expand=True)

        self.fields = {}
        m = self.machine or {}

        for display, db_key, current in [
            ("Address",           "Address",         m.get("Address", "")),
            ("Model Number",      "ModelNumber",      m.get("ModelNumber", "")),
            ("Max Product Slots", "MaxProductSlots",  str(m.get("MaxProductSlots", ""))),
        ]:
            var = tk.StringVar(value=current)
            labeled_entry(left_col, display, var=var, bg=BG_WHITE)
            self.fields[db_key] = var

        for display, db_key, current in [
            ("Days Between Services", "DaysBetweenServices", str(m.get("DaysBetweenServices", ""))),
            ("Current State",         "CurrentState",         m.get("CurrentState", "")),
        ]:
            var = tk.StringVar(value=current)
            labeled_entry(right_col, display, var=var, bg=BG_WHITE)
            self.fields[db_key] = var

        action_button(pad, "Save Changes  ▶", self._save)

        self.confirm_label = tk.Label(pad, text="", font=("Segoe UI", 9),
                                      fg=GREEN, bg=BG_WHITE,
                                      wraplength=600, justify="left")
        self.confirm_label.pack(anchor="w", pady=(12, 0))

    def _save(self):
        """Validates required fields and writes the updated machine profile to the database."""
        data = {key: var.get().strip() for key, var in self.fields.items()}

        if not data["Address"] or not data["ModelNumber"]:
            messagebox.showwarning("Missing Info", "Address and Model Number are required.")
            return

        try:
            db_connection.update_machine_info(
                machine_id=self.master.machine_id,
                address=data["Address"],
                model_number=data["ModelNumber"],
                max_slots=data["MaxProductSlots"],
                days_between_services=data["DaysBetweenServices"],
                current_state=data["CurrentState"])
            # Refresh the cached machine info so the header updates immediately
            self.master.machine_info = db_connection.get_machine_info()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save changes:\n{e}")
            return

        self.confirm_label.configure(
            text=(f"✅  Machine profile updated\n{'─'*36}\n"
                  f"Address:      {data['Address']}\n"
                  f"Model:        {data['ModelNumber']}\n"
                  f"Max Slots:    {data['MaxProductSlots']}\n"
                  f"Service Int.: {data['DaysBetweenServices']} days\n"
                  f"State:        {data['CurrentState']}\n"
                  f"Saved:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))


# ── App entry point ─────────────────────────────────────────────
if __name__ == "__main__":
    app = VendingMachineApp()
    app.mainloop()
