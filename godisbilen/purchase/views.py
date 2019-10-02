from flask_login import current_user
from godisbilen.admin.views import AdminView

class PurchaseView(AdminView):
    column_searchable_list = ["order_number"]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ("order_number", "user", "count_products", "products")
    column_hide_backrefs = False
    column_labels = {
        "order_number": "Ordernummer",
        "user": "Användare",
        "count_products": "Antal produkter",
        "products": "Produkter"
    }

    def is_visible(self):
        return current_user.is_authenticated and current_user.has_roles("Developer")