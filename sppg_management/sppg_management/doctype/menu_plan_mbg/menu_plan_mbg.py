import frappe
from frappe.model.document import Document
from frappe.utils import flt, cint


class MenuPlanMBG(Document):

    def validate(self):
        if not self.master_menu:
            frappe.throw("Master Menu wajib dipilih.")
        if cint(self.total_portion_plan) <= 0:
            frappe.throw("Total Porsi Plan harus lebih dari 0.")
        self.calculate_ingredient_requirements()
        self.check_stock_availability()

    def before_submit(self):
        menu_status = frappe.db.get_value("Master Menu MBG", self.master_menu, "status")
        if menu_status != "Aktif":
            frappe.throw(f"Master Menu '{self.master_menu}' belum berstatus Aktif.")

    def on_submit(self):
        self.generate_stock_forecast()

    def calculate_ingredient_requirements(self):
        menu_doc = frappe.get_doc("Master Menu MBG", self.master_menu)
        self.menu_plan_details = []
        total_cost = 0.0
        for item in menu_doc.menu_items:
            std_porsi = frappe.db.get_value(
                "Standar Porsi MBG",
                {"produk": item.produk, "sasaran_penerima": self.sasaran_penerima or ""},
                "berat_gram",
            )
            if not std_porsi:
                std_porsi = frappe.db.get_value(
                    "Standar Porsi MBG",
                    {"produk": item.produk},
                    "berat_gram",
                ) or 100
            item_code = frappe.db.get_value("Produk Hasil Masakan", item.produk, "item_code")
            qty_kg = flt(std_porsi) * cint(self.total_portion_plan) / 1000
            valuation = 0
            if item_code:
                valuation = frappe.db.get_value("Item", item_code, "valuation_rate") or 0
            row_cost = qty_kg * flt(valuation)
            total_cost += row_cost
            self.append("menu_plan_details", {
                "produk":             item.produk,
                "item_code":          item_code or "",
                "qty_gram_per_porsi": std_porsi,
                "qty_kg_total":       round(qty_kg, 3),
                "harga_satuan":       valuation,
                "total_biaya":        round(row_cost, 2),
            })
        self.estimated_material_cost = round(total_cost, 2)
        if cint(self.total_portion_plan) > 0:
            self.estimated_cost_per_portion = round(
                total_cost / cint(self.total_portion_plan), 2
            )

    def check_stock_availability(self):
        shortage = False
        for d in self.menu_plan_details:
            if not d.item_code or not self.warehouse:
                continue
            actual_qty = frappe.db.get_value(
                "Bin",
                {"item_code": d.item_code, "warehouse": self.warehouse},
                "actual_qty",
            ) or 0
            d.available_stock_kg = flt(actual_qty)
            if flt(actual_qty) < flt(d.qty_kg_total):
                shortage = True
                d.stock_status = "Kurang"
            else:
                d.stock_status = "Cukup"
        self.stock_status = "Stock Shortage" if shortage else "Stock Available"

    def generate_stock_forecast(self):
        sf = frappe.new_doc("Stock Forecast MBG")
        sf.menu_plan = self.name
        sf.production_date = self.service_date
        sf.sppg_unit = self.sppg_unit
        sf.warehouse = self.warehouse or ""
        for d in self.menu_plan_details:
            sf.append("forecast_details", {
                "item_code":    d.item_code,
                "required_qty": d.qty_kg_total,
                "available_qty": d.available_stock_kg or 0,
                "stock_status": d.stock_status or "",
            })
        sf.insert(ignore_permissions=True)
        self.db_set("stock_forecast", sf.name)
        if self.stock_status == "Stock Shortage":
            self._create_purchase_planning(sf.name)

    def _create_purchase_planning(self, sf_name):
        pp = frappe.new_doc("Purchase Planning MBG")
        pp.menu_plan = self.name
        pp.stock_forecast = sf_name
        pp.planning_date = self.service_date
        pp.sppg_unit = self.sppg_unit
        for d in self.menu_plan_details:
            if d.stock_status == "Kurang":
                shortage = flt(d.qty_kg_total) - flt(d.available_stock_kg or 0)
                pp.append("purchase_items", {
                    "item_code":   d.item_code,
                    "required_qty": shortage,
                    "uom":         "Kg",
                })
        if pp.purchase_items:
            pp.insert(ignore_permissions=True)


def on_submit_handler(doc, method):
    """Called from hooks doc_events."""
    pass


@frappe.whitelist()
def generate_production_plan(menu_plan_name):
    doc = frappe.get_doc("Menu Plan MBG", menu_plan_name)
    if doc.workflow_state not in ("Sudah Dikonfirmasi",):
        frappe.throw("Menu Plan harus dalam status Sudah Dikonfirmasi.")
    if doc.production_plan:
        frappe.throw(f"Production Plan sudah ada: {doc.production_plan}")
    pp = frappe.new_doc("Production Plan MBG")
    pp.menu_plan = menu_plan_name
    pp.production_date = doc.service_date
    pp.sppg_unit = doc.sppg_unit
    pp.target_portion = doc.total_portion_plan
    pp.workflow_state = "Menunggu Produksi"
    pp.insert(ignore_permissions=True)
    doc.db_set("production_plan", pp.name)
    return pp.name
