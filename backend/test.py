import requests

key = ""

header = {
    'Authorization': f'Bearer {key}',
    'Content-Type': 'application/json',
}

url = "https://api.flutterwave.com/v3/payments"

data = {
    'amount': 8360.0,
    'redirect_url': 'https://127.0.0.1:8000/api/v1/payment/callback-payment/',
    'currency': 'NGN',
    'tx_ref': '0130f7eacd2e4f3689e6771bb4479c7a',
    'customer': {
        'email': 'admin@gmail.com'
    },
    'customizations': {
        'title': 'Trip Value',
        'logo': 'https://tripvalue.com/static/images/logo.png',
        'description': 'Trip Value is a platform that allows you to send packages to your loved ones in Nigeria from anywhere in the world.'
    }
}


response = requests.post(headers=header, url=url, json=data)

print(response.url)
print(response.status_code)
print(response.text)
