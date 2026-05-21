class TestSpeaker:
    """Test speaker profile endpoints."""

    async def test_speaker_endpoints_require_authentication(self, client):
        response = await client.get("/profiles")
        assert response.status_code == 401

        response = await client.post(
            "/train",
            json={"name": "test voice", "sample_text": "hello world"},
        )
        assert response.status_code == 401

    async def test_authenticated_train_uses_embedding_and_saves_profile(self, client, auth_headers, monkeypatch):
        monkeypatch.setattr("app.routes.speaker.get_embedding", lambda sample: [0.1] * 3)
        monkeypatch.setattr("app.routes.speaker.add_voice", lambda name, embedding: True)

        response = await client.post(
            "/train",
            json={"name": "test voice", "sample_text": "hello world"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        assert response.json()["name"] == "test voice"