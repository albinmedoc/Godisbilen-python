from flask_login import current_user
from godisbilen.admin.views import AdminView

class RegionView(AdminView):
    column_searchable_list = ["id", "name"]
    column_sortable_list = ["id", "name"]
    page_size = 50
    can_view_details = True
    create_modal = False
    column_list = ["id", "name", "admins", "center"]
    column_labels = {
        "id": "Id",
        "name": "Namn",
        "admins": "Admins",
        "center": "Center"
    }