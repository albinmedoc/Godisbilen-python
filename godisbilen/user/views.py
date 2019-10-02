from godisbilen.admin.views import AdminView

class UserView(AdminView):
    column_searchable_list = ["phone_number"]
    column_sortable_list = ("phone_number",)
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_hide_backrefs = False
    column_list = ("phone_number", "home_adress", "count_orders")
    column_labels = {
        "phone_number": "Telefonnummer",
        "home_adress": "Hemadress",
        "count_orders": "Antal ordrar",
    }
