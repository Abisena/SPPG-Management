frappe.ui.form.on("Menu Plan MBG", {

    master_menu: function(frm) {
        if (frm.doc.master_menu && frm.doc.total_portion_plan > 0) {
            frm.call("calculate_ingredient_requirements").then(() => {
                frm.refresh_fields(["menu_plan_details", "estimated_material_cost",
                                    "estimated_cost_per_portion"]);
                frappe.show_alert({ message: "Detail bahan diperbarui", indicator: "green" });
            });
        }
    },

    total_portion_plan: function(frm) {
        if (frm.doc.master_menu) {
            frm.trigger("master_menu");
        }
    },

    refresh: function(frm) {
        // Stock shortage warning
        if (frm.doc.stock_status === "Stock Shortage") {
            frm.dashboard.add_comment(
                "⚠️ STOK TIDAK MENCUKUPI — Beberapa bahan kekurangan stok. Cek detail bahan.",
                "red", true
            );
        }

        // Generate Production Plan button
        if (frm.doc.docstatus === 1 && frm.doc.workflow_state === "Sudah Dikonfirmasi"
                && !frm.doc.production_plan) {
            frm.add_custom_button(__("Generate Production Plan"), function() {
                frappe.call({
                    method: "sppg_management.sppg_management.doctype.menu_plan_mbg"
                            + ".menu_plan_mbg.generate_production_plan",
                    args: { menu_plan_name: frm.doc.name },
                    freeze: true,
                    freeze_message: "Membuat Production Plan...",
                    callback: function(r) {
                        if (r.message) {
                            frappe.show_alert({
                                message: "Production Plan dibuat: " + r.message,
                                indicator: "green"
                            });
                            frm.reload_doc();
                        }
                    }
                });
            }, __("Actions"));
        }

        // Status indicator colour
        frm.set_indicator_formatter("stock_status", function(doc) {
            if (doc.stock_status === "Stock Available") return "green";
            if (doc.stock_status === "Stock Shortage")  return "red";
            return "orange";
        });
    }
});
