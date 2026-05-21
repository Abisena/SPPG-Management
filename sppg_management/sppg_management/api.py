"""
Whitelisted REST API endpoints for SPPG Management.
Mobile app / external integration ready.
"""
import frappe
from frappe import _
from frappe.utils import today, now


@frappe.whitelist()
def get_owner_dashboard_summary(sppg_unit=None, date=None):
    """
    GET /api/method/sppg_management.sppg_management.api.get_owner_dashboard_summary
    Params: sppg_unit (optional), date (optional, default today)
    Returns: dict of KPI values
    """
    target_date = date or today()
    f_unit = {"sppg_unit": sppg_unit} if sppg_unit else {}

    total_portion = frappe.db.sql("""
        SELECT COALESCE(SUM(total_portion_plan), 0)
        FROM `tabMenu Plan MBG`
        WHERE service_date = %s AND docstatus = 1
        {unit_filter}
    """.format(unit_filter="AND sppg_unit = %(u)s" if sppg_unit else ""),
    {"s": target_date, "u": sppg_unit} if sppg_unit else {"s": target_date})[0][0]

    return {
        "total_portion_today":       int(total_portion or 0),
        "active_contracts":          frappe.db.count("Kontrak Penyediaan MBG",
                                        {**f_unit, "workflow_state": "Kontrak Berjalan"}),
        "ongoing_production":        frappe.db.count("Production Plan MBG",
                                        {**f_unit, "production_date": target_date,
                                         "workflow_state": ["in", ["Menunggu Produksi", "Sedang Produksi"]]}),
        "ongoing_delivery":          frappe.db.count("Delivery Plan MBG",
                                        {**f_unit, "delivery_date": target_date,
                                         "workflow_state": "Dalam Perjalanan"}),
        "delivery_issues":           frappe.db.count("Delivery Plan MBG",
                                        {**f_unit, "delivery_date": target_date,
                                         "workflow_state": "Bermasalah"}),
        "menu_plan_not_confirmed":   frappe.db.count("Menu Plan MBG",
                                        {**f_unit, "service_date": target_date,
                                         "workflow_state": "Draft"}),
        "qc_failed_today":           frappe.db.count("Cooking Batch MBG",
                                        {"status": "QC Failed"}),
    }


@frappe.whitelist()
def get_today_menu_plan(sppg_unit=None):
    """GET /api/method/...get_today_menu_plan"""
    filters = {"service_date": today(), "docstatus": 1}
    if sppg_unit:
        filters["sppg_unit"] = sppg_unit
    return frappe.get_all(
        "Menu Plan MBG",
        filters=filters,
        fields=["name", "konsumen", "total_portion_plan", "stock_status", "workflow_state", "master_menu"],
    )


@frappe.whitelist()
def get_today_production_tasks(sppg_unit=None):
    """GET /api/method/...get_today_production_tasks"""
    filters = {"production_date": today()}
    if sppg_unit:
        filters["sppg_unit"] = sppg_unit
    return frappe.get_all(
        "Production Plan MBG",
        filters=filters,
        fields=["name", "menu_plan", "target_portion", "actual_portion",
                "workflow_state", "cooking_shift", "head_chef"],
    )


@frappe.whitelist()
def get_driver_delivery_tasks(driver=None):
    """GET /api/method/...get_driver_delivery_tasks"""
    if not driver:
        driver = frappe.session.user
    filters = {
        "delivery_date": today(),
        "driver": driver,
        "workflow_state": ["in", ["Siap Kirim", "Dalam Perjalanan"]],
    }
    tasks = frappe.get_all(
        "Delivery Plan MBG",
        filters=filters,
        fields=["name", "total_portion", "planned_departure", "workflow_state", "sppg_unit"],
    )
    for t in tasks:
        t["routes"] = frappe.get_all(
            "Route Delivery",
            filters={"parent": t["name"]},
            fields=["konsumen", "alamat", "jumlah_porsi", "status_titik", "urutan"],
            order_by="urutan asc",
        )
    return tasks


@frappe.whitelist()
def update_delivery_status(delivery_plan, new_status, notes=None):
    """POST /api/method/...update_delivery_status"""
    allowed = ["Siap Kirim", "Dalam Perjalanan", "Diterima", "Bermasalah", "Selesai"]
    if new_status not in allowed:
        frappe.throw(_("Status tidak valid: {0}").format(new_status))
    doc = frappe.get_doc("Delivery Plan MBG", delivery_plan)
    doc.workflow_state = new_status
    if new_status == "Dalam Perjalanan":
        doc.actual_departure = now()
    if new_status == "Diterima":
        doc.return_datetime = now()
    if notes:
        doc.notes = notes
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "ok", "new_state": doc.workflow_state}


@frappe.whitelist()
def submit_pod(delivery_plan, nama_penerima, foto_url=None, catatan=None):
    """POST /api/method/...submit_pod — Submit Proof of Delivery"""
    pod = frappe.new_doc("Proof of Delivery")
    pod.delivery_plan = delivery_plan
    pod.nama_penerima = nama_penerima
    pod.tanggal = today()
    pod.waktu = now()
    if foto_url:
        pod.foto_penerimaan = foto_url
    if catatan:
        pod.catatan = catatan
    pod.insert(ignore_permissions=True)
    frappe.db.set_value("Delivery Plan MBG", delivery_plan, {
        "pod_ref": pod.name,
        "workflow_state": "Diterima",
    })
    frappe.db.commit()
    return {"pod": pod.name}


@frappe.whitelist()
def get_stock_shortage(sppg_unit=None):
    """GET /api/method/...get_stock_shortage — Items below reorder"""
    rows = frappe.db.sql("""
        SELECT b.item_code, i.item_name, b.warehouse,
               b.actual_qty, i.reorder_level,
               (i.reorder_level - b.actual_qty) AS shortage_qty
        FROM `tabBin` b
        JOIN `tabItem` i ON b.item_code = i.name
        WHERE b.actual_qty < i.reorder_level AND i.disabled = 0
        ORDER BY shortage_qty DESC
        LIMIT 50
    """, as_dict=True)
    return rows


@frappe.whitelist()
def generate_production_plan(menu_plan_name):
    """POST /api/method/...generate_production_plan"""
    from sppg_management.sppg_management.doctype.menu_plan_mbg.menu_plan_mbg import (
        generate_production_plan as _gen,
    )
    return _gen(menu_plan_name)


@frappe.whitelist()
def calculate_cost_per_portion(menu_plan_name):
    """POST /api/method/...calculate_cost_per_portion"""
    from sppg_management.sppg_management.doctype.cost_per_portion_mbg.cost_per_portion_mbg import (
        calculate as _calc,
    )
    return _calc(menu_plan_name)
