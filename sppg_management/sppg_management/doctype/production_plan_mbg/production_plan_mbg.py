import frappe
from frappe.model.document import Document
from frappe.utils import now


class ProductionPlanMBG(Document):

    def validate(self):
        if self.finish_datetime and self.start_datetime:
            if self.finish_datetime < self.start_datetime:
                frappe.throw("Waktu selesai tidak boleh lebih awal dari waktu mulai.")

    def on_submit(self):
        self._create_material_issue()

    def _create_material_issue(self):
        """Create Stock Entry Material Issue for ingredients."""
        menu_plan = frappe.get_doc("Menu Plan MBG", self.menu_plan)
        if not menu_plan.menu_plan_details:
            return
        warehouse = menu_plan.warehouse
        if not warehouse:
            return
        se = frappe.new_doc("Stock Entry")
        se.stock_entry_type = "Material Issue"
        se.custom_production_plan_mbg = self.name
        for d in menu_plan.menu_plan_details:
            if d.item_code and d.qty_kg_total:
                se.append("items", {
                    "item_code": d.item_code,
                    "qty":       d.qty_kg_total,
                    "uom":       "Kg",
                    "s_warehouse": warehouse,
                })
        if se.items:
            try:
                se.insert(ignore_permissions=True)
                self.db_set("stock_entry", se.name)
            except Exception as e:
                frappe.log_error(str(e), "Production Plan - Stock Entry Error")
