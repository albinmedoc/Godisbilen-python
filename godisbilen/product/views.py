from godisbilen.admin.views import AdminView

class ProductView(AdminView):
    column_searchable_list = ["title"]
    form_create_rules = ("title", "total")
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ("title", "sold", "stock")