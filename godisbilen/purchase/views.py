from godisbilen.admin.views import AdminView

class PurchaseView(AdminView):
    column_searchable_list = ["order_number"]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ("order_number", "user", "count_products", "products")