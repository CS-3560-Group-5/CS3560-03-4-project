import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Update 4/23/2026 - Connect to database
import db_connection
#----

# ── Color palette ──────────────────────────────────────────────
# Define consistent colors used throughout the UI
BG_DARK    = "#1a1a2e"  # Main dark background
BG_PANEL   = "#16213e"  # Slightly lighter panel background
BG_CARD    = "#0f3460"  # Card/tile background color
ACCENT     = "#e94560"  # Primary accent color (red-pink) for headers and buttons
ACCENT2    = "#f5a623"  # Secondary accent color (orange) for prices and highlights
TEXT_WHITE = "#ffffff"  # Primary text color
TEXT_GRAY  = "#a0aec0"  # Secondary/muted text color
GREEN      = "#48bb78"  # Status OK and success messages
RED        = "#fc8181"  # Status EMPTY and error messages
BTN_HOVER  = "#c73652"  # Button hover state color

# ═══════════════════════════════════════════════════════════════
# Main application class — manages the window and screen navigation
# Extends tk.Tk to serve as the root window
# ═══════════════════════════════════════════════════════════════
class VendingMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Vending Machine System")
        self.geometry("900x680")
        self.resizable(False, False)  # Fixed window size for consistent layout
        self.configure(bg=BG_DARK)
        self.current_frame = None  # Tracks the currently displayed screen

        # Update 4/23/2026 - Load machine info from database on startup
        try:
            self.machine_info = db_connection.get_machine_info()
            self.machine_id = self.machine_info["MachineID"]
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not connect to database:\n{e}")
            self.machine_info = None
            self.machine_id = 1
        #----

        self.show_home()           # Start on the home screen

    def switch_frame(self, FrameClass, **kwargs):
        """Destroys the current screen and replaces it with a new one."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = FrameClass(self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    # Navigation methods — called by buttons to switch between screens
    def show_home(self):        self.switch_frame(HomeScreen)
    def show_record_sale(self): self.switch_frame(RecordSaleScreen)
    def show_inventory(self):   self.switch_frame(UpdateInventoryScreen)


# ═══════════════════════════════════════════════════════════════
# Home Screen — the main menu shown when the app launches
# Displays two action buttons: Record Sale and Update Inventory
# ═══════════════════════════════════════════════════════════════
class HomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self._build()

    def _build(self):
        """Builds the header bar and two large navigation buttons."""
        # Top header bar with machine name and current date
        hdr = tk.Frame(self, bg=BG_PANEL, height=80)
        hdr.pack(fill="x")
        tk.Label(hdr, text="🏪  VENDING MACHINE SYSTEM",
                 font=("Courier", 20, "bold"), fg=ACCENT, bg=BG_PANEL
                 ).pack(side="left", padx=24, pady=20)
        tk.Label(hdr, text=f"Machine ID: VM-001  |  {datetime.now().strftime('%Y-%m-%d')}",
                 font=("Courier", 10), fg=TEXT_GRAY, bg=BG_PANEL
                 ).pack(side="right", padx=24)
        
        # Update 4/23/2026 - Display machine model from database instead of hardcoded ID
        machine = self.master.machine_info
        if machine:
            info_text = f"Machine: {machine['ModelNumber']}  |  {datetime.now().strftime('%Y-%m-%d')}"
        else:
            info_text = f"Machine: N/A  |  {datetime.now().strftime('%Y-%m-%d')}"
        tk.Label(hdr, text=info_text,
                 font=("Courier", 10), fg=TEXT_GRAY, bg=BG_PANEL
                 ).pack(side="right", padx=24)
        #----

        # Center body with action selection label and buttons
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(expand=True)
        tk.Label(body, text="Select an Action",
                 font=("Courier", 16), fg=TEXT_WHITE, bg=BG_DARK
                 ).pack(pady=(60, 40))

        # Create the two main action buttons
        self._big_btn(body, "💳  Record Sale",      "Customer purchases a product",   self.master.show_record_sale)
        tk.Frame(body, height=20, bg=BG_DARK).pack()  # Spacer between buttons
        self._big_btn(body, "📦  Update Inventory", "Restocker updates machine slots", self.master.show_inventory)

    def _big_btn(self, parent, title, subtitle, cmd):
        """Creates a large clickable card button with title, subtitle, and hover effect."""
        card = tk.Frame(parent, bg=BG_CARD, cursor="hand2", width=420, height=90)
        card.pack_propagate(False)
        card.pack()
        tk.Label(card, text=title,    font=("Courier", 14, "bold"), fg=TEXT_WHITE, bg=BG_CARD).pack(anchor="w", padx=20, pady=(18, 2))
        tk.Label(card, text=subtitle, font=("Courier", 10),         fg=TEXT_GRAY,  bg=BG_CARD).pack(anchor="w", padx=20)

        # Bind click event to the card and all child labels
        card.bind("<Button-1>", lambda e: cmd())
        for w in card.winfo_children():
            w.bind("<Button-1>", lambda e: cmd())

        # Hover effect: highlight card red on mouse enter, restore on leave
        card.bind("<Enter>", lambda e: card.configure(bg=ACCENT))
        card.bind("<Leave>", lambda e: card.configure(bg=BG_CARD))


# ═══════════════════════════════════════════════════════════════
# Use Case 1: Record Sale Screen
# Allows a customer to select a product, choose a payment method
# (cash or card), and process the transaction with receipt output
# ═══════════════════════════════════════════════════════════════
class RecordSaleScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self.selected   = None              # Currently selected product dict
        self.payment    = tk.StringVar(value="cash")  # Payment method selection
        self.cash_given = tk.DoubleVar()    # Amount of cash entered by customer

        # Update 4/23/2026 - Load products from database instead of hardcoded PRODUCTS list
        try:
            self.products = db_connection.get_all_products_with_slots()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load products:\n{e}")
            self.products = []
        #----
        
        self._build()

    def _build(self):
        """Builds the full Record Sale layout: header, product grid, and sale panel."""
        self._header()
        main = tk.Frame(self, bg=BG_DARK)
        main.pack(fill="both", expand=True, padx=16, pady=10)

        # Split layout: product grid on left, order/payment panel on right
        left  = tk.Frame(main, bg=BG_DARK)
        right = tk.Frame(main, bg=BG_DARK, width=300)
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="y", padx=(10, 0))

        self._product_grid(left)
        self._sale_panel(right)

    def _header(self):
        """Builds the top navigation bar with a Back button and screen title."""
        hdr = tk.Frame(self, bg=BG_PANEL)
        hdr.pack(fill="x")
        tk.Button(hdr, text="← Back", font=("Courier", 10), bg=BG_PANEL, fg=TEXT_GRAY,
                  bd=0, cursor="hand2", command=self.master.show_home).pack(side="left", padx=14, pady=14)
        tk.Label(hdr, text="💳  RECORD SALE", font=("Courier", 16, "bold"),
                 fg=ACCENT, bg=BG_PANEL).pack(side="left", padx=4, pady=14)

    def _product_grid(self, parent):
        """Builds the 4-column product grid showing all 12 machine slots."""
        tk.Label(parent, text="Select Product", font=("Courier", 11, "bold"),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w", pady=(4, 6))
        grid_frame = tk.Frame(parent, bg=BG_DARK)
        grid_frame.pack(fill="both", expand=True)

        # Update 4/23/2026 - Uses self.products from database instead of PRODUCTS
        for i, p in enumerate(self.products):
            r, c = divmod(i, 4)
            self._product_tile(grid_frame, p, r, c)
        for c in range(4):
            grid_frame.grid_columnconfigure(c, weight=1)
        #----

    def _product_tile(self, parent, p, row, col):
        """Creates a single product tile showing code, name, price, and stock status.
        Sold-out items are grayed out and non-clickable."""
        is_empty = p["count"] == 0
        # Update 4/23/2026 - Also checks for empty slots (no product assigned)
        is_empty = p["count"] == 0 or p["name"] == "Empty"
        #----
        bg = "#2d3748" if is_empty else BG_CARD  # Gray out sold-out tiles

        tile = tk.Frame(parent, bg=bg, width=130, height=100,
                        highlightbackground=BG_DARK, highlightthickness=2)
        tile.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
        tile.grid_propagate(False)
        parent.grid_columnconfigure(col, weight=1)

        # Display slot code (e.g. A1), product name, price, and quantity
        tk.Label(tile, text=p["code"], font=("Courier", 10, "bold"), fg=ACCENT2, bg=bg).place(x=6, y=4)
        tk.Label(tile, text=p["name"], font=("Courier", 9, "bold"),
                 fg=TEXT_WHITE if not is_empty else TEXT_GRAY,
                 bg=bg, wraplength=110, justify="center").place(relx=0.5, rely=0.42, anchor="center")
        tk.Label(tile, text=f"${p['price']:.2f}", font=("Courier", 10),
                 fg=GREEN if not is_empty else TEXT_GRAY, bg=bg).place(relx=0.5, rely=0.75, anchor="center")

        if is_empty:
            # Update 4/23/2026 - Show EMPTY for unassigned slots, SOLD OUT for zero stock
            label = "EMPTY" if p["name"] == "Empty" else "SOLD OUT"
            tk.Label(tile, text=label, font=("Courier", 7, "bold"), fg=RED, bg=bg).place(relx=0.5, rely=0.9, anchor="center")
            #----
        else:
            # Show remaining quantity and bind click to select this product
            tk.Label(tile, text=f"Qty: {p['count']}", font=("Courier", 7), fg=TEXT_GRAY, bg=bg).place(relx=0.95, rely=0.96, anchor="se")
            tile.bind("<Button-1>", lambda e, prod=p: self._select(prod))
            for w in tile.winfo_children():
                w.bind("<Button-1>", lambda e, prod=p: self._select(prod))

    def _sale_panel(self, parent):
        """Builds the right-side panel: order summary, payment method, and process button."""
        # Order summary section — updates when a product is selected
        tk.Label(parent, text="Order Summary", font=("Courier", 11, "bold"),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w")
        self.summary_frame = tk.Frame(parent, bg=BG_PANEL, width=280, height=110)
        self.summary_frame.pack(fill="x", pady=(4, 12))
        self.summary_frame.pack_propagate(False)
        self._refresh_summary()

        # Payment method radio buttons (Cash or Card)
        tk.Label(parent, text="Payment Method", font=("Courier", 11, "bold"),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w")
        pf = tk.Frame(parent, bg=BG_DARK)
        pf.pack(fill="x", pady=(4, 12))
        for val, label in [("cash", "💵 Cash"), ("card", "💳 Card")]:
            tk.Radiobutton(pf, text=label, variable=self.payment, value=val,
                           font=("Courier", 10), fg=TEXT_WHITE, bg=BG_DARK,
                           selectcolor=BG_CARD, activebackground=BG_DARK,
                           activeforeground=TEXT_WHITE,
                           command=self._refresh_payment).pack(side="left", padx=8)

        # Cash input field — shown when cash payment is selected
        self.cash_frame = tk.Frame(parent, bg=BG_DARK)
        self.cash_frame.pack(fill="x", pady=(0, 8))
        tk.Label(self.cash_frame, text="Cash Given ($)", font=("Courier", 10),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w")
        self.cash_entry = tk.Entry(self.cash_frame, textvariable=self.cash_given,
                                   font=("Courier", 12), bg=BG_CARD,
                                   fg=TEXT_WHITE, insertbackground=TEXT_WHITE, bd=0)
        self.cash_entry.pack(fill="x", ipady=6, pady=2)

        # Card input field — shown when card payment is selected
        self.card_frame = tk.Frame(parent, bg=BG_DARK)
        tk.Label(self.card_frame, text="Card Number (last 4)", font=("Courier", 10),
                 fg=TEXT_GRAY, bg=BG_DARK).pack(anchor="w")
        self.card_entry = tk.Entry(self.card_frame, font=("Courier", 12),
                                   bg=BG_CARD, fg=TEXT_WHITE,
                                   insertbackground=TEXT_WHITE, bd=0)
        self.card_entry.pack(fill="x", ipady=6, pady=2)
        self._refresh_payment()  # Show correct input field on load

        # Process Sale button — triggers payment validation and receipt generation
        tk.Button(parent, text="PROCESS SALE ▶", font=("Courier", 12, "bold"),
                  bg=ACCENT, fg=TEXT_WHITE, bd=0, activebackground=BTN_HOVER,
                  cursor="hand2", pady=12, command=self._process_sale).pack(fill="x", pady=(10, 0))

        # Receipt label — displays transaction result after processing
        self.receipt_label = tk.Label(parent, text="", font=("Courier", 9),
                                      fg=GREEN, bg=BG_DARK, justify="left", wraplength=270)
        self.receipt_label.pack(anchor="w", pady=(10, 0))

    def _refresh_summary(self):
        """Updates the order summary panel based on the currently selected product."""
        for w in self.summary_frame.winfo_children():
            w.destroy()  # Clear previous summary content

        if not self.selected:
            # Show placeholder if no product has been selected yet
            tk.Label(self.summary_frame, text="No product selected",
                     font=("Courier", 10), fg=TEXT_GRAY, bg=BG_PANEL).pack(expand=True)
        else:
            # Calculate tax (9.5%) and total, then display each line item
            p = self.selected
            tax = round(p["price"] * 0.095, 2)
            total = round(p["price"] + tax, 2)
            for label, val in [("Product:", p["name"]), ("Code:", p["code"]),
                                ("Price:", f"${p['price']:.2f}"), ("Tax:", f"${tax:.2f}"),
                                ("TOTAL:", f"${total:.2f}")]:
                row = tk.Frame(self.summary_frame, bg=BG_PANEL)
                row.pack(fill="x", padx=10, pady=1)
                tk.Label(row, text=label, font=("Courier", 9), fg=TEXT_GRAY,
                         bg=BG_PANEL, width=10, anchor="w").pack(side="left")
                # Highlight the TOTAL row in orange
                tk.Label(row, text=val,
                         font=("Courier", 9, "bold" if label == "TOTAL:" else "normal"),
                         fg=ACCENT2 if label == "TOTAL:" else TEXT_WHITE,
                         bg=BG_PANEL).pack(side="left")

    def _refresh_payment(self):
        """Shows the cash input or card input field based on the selected payment method."""
        if self.payment.get() == "cash":
            self.cash_frame.pack(fill="x", pady=(0, 8))
            self.card_frame.pack_forget()
        else:
            self.card_frame.pack(fill="x", pady=(0, 8))
            self.cash_frame.pack_forget()

    def _select(self, prod):
        """Handles product tile click — sets selected product and refreshes summary."""
        self.selected = prod
        self.receipt_label.configure(text="")  # Clear any previous receipt
        self._refresh_summary()

    def _process_sale(self):
        """Validates payment and processes the sale. Generates a receipt on success.
        For cash: checks sufficient funds and calculates change.
        For card: validates last 4 digits of card number."""
        if not self.selected:
            messagebox.showwarning("No Selection", "Please select a product first.")
            return

        p = self.selected
        tax   = round(p["price"] * 0.095, 2)
        total = round(p["price"] + tax, 2)

        if self.payment.get() == "cash":
            given = self.cash_given.get()
            # Reject payment if cash given is less than total due
            if given < total:
                messagebox.showerror("Insufficient Funds", f"Cash ${given:.2f} < total ${total:.2f}.")
                return
            change = round(given - total, 2)
            receipt_extra = f"Cash Given:  ${given:.2f}\nChange:      ${change:.2f}"
        else:
            last4 = self.card_entry.get().strip()
            # Validate that exactly 4 numeric digits were entered
            if not last4.isdigit() or len(last4) != 4:
                messagebox.showerror("Card Error", "Enter valid last 4 digits.")
                return
            receipt_extra = f"Card:        xxxx-{last4}\nCard Fee:    $0.00"

         # Update 4/23/2026 - Record transaction in database and update inventory
        try:
            # Record the transaction in the database
            if self.payment.get() == "cash":
                sale_num = db_connection.record_cash_sale(
                    product_id=p["product_id"],
                    machine_id=self.master.machine_id,
                    tax=tax,
                    cash_given=self.cash_given.get()
                )
            else:
                sale_num = db_connection.record_card_sale(
                    product_id=p["product_id"],
                    machine_id=self.master.machine_id,
                    tax=tax,
                    card_fee=0.00,
                    account_charged=f"xxxx-{last4}"
                )

            # Decrement the product count in the database
            new_count = p["count"] - 1
            db_connection.update_slot_count(p["code"], new_count)

            # Check if restock is needed after this sale
            db_connection.check_and_create_restock_request(p["code"])

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not record sale:\n{e}")
            return

        # Update local data to reflect the sale
        p["count"] = new_count
        #----

        # Display the formatted receipt in the receipt label
        self.receipt_label.configure(text=(
            f"✅ SALE APPROVED\n{'─'*32}\n"
            f"Sale #:      {sale_num}\n"
            f"Product:     {p['name']} ({p['code']})\n"
            f"Price:       ${p['price']:.2f}\n"
            f"Tax:         ${tax:.2f}\n"
            f"Total:       ${total:.2f}\n"
            f"{receipt_extra}\n{'─'*32}\n"
            f"Time: {datetime.now().strftime('%H:%M:%S')}\nThank you!"
        ))

        # Reset selection after successful sale
        self.selected = None
        self._refresh_summary()


# ═══════════════════════════════════════════════════════════════
# Use Case 2: Update Inventory Screen
# Allows a restocker (service worker) to view current stock levels
# for all machine slots and add quantities to restock them
# ═══════════════════════════════════════════════════════════════
class UpdateInventoryScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG_DARK)
        self.restock_vars = {}  # Stores IntVar for each slot's "Add Qty" input

        # Update 4/23/2026 - Load products from database instead of hardcoded PRODUCTS list
        try:
            self.products = db_connection.get_all_products_with_slots()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load inventory:\n{e}")
            self.products = []
        #----

        self._build()

    def _build(self):
        """Builds all sections of the inventory screen in order."""
        self._header()
        self._worker_bar()
        self._table()
        self._footer()

    def _header(self):
        """Builds the top navigation bar with Back button, title, and machine ID."""
        hdr = tk.Frame(self, bg=BG_PANEL)
        hdr.pack(fill="x")
        tk.Button(hdr, text="← Back", font=("Courier", 10), bg=BG_PANEL, fg=TEXT_GRAY,
                  bd=0, cursor="hand2", command=self.master.show_home).pack(side="left", padx=14, pady=14)
        tk.Label(hdr, text="📦  UPDATE INVENTORY", font=("Courier", 16, "bold"),
                 fg=ACCENT, bg=BG_PANEL).pack(side="left", padx=4, pady=14)
        tk.Label(hdr, text="Machine: VM-001", font=("Courier", 10),
                 fg=TEXT_GRAY, bg=BG_PANEL).pack(side="right", padx=20)
        
        # Update 4/23/2026 - Display machine model from database instead of hardcoded VM-001
        machine = self.master.machine_info
        machine_text = f"Machine: {machine['ModelNumber']}" if machine else "Machine: N/A"
        tk.Label(hdr, text=machine_text, font=("Courier", 10),
                 fg=TEXT_GRAY, bg=BG_PANEL).pack(side="right", padx=20)
        #----

    def _worker_bar(self):
        """Displays the logged-in restocker ID and current date/time."""
        bar = tk.Frame(self, bg=BG_CARD, height=36)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        # Update 4/23/2026 - Load restocker info from database instead of hardcoded WORKER_ID
        try:
            workers = db_connection.get_service_workers()
            worker_name = workers[0]["Name"] if workers else "Unknown"
            worker_id = workers[0]["WorkerID"] if workers else "N/A"
        except Exception:
            worker_name = "Unknown"
            worker_id = "N/A"
        tk.Label(bar, text=f"👷 Restocker: {worker_name} (ID: {worker_id})   |   Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                 font=("Courier", 10), fg=ACCENT2, bg=BG_CARD).pack(side="left", padx=16, pady=8)
        #----

    def _table(self):
        """Builds the inventory table with a header row and one row per product slot."""
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True, padx=16, pady=10)

        # Column header row
        hdr_row = tk.Frame(container, bg=BG_CARD, height=32)
        hdr_row.pack(fill="x")
        hdr_row.pack_propagate(False)
        for h, w in zip(["Slot", "Product Name", "Current", "Max", "Add Qty", "Status"],
                         [6,      20,              9,         6,     9,          10]):
            tk.Label(hdr_row, text=h, font=("Courier", 9, "bold"),
                     fg=ACCENT2, bg=BG_CARD, width=w, anchor="w").pack(side="left", padx=6, pady=6)

        # Update 4/23/2026 - Uses self.products from database instead of PRODUCTS
        for i, p in enumerate(self.products):
            self._table_row(container, p, i)
        #----

    def _table_row(self, parent, p, idx):
        """Creates a single inventory row showing slot info and a quantity input field.
        Alternates row background for readability. Status is color-coded:
        GREEN = OK (>40% full), ORANGE = LOW (>0%), RED = EMPTY (0 count)."""
        # Alternate row background color for readability
        bg = BG_PANEL if idx % 2 == 0 else BG_DARK

        # Calculate fill percentage to determine status label and color
        # Update 4/23/2026 - Handle empty slots where max could be 0
        max_amt = p["max"] if p["max"] else 1
        pct = p["count"] / max_amt if max_amt > 0 else 0
        #----
        status_color = GREEN if pct > 0.4 else (ACCENT2 if pct > 0 else RED)
        status_text  = "OK" if pct > 0.4 else ("LOW" if pct > 0 else "EMPTY")

        row = tk.Frame(parent, bg=bg, height=36)
        row.pack(fill="x")
        row.pack_propagate(False)

        # Display slot code, product name, current count, and max capacity
        for val, w in zip([p["code"], p["name"], str(p["count"]), str(p["max"])],
                           [6,         20,         9,               6]):
            tk.Label(row, text=val, font=("Courier", 10),
                     fg=TEXT_WHITE, bg=bg, width=w, anchor="w").pack(side="left", padx=6)

        # Integer input field for how many units the restocker wants to add
        var = tk.IntVar(value=0)
        self.restock_vars[p["code"]] = var  # Store reference for later retrieval
        tk.Entry(row, textvariable=var, font=("Courier", 10),
                 bg=BG_CARD, fg=TEXT_WHITE, insertbackground=TEXT_WHITE,
                 bd=0, width=5).pack(side="left", padx=6, ipady=3)

        # Color-coded status label
        tk.Label(row, text=status_text, font=("Courier", 9, "bold"),
                 fg=status_color, bg=bg, width=10, anchor="w").pack(side="left", padx=6)

    def _footer(self):
        """Builds the bottom bar with the Apply Restock button and status message label."""
        footer = tk.Frame(self, bg=BG_PANEL, height=60)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        # Apply Restock button — triggers validation and inventory update
        tk.Button(footer, text="APPLY RESTOCK ▶", font=("Courier", 12, "bold"),
                  bg=ACCENT, fg=TEXT_WHITE, bd=0, cursor="hand2",
                  activebackground=BTN_HOVER, padx=20,
                  command=self._apply_restock).pack(side="right", padx=20, pady=12)

        # Status label — shows success message or stays blank
        self.status_label = tk.Label(footer, text="", font=("Courier", 10),
                                     fg=GREEN, bg=BG_PANEL)
        self.status_label.pack(side="left", padx=20, pady=12)

    def _apply_restock(self):
        """Validates all Add Qty inputs and applies restock to matching slots.
        Rejects negative quantities and quantities that exceed slot maximum.
        Logs a unique restock ID on success and refreshes the inventory table."""
        updated = []  # Tracks successfully restocked slot codes
        errors  = []  # Tracks validation error messages

        # Update 4/23/2026 - Uses self.products from database instead of PRODUCTS
        for p in self.products:
        #----
            add = self.restock_vars[p["code"]].get()  # Get quantity to add for this slot

            # Skip slots with no quantity entered
            if add == 0:
                continue

            # Reject negative input
            if add < 0:
                errors.append(f"{p['code']}: negative quantity")
                continue

            # Reject if new total would exceed the slot's maximum capacity
            new_count = p["count"] + add
            if new_count > p["max"]:
                errors.append(f"{p['code']}: exceeds max ({p['max']})")
                continue

            # Apply the restock and reset the input field
            # Update 4/23/2026 - Write restock to database instead of just updating local data
            try:
                db_connection.update_slot_count(p["code"], new_count)
                updated.append(p["code"])
                self.restock_vars[p["code"]].set(0)
            except Exception as e:
                errors.append(f"{p['code']}: database error - {e}")
            #----

        # Show errors if any validation failed
        if errors:
            messagebox.showerror("Restock Errors", "\n".join(errors))
            return

        # Inform user if no quantities were entered
        if not updated:
            self.status_label.configure(text="No changes made.", fg=TEXT_GRAY)
            return

        # Generate unique restock log ID using current timestamp
        # Update 4/23/2026 - Updated success message to reflect database write
        self.status_label.configure(
            text=f"✅ Restock complete: {len(updated)} slot(s) updated in database.", fg=GREEN)
        #----

        # Refresh the inventory screen to reflect updated counts
        self.destroy()
        self.master.show_inventory()


# ── App entry point ─────────────────────────────────────────────
# Only runs when this file is executed directly (not imported)
if __name__ == "__main__":
    app = VendingMachineApp()
    app.mainloop()
