import io 
import json



def test_register_and_login(client):
    response = client.post("/api/users/register", json={
        "username":"Blues",
        "email":"cuzan2004@gmail.com",
        "password":"admin1234",
        "role":"admin"
    })
    assert response.status_code in (201, 400)



    response = client.post("/api/users/login", json={
        "username" :"Blues",
        "password":"admin1234"

    })
    
    data = response.get_json()
    assert "token" in data
    token = data["token"]
    return token


