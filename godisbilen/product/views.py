from godisbilen.admin.views import AdminView

class ProductView(AdminView):
    column_searchable_list = ["title"]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ("title", "stock")