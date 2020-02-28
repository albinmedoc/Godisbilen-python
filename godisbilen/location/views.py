from flask_login import current_user
from godisbilen.admin.views import AdminView

class LocationView(AdminView):
    column_searchable_list = ["id", "region.name"]
    column_sortable_list = ["id", "region.name", "lat", "lng", "count_orders"]
    page_size = 50
    can_view_details = True
    create_modal = False
    column_list = ["id", "street_name", "street_number", "formatted_address", "lat", "lng", "region.name", "count_orders"]
    column_labels = {
        "id": "Id",
        "street_name": "Gatunamn",
        "street_number": "Gatunummer",
        "formatted_address": "Formaterad adress",
        "lat": "Latitude",
        "lng": "Longitude",
        "region.name": "Region",
        "count_orders": "Antal ordrar"
    }

    def is_visible(self):
        return current_user.is_authenticated and current_user.has_roles("Admin", "Developer")