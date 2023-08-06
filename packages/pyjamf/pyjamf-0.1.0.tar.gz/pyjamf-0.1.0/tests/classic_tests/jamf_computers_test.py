import os

from pyjamf.identity import UsernamePasswordCredential
from pyjamf.core import JamfServiceClient
from pyjamf.types.classic.models import Computer

def computer_collection_test():
    
    credential = UsernamePasswordCredential(os.environ["JAMF_INSTANCE"], os.environ["JAMF_USERNAME"], os.environ["JAMF_PASSWORD"])

    client = JamfServiceClient(credential, os.environ["JAMF_INSTANCE"])
    
    computers = client.classic_api.computers.request.Get.invoke_request
    
    assert isinstance(computers, list)
    
def computer_by_id_test():
    
    credential = UsernamePasswordCredential(os.environ["JAMF_INSTANCE"], os.environ["JAMF_USERNAME"], os.environ["JAMF_PASSWORD"])

    client = JamfServiceClient(credential, os.environ["JAMF_INSTANCE"])
    
    computer = client.classic_api.computers.request_by_id("4424").request.Get.invoke_request
    
    assert isinstance(computer, Computer)

def computer_by_id_subset():
    pass

def computer_by_mac_address_test():
    pass

def computer_by_name():
    pass

def computer_by_serial_number():
    pass

def computer_collection_subset_basic():
    pass

def computer_by_udid():
    pass