# Lead CRM Library
Save Leads CRM Library

### Install
```pip install lead_crm_library```

### How to use
#### Salesforce
```
from lead_crm_library.salesforce.auth import SalesforceAuth
from lead_crm_library.salesforce.leads import SalesforceLeads
from lead_crm_library.salesforce.exceptions import SalesforceError
.
.
.
auth = SalesforceAuth(
            username=os.getenv("SALESFORCE_USERNAME"),
            password=os.getenv("SALESFORCE_PASSWORD"),
            security_token=os.getenv("SALESFORCE_SECURITY_TOKEN"))

sf_leads = SalesforceLeads(auth)
try:
    sf_leads.add_lead(lead_data)
except SalesforceError:
    // Error Code
```

### Generate New version
- Change version in setup.py file (semver)
- Delete folders (build, dist, lead_crm_library.egg-info)
- Run ```python setup.py sdist bdist_wheel```
- Run ```twine upload dist/*``` (You must have a PyPI account)