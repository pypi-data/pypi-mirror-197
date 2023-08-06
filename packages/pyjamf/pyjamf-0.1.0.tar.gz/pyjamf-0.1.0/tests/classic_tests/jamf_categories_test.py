import os

from pyjamf.identity import UsernamePasswordCredential
from pyjamf.core import JamfServiceClient
from pyjamf.types.classic.models import Category

def category_collection_test():
    
    credential = UsernamePasswordCredential(os.environ["JAMF_INSTANCE"], os.environ["JAMF_USERNAME"], os.environ["JAMF_PASSWORD"])

    client = JamfServiceClient(credential, os.environ["JAMF_INSTANCE"])
    
    categories = client.classic_api.category.request.Get.invoke_request
    
    assert isinstance(categories, list)
    assert isinstance(categories[0], Category)
    
def category_by_id_test():

    credential = UsernamePasswordCredential(os.environ["JAMF_INSTANCE"], os.environ["JAMF_USERNAME"], os.environ["JAMF_PASSWORD"])

    client = JamfServiceClient(credential, os.environ["JAMF_INSTANCE"])

    category = client.classic_api.category.request_by_id("2").Get.invoke_request
    
    assert isinstance(category, Category)
    
def category_by_name_test():
    
    credential = UsernamePasswordCredential(os.environ["JAMF_INSTANCE"], os.environ["JAMF_USERNAME"], os.environ["JAMF_PASSWORD"])

    client = JamfServiceClient(credential, os.environ["JAMF_INSTANCE"])
    
    category = client.classic_api.category.request_by_name("CIS Security Settings").Get.invoke_request
    
    assert isinstance(category, Category)