from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_whatsapp_campaign_endpoint():
    response = client.post(
        "/api/v1/whatsapp-campaigns/generate",
        json={
            "brand_name": "Kulfi Lounge",
            "offer_title": "Mixed Berries Milkshake at Rs.90 only",
            "offer_details": "Now get refreshing mixed berries milkshake at Rs.90 only",
            "target_audience": "Dessert and milkshake lovers",
            "tone": "urgent",
            "validity": "1st July",
            "call_to_action": "Grab it soon",
            "output_count": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["brand_name"] == "Kulfi Lounge"
    assert data["offer_title"] == "Mixed Berries Milkshake at Rs.90 only"
    assert data["tone"] == "urgent"
    assert data["output_count"] == 3
    assert len(data["messages"]) == 3

    first_message = data["messages"][0]

    assert first_message["variation"] == 1
    assert "Kulfi Lounge" in first_message["message"]
    assert "Mixed Berries Milkshake" in first_message["message"]
    assert "1st July" in first_message["message"]
    assert first_message["call_to_action"] == "Grab it soon"


def test_generate_whatsapp_campaign_validates_output_count():
    response = client.post(
        "/api/v1/whatsapp-campaigns/generate",
        json={
            "brand_name": "Kulfi Lounge",
            "offer_title": "Special Offer",
            "offer_details": "Buy 2 get 1 free",
            "output_count": 20,
        },
    )

    assert response.status_code == 422
