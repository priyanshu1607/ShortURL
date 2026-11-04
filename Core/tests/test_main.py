from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock

from main import app

URLLL ='https://claude.ai/chat/0f021217-70eb-4a15-bad0-3f4551903723'
client = TestClient(app)

def test_healthcheck():
    response = client.get("/health")
    assert response.status_code ==200

@patch("main.generate_unique_slug", return_value = "qwerty", )
@patch("main.setInRedis")
@patch("main.URL_collection")
def test_shortenURL(mock_URL, mock_redis ,mock_slug):
    mock_URL.insert_one = AsyncMock(return_value=MagicMock(inserted_id="id"))
    res = client.post("/api/v1/urls", json={"url": URLLL})
    assert res.status_code == 200
    doc = mock_URL.insert_one.call_args.args[0]
    assert doc['Longurl'] == URLLL
    assert doc['shortURL'].endswith("/qwerty")
    mock_redis.assert_called_once_with(doc["shortURL"], URLLL)



@patch("main.getFromRedis", return_value =None)
@patch("main.URL_collection")
def test_getOrignalURL(mock_URL_collection,mock_Redis):
    mock_URL_collection.find_one = AsyncMock(return_value={"_id": "1", "Longurl": "https://example.com", "expires_at": None})
    mock_URL_collection.update_one =AsyncMock()
    
    res = client.get("/qwerty",follow_redirects=False)
    assert res.status_code in (302, 307)