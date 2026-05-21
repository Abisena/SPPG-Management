import frappe
from frappe.model.document import Document
from frappe.utils import flt


class PurchasePlanningMBG(Document):

    def validate(self):
        self._calc_total()

    def _calc_total(self):
        total = 0
        for d in self.purchase_items:
            d.amount = flt(d.required_qty) * flt(d.rate)
            total += d.amount
        self.total_amount = total

    def on_submit(self):
        self._create_material_request()

    def _create_material_request(self):
        if self.material_request:
            return
        mr = frappe.new_doc("Material Request")
        mr.material_request_type = "Purchase"
        mr.transaction_date = self.planning_date
        mr.custom_purchase_planning_mbg = self.name
        for d in self.purchase_items:
            if not d.item_code:
                continue
            mr.append("items", {
                "item_code":      d.item_code,
                "qty":            d.required_qty,
                "uom":            d.uom or "Kg",
                "schedule_date":  self.planning_date,
            })
        if mr.items:
            mr.insert(ignore_permissions=True)
            self.db_set("material_request", mr.name)
