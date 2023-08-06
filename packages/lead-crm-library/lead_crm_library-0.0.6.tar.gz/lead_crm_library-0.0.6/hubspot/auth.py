# lead_crm_library/hubspot/auth.py
from hubspot import HubSpot

class HubspotAuth:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = None

    def authenticate(self):
        # Autenticación con la API Key de HubSpot
        self.client = HubSpot(api_key=self.api_key)

        return self.client
