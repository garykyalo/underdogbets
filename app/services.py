import requests 
from .config import settings

##parameters 
url = f"{settings.WHATSAPP_API_URL}/{settings.PHONE_ID}/messages"
headers = {
            "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

def send_reply(payload):
     #extract data                                                         
    response = requests.post(url, json=payload, headers=headers)
    print(response)


def template_payload(message_data):
    contact_info = message_data['contacts'][0]
    name = contact_info['profile']['name']
    phone_number = contact_info['wa_id']
    template_name = "underdog"
    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": "en"
            },
            "components": [
                    {
                        "type": "button",
                        "sub_type": "flow",
                        "index": "0"
                    }
                ]}
        }
    
    return payload

def response_payload(message_data):
    contact_info = message_data['contacts'][0]
    phone_number = contact_info['wa_id']
    payload = { 
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": 'text',
            'text' : {
        "body": "you have selected a package, proceed to payment"
        }}
    return payload