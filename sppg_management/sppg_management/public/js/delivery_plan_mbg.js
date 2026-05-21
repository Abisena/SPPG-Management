frappe.ui.form.on("Delivery Plan MBG", {

    refresh: function(frm) {
        if (!frm.doc.driver || !frm.doc.vehicle) {
            frm.dashboard.add_comment(
                "Driver dan Kendaraan wajib diisi sebelum pengiriman dimulai.",
                "orange", true
            );
        }

        if (frm.doc.workflow_state === "Siap Kirim") {
            frm.add_custom_button(__("Berangkat Sekarang"), function() {
                frappe.call({
                    method: "sppg_management.sppg_management.api.update_delivery_status",
                    args: { delivery_plan: frm.doc.name, new_status: "Dalam Perjalanan" },
                    callback: () => frm.reload_doc()
                });
            }, __("Actions")).addClass("btn-primary");
        }

        if (frm.doc.workflow_state === "Dalam Perjalanan") {
            frm.add_custom_button(__("Upload Proof of Delivery"), function() {
                let d = new frappe.ui.Dialog({
                    title: __("Upload Proof of Delivery"),
                    fields: [
                        { label: "Nama Penerima",    fieldname: "nama",  fieldtype: "Data",         reqd: 1 },
                        { label: "Foto Penerimaan",  fieldname: "foto",  fieldtype: "Attach Image" },
                        { label: "Catatan",          fieldname: "notes", fieldtype: "Small Text" }
                    ],
                    primary_action_label: __("Submit"),
                    primary_action: function(vals) {
                        frappe.call({
                            method: "sppg_management.sppg_management.api.submit_pod",
                            args: {
                                delivery_plan:  frm.doc.name,
                                nama_penerima:  vals.nama,
                                foto_url:       vals.foto,
                                catatan:        vals.notes
                            },
                            callback: function(r) {
                                d.hide();
                                frappe.show_alert({ message: "POD berhasil disimpan", indicator: "green" });
                                frm.reload_doc();
                            }
                        });
                    }
                });
                d.show();
            }, __("Actions")).addClass("btn-success");
        }
    }
});
