import frappe


def execute(filters=None):
    filters = filters or {}
    columns = [
        {"label": "Item Code",    "fieldname": "item_code",    "fieldtype": "Link",
         "options": "Item", "width": 140},
        {"label": "Nama Item",    "fieldname": "item_name",    "fieldtype": "Data",     "width": 200},
        {"label": "Warehouse",    "fieldname": "warehouse",    "fieldtype": "Link",
         "options": "Warehouse", "width": 160},
        {"label": "Stok (kg)",    "fieldname": "actual_qty",   "fieldtype": "Float",    "width": 90},
        {"label": "Reorder Level","fieldname": "reorder_level","fieldtype": "Float",    "width": 110},
        {"label": "Kekurangan",   "fieldname": "shortage",     "fieldtype": "Float",    "width": 100},
    ]
    data = frappe.db.sql("""
        SELECT b.item_code, i.item_name, b.warehouse,
               b.actual_qty, i.reorder_level,
               (i.reorder_level - b.actual_qty) AS shortage
        FROM `tabBin` b
        JOIN `tabItem` i ON b.item_code = i.name
        WHERE b.actual_qty < i.reorder_level AND i.disabled = 0
        ORDER BY shortage DESC
    """, as_dict=True)
    return columns, data
