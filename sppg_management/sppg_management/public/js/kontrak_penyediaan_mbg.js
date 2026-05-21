frappe.ui.form.on("Kontrak Penyediaan MBG", {

    konsumen: function(frm) {
        if (!frm.doc.konsumen) return;
        frappe.db.get_value("Konsumen MBG", frm.doc.konsumen,
            ["sppg_unit", "status", "area_distribusi"],
            function(r) {
                if (r) {
                    frm.set_value("sppg_unit", r.sppg_unit);
                    if (r.status !== "Aktif") {
                        frappe.msgprint({
                            title: __("Peringatan"),
                            message: __("Konsumen {0} tidak dalam status Aktif!", [frm.doc.konsumen]),
                            indicator: "orange"
                        });
                    }
                }
            }
        );
    },

    end_date: function(frm) {
        if (frm.doc.start_date && frm.doc.end_date
                && frm.doc.end_date <= frm.doc.start_date) {
            frappe.msgprint(__("Tanggal berakhir harus lebih besar dari tanggal mulai!"));
            frm.set_value("end_date", "");
        }
    },

    refresh: function(frm) {
        // Auto hitung total porsi dari penerima_details
        if (frm.doc.penerima_details) {
            let total = frm.doc.penerima_details.reduce(
                (s, r) => s + (r.jumlah_penerima || 0), 0
            );
            frm.set_value("total_daily_portion", total);
        }
    }
});

// Recalculate total when child table changes
frappe.ui.form.on("Detail Penerima Manfaat", {
    jumlah_penerima: function(frm) {
        let total = frm.doc.penerima_details.reduce(
            (s, r) => s + (r.jumlah_penerima || 0), 0
        );
        frm.set_value("total_daily_portion", total);
    }
});
