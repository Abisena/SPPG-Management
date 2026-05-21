import frappe
from frappe.model.document import Document


class CookingBatchMBG(Document):

    def validate(self):
        if self.finish_time and self.start_time and self.finish_time < self.start_time:
            frappe.throw("Waktu selesai tidak boleh lebih awal dari waktu mulai masak.")

    def on_submit(self):
        pass


def on_submit_handler(doc, method):
    pass
