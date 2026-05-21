import frappe
from frappe.model.document import Document
from frappe.utils import flt, cint


class CostPerPortionMBG(Document):

    def validate(self):
        self._calculate()

    def _calculate(self):
        self.total_cost = (
            flt(self.material_cost) + flt(self.packaging_cost) +
            flt(self.energy_cost)   + flt(self.transport_cost) +
            flt(self.labor_cost)    + flt(self.waste_cost) +
            flt(self.overhead_cost)
        )
        if cint(self.total_portion) > 0:
            self.actual_cost_per_portion = round(
                self.total_cost / cint(self.total_portion), 2
            )
        else:
            self.actual_cost_per_portion = 0
        self.hpp_variance = flt(self.actual_cost_per_portion) - flt(self.planned_cost_per_portion)
        self.gross_margin = flt(self.selling_price) - flt(self.actual_cost_per_portion)
        if flt(self.selling_price) > 0:
            self.margin_pct = (self.gross_margin / flt(self.selling_price)) * 100
        else:
            self.margin_pct = 0


def calculate(menu_plan_name):
    """Called from api.py"""
    menu_plan = frappe.get_doc("Menu Plan MBG", menu_plan_name)
    if frappe.db.exists("Cost Per Portion MBG", {"menu_plan": menu_plan_name}):
        return frappe.db.get_value("Cost Per Portion MBG", {"menu_plan": menu_plan_name}, "name")

    # Gather transport cost from delivery plan
    transport_cost = 0
    delivery_name = frappe.db.get_value("Pemorsian MBG", {"menu_plan": menu_plan_name}, "delivery_plan")
    if delivery_name:
        transport_cost = frappe.db.get_value("Delivery Plan MBG", delivery_name, "transport_cost") or 0

    # Gather material cost from stock entries
    se_total = frappe.db.sql("""
        SELECT COALESCE(SUM(total_amount), 0)
        FROM `tabStock Entry`
        WHERE custom_production_plan_mbg IN (
            SELECT name FROM `tabProduction Plan MBG` WHERE menu_plan = %s
        ) AND docstatus = 1
    """, menu_plan_name)[0][0] or menu_plan.estimated_material_cost

    total_portion = frappe.db.get_value("Pemorsian MBG",
        {"menu_plan": menu_plan_name}, "actual_portion") or menu_plan.total_portion_plan

    cpp = frappe.new_doc("Cost Per Portion MBG")
    cpp.menu_plan = menu_plan_name
    cpp.period    = menu_plan.service_date
    cpp.sppg_unit = menu_plan.sppg_unit
    cpp.total_portion    = total_portion
    cpp.material_cost    = se_total
    cpp.transport_cost   = transport_cost
    cpp.selling_price    = menu_plan.price_per_portion or 0
    cpp.insert(ignore_permissions=True)
    return cpp.name
