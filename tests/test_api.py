"""
DropOrCop - Phase 5 API Integration Tests
Tests all endpoints: /, /health, /brands, /predict (valid & invalid inputs)
"""

import unittest
from fastapi.testclient import TestClient
from api.main import app


class TestDropOrCopAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root_endpoint(self):
        """Test GET / returns 200 and expected welcome message."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("DropOrCop", data["message"])
        self.assertEqual(data.get("version"), "1.0.0")

    def test_health_endpoint(self):
        """Test GET /health returns healthy status and connected model."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "DropOrCop API")
        self.assertTrue(data["model_loaded"])
        self.assertEqual(data["model_status"], "connected")

    def test_brands_endpoint(self):
        """Test GET /brands returns supported brands Yeezy and Off-White."""
        response = self.client.get("/brands")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("brands", data)
        self.assertIn("Yeezy", data["brands"])
        self.assertIn("Off-White", data["brands"])
        self.assertEqual(data["total"], 2)
        self.assertIn("default_retail", data)

    def test_predict_endpoint_yeezy_cop(self):
        """Test POST /predict with a typical Yeezy release that yields a COP."""
        payload = {
            "brand": "Yeezy",
            "retail_price": 220.0,
            "shoe_size": 10.5,
            "days_since_release": 45,
            "threshold": 0.15,
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["brand"], "Yeezy")
        self.assertEqual(data["retail_price"], 220.0)
        self.assertGreater(data["estimated_resale_price"], 0)
        self.assertIn("verdict", data)
        self.assertIn(data["verdict"], ["COP", "DROP"])

    def test_predict_endpoint_offwhite(self):
        """Test POST /predict with an Off-White release."""
        payload = {
            "brand": "Off-White",
            "retail_price": 190.0,
            "shoe_size": 9.0,
            "days_since_release": 120,
            "threshold": 0.15,
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["brand"], "Off-White")
        self.assertEqual(data["retail_price"], 190.0)
        self.assertGreater(data["estimated_resale_price"], 0)
        self.assertIn(data["verdict"], ["COP", "DROP"])

    def test_predict_unsupported_brand(self):
        """Test POST /predict with an unsupported brand returns 400."""
        payload = {
            "brand": "Converse",
            "retail_price": 70.0,
            "shoe_size": 10.0,
            "days_since_release": 30,
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("Unsupported brand", data["detail"])

    def test_predict_missing_fields(self):
        """Test POST /predict with missing required fields returns 422."""
        response = self.client.post("/predict", json={"brand": "Yeezy"})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
