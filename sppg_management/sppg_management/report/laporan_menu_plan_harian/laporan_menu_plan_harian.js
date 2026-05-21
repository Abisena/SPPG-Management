frappe.query_reports["Laporan Menu Plan Harian"] = {
    filters: [
        { fieldname: "from_date", label: "Dari Tanggal", fieldtype: "Date",
          default: frappe.datetime.month_start() },
        { fieldname: "to_date",   label: "Sampai Tanggal", fieldtype: "Date",
          default: frappe.datetime.month_end() },
        { fieldname: "sppg_unit", label: "SPPG Unit",  fieldtype: "Link",
          options: "SPPG Unit" },
        { fieldname: "konsumen",  label: "Konsumen",   fieldtype: "Link",
          options: "Konsumen MBG" },
    ]
};
