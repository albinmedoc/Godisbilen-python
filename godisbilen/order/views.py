from godisbilen.admin.views import AdminView

class OrderView(AdminView):
    column_searchable_list = ["order_number.number", "order_number.created", "estimated_delivery"]
    column_sortable_list = ["order_number.number", "order_number.created", "estimated_delivery", "completed"]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ("order_number.number", "user", "location", "order_number.created", "estimated_delivery", "completed", "status")
    column_labels = {
        "order_number.number": "Ordernummer",
        "user": "Användare",
        "location": "Adress",
        "order_number.created": "Placerad",
        "estimated_delivery": "Beräknad leverans",
        "completed": "Levererad",
        "status": "Status"
    }