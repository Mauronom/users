from django.test import TestCase
from django.test import Client
from django.contrib.auth import get_user_model
from users.models import Profile
User = get_user_model()
# Create your tests here.
class CQRSApiTest(TestCase):

    def setUp(self):
        self.client = Client()

        user = User.objects.create(
            username="u1",
            email="u1@test.com",
        )
        Profile.objects.create(uuid="550e8400-e29b-41d4-a716-446655440000",dni="12345678A", user=user)

    def test_query_api(self):
        response = self.client.get("/query/get.user.info/", {"username": "u1"})

        self.assertEqual(response.status_code, 200)

        data = response.json()
        user = User.objects.get(username='u1')
        self.assertEqual(data["uuid"], str(user.profile.uuid))
        self.assertEqual(data["username"], user.username)
        self.assertEqual(data["email"], user.email)
        self.assertEqual(data["dni"], user.profile.dni)

    def test_command_api(self):
        c = User.objects.filter(username='u2').count()
        self.assertEqual(c,0)
        import json

        response = self.client.post(
            "/command/create.user/",
            data=json.dumps({
                "uuid": "550e8400-e29b-41d4-a716-446655440001",
                "username": "u2",
                "email": "u2@test.com",
                "dni": "12345677A"
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        user = User.objects.get(username='u2')
        self.assertEqual(str(user.profile.uuid), "550e8400-e29b-41d4-a716-446655440001")
        self.assertEqual(user.username, "u2")
        self.assertEqual(user.email, "u2@test.com")
        self.assertEqual(user.profile.dni, "12345677A")
