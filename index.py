import requests

url = "https://kr.louisvuitton.com/kor-kr/products/multi-pochette-accessoires-monogram-nvprod1770359v"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
response = requests.get(url, headers = headers)

print('status code : ', response.status_code)