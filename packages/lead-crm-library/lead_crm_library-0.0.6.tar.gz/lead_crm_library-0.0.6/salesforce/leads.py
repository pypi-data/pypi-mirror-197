# lead_crm_library/salesforce/leads.py

from .exceptions import SalesforceError
from .utils import normalize_lead_data


class SalesforceLeads:
    def __init__(self, auth):
        self.auth = auth

    def add_lead(self, lead_data):
        try:
            # Autenticarse con las credenciales del objeto auth
            sfClient = self.auth.authenticate()

            # Normalizar los datos del lead antes de agregarlos a Salesforce
            normalized_data = normalize_lead_data(lead_data)

            # Código para agregar un lead a Salesforce usando el token de acceso y los datos normalizados
            sfClient.Lead.create(normalized_data)

        except Exception as e:
            raise SalesforceError(f"Error al agregar lead a Salesforce: {str(e)}")
