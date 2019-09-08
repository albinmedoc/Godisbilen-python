from godisbilen.admin.views import AdminView

class LocationView(AdminView):
    page_size = 50
    column_searchable_list = ["city", "street", "postal_code", "lat", "lng"]
    can_view_details = True
    create_modal = True
    edit_modal = True