import frappe
from frappe.utils import today, add_days


def check_expired_stock():
    """Daily: alert for batches expiring within 7 days."""
    batches = frappe.db.sql("""
        SELECT name, item, expiry_date, warehouse
        FROM `tabBatch`
        WHERE expiry_date BETWEEN %(today)s AND %(future)s
        AND docstatus < 2
    """, {"today": today(), "future": add_days(today(), 7)}, as_dict=True)

    if batches:
        msg = "Bahan mendekati expired dalam 7 hari:<br>"
        for b in batches:
            msg += f"- {b.item} | Batch {b.name} | Exp: {b.expiry_date}<br>"
        frappe.sendmail(
            recipients=frappe.db.get_single_value("SPPG Management Settings", "alert_email") or [],
            subject="[SPPG Alert] Bahan Mendekati Expired",
            message=msg,
        )


def check_critical_stock():
    """Daily: alert for items below reorder level."""
    items = frappe.db.sql("""
        SELECT b.item_code, b.warehouse, b.actual_qty, i.reorder_level
        FROM `tabBin` b
        JOIN `tabItem` i ON b.item_code = i.name
        WHERE b.actual_qty < i.reorder_level
        AND i.disabled = 0
    """, as_dict=True)
    for item in items:
        frappe.logger().warning(
            f"SPPG Critical Stock: {item.item_code} | "
            f"Qty: {item.actual_qty} | Min: {item.reorder_level}"
        )


def auto_complete_contracts():
    """Daily: auto-complete contracts past end_date."""
    contracts = frappe.db.get_all(
        "Kontrak Penyediaan MBG",
        filters={"workflow_state": "Kontrak Berjalan", "end_date": ["<", today()]},
        fields=["name"],
    )
    for c in contracts:
        doc = frappe.get_doc("Kontrak Penyediaan MBG", c.name)
        doc.workflow_state = "Selesai Kontrak"
        doc.save(ignore_permissions=True)
    if contracts:
        frappe.db.commit()
