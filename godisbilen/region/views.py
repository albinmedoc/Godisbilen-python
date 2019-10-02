from flask_login import current_user
from godisbilen.admin.views import AdminView

class RegionView(AdminView):
    column_searchable_list = ["name"]
    page_size = 50
    can_view_details = True
    create_modal = False
    column_list = ("id", "name", "admins", "area")
    column_labels = {
        "name": "Namn",
        "admins": "Admins",
        "area": "Area"
    }