import frappe
from frappe.model.document import Document
from frappe.utils import flt


class MasterMenuMBG(Document):

    def validate(self):
        if not self.menu_items:
            frappe.throw("Menu harus memiliki minimal 1 produk masakan.")
        self.calculate_nutrition()

    def calculate_nutrition(self):
        """Hitung total nilai gizi dari semua produk masakan."""
        total = {"energy": 0, "protein": 0, "fat": 0, "carbo": 0, "sodium": 0}
        for item in self.menu_items:
            if not item.produk:
                continue
            porsi = frappe.db.get_value(
                "Standar Porsi MBG",
                {"produk": item.produk, "sasaran_penerima": self.sasaran_penerima},
                "berat_gram",
            ) or 0
            factor = flt(porsi) / 100
            prod = frappe.db.get_value(
                "Produk Hasil Masakan", item.produk,
                ["energy_per_100g", "protein_per_100g", "fat_per_100g",
                 "carbo_per_100g", "sodium_per_100g"], as_dict=True,
            )
            if prod:
                total["energy"]  += flt(prod.energy_per_100g)  * factor
                total["protein"] += flt(prod.protein_per_100g) * factor
                total["fat"]     += flt(prod.fat_per_100g)     * factor
                total["carbo"]   += flt(prod.carbo_per_100g)   * factor
                total["sodium"]  += flt(prod.sodium_per_100g)  * factor

        self.total_energy_kcal  = round(total["energy"],  2)
        self.total_protein_g    = round(total["protein"], 2)
        self.total_fat_g        = round(total["fat"],     2)
        self.total_carbo_g      = round(total["carbo"],   2)
        self.total_sodium_mg    = round(total["sodium"],  2)
        self._validate_against_akg()

    def _validate_against_akg(self):
        akg = frappe.db.get_value(
            "Angka Kecukupan Gizi",
            {"sasaran_penerima": self.sasaran_penerima, "tipe_layanan": self.service_type},
            ["energi_kcal", "tol_kurang_pct", "tol_lebih_pct"], as_dict=True,
        )
        if not akg or not akg.energi_kcal:
            self.nutrition_status = ""
            return
        ratio = flt(self.total_energy_kcal) / flt(akg.energi_kcal)
        tol_low  = 1 - flt(akg.tol_kurang_pct) / 100
        tol_high = 1 + flt(akg.tol_lebih_pct) / 100
        if tol_low <= ratio <= tol_high:
            self.nutrition_status = "Sesuai"
        elif ratio < tol_low:
            self.nutrition_status = "Kurang"
        else:
            self.nutrition_status = "Melebihi"
