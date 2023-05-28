from test_login_api import logged_client, valid_api_response

def test_carro(logged_client):
    json = {"productos": {"id": 1, "adimentos": [1, 2, 3]}, "ubicacion": None}
    response = logged_client.post("http://localhost:5000/api/carro/add", json = json)
    assert valid_api_response(response)