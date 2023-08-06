# lead_crm_library/hubspot/leads.py

from .auth import HubspotAuth
from .exceptions import HubspotError
from .utils import normalize_lead_data


class HubspotLeads:
    def __init__(self, api_key):
        self.api_key = api_key
        self.auth = HubspotAuth(api_key=self.api_key)

    def add_lead(self, lead_data):
        try:
            # Autenticarse con la API Key de HubSpot
            hubspot_client = self.auth.authenticate()

            # Normalizar los datos del lead antes de agregarlos a HubSpot
            normalized_data = normalize_lead_data(lead_data)

            # Código para agregar un lead a HubSpot usando la API Key y los datos normalizados
            hubspot_client.contacts.create(data=[normalized_data])

        except Exception as e:
            raise HubspotError(f"Error al agregar lead a HubSpot: {str(e)}")
