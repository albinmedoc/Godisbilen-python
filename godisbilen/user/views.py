from godisbilen.admin.views import AdminView

class UserView(AdminView):
    column_searchable_list = ["phone_number"]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True