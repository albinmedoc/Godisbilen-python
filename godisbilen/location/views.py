from godisbilen.admin.views import AdminView

class LocationView(AdminView):
    column_searchable_list = ["city", "street", "postal_code", "lat", "lng"]
    form_create_rules = ("city", "street", "street_number", "postal_code", "lat", "lng")
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True