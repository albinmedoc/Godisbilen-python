from flask_httpauth import HTTPBasicAuth
from godisbilen.user import User
from godisbilen.app import bcrypt

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(phone_number, password):
    user = User.query.filter_by(phone_number=phone_number).first()
    if(user and user.has_roles("Admin")):
        if(bcrypt.check_password_hash(user.admin.password, password)):
            return True
    return False
    
