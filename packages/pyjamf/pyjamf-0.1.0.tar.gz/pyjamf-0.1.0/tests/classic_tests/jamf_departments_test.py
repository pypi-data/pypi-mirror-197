import os

from pyjamf.identity import UsernamePasswordCredential
from pyjamf.core import JamfServiceClient
from pyjamf.types.classic.models import Department

def computer_collection_test():
    
    credential = UsernamePasswordCredential(os.environ["JAMF_INSTANCE"], os.environ["JAMF_USERNAME"], os.environ["JAMF_PASSWORD"])

    client = JamfServiceClient(credential, os.environ["JAMF_INSTANCE"])
    
    departments = client.classic_api.deparments.request.Get.invoke_request
    
    assert isinstance(departments, list)
    
def computer_by_id_test():
    
    credential = UsernamePasswordCredential(os.environ["JAMF_INSTANCE"], os.environ["JAMF_USERNAME"], os.environ["JAMF_PASSWORD"])

    client = JamfServiceClient(credential, os.environ["JAMF_INSTANCE"])
    
    department = client.classic_api.deparments.request_by_id("4").Get.invoke_request
    
    assert isinstance(department, Department)
    
def computer_by_name_test():
    
    credential = UsernamePasswordCredential(os.environ["JAMF_INSTANCE"], os.environ["JAMF_USERNAME"], os.environ["JAMF_PASSWORD"])

    client = JamfServiceClient(credential, os.environ["JAMF_INSTANCE"])
    
    department = client.classic_api.deparments.request_by_name("Ticket Office").Get.invoke_request
    
    assert isinstance(department, Department)