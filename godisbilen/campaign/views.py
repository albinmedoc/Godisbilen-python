from datetime import datetime
from flask import Markup, url_for, flash, redirect
from flask_admin import expose
from flask_admin.helpers import get_form_data
from flask_admin.babel import gettext
from godisbilen.admin.views import AdminView

class CampaignView(AdminView):
    column_searchable_list = ["id", "title", "start", "end", "delivery", "amount"]
    column_sortable_list = ["id", "title", "info", "terms", "start", "end", "delivery", "per_user", "per_address", "amount", "count_orders"]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ["id", "title", "info", "terms", "start", "end", "delivery", "per_user", "per_address", "amount", "count_orders"]
    column_labels = {
        "title": "Titel",
        "info": "Information",
        "terms": "Villkor",
        "start": "Öppnar",
        "end": "Stänger",
        "delivery": "Levererans",
        "per_user": "Per användare",
        "per_address": "Per adress",
        "amount": "Antal",
        "count_orders": "Antal ordrar"
    }

class CampaignOrderView(AdminView):
    column_searchable_list = ["campaign.title", "order_number.number", "user.phone_number", "order_number.created", "delivered"]
    column_sortable_list = ["order_number.number", "order_number.created", "delivered"]
    page_size = 50
    can_view_details = True
    create_modal = True
    edit_modal = True
    column_list = ["order_number.number", "campaign.title", "user", "location", "order_number.created", "delivered", "Status"]
    column_labels = {
        "order_number.number": "Ordernummer",
        "campaign.title": "Erbjudande",
        "user": "Användare",
        "location": "Adress",
        "order_number.created": "Placerad",
        "delivered": "Levererad"
    }

    def deliver_button(view, context, model, name):
        if(model.delivered):
            return "Utlämnad"
        checkout_url = url_for(".deliver")

        _html = '''
            <form action="{checkout_url}" method="POST">
                <input name="campaign_order_id"  type="hidden" value="{campaign_order_id}">
                <button type="submit">Leverera</button>
            </form
        '''.format(checkout_url=checkout_url, campaign_order_id=model.id)
        return Markup(_html)

    column_formatters = {
        "Status": deliver_button
    }
    
    @expose("deliver", methods=["POST"])
    def deliver(self):
        return_url = self.get_url(".index_view")

        form = get_form_data()
        if(not form):
            flash(gettext("Could not get form from request."), "error")
            return redirect(return_url)
        
        campaign_order_id = form["campaign_order_id"]

        model = self.get_one(campaign_order_id)

        if(model is None):
            flash(gettext("CampaignOrder not not found."), "error")
            return redirect(return_url)
        
        model.delivered = datetime.now()

        try:
            self.session.commit()
            flash(gettext("CampaignOrder, Id: {campaign_order_id}, marked as delivered".format(campaign_order_id=campaign_order_id)))
        except Exception as ex:
            if not self.handle_view_exception(ex):
                raise

            flash(gettext("Failed to mark CampaignOrder, Id: {campaign_order_id}, as delivered".format(campaign_order_id=campaign_order_id), error=str(ex)), "error")

        return redirect(return_url)