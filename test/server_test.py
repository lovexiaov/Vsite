# coding:utf-8

import requests
import json

data = {
    'city': '丰台'
}

response = requests.get(u'http://localhost:5000/weather', params=data)
print(response.text)
result = json.loads(response.text, encoding='utf-8')
print(json.loads(result.get('content')))
