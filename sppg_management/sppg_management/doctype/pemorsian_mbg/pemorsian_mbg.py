import frappe
from frappe.model.document import Document
from frappe.utils import cint


class PemorsianMBG(Document):

    def validate(self):
        self.portion_variance = cint(self.actual_portion) - cint(self.target_portion)

    def on_submit(self):
        self._update_menu_plan()
        self._create_delivery_plan()

    def _update_menu_plan(self):
        if self.menu_plan:
            frappe.db.set_value("Menu Plan MBG", self.menu_plan, {
                "total_portion_actual": self.actual_portion,
                "portion_variance":     self.portion_variance,
            })

    def _create_delivery_plan(self):
        if self.delivery_plan:
            return
        dp = frappe.new_doc("Delivery Plan MBG")
        dp.pemorsian = self.name
        dp.delivery_date = self.portioning_date
        menu_plan_doc = frappe.get_doc("Menu Plan MBG", self.menu_plan)
        dp.sppg_unit   = menu_plan_doc.sppg_unit
        dp.total_portion = self.actual_portion
        dp.workflow_state = "Draft"
        dp.insert(ignore_permissions=True)
        self.db_set("delivery_plan", dp.name)


def on_submit_handler(doc, method):
    pass
