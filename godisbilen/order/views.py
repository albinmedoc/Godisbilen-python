from godisbilen.admin.views import AdminView

class OrderView(AdminView):
    page_size = 50
    can_view_details = True
    column_searchable_list = ["order_number", "location_id"]
    create_modal = True
    edit_modal = True