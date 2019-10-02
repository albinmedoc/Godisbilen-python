from godisbilen.admin.views import AdminView

class ProductView(AdminView):
    column_searchable_list = ["title"]
    column_sortable_list = ("title", "sold", "stock", "total")
    form_create_rules = ("title", "total")
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ("title", "sold", "stock", "total")
    column_labels = {
        "title": "Namn",
        "sold": "Sålda",
        "stock": "Lager",
        "total": "Totalt"
    }