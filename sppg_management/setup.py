import frappe

def after_install():
    """Create default roles after app install."""
    roles = [
        "SPPG Owner", "SPPG Manager", "Admin SPPG",
        "Ahli Gizi", "Kepala Dapur", "Staff Dapur",
        "Staff Gudang", "Purchasing SPPG", "Finance SPPG",
        "Driver Logistik", "Quality Control SPPG",
    ]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({"doctype": "Role", "role_name": role}).insert()
    frappe.db.commit()
    print("SPPG Management: Roles created.")
