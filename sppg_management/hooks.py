def get_item_dashboard():
    return {
        "heatmap": True,
        "heatmap_message": "Pemakaian bahan SPPG",
        "fieldname": "item_code",
        "transactions": [
            {"label": "SPPG", "items": ["Menu Plan MBG", "Stock Forecast MBG", "Purchase Planning MBG"]},
        ],
    }

def get_supplier_dashboard():
    return {
        "fieldname": "supplier",
        "transactions": [
            {"label": "SPPG Buying", "items": ["Purchase Planning MBG", "Supplier Evaluation MBG"]},
        ],
    }
