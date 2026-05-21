import frappe


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Dokumen",      "fieldname": "name",     "fieldtype": "Link",
         "options": "Cost Per Portion MBG", "width": 140},
        {"label": "Periode",      "fieldname": "period",   "fieldtype": "Date",   "width": 100},
        {"label": "SPPG Unit",    "fieldname": "sppg_unit","fieldtype": "Data",   "width": 120},
        {"label": "Menu Plan",    "fieldname": "menu_plan","fieldtype": "Data",   "width": 140},
        {"label": "Total Porsi",  "fieldname": "total_portion","fieldtype":"Int", "width": 90},
        {"label": "Biaya Bahan",  "fieldname": "material_cost","fieldtype":"Currency","width":120},
        {"label": "Total Biaya",  "fieldname": "total_cost","fieldtype":"Currency","width":120},
        {"label": "HPP Plan",     "fieldname": "planned_cost_per_portion","fieldtype":"Currency","width":110},
        {"label": "HPP Aktual",   "fieldname": "actual_cost_per_portion", "fieldtype":"Currency","width":110},
        {"label": "Variance",     "fieldname": "hpp_variance","fieldtype":"Currency","width":100},
        {"label": "Margin %",     "fieldname": "margin_pct","fieldtype":"Percent","width":90},
    ]
    conds = ["docstatus >= 0"]
    if filters.get("from_date"):
        conds.append("period >= %(from_date)s")
    if filters.get("to_date"):
        conds.append("period <= %(to_date)s")
    if filters.get("sppg_unit"):
        conds.append("sppg_unit = %(sppg_unit)s")
    data = frappe.db.sql(f"""
        SELECT name, period, sppg_unit, menu_plan, total_portion,
               material_cost, total_cost, planned_cost_per_portion,
               actual_cost_per_portion, hpp_variance, margin_pct
        FROM `tabCost Per Portion MBG`
        WHERE {" AND ".join(conds)}
        ORDER BY period DESC
    """, filters, as_dict=True)
    return columns, data
