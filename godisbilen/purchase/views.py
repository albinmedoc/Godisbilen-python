from godisbilen.admin.views import AdminView

class PurchaseView(AdminView):
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True