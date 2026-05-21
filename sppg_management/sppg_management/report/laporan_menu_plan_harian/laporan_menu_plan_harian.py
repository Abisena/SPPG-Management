import frappe


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "No. Menu Plan", "fieldname": "name",              "fieldtype": "Link",     "options": "Menu Plan MBG", "width": 140},
        {"label": "Tanggal",       "fieldname": "service_date",      "fieldtype": "Date",     "width": 100},
        {"label": "Konsumen",      "fieldname": "konsumen",          "fieldtype": "Data",     "width": 160},
        {"label": "SPPG Unit",     "fieldname": "sppg_unit",         "fieldtype": "Data",     "width": 120},
        {"label": "Master Menu",   "fieldname": "master_menu",       "fieldtype": "Data",     "width": 160},
        {"label": "Porsi Plan",    "fieldname": "total_portion_plan","fieldtype": "Int",      "width": 100},
        {"label": "Porsi Aktual",  "fieldname": "total_portion_actual","fieldtype":"Int",     "width": 100},
        {"label": "Variance",      "fieldname": "portion_variance",  "fieldtype": "Int",      "width": 80},
        {"label": "Status Stok",   "fieldname": "stock_status",      "fieldtype": "Data",     "width": 120},
        {"label": "Status",        "fieldname": "workflow_state",    "fieldtype": "Data",     "width": 120},
        {"label": "Est. HPP/Porsi","fieldname": "estimated_cost_per_portion","fieldtype":"Currency","width":120},
    ]
    conds = ["docstatus >= 0"]
    if filters.get("service_date"):
        conds.append(f"service_date = %(service_date)s")
    if filters.get("from_date") and filters.get("to_date"):
        conds.append(f"service_date BETWEEN %(from_date)s AND %(to_date)s")
    if filters.get("sppg_unit"):
        conds.append(f"sppg_unit = %(sppg_unit)s")
    if filters.get("konsumen"):
        conds.append(f"konsumen = %(konsumen)s")

    data = frappe.db.sql(f"""
        SELECT name, service_date, konsumen, sppg_unit, master_menu,
               total_portion_plan, total_portion_actual, portion_variance,
               stock_status, workflow_state, estimated_cost_per_portion
        FROM `tabMenu Plan MBG`
        WHERE {" AND ".join(conds)}
        ORDER BY service_date DESC, sppg_unit
    """, filters, as_dict=True)
    return columns, data
