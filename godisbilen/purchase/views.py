from godisbilen.admin.views import AdminView
from godisbilen.purchase import Purchase
from godisbilen.user import User

class PurchaseView(AdminView):
    column_searchable_list = [User.phone_number]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_hide_backrefs = False
    column_select_related_list = (Purchase.user, Purchase.products)
    column_list = ("id", "user", "count_products", "products")