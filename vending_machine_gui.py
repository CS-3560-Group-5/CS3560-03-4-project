import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date, timedelta

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


# Helper function : refreshes all restock requests
def refresh_restock_requests():
        db_connection.check_and_create_currency_restock_request_ALL()   # check currency for any bills/coins that need a request
        db_connection.resolve_restock_request_currency_ALL()            # check currency for any bill/coin requests that need to be resolved
        db_connection.check_and_create_restock_request_ALL()            # check slot statuses for any slots that need a request
        db_connection.resolve_slot_restock_request_ALL()                # check slots for any that need to be resolved

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

        self._maintenance_scheduled = False
        self._check_maintenance_schedule()
        self.show_home()

    def _check_maintenance_schedule(self):
        """Runs every 60 s. Auto-creates a maintenance request if service is overdue."""
        try:
            info = db_connection.get_machine_info()
            if info and info.get("DateLastServiced") and info.get("DaysBetweenServices"):
                last = info["DateLastServiced"]
                if isinstance(last, str):
                    last = datetime.strptime(last, "%Y-%m-%d").date()
                interval = int(info["DaysBetweenServices"])
                due = last + timedelta(days=interval)
                if date.today() > due and not self._maintenance_scheduled:
                    if not db_connection.has_open_auto_maintenance(info["MachineID"]):
                        workers = db_connection.get_service_workers(info["MachineID"])
                        worker_id = workers[0]["WorkerID"] if workers else 1
                        db_connection.create_maintenance_request(
                            machine_id=info["MachineID"],
                            worker_id=worker_id,
                            reason="Auto-Scheduled Servicing",
                            date_requested=datetime.now().strftime("%Y-%m-%d"))
                        db_connection.update_machine_status(info["MachineID"], "SCHEDULED")
                    self._maintenance_scheduled = True
        except Exception:
            pass
        self.after(60000, self._check_maintenance_schedule)

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
    def show_restock_requests(self):    self.switch_frame(RestockRequestsScreen)
    def show_machine_info(self):        self.switch_frame(UpdateMachineInfoScreen)
    def show_transactions(self):        self.switch_frame(ViewTransactionsScreen)
    def show_manage_workers(self):       self.switch_frame(ManageWorkersScreen)


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

        # Scrollable body
        scroll_wrap = tk.Frame(self, bg=BG_MAIN)
        scroll_wrap.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_wrap, bg=BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_wrap, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        body = tk.Frame(canvas, bg=BG_MAIN)
        body_window = canvas.create_window((0, 0), window=body, anchor="nw")

        def _on_resize(e):
            canvas.itemconfig(body_window, width=e.width)
        canvas.bind("<Configure>", _on_resize)

        def _on_body_resize(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
        body.bind("<Configure>", _on_body_resize)

        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        self.master.bind_all("<MouseWheel>", _scroll)

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
        self._card(body, "📋", "View Restocker Requests",
                   "See open product, coin, and bill requests",
                   self.master.show_restock_requests)
        self._card(body, "💵", "Update Cash Level",
                   "Collect cash or refill coins",
                   self.master.show_cash_level)

        # Technician section
        self._section(body, "Technician")
        self._card(body, "🔧", "Report Maintenance Issue",
                   "Log a malfunction or request service",
                   self.master.show_maintenance_request)
        self._card(body, "✅", "Close Maintenance Ticket",
                   "Technician marks a repair as complete",
                   self.master.show_maintenance_tickets)

        # Admin section
        self._section(body, "Admin")
        self._card(body, "⚙️", "Machine Information",
                   "Admin updates the machine profile",
                   self.master.show_machine_info)
        self._card(body, "📊", "View Transactions",
                   "View all sales history and revenue totals",
                   self.master.show_transactions)
        self._card(body, "👷", "Manage Workers",
                   "Add, edit, or remove service workers",
                   self.master.show_manage_workers)

        tk.Frame(body, bg=BG_MAIN, height=20).pack()

    def destroy(self):
        try:
            self.master.unbind_all("<MouseWheel>")
        except Exception:
            pass
        super().destroy()

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
        self.qty_labels = {}

        refresh_restock_requests()

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
            qty_lbl = tk.Label(tile, text=f"Qty: {p['count']} / {p['max']}", font=("Segoe UI", 7),
                               fg=TEXT_LIGHT, bg=BG_WHITE)
            qty_lbl.place(relx=0.95, rely=0.95, anchor="se")
            self.qty_labels[p["code"]] = qty_lbl

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
        tk.Label(self.cash_frame, text="Money Given", font=("Segoe UI", 9),
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

        # EDIT : added checking for products that are sold out
        if p["count"] <= 0:
            messagebox.showerror("Product Out Of Stock", 
                                f"Selected item is out of stock.")
            return
        #

        if self.payment.get() == "cash":
            given = self.cash_given.get()
            if given < total:
                messagebox.showerror("Insufficient Funds",
                                     f"Cash ${given:.2f} is less than total ${total:.2f}.")
                return
            if not db_connection.check_cash_in(self.master.machine_id, given):      # check if the machine can't take in any more money
                messagebox.showerror("Machine Cash Too Full",
                                     f"Money must be emptied to take that amount. Try giving a smaller amount.")
                return
            change        = round(given - total, 2)
            if not db_connection.check_cash_out(self.master.machine_id, change):      # check if the machine can't give out any more money
                messagebox.showerror("Machine Cash Not Full Enough For Change",
                                     f"Money must be refilled to give change for that amount. Try giving a smaller amount.")
                return
            receipt_extra = f"Money Given:   ${given:.2f}\n    Change:       ${change:.2f}" # edit : added a few spaces for formatting
        else:
            last4 = self.card_entry.get().strip()
            if not last4.isdigit() or len(last4) != 4:
                messagebox.showerror("Card Error", "Please enter valid last 4 digits.")
                return
            receipt_extra = f"Card:         xxxx-{last4}\n    Card Fee:     $0.00"

        # Record transaction and update inventory in the database
        try:
            if self.payment.get() == "cash":
                sale_num = db_connection.record_cash_sale(
                    product_id=p["product_id"], machine_id=self.master.machine_id,
                    tax=tax, cash_given=self.cash_given.get(), price=p["price"])
            else:
                sale_num = db_connection.record_card_sale(
                    product_id=p["product_id"], machine_id=self.master.machine_id,
                    tax=tax, card_fee=0.00, account_charged=f"xxxx-{last4}")

            new_count = p["count"] - 1
            db_connection.update_slot_count(p["code"], new_count)
            # System-triggered: auto-generate restock request if stock is low
            db_connection.check_and_create_restock_request(p["code"])
            # System-triggered: also surface cash threshold breaches (coins low / bills high)
            db_connection.check_and_create_money_handler_requests(self.master.machine_id)

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not record sale:\n{e}")
            return

        p["count"] = new_count
        if p["code"] in self.qty_labels:
            self.qty_labels[p["code"]].configure(text=f"Qty: {new_count} / {p['max']}")

        # Display receipt in the green banner
        # EDIT : text was being cut off in receipt box. added some spaces in text to fix. also changed '─' amount from 28 to 20
        self.receipt_label.configure(text=(
            f"    ✅  Sale Approved\n{'─'*20}\n"
            f"    Sale #:       TXN-{sale_num}\n"
            f"    Product:      {p['name']} ({p['code']})\n"
            f"    Price:        ${p['price']:.2f}\n"
            f"    Tax:          ${tax:.2f}\n"
            f"    Total:        ${total:.2f}\n"
            f"    {receipt_extra}\n{'─'*20}\n"
            f"    Time: {datetime.now().strftime('%H:%M:%S')}\n    Thank you!"))
        self.receipt_frame.pack(fill="x", pady=(14, 0))

        # update all restock requests
        refresh_restock_requests()

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

        refresh_restock_requests()

        try:
            self.all_products = db_connection.get_all_products_with_slots()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load inventory:\n{e}")
            self.all_products = []

        try:
            self.workers = db_connection.get_service_workers(self.master.machine_id)
        except Exception:
            self.workers = []

        self.products = list(self.all_products)
        self._build()

    def _build(self):
        screen_header(self, "📦  Update Inventory",
                      self.master.show_home, self.master.machine_info)
        self._worker_bar()
        self._table_container = tk.Frame(self, bg=BG_MAIN)
        self._table_container.pack(fill="both", expand=True, padx=20, pady=14)
        self._build_table()
        self._footer()

    def _worker_bar(self):
        """Thin blue banner showing the first assigned restocker and current date/time."""
        bar = tk.Frame(self, bg=ACCENT_LT, height=38)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        worker_name = self.workers[0]["Name"]     if self.workers else "Unknown"
        worker_id   = self.workers[0]["WorkerID"] if self.workers else "N/A"

        tk.Label(bar,
                 text=f"👷  {worker_name}  (ID: {worker_id})     {datetime.now().strftime('%A, %B %d  %H:%M')}",
                 font=("Segoe UI", 9), fg=ACCENT, bg=ACCENT_LT
                 ).pack(side="left", padx=20, pady=10)

    def _build_table(self):
        """Renders the inventory table into self._table_container."""
        container = self._table_container

        # Header row
        hdr = tk.Frame(container, bg=ACCENT, height=34)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        for h, w in zip(["Slot", "Product", "Current", "Max", "Add Qty", "Status"],
                        [6,       22,         9,         7,     9,          10]):
            tk.Label(hdr, text=h, font=("Segoe UI", 9, "bold"),
                     fg=BG_WHITE, bg=ACCENT, width=w, anchor="w"
                     ).pack(side="left", padx=10, pady=8)

        if not self.products:
            tk.Label(container, text="No slots match the selected worker filter.",
                     font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_MAIN
                     ).pack(pady=20)
            return

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

        add_btn = tk.Button(footer, text="➕  Add New Item",
                            font=("Segoe UI", 10),
                            bg=GREEN_BG, fg=GREEN, activebackground=GREEN_BG,
                            activeforeground=GREEN, relief="flat", bd=0,
                            cursor="hand2", padx=16, command=self._add_new_item_dialog)
        add_btn.pack(side="right", padx=(0, 8), pady=12)

        self.status_label = tk.Label(footer, text="", font=("Segoe UI", 10),
                                     fg=GREEN, bg=BG_WHITE)
        self.status_label.pack(side="left", padx=20)

    def _add_new_item_dialog(self):
        """Opens a popup dialog to add a brand-new product to a new machine slot."""
        dlg = tk.Toplevel(self, bg=BG_WHITE)
        dlg.title("Add New Item")
        dlg.geometry("420x520")
        dlg.resizable(False, True)
        dlg.grab_set()

        # Scrollable canvas wrapper
        _canvas = tk.Canvas(dlg, bg=BG_WHITE, highlightthickness=0)
        _sb = ttk.Scrollbar(dlg, orient="vertical", command=_canvas.yview)
        _canvas.configure(yscrollcommand=_sb.set)
        _sb.pack(side="right", fill="y")
        _canvas.pack(side="left", fill="both", expand=True)

        pad = tk.Frame(_canvas, bg=BG_WHITE)
        _win = _canvas.create_window((0, 0), window=pad, anchor="nw")

        def _on_pad_configure(e):
            _canvas.configure(scrollregion=_canvas.bbox("all"))
        def _on_canvas_configure(e):
            _canvas.itemconfigure(_win, width=e.width)
        def _on_mousewheel(e):
            _canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        pad.bind("<Configure>", _on_pad_configure)
        _canvas.bind("<Configure>", _on_canvas_configure)
        dlg.bind("<MouseWheel>", _on_mousewheel)

        # Inner content uses padx/pady via pack
        inner = tk.Frame(pad, bg=BG_WHITE)
        inner.pack(fill="both", expand=True, padx=28, pady=20)

        tk.Label(inner, text="Add New Product to Slot",
                 font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Label(inner, text="Creates a new product and assigns it to a slot.",
                 font=("Segoe UI", 9), fg=TEXT_LIGHT, bg=BG_WHITE).pack(anchor="w", pady=(2, 10))
        tk.Frame(inner, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))

        # Alias so the rest of the method still refers to `pad`
        pad = inner

        slot_var  = tk.StringVar()
        name_var  = tk.StringVar()
        price_var = tk.StringVar()
        max_var   = tk.StringVar()
        thr_var   = tk.StringVar()

        labeled_entry(pad, "Slot Code *",          var=slot_var,  bg=BG_WHITE)
        labeled_entry(pad, "Product Name *",        var=name_var,  bg=BG_WHITE)
        labeled_entry(pad, "Price ($) *",           var=price_var, bg=BG_WHITE)
        labeled_entry(pad, "Max Quantity *",        var=max_var,   bg=BG_WHITE)
        labeled_entry(pad, "Restock Threshold",     var=thr_var,   bg=BG_WHITE)

        desc_label = tk.Label(pad, text="Description", font=("Segoe UI", 10, "bold"),
                              fg=TEXT_MID, bg=BG_WHITE)
        desc_label.pack(anchor="w", pady=(10, 2))
        desc_text = tk.Text(pad, font=("Segoe UI", 10), bg=BG_SIDEBAR, fg=TEXT_DARK,
                            relief="flat", bd=0, height=3, wrap="word",
                            highlightthickness=1, highlightbackground=BORDER,
                            highlightcolor=ACCENT)
        desc_text.pack(fill="x", ipady=4)

        status_lbl = tk.Label(pad, text="", font=("Segoe UI", 9),
                              fg=RED, bg=BG_WHITE, wraplength=360, justify="left")
        status_lbl.pack(anchor="w", pady=(6, 0))

        def _submit():
            slot  = slot_var.get().strip().upper()
            name  = name_var.get().strip()
            price = price_var.get().strip()
            maxq  = max_var.get().strip()
            thr   = thr_var.get().strip() or "0"
            desc  = desc_text.get("1.0", "end").strip()

            if not slot or not name or not price or not maxq:
                status_lbl.configure(text="Slot Code, Name, Price, and Max Qty are required.", fg=RED)
                return
            try:
                price_f = float(price)
                maxq_i  = int(maxq)
                thr_f   = float(thr)
            except ValueError:
                status_lbl.configure(text="Price and Max Qty must be valid numbers.", fg=RED)
                return

            try:
                db_connection.add_product_to_slot(slot, name, price_f, desc, maxq_i, thr_f)
            except Exception as e:
                status_lbl.configure(text=f"Database error: {e}", fg=RED)
                return

            dlg.destroy()
            self.destroy()
            self.master.show_inventory()

        btn = tk.Button(pad, text="Add Item  ▶", font=("Segoe UI", 11, "bold"),
                        bg=ACCENT, fg=BG_WHITE, activebackground=ACCENT_HOV,
                        activeforeground=BG_WHITE, relief="flat", bd=0,
                        cursor="hand2", pady=10, command=_submit)
        btn.pack(fill="x", pady=(12, 0))

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

        refresh_restock_requests()

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
        try:
            self.workers = db_connection.get_service_workers(master.machine_id)
        except Exception:
            self.workers = []
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

        # Reason text area and worker selector
        self.reason_entry = labeled_entry(pad, "Reason for Request", height=4, bg=BG_WHITE)

        tk.Label(pad, text="Your Worker", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w", pady=(10, 2))
        self.worker_var = tk.StringVar()
        worker_options = [f"{w['Name']} (ID: {w['WorkerID']})" for w in self.workers]
        self.worker_combo = ttk.Combobox(pad, textvariable=self.worker_var,
                                         values=worker_options, state="readonly",
                                         font=("Segoe UI", 11))
        self.worker_combo.pack(fill="x", ipady=4)
        if worker_options:
            self.worker_combo.set(worker_options[0])

        action_button(pad, "Submit Request  ▶", self._submit)

        self.confirm_label = tk.Label(pad, text="", font=("Segoe UI", 9),
                                      fg=GREEN, bg=BG_WHITE,
                                      wraplength=600, justify="left")
        self.confirm_label.pack(anchor="w", pady=(14, 0))

    def _submit(self):
        """Validates form and writes a new maintenance request to the database."""
        reason   = self.reason_entry.get("1.0", "end").strip()
        selected = self.worker_var.get()

        if not reason:
            messagebox.showwarning("Missing Info", "Please describe the reason for the request.")
            return
        if not selected:
            messagebox.showwarning("Missing Info", "Please select a worker.")
            return

        worker = next((w for w in self.workers
                       if f"{w['Name']} (ID: {w['WorkerID']})" == selected), None)
        if not worker:
            messagebox.showerror("Error", "Invalid worker selection.")
            return
        worker_id = worker["WorkerID"]

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
                  f"Worker:      {selected}\n"
                  f"Time:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                  f"Status:      Pending — a technician will be assigned shortly."))
        self.reason_entry.delete("1.0", "end")


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

        try:
            self.workers = db_connection.get_service_workers(master.machine_id)
        except Exception:
            self.workers = []

        self.filtered_tickets = list(self.tickets)
        self._build()

    def _build(self):
        screen_header(self, "✅  Close Maintenance Ticket",
                      self.master.show_home, self.master.machine_info)

        # Filter bar above the two-column layout
        self._filter_bar()

        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=16)

        # Left: list of open tickets  |  Right: resolution form
        self._left_frame = tk.Frame(main, bg=BG_MAIN)
        right = tk.Frame(main, bg=BG_WHITE, width=320,
                         highlightthickness=1, highlightbackground=BORDER)
        self._left_frame.pack(side="left", fill="both", expand=True, padx=(0, 16))
        right.pack(side="right", fill="y")

        self._ticket_list(self._left_frame)
        self._resolution_form(right)

    def _filter_bar(self):
        bar = tk.Frame(self, bg=BG_WHITE, height=40,
                       highlightthickness=1, highlightbackground=BORDER)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="Filter by worker:", font=("Segoe UI", 9),
                 fg=TEXT_MID, bg=BG_WHITE).pack(side="left", padx=(16, 6), pady=10)

        self.filter_var = tk.StringVar(value="All Workers")
        options = ["All Workers"] + [f"{w['Name']} (ID: {w['WorkerID']})" for w in self.workers]
        cb = ttk.Combobox(bar, textvariable=self.filter_var, values=options,
                          state="readonly", font=("Segoe UI", 9), width=28)
        cb.pack(side="left", pady=8)
        cb.bind("<<ComboboxSelected>>", self._on_filter_change)

    def _on_filter_change(self, event=None):
        selected = self.filter_var.get()
        if selected == "All Workers":
            self.filtered_tickets = list(self.tickets)
        else:
            worker = next((w for w in self.workers
                           if f"{w['Name']} (ID: {w['WorkerID']})" == selected), None)
            if worker:
                wid = worker["WorkerID"]
                self.filtered_tickets = [t for t in self.tickets
                                          if t["ServiceWorkerID"] == wid]
            else:
                self.filtered_tickets = list(self.tickets)

        # Rebuild just the ticket list panel
        for w in self._left_frame.winfo_children():
            w.destroy()
        self.selected_ticket = None
        if hasattr(self, "selected_label"):
            self.selected_label.configure(text="No ticket selected.", fg=TEXT_LIGHT)
        self._ticket_list(self._left_frame)

    def _ticket_list(self, parent):
        """Renders filtered open tickets as clickable white cards."""
        tk.Label(parent, text="Open Tickets",
                 font=("Segoe UI", 11, "bold"), fg=TEXT_MID, bg=BG_MAIN
                 ).pack(anchor="w", pady=(0, 10))

        if not self.filtered_tickets:
            ok = tk.Frame(parent, bg=GREEN_BG,
                          highlightthickness=1, highlightbackground=GREEN)
            ok.pack(fill="x")
            tk.Label(ok,
                     text="✅  No open maintenance tickets — machine is running normally.",
                     font=("Segoe UI", 10), fg=GREEN, bg=GREEN_BG
                     ).pack(padx=16, pady=14)
            return

        for t in self.filtered_tickets:
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

        tk.Label(pad, text="Technician", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w", pady=(10, 2))
        self.tech_var = tk.StringVar()
        tech_options = [f"{w['Name']} (ID: {w['WorkerID']})" for w in self.workers]
        self.tech_combo = ttk.Combobox(pad, textvariable=self.tech_var,
                                       values=tech_options, state="readonly",
                                       font=("Segoe UI", 11))
        self.tech_combo.pack(fill="x", ipady=4)
        if tech_options:
            self.tech_combo.set(tech_options[0])

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

        notes    = self.notes_entry.get("1.0", "end").strip()
        selected = self.tech_var.get()

        if not notes:
            messagebox.showwarning("Missing Info", "Please enter service notes.")
            return
        if not selected:
            messagebox.showwarning("Missing Info", "Please select a technician.")
            return

        worker = next((w for w in self.workers
                       if f"{w['Name']} (ID: {w['WorkerID']})" == selected), None)
        if not worker:
            messagebox.showerror("Error", "Invalid technician selection.")
            return

        date_resolved = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        req_id = self.selected_ticket["MaintenanceRequestID"]

        try:
            db_connection.close_maintenance_request(
                request_id=req_id, date_resolved=date_resolved, notes=notes)
            # System-triggered: restore machine to ONLINE after repair is complete
            db_connection.update_machine_status(self.master.machine_id, "ONLINE")
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not close ticket:\n{e}")
            return

        messagebox.showinfo("Ticket Closed",
                            f"✅  Ticket closed\n{'─'*28}\n"
                            f"Request ID:  MR-{req_id}\n"
                            f"Technician:  {selected}\n"
                            f"Resolved:    {date_resolved}\n"
                            f"Machine status → ONLINE")
        self.destroy()
        self.master.show_maintenance_tickets()


# ═══════════════════════════════════════════════════════════════
# View Restocker Requests Screen (read-only)
# System auto-creates rows after sales when slots run low or cash
# crosses MoneyHandler thresholds; this screen surfaces the queue.
# Resolution happens via Update Inventory or Update Cash Level.
# ═══════════════════════════════════════════════════════════════
class RestockRequestsScreen(tk.Frame):
    PRODUCT = "Product Restock"
    COLLECT = "Cash Collection"
    REFILL_COINS  = "Coin Refill"
    COLLECT_COINS = "Coin Collection"
    OTHER = "Other Requests"
    CATEGORIES = ["All Requests", PRODUCT, COLLECT, REFILL_COINS, COLLECT_COINS, OTHER]

    def __init__(self, master):
        refresh_restock_requests()

        super().__init__(master, bg=BG_MAIN)

        try:
            self.requests = db_connection.get_open_restock_requests()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load restock requests:\n{e}")
            self.requests = []

        # Classify each request once based on its reason text.
        for r in self.requests:
            r["_kind"] = self._classify(r.get("ReasonForRequest", ""))

        self.filtered = list(self.requests)
        self._build()

    @classmethod
    def _classify(cls, reason):
        text = (reason or "").lower()
        if "bills above" in text:
            return cls.COLLECT
        elif "coins below" in text:
            return cls.REFILL_COINS
        elif "coins " in text:
            return cls.COLLECT_COINS
        elif "slot" in text:
            return cls.PRODUCT
        return cls.OTHER

    def _build(self):
        screen_header(self, "📋  View Restocker Requests",
                      self.master.show_home, self.master.machine_info)
        self._filter_bar()

        body = tk.Frame(self, bg=BG_MAIN)
        body.pack(fill="both", expand=True, padx=20, pady=16)

        self._list_frame = tk.Frame(body, bg=BG_MAIN)
        self._list_frame.pack(fill="both", expand=True)
        self._render_list()

    def _filter_bar(self):
        bar = tk.Frame(self, bg=BG_WHITE, height=40,
                       highlightthickness=1, highlightbackground=BORDER)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="Filter by type:", font=("Segoe UI", 9),
                 fg=TEXT_MID, bg=BG_WHITE).pack(side="left", padx=(16, 6), pady=10)

        self.filter_var = tk.StringVar(value=self.CATEGORIES[0])
        cb = ttk.Combobox(bar, textvariable=self.filter_var, values=self.CATEGORIES,
                          state="readonly", font=("Segoe UI", 9), width=24)
        cb.pack(side="left", pady=8)
        cb.bind("<<ComboboxSelected>>", self._on_filter_change)

        # Right-aligned count of currently displayed requests.
        self.count_label = tk.Label(bar, text="", font=("Segoe UI", 9),
                                    fg=TEXT_LIGHT, bg=BG_WHITE)
        self.count_label.pack(side="right", padx=16)

    def _on_filter_change(self, event=None):
        refresh_restock_requests()
        choice = self.filter_var.get()
        if choice == self.CATEGORIES[0]:
            self.filtered = list(self.requests)
        else:
            self.filtered = [r for r in self.requests if r["_kind"] == choice]
        for w in self._list_frame.winfo_children():
            w.destroy()
        self._render_list()

    def _render_list(self):
        refresh_restock_requests()
        self.count_label.configure(text=f"{len(self.filtered)} open")

        if not self.filtered:
            ok = tk.Frame(self._list_frame, bg=GREEN_BG,
                          highlightthickness=1, highlightbackground=GREEN)
            ok.pack(fill="x")
            tk.Label(ok, text="✅  No open restock requests.",
                     font=("Segoe UI", 10), fg=GREEN, bg=GREEN_BG
                     ).pack(padx=16, pady=14)
            return

        for r in self.filtered:
            self._request_card(self._list_frame, r)

    def _request_card(self, parent, r):
        card = tk.Frame(parent, bg=BG_WHITE,
                        highlightthickness=1, highlightbackground=BORDER)
        card.pack(fill="x", pady=4, ipady=2)

        top = tk.Frame(card, bg=BG_WHITE)
        top.pack(fill="x", padx=14, pady=(10, 2))
        tk.Label(top, text=f"RR-{r['RestockRequestID']}",
                 font=("Segoe UI", 10, "bold"), fg=ACCENT, bg=BG_WHITE
                 ).pack(side="left")
        tk.Label(top, text=r["_kind"], font=("Segoe UI", 9, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(side="left", padx=(10, 0))
        tk.Label(top, text=str(r.get("DateRequested", "")),
                 font=("Segoe UI", 9), fg=TEXT_LIGHT, bg=BG_WHITE
                 ).pack(side="right")

        tk.Label(card, text=r.get("ReasonForRequest", ""),
                 font=("Segoe UI", 9), fg=TEXT_MID, bg=BG_WHITE,
                 wraplength=820, justify="left", anchor="w"
                 ).pack(fill="x", padx=14, pady=(0, 4))

        bottom = tk.Frame(card, bg=BG_WHITE)
        bottom.pack(fill="x", padx=14, pady=(0, 10))
        worker = r.get("WorkerName") or f"Worker #{r.get('ServiceWorkerID')}"
        tk.Label(bottom, text=f"Assigned: {worker}",
                 font=("Segoe UI", 9), fg=TEXT_LIGHT, bg=BG_WHITE, anchor="w"
                 ).pack(side="left")
        """ This is disabled because restockers don't resolve from this screen. The system detects they're resolved automatically when the correct action is taken.
        tk.Button(bottom, text="Mark As Resolved ✓",
                  font=("Segoe UI", 9, "bold"), fg=BG_WHITE, bg=GREEN,
                  activebackground=GREEN, activeforeground=BG_WHITE,
                  relief="flat", cursor="hand2", padx=10, pady=2,
                  command=lambda rid=int(r["RestockRequestID"]): self._resolve(rid)
                  ).pack(side="right")
        """

    def _resolve(self, request_id):
        try:
            db_connection.resolve_restock_request_by_id(request_id)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not resolve request:\n{e}")
            return
        self.master.show_restock_requests()
        refresh_restock_requests()


# ═══════════════════════════════════════════════════════════════
# Use Case 5: Update Cash Level Screen
# Restocker logs a cash collection or a coin change refill.
# System side effects: resolves open cash or change alerts.
# ═══════════════════════════════════════════════════════════════
class UpdateCashLevelScreen(tk.Frame):
    def __init__(self, master):
        refresh_restock_requests()
        super().__init__(master, bg=BG_MAIN)

        # Load money handler data from the database
        try:
            self.money_info = db_connection.get_money_handler(self.master.machine_id)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load cash data:\n{e}")
            self.money_info = None

        try:
            self.currency_breakdown = db_connection.get_currency_breakdown(self.master.machine_id)
        except Exception:
            self.currency_breakdown = []

        try:
            self.currency_details = db_connection.get_currency_details(self.master.machine_id)
        except Exception:
            self.currency_details = []

        try:
            self.workers = db_connection.get_service_workers(master.machine_id)
        except Exception:
            self.workers = []

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
        pad.pack(fill="both", expand=True, padx=5, pady=4)

        tk.Label(pad, text="Current Cash Status",
                 font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Label(pad, text="Thresholds and limits configured for this machine.",
                 font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_WHITE
                 ).pack(anchor="w", pady=(2, 18))
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(0, 16))

        if self.money_info:
            m = self.money_info
            for label, val in [
                ("Bill Max Amount",            f"{m.get('BillMaxAmount', 'N/A')}"),
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

        if self.currency_breakdown:
            tk.Label(pad, text="Current Denomination Levels",
                     font=("Segoe UI", 11, "bold"), fg=TEXT_DARK, bg=BG_WHITE
                     ).pack(anchor="w", pady=(16, 4))
            col_hdr = tk.Frame(pad, bg=ACCENT, height=28)
            col_hdr.pack(fill="x")
            col_hdr.pack_propagate(False)
            # edit : added new column "max amount (coins only)"
            total_amounts = db_connection.get_total_currency_amounts(self.master.machine_id)
            for h, w in [("Denomination", 24), ("Type", 12), ("Count", 10), ("Max Amount", 20)]:
                tk.Label(col_hdr, text=h, font=("Segoe UI", 8, "bold"),
                         fg=BG_WHITE, bg=ACCENT, width=w, anchor="w"
                         ).pack(side="left", padx=8, pady=4)
            for i, denom in enumerate(self.currency_breakdown):
                bg = BG_WHITE if i % 2 == 0 else BG_SIDEBAR
                worth = float(denom.get("CurrencyWorth") or 0)
                label = f"${worth:.2f}" if worth >= 1.0 else f"{int(worth * 100)}¢"
                type_label = "Bill" if worth >= 1.0 else "Coin"
                max_amt = str(total_amounts[i].get("MaxAmount"))
                row = tk.Frame(pad, bg=bg, height=30)
                row.pack(fill="x")
                row.pack_propagate(False)
                tk.Label(row, text=label, font=("Segoe UI", 9),
                         fg=TEXT_DARK, bg=bg, width=24, anchor="w").pack(side="left", padx=10, pady=4)
                tk.Label(row, text=type_label, font=("Segoe UI", 9),
                         fg=TEXT_MID, bg=bg, width=12, anchor="w").pack(side="left", padx=4)
                tk.Label(row, text=str(denom.get("CurrentAmount", 0)), font=("Segoe UI", 9, "bold"),
                         fg=TEXT_DARK, bg=bg, width=10, anchor="w").pack(side="left", padx=10)
                tk.Label(row, text=max_amt, font=("Segoe UI", 9),
                         fg=TEXT_DARK, bg=bg, width=10, anchor="w").pack(side="left", padx=12)      

        total_cash = sum(
            float(d.get("CurrencyWorth") or 0) * int(d.get("CurrentAmount") or 0)
            for d in self.currency_breakdown
        )
        total_row = tk.Frame(pad, bg=ACCENT_LT,
                             highlightthickness=1, highlightbackground=ACCENT)
        total_row.pack(fill="x", pady=(6, 0))
        tk.Label(total_row, text="Total Cash in Machine", font=("Segoe UI", 10, "bold"),
                 fg=ACCENT, bg=ACCENT_LT, width=24, anchor="w").pack(side="left", padx=14, pady=8)
        tk.Label(total_row, text=f"${total_cash:.2f}", font=("Segoe UI", 11, "bold"),
                 fg=TEXT_DARK, bg=ACCENT_LT).pack(side="right", padx=14)

    def _action_form(self, parent):
        """Right-side form for refilling or collecting per-denomination."""
        pad = tk.Frame(parent, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(pad, text="Log an Action",
                 font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(4, 12))

        # Mode toggle: Refill or Collect — applies per-denomination below.
        tk.Label(pad, text="Action Type", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w")
        self.action_type = tk.StringVar(value="refill")
        af = tk.Frame(pad, bg=BG_WHITE)
        af.pack(anchor="w", pady=(4, 12))
        for val, label in [("refill",  "🔄  Refill"),
                           ("collect", "💰  Collect")]:
            tk.Radiobutton(af, text=label, variable=self.action_type, value=val,
                           font=("Segoe UI", 10), fg=TEXT_DARK, bg=BG_WHITE,
                           selectcolor=ACCENT_LT, activebackground=BG_WHITE,
                           command=self._refresh_preview).pack(side="left", padx=(0, 14))

        # Per-denomination grid: one row per Currency. Refill mode uses the count
        # entry; collect mode uses the entry OR the "Empty" checkbox (sets to 0).
        tk.Label(pad, text="Per-Denomination", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w", pady=(2, 4))

        hdr = tk.Frame(pad, bg=ACCENT, height=24)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        for h, w in [("Denom", 6), ("Cur/Max", 9), ("Count", 6), ("Empty", 6)]:
            tk.Label(hdr, text=h, font=("Segoe UI", 8, "bold"),
                     fg=BG_WHITE, bg=ACCENT, width=w, anchor="w"
                     ).pack(side="left", padx=4, pady=3)

        self.denom_inputs = []
        for i, c in enumerate(self.currency_details):
            row_bg = BG_WHITE if i % 2 == 0 else BG_SIDEBAR
            row = tk.Frame(pad, bg=row_bg, height=28)
            row.pack(fill="x")
            row.pack_propagate(False)

            worth = float(c.get("CurrencyWorth") or 0)
            cur = int(c.get("CurrentAmount") or 0)
            max_amt = c.get("MaxAmount")
            denom_label = f"${worth:.2f}" if worth >= 1.0 else f"{int(worth * 100)}¢"
            cap_label = f"{cur}/{max_amt}" if max_amt is not None else f"{cur}/—"

            tk.Label(row, text=denom_label, font=("Segoe UI", 9, "bold"),
                     fg=TEXT_DARK, bg=row_bg, width=6, anchor="w"
                     ).pack(side="left", padx=4)
            tk.Label(row, text=cap_label, font=("Segoe UI", 9),
                     fg=TEXT_MID, bg=row_bg, width=9, anchor="w"
                     ).pack(side="left", padx=4)

            count_var = tk.StringVar(value="0")
            count_var.trace_add("write", lambda *_: self._refresh_preview())
            entry = tk.Entry(row, textvariable=count_var, width=6,
                             font=("Segoe UI", 9), justify="right")
            entry.pack(side="left", padx=4)

            empty_var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(row, variable=empty_var, bg=row_bg,
                                 activebackground=row_bg,
                                 command=self._refresh_preview)
            chk.pack(side="left", padx=4)

            self.denom_inputs.append({
                "currency_id": int(c["CurrencyID"]),
                "worth": worth,
                "current": cur,
                "max": max_amt,
                "count_var": count_var,
                "empty_var": empty_var,
            })

        # Quick-fill helpers
        helpers = tk.Frame(pad, bg=BG_WHITE)
        helpers.pack(fill="x", pady=(8, 2))
        tk.Button(helpers, text="Collect All",
                  font=("Segoe UI", 9, "bold"), fg=BG_WHITE, bg=ACCENT,
                  activebackground=ACCENT, activeforeground=BG_WHITE,
                  relief="flat", cursor="hand2", padx=10, pady=2,
                  command=self._collect_all).pack(side="left")
        tk.Button(helpers, text="Clear",
                  font=("Segoe UI", 9), fg=TEXT_MID, bg=BG_SIDEBAR,
                  activebackground=BG_SIDEBAR, relief="flat", cursor="hand2",
                  padx=10, pady=2, command=self._clear_inputs).pack(side="left", padx=6)

        # Live total preview of what the Apply button will do.
        self.preview_label = tk.Label(pad, text="Refilling: $0.00",
                                      font=("Segoe UI", 10, "bold"),
                                      fg=ACCENT, bg=BG_WHITE)
        self.preview_label.pack(anchor="w", pady=(10, 2))

        tk.Label(pad, text="Your Worker", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w", pady=(8, 2))
        self.worker_var = tk.StringVar()
        worker_options = [f"{w['Name']} (ID: {w['WorkerID']})" for w in self.workers]
        self.worker_combo = ttk.Combobox(pad, textvariable=self.worker_var,
                                         values=worker_options, state="readonly",
                                         font=("Segoe UI", 10))
        self.worker_combo.pack(fill="x", ipady=2)
        if worker_options:
            self.worker_combo.set(worker_options[0])

        action_button(pad, "Apply Cash Update  ▶", self._apply)

        self.confirm_label = tk.Label(pad, text="", font=("Segoe UI", 9),
                                      fg=GREEN, bg=BG_WHITE,
                                      wraplength=280, justify="left")
        self.confirm_label.pack(anchor="w", pady=(8, 0))

    def _collect_deltas(self):
        """Resolves UI inputs to a list of {currency_id, count, worth} for the action.
        Returns (deltas, total_dollars). Invalid count entries are treated as 0."""
        action = self.action_type.get()
        deltas = []
        total = 0.0
        for d in self.denom_inputs:
            try:
                count = int(d["count_var"].get() or 0)
            except ValueError:
                count = 0
            if action == "collect" and d["empty_var"].get():
                count = d["current"]
            if count <= 0:
                continue
            deltas.append({
                "currency_id": d["currency_id"],
                "count": count,
                "worth": d["worth"],
            })
            total += count * d["worth"]
        return deltas, total

    def _refresh_preview(self):
        action = self.action_type.get()
        _, total = self._collect_deltas()
        verb = "Refilling" if action == "refill" else "Collecting"
        self.preview_label.configure(text=f"{verb}: ${total:.2f}")

    def _collect_all(self):
        """Switches to Collect mode and marks every denomination to be emptied."""
        self.action_type.set("collect")
        for d in self.denom_inputs:
            d["empty_var"].set(True)
            d["count_var"].set(str(d["current"]))
        self._refresh_preview()

    def _clear_inputs(self):
        for d in self.denom_inputs:
            d["empty_var"].set(False)
            d["count_var"].set("0")
        self._refresh_preview()

    def _apply(self):
        """Validates per-denomination inputs and writes the adjustment to the DB."""
        action = self.action_type.get()
        selected = self.worker_var.get()
        deltas, total = self._collect_deltas()

        if not deltas:
            messagebox.showwarning("Nothing to do",
                                   "Enter a count for at least one denomination.")
            return
        if not selected:
            messagebox.showwarning("Missing Info", "Please select a worker.")
            return

        worker = next((w for w in self.workers
                       if f"{w['Name']} (ID: {w['WorkerID']})" == selected), None)
        if not worker:
            messagebox.showerror("Error", "Invalid worker selection.")
            return
        worker_id = worker["WorkerID"]

        if action == "refill":
            # Per-row coin cap.
            for d in deltas:
                row = next(r for r in self.denom_inputs
                           if r["currency_id"] == d["currency_id"])
                if row["max"] is not None and row["current"] + d["count"] > int(row["max"]):
                    denom_label = (f"${row['worth']:.2f}" if row["worth"] >= 1.0
                                   else f"{int(row['worth']*100)}¢")
                    messagebox.showwarning(
                        "Over Capacity",
                        f"Refilling {d['count']} of {denom_label} would exceed "
                        f"the max ({row['max']}). Currently has {row['current']}.")
                    return
            # Global bill cap (BillMaxAmount in MoneyHandler).
            if self.money_info:
                bill_cap = float(self.money_info.get("BillMaxAmount") or 0)
                bills_current = 0
                for denom in self.currency_breakdown:
                    if denom.get("CurrencyWorth") >= 1:
                        bills_current += denom.get("CurrentAmount")
                #print(self.denom_inputs)
                if bill_cap > 0:
                    bill_total_after = bills_current
                    for item in self.denom_inputs:
                        if item.get("max") == None:
                            bill_total_after += int(item.get("count_var").get())
                    print(bill_total_after)
                    if bill_total_after > bill_cap:
                        messagebox.showwarning(
                            "Over Bill Capacity",
                            f"This refill would push bill total to "
                            f"{bill_total_after:.2f} bills, exceeding cap of {bill_cap} bills.")
                        return
        else:
            # Collect can't take more than what's there (the Empty checkbox enforces this).
            for d in deltas:
                row = next(r for r in self.denom_inputs
                           if r["currency_id"] == d["currency_id"])
                if d["count"] > row["current"]:
                    denom_label = (f"${row['worth']:.2f}" if row["worth"] >= 1.0
                                   else f"{int(row['worth']*100)}¢")
                    messagebox.showwarning(
                        "Not Enough",
                        f"Cannot collect {d['count']} of {denom_label}; "
                        f"only {row['current']} present.")
                    return

        try:
            db_connection.apply_cash_adjustments(
                machine_id=self.master.machine_id,
                worker_id=worker_id,
                action=action,
                deltas=deltas,
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # Resolve any matching open auto-alerts the operator just addressed.
            if action == "refill" and any(d["worth"] < 1.0 for d in deltas):
                db_connection.resolve_change_refill_alert(self.master.machine_id)
            if action == "collect" and any(d["worth"] >= 1.0 for d in deltas):
                db_connection.resolve_cash_collection_alert(self.master.machine_id)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not update cash level:\n{e}")
            return

        action_label = "Cash Refilled" if action == "refill" else "Cash Collected"
        breakdown = ", ".join(
            f"{d['count']}×"
            + (f"${d['worth']:.2f}" if d["worth"] >= 1.0 else f"{int(d['worth']*100)}¢")
            for d in deltas
        )
        self.confirm_label.configure(
            text=(f"✅  {action_label}\n{'─'*30}\n"
                  f"Total:    ${total:.2f}\n"
                  f"Items:    {breakdown}\n"
                  f"Worker:   {selected}"))
        
        refresh_restock_requests()

        # Reload so the status panel reflects new counts.
        self.destroy()
        self.master.show_cash_level()


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

        # Read-only: Date Last Serviced
        m = self.machine or {}
        date_val = m.get("DateLastServiced", "N/A")
        info_row = tk.Frame(pad, bg=BG_SIDEBAR,
                            highlightthickness=1, highlightbackground=BORDER)
        info_row.pack(fill="x", pady=(0, 12))
        tk.Label(info_row, text="Date Last Serviced", font=("Segoe UI", 10),
                 fg=TEXT_MID, bg=BG_SIDEBAR, width=22, anchor="w"
                 ).pack(side="left", padx=14, pady=8)
        tk.Label(info_row, text=str(date_val), font=("Segoe UI", 10, "bold"),
                 fg=TEXT_DARK, bg=BG_SIDEBAR).pack(side="left", padx=4)

        # Two-column layout for the editable fields
        cols     = tk.Frame(pad, bg=BG_WHITE)
        cols.pack(fill="x")
        left_col  = tk.Frame(cols, bg=BG_WHITE)
        right_col = tk.Frame(cols, bg=BG_WHITE)
        left_col.pack(side="left",  fill="both", expand=True, padx=(0, 20))
        right_col.pack(side="right", fill="both", expand=True)

        self.fields = {}

        for display, db_key, current in [
            ("Address",      "Address",     m.get("Address", "")),
            ("Model Number", "ModelNumber", m.get("ModelNumber", "")),
        ]:
            var = tk.StringVar(value=current)
            labeled_entry(left_col, display, var=var, bg=BG_WHITE)
            self.fields[db_key] = var

        days_var = tk.StringVar(value=str(m.get("DaysBetweenServices", "")))
        labeled_entry(right_col, "Days Between Services", var=days_var, bg=BG_WHITE)
        self.fields["DaysBetweenServices"] = days_var

        state_var = tk.StringVar(value=m.get("CurrentState", "ONLINE"))
        tk.Label(right_col, text="Current State", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w", pady=(10, 2))
        state_cb = ttk.Combobox(right_col, textvariable=state_var,
                                values=["ONLINE", "OFFLINE", "SCHEDULED", "MAINTENANCE"],
                                state="readonly", font=("Segoe UI", 10))
        state_cb.pack(fill="x", ipady=4)
        self.fields["CurrentState"] = state_var

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
                  f"Service Int.: {data['DaysBetweenServices']} days\n"
                  f"State:        {data['CurrentState']}\n"
                  f"Saved:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))


# ═══════════════════════════════════════════════════════════════
# View Transactions Screen
# Admin reviews all past sales with revenue/tax/cash summary totals.
# ═══════════════════════════════════════════════════════════════
class ViewTransactionsScreen(tk.Frame):
    def __init__(self, master):
        refresh_restock_requests()
        super().__init__(master, bg=BG_MAIN)

        try:
            self.rows, self.totals = db_connection.get_all_transactions(self.master.machine_id)
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load transactions:\n{e}")
            self.rows, self.totals = [], {}

        try:
            self.current_cash = db_connection.get_total_cash_in_machine(self.master.machine_id)
        except Exception:
            self.current_cash = 0.0

        self._build()

    def _build(self):
        screen_header(self, "📊  View Transactions",
                      self.master.show_home, self.master.machine_info)
        self._summary_bar()
        self._table()

    def _summary_bar(self):
        """Thin colored banner showing aggregate totals."""
        bar = tk.Frame(self, bg=ACCENT_LT, highlightthickness=1, highlightbackground=BORDER)
        bar.pack(fill="x", padx=20, pady=(14, 0))

        t = self.totals or {}
        rev  = t.get("total_revenue") or 0.0
        tax  = t.get("total_tax")     or 0.0

        for label, val in [
            ("Total Revenue", f"${rev:.2f}"),
            ("Total Tax",     f"${tax:.2f}"),
            ("Cash In Machine", f"${self.current_cash:.2f}"),
            ("Transactions",  str(len(self.rows))),
        ]:
            cell = tk.Frame(bar, bg=ACCENT_LT)
            cell.pack(side="left", padx=28, pady=10)
            tk.Label(cell, text=label, font=("Segoe UI", 8),
                     fg=ACCENT, bg=ACCENT_LT).pack(anchor="w")
            tk.Label(cell, text=val, font=("Segoe UI", 12, "bold"),
                     fg=TEXT_DARK, bg=ACCENT_LT).pack(anchor="w")

    def _table(self):
        """Scrollable table of all transaction rows."""
        container = tk.Frame(self, bg=BG_MAIN)
        container.pack(fill="both", expand=True, padx=20, pady=12)

        # Header
        hdr = tk.Frame(container, bg=ACCENT, height=34)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        for h, w in zip(["#", "Date / Time", "Product", "Price", "Tax", "Total", "Method"],
                        [5,    20,             20,         8,       7,     8,       10]):
            tk.Label(hdr, text=h, font=("Segoe UI", 9, "bold"),
                     fg=BG_WHITE, bg=ACCENT, width=w, anchor="w"
                     ).pack(side="left", padx=8, pady=8)

        # Scrollable body
        scroll_frame = tk.Frame(container, bg=BG_MAIN)
        scroll_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(scroll_frame, bg=BG_MAIN, highlightthickness=0)
        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        body = tk.Frame(canvas, bg=BG_MAIN)

        win_id = canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win_id, width=e.width))
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        self.master.bind_all("<MouseWheel>", _scroll)
        self._scroll_canvas = canvas

        if not self.rows:
            tk.Label(body, text="No transactions recorded yet.",
                     font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_MAIN
                     ).pack(pady=24)
            body.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
            return

        for i, row in enumerate(self.rows):
            bg = BG_WHITE if i % 2 == 0 else BG_SIDEBAR
            price = float(row["Price"]) if row["Price"] else 0.0
            tax   = float(row["Tax"])   if row["Tax"]   else 0.0
            total = price + tax

            if row["CashGiven"] is not None:
                method = "💵 Cash"
            else:
                method = "💳 Card"

            dt = str(row["SaleDateTime"])[:16]

            tr = tk.Frame(body, bg=bg, height=34)
            tr.pack(fill="x")
            tr.pack_propagate(False)

            for val, w in zip([
                str(row["SaleNumber"]),
                dt,
                row["ProductName"] or "—",
                f"${price:.2f}",
                f"${tax:.2f}",
                f"${total:.2f}",
                method,
            ], [5, 20, 20, 8, 7, 8, 10]):
                tk.Label(tr, text=val, font=("Segoe UI", 9),
                         fg=TEXT_DARK, bg=bg, width=w, anchor="w"
                         ).pack(side="left", padx=8)

        body.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def destroy(self):
        try:
            self.master.unbind_all("<MouseWheel>")
        except Exception:
            pass
        super().destroy()


# ═══════════════════════════════════════════════════════════════
# Manage Workers Screen
# Admin views, adds, edits, and removes service workers.
# ═══════════════════════════════════════════════════════════════
class ManageWorkersScreen(tk.Frame):
    refresh_restock_requests()
    def __init__(self, master):
        super().__init__(master, bg=BG_MAIN)
        self._editing_id = None
        self._worker_canvas = None
        self._load_workers()
        self._build()
        self.master.bind_all("<MouseWheel>", self._on_scroll)

    def _on_scroll(self, e):
        if self._worker_canvas:
            self._worker_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    def destroy(self):
        try:
            self.master.unbind_all("<MouseWheel>")
        except Exception:
            pass
        super().destroy()

    def _load_workers(self):
        #refresh_restock_requests()
        try:
            self.workers = db_connection.get_all_service_workers()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load workers:\n{e}")
            self.workers = []

    def _build(self):
        screen_header(self, "👷  Manage Workers",
                      self.master.show_home, self.master.machine_info)

        main = tk.Frame(self, bg=BG_MAIN)
        main.pack(fill="both", expand=True, padx=20, pady=16)

        self._left = tk.Frame(main, bg=BG_WHITE,
                              highlightthickness=1, highlightbackground=BORDER)
        self._left.pack(side="left", fill="both", expand=True, padx=(0, 16))

        right = tk.Frame(main, bg=BG_WHITE, width=310,
                         highlightthickness=1, highlightbackground=BORDER)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        self._build_table()
        self._build_form(right)

    def _build_table(self):
        for w in self._left.winfo_children():
            w.destroy()

        pad = tk.Frame(self._left, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(pad, text="Service Workers",
                 font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE).pack(anchor="w")
        tk.Label(pad, text=f"{len(self.workers)} worker(s) assigned to this machine.",
                 font=("Segoe UI", 9), fg=TEXT_LIGHT, bg=BG_WHITE).pack(anchor="w", pady=(2, 10))
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))

        if not self.workers:
            tk.Label(pad, text="No workers found. Add one using the form.",
                     font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=BG_WHITE).pack(pady=24)
            return

        col_hdr = tk.Frame(pad, bg=ACCENT, height=30)
        col_hdr.pack(fill="x")
        col_hdr.pack_propagate(False)
        for h, w in [("ID", 4), ("Name", 15), ("Type", 12), ("Phone", 14), ("Actions", 14)]:
            tk.Label(col_hdr, text=h, font=("Segoe UI", 9, "bold"),
                     fg=BG_WHITE, bg=ACCENT, width=w, anchor="w"
                     ).pack(side="left", padx=6, pady=4)

        canvas = tk.Canvas(pad, bg=BG_WHITE, highlightthickness=0)
        sb = ttk.Scrollbar(pad, orient="vertical", command=canvas.yview)
        body = tk.Frame(canvas, bg=BG_WHITE)

        win_id = canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)

        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(win_id, width=e.width))
        body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self._worker_canvas = canvas

        for i, wk in enumerate(self.workers):
            bg = BG_WHITE if i % 2 == 0 else BG_SIDEBAR
            row = tk.Frame(body, bg=bg, height=36)
            row.pack(fill="x")
            row.pack_propagate(False)

            for val, width in [
                (str(wk["WorkerID"]),              4),
                (wk.get("Name", "")        or "",  15),
                (wk.get("WorkerType", "")  or "",  12),
                (wk.get("PhoneNumber", "") or "",   14),
            ]:
                tk.Label(row, text=val, font=("Segoe UI", 9),
                         fg=TEXT_DARK, bg=bg, width=width, anchor="w"
                         ).pack(side="left", padx=6)

            btn_frame = tk.Frame(row, bg=bg)
            btn_frame.pack(side="left", padx=4)

            tk.Button(btn_frame, text="Edit", font=("Segoe UI", 8),
                      bg=ACCENT_LT, fg=ACCENT, relief="flat", bd=0,
                      cursor="hand2", padx=6, pady=2,
                      command=lambda wk=wk: self._edit_worker(wk)
                      ).pack(side="left", padx=(0, 4))

            tk.Button(btn_frame, text="Remove", font=("Segoe UI", 8),
                      bg=RED_BG, fg=RED, relief="flat", bd=0,
                      cursor="hand2", padx=6, pady=2,
                      command=lambda wk=wk: self._remove_worker(wk)
                      ).pack(side="left")

        body.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _build_form(self, parent):
        pad = tk.Frame(parent, bg=BG_WHITE)
        pad.pack(fill="both", expand=True, padx=20, pady=20)

        self._form_title = tk.Label(pad, text="Add New Worker",
                                    font=("Segoe UI", 13, "bold"), fg=TEXT_DARK, bg=BG_WHITE)
        self._form_title.pack(anchor="w")
        tk.Label(pad, text="* required", font=("Segoe UI", 8),
                 fg=TEXT_LIGHT, bg=BG_WHITE).pack(anchor="w", pady=(0, 4))
        tk.Frame(pad, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))

        self._name_var    = tk.StringVar()
        self._type_var    = tk.StringVar()
        self._phone_var   = tk.StringVar()
        self._email_var   = tk.StringVar()
        self._company_var = tk.StringVar()

        labeled_entry(pad, "Name *", var=self._name_var, bg=BG_WHITE)

        tk.Label(pad, text="Worker Type", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_MID, bg=BG_WHITE).pack(anchor="w", pady=(10, 2))
        self._type_combo = ttk.Combobox(pad, textvariable=self._type_var,
                                        values=["Restocker", "Technician"],
                                        font=("Segoe UI", 10))
        self._type_combo.pack(fill="x", ipady=4)

        labeled_entry(pad, "Phone Number", var=self._phone_var, bg=BG_WHITE)
        labeled_entry(pad, "Email",        var=self._email_var, bg=BG_WHITE)
        labeled_entry(pad, "Company",      var=self._company_var, bg=BG_WHITE)

        self._save_btn = action_button(pad, "Add Worker  ▶", self._save_worker)

        self._cancel_btn = tk.Button(pad, text="Clear Form", font=("Segoe UI", 10),
                                     bg=BG_SIDEBAR, fg=TEXT_MID, relief="flat", bd=0,
                                     cursor="hand2", pady=8, command=self._cancel_edit)
        self._cancel_btn.pack(fill="x", pady=(6, 0))

        self._status_lbl = tk.Label(pad, text="", font=("Segoe UI", 9),
                                    fg=GREEN, bg=BG_WHITE, wraplength=260, justify="left")
        self._status_lbl.pack(anchor="w", pady=(8, 0))

    def _edit_worker(self, worker):
        self._editing_id = worker["WorkerID"]
        self._form_title.configure(text=f"Edit Worker — ID {worker['WorkerID']}")
        self._name_var.set(worker.get("Name", "")        or "")
        self._type_var.set(worker.get("WorkerType", "")  or "")
        self._phone_var.set(worker.get("PhoneNumber", "") or "")
        self._email_var.set(worker.get("Email", "")       or "")
        self._company_var.set(worker.get("Company", "")   or "")
        self._save_btn.configure(text="Save Changes  ▶")
        self._cancel_btn.configure(text="Cancel Edit")
        self._status_lbl.configure(text="")

    def _cancel_edit(self):
        self._editing_id = None
        self._form_title.configure(text="Add New Worker")
        self._name_var.set("")
        self._type_var.set("")
        self._phone_var.set("")
        self._email_var.set("")
        self._company_var.set("")
        self._save_btn.configure(text="Add Worker  ▶")
        self._cancel_btn.configure(text="Clear Form")
        self._status_lbl.configure(text="")

    def _save_worker(self):
        name    = self._name_var.get().strip()
        wtype   = self._type_var.get().strip()
        phone   = self._phone_var.get().strip()
        email   = self._email_var.get().strip()
        company = self._company_var.get().strip()

        if not name:
            messagebox.showwarning("Missing Info", "Worker name is required.")
            return

        try:
            if self._editing_id is None:
                db_connection.add_service_worker(
                    self.master.machine_id, name, wtype, phone, email, company)
                msg = f"✅  Worker '{name}' added."
            else:
                db_connection.update_service_worker(
                    self._editing_id, name, wtype, phone, email, company)
                msg = f"✅  Worker '{name}' updated."
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save worker:\n{e}")
            return

        self._load_workers()
        self._build_table()
        self._cancel_edit()
        self._status_lbl.configure(text=msg)
        refresh_restock_requests()

    # helper function : counts number of worker "type" in  self.workers
    def count_worker(self, workertype):
        count = 0
        for worker in self.workers:
            if worker.get("WorkerType") == workertype:
                count += 1
        return count

    def _remove_worker(self, worker):
        name = worker.get("Name") or f"ID {worker['WorkerID']}"
        if self.count_worker(worker.get("WorkerType")) <= 1:     # check if deleting last of worker. don't allow if so
            messagebox.showwarning("Deletion canceled.", 
                                   f"Database needs at least 1 of each worker type. Add another %s before deleting one." % worker.get("WorkerType"))
            return
        if not messagebox.askyesno("Confirm Remove",
                                   f"Remove worker '{name}'?\n\n"
                                   f"Warning: all maintenance tickets and restock requests "
                                   f"assigned to this worker will also be permanently deleted."):
            return
        try:
            db_connection.delete_service_worker(worker["WorkerID"])
        except Exception as e:
            messagebox.showerror("Cannot Remove Worker",
                                 f"Could not delete worker.\n\nDatabase error:\n{e}")
            return

        self._load_workers()
        self._build_table()
        self._status_lbl.configure(text=f"✅  Worker '{name}' removed.")
        #refresh_restock_requests()


# ── App entry point ─────────────────────────────────────────────
if __name__ == "__main__":
    app = VendingMachineApp()
    # make sure db is correct
    refresh_restock_requests()
    app.mainloop()
