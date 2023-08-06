# lead_crm_library/salesforce/auth.py
from simple_salesforce import Salesforce


class SalesforceAuth:
    def __init__(self, username, password, security_token):
        self.username = username
        self.password = password
        self.security_token = security_token

    def authenticate(self):
        # Código para autenticarse con Salesforce usando credenciales de usuario y un token de seguridad
        f = Salesforce(username=self.username, password=self.password,
                       security_token=self.security_token)
        return f
