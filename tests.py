import requests

url = "http://127.0.0.1:5555"


# route 1
def test_update_types():
    global url
    res = requests.put(url=f'{url}/update_type?name=venusaur').json()
    print(res)
