from flask_login import current_user
from godisbilen.admin.views import AdminView

class LocationView(AdminView):
    column_searchable_list = []
    page_size = 50
    can_view_details = True
    create_modal = False
    column_list = ("id", "street_name", "street_number", "lat", "lng", "region")
    column_labels = {
        "street_name": "Gatunamn",
        "street_number": "Gatunummer",
        "lat": "Latitude",
        "lng": "Longitude",
        "region": "Region",
    }

    def is_visible(self):
        return current_user.is_authenticated and current_user.has_roles("Admin", "Developer")