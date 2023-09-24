import requests

url = "https://api.sms.net.bd/sendsms"

payload = {'api_key': 'xBm4as3r9KSjfgmCsgib8Q1vk0seLmVkYHMoiDEF',
    'msg': 'Your Growexo OTP code is 8976. Growexo.com',
    'to': '8801319347889'
    }

response = requests.request("POST", url, data=payload)

print(response)