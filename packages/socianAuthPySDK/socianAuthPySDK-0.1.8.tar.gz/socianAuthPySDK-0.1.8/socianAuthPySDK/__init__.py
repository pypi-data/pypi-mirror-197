import json
import requests

class authSDK():
    def __init__(self, token=None):
        self.base_url = "https://auth.socian.ai:8082/api/"
        self.token = token

    def test(self, numOne, numTwo):
        return numOne * numTwo

    def serviceAccountsIndex(self):
        url = self.base_url+"service-accounts/"

        payload = json.dumps({})
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()
        
    def serviceAccountsCreate(self, name, is_verified, is_active, is_alive, appId, appSecret, host_url, callback_url, webhook_url):
        url = self.base_url+"service-accounts/"

        payload = json.dumps({
            "name": name,
            "is_verified": is_verified,
            "is_active": is_active,
            "is_alive": is_alive,
            "config_json": {
                "app_id": appId,
                "app_secret": appSecret
            },
            "host_url": host_url,
            "callback_url": callback_url,
            "webhook_url": webhook_url
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
        
        
    def serviceAccountsUpdate(self, app_id, is_verified, is_active, is_alive, host_url, callback_url, webhook_url):
        
        url = self.base_url+"service-accounts"

        payload = json.dumps({
            "app_id": app_id,
            "is_verified": is_verified,
            "is_active": is_active,
            "is_alive": is_alive,
            "host_url": host_url,
            "callback_url": callback_url,
            "webhook_url": webhook_url
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        return response.json()
        
    def webhookGet(self, service_account=1):
        
        url = self.base_url+"servicewebhooks?service_account="+service_account

        payload={}
        headers = {
        'Authorization': '{{token_local}}'
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()
    
    def webhookCreate(self, service_account, hook_name, webhook_uri, event_scope):
        
        url = self.base_url+"servicewebhooks/?Authorization="+self.token

        payload = json.dumps({
            "service_account": service_account,
            "hook_name": hook_name,
            "webhook_uri": webhook_uri,
            "event_scope": event_scope
        })
        headers = {
            'Authorization': 'Bearer '+self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
        
    
    def helth_check(self, app_id, app_secret):
        
        url = self.base_url+"health-check/"

        payload = json.dumps({
            "config": {
                "app_id": app_id,
                "app_secret": app_secret
            }
        })

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
    
    
    def signup(self, name, email, password):
        
        url = self.base_url+"signup/"

        payload = json.dumps({
            "name": name,
            "email": email,
            "password": password
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
        
    def signIn(self, email, password):
        
        url = self.base_url+"signIn/"

        payload = json.dumps({
            "email": email,
            "password": password
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
        
    def signout(self, email, password):
        
        url = self.base_url+"signout/"

        payload = json.dumps({
            "email": email,
            "password": password
        })
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
        
    def profileMe(self, email, password):
        
        url = self.base_url+"profile/me/"

        payload = json.dumps({})
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()
        
    def providers(self, email, password):
        
        url = self.base_url+"providers/"
        
        payload = json.dumps({})
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.json()

if __name__ == '__main__':
    authSDK(token)
    print("process done")