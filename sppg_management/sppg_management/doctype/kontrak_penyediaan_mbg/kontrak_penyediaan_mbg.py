import frappe
from frappe.model.document import Document
from frappe.utils import flt, cint


class KontrakPenyediaanMBG(Document):

    def validate(self):
        self._validate_dates()
        self._validate_konsumen()
        self._calc_totals()

    def _validate_dates(self):
        if self.end_date and self.start_date and self.end_date <= self.start_date:
            frappe.throw("Tanggal berakhir harus lebih besar dari tanggal mulai.")

    def _validate_konsumen(self):
        if self.konsumen:
            status = frappe.db.get_value("Konsumen MBG", self.konsumen, "status")
            if status != "Aktif":
                frappe.msgprint(
                    f"Konsumen {self.konsumen} tidak dalam status Aktif.", alert=True
                )

    def _calc_totals(self):
        total_penerima = sum(cint(d.jumlah_penerima) for d in self.penerima_details)
        self.total_daily_portion = total_penerima
        if self.price_per_portion and self.start_date and self.end_date:
            from frappe.utils import date_diff
            days = date_diff(self.end_date, self.start_date)
            weeks = days / 7
            total_hari = weeks * cint(self.service_days_per_week)
            self.contract_value = (
                flt(self.price_per_portion) * total_penerima * total_hari
            )

    def on_submit(self):
        self._create_sales_order()

    def _create_sales_order(self):
        if self.sales_order:
            return
        customer = frappe.db.get_value("Konsumen MBG", self.konsumen, "customer")
        if not customer:
            return
        so = frappe.new_doc("Sales Order")
        so.customer = customer
        so.transaction_date = self.start_date
        so.delivery_date = self.end_date
        so.custom_kontrak_mbg = self.name
        so.append("items", {
            "item_code": "MBG-SERVICE",
            "qty": self.total_daily_portion,
            "rate": self.price_per_portion,
            "description": f"Layanan MBG - {self.konsumen}",
        })
        try:
            so.insert(ignore_permissions=True)
            self.db_set("sales_order", so.name)
        except Exception:
            pass  # SO creation is optional
