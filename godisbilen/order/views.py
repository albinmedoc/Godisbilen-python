from godisbilen.admin.views import AdminView

class OrderView(AdminView):
    column_searchable_list = ["order_number", "phase"]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ("order_number", "user", "location", "placed", "estimated_time", "completed", "status")