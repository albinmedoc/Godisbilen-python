from godisbilen.admin.views import AdminView

class ShortURLView(AdminView):
    column_searchable_list = ["original_url", "short_url", "visits", "created"]
    column_sortable_list = ["original_url", "short_url", "visits", "created"]
    page_size = 50
    can_view_details = True
    create_modal = True
    column_list = ["original_url", "short_url", "visits", "created"]
    column_labels = {
        "original_url": "Mållänk",
        "short_url": "Kort URL",
        "visits": "besökare",
        "created": "skapad",
    }