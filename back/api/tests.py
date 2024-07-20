from django.test import TestCase
from .models import Bridge
from rest_framework.test import APITestCase
from .serializers import BridgeSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class BridgeModelTest(TestCase):
    """
    Test class for the Bridge model.
    """

    def setUp(self):
        """
        Initial setup for tests. This method is called before every test.
        """
        self.bridge = Bridge.objects.create(
            name="Golden Gate Bridge",
            location="0101000020E610000050FC1873D79A5EC0D0D556EC2FE34240",
            inspection_date="2023-01-01",
            status="Good",
            traffic_load=10000
        )

    def test_bridge_creation(self):
        """
        Test the creation of a bridge and ensure the fields are correctly populated.
        """
        bridge = Bridge.objects.get(name="Golden Gate Bridge")
        self.assertEqual(bridge.name, "Golden Gate Bridge")
        self.assertEqual(bridge.location, "0101000020E610000050FC1873D79A5EC0D0D556EC2FE34240")
        self.assertEqual(bridge.status, "Good")
        self.assertEqual(bridge.traffic_load, 10000)

    def test_str_method(self):
        """
        Test the __str__ method of the Bridge model.
        """
        bridge = Bridge.objects.get(name="Golden Gate Bridge")
        self.assertEqual(str(bridge), "Golden Gate Bridge")

    def test_bridge_update(self):
        """
        Test updating a bridge's information.
        """
        bridge = Bridge.objects.get(name="Golden Gate Bridge")
        bridge.status = "Needs Repair"
        bridge.save()
        self.assertEqual(bridge.status, "Needs Repair")

    def test_bridge_deletion(self):
        """
        Test the deletion of a bridge.
        """
        bridge = Bridge.objects.get(name="Golden Gate Bridge")
        bridge.delete()
        self.assertFalse(Bridge.objects.filter(name="Golden Gate Bridge").exists())


class BridgeSerializerTest(APITestCase):
    """
    Test class for the BridgeSerializer.
    """

    def setUp(self):
        """
        Initial setup for tests.
        """
        self.bridge_data = {
            'name': 'Golden Gate Bridge',
            'location': '0101000020E610000050FC1873D79A5EC0D0D556EC2FE34240',
            'inspection_date': '2023-01-01',
            'status': 'Good',
            'traffic_load': 10000
        }
        self.serializer = BridgeSerializer(data=self.bridge_data)

    def test_serializer_valid(self):
        """
        Test that the serializer with valid data is valid.
        """
        self.assertTrue(self.serializer.is_valid())

    def test_serializer_invalid_status(self):
        """
        Test that the serializer with an invalid status is invalid.
        """
        self.bridge_data['status'] = 'Excellent'
        serializer = BridgeSerializer(data=self.bridge_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), set(['status']))


class BridgeURLsTest(APITestCase):
    """
    Test the URL patterns for the Bridge app.
    """

    def setUp(self):
        """
        Create a Bridge instance for testing.
        """
        self.bridge = Bridge.objects.create(
            name="Golden Gate Bridge",
            location="0101000020E610000050FC1873D79A5EC0D0D556EC2FE34240",
            inspection_date="2023-01-01",
            status="Good",
            traffic_load=10000
        )
        self.list_url = reverse('bridge-list')
        self.detail_url = reverse('bridge-one', kwargs={'id': self.bridge.id})

    def test_create_bridge(self):
        """
        Test that a new bridge can be created using the list URL.
        """
        data = {
            'name': 'Brooklyn Bridge',
            'location': '0101000020E6100000F2D8C35B7B2D5D039F5A6C0108B9E9A40',
            'inspection_date': '2024-07-01',
            'status': 'Fair',
            'traffic_load': 15000
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bridge.objects.count(), 2)
        self.assertEqual(Bridge.objects.latest('id').name, 'Brooklyn Bridge')

    def test_detail_url(self):
        """
        Test that the URL pattern for retrieving a single bridge by ID works.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Golden Gate Bridge')

    def test_update_bridge(self):
        """
        Test that an existing bridge can be updated using the detail URL.
        """
        data = {
            'name': 'Golden Gate Bridge Updated',
            'location': '0101000020E610000050FC1873D79A5EC0D0D556EC2FE34240',
            'inspection_date': '2023-01-01',
            'status': 'Poor',
            'traffic_load': 11000
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bridge.refresh_from_db()
        self.assertEqual(self.bridge.name, 'Golden Gate Bridge Updated')
        self.assertEqual(self.bridge.status, 'Poor')

    def test_delete_bridge(self):
        """
        Test that an existing bridge can be deleted using the detail URL.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bridge.objects.count(), 0)

class BridgeViewTests(APITestCase):
    """
    Test suite for the Bridge API views.
    """

    def setUp(self):
        """
        Create a sample Bridge instance for testing.
        """
        self.bridge_data = {
            'name': 'Golden Gate Bridge',
            'location': '0101000020E610000050FC1873D79A5EC0D0D556EC2FE34240',
            'inspection_date': '2023-01-01',
            'status': 'Good',
            'traffic_load': 10000
        }
        self.bridge = Bridge.objects.create(**self.bridge_data)
        self.list_url = '/bridges/'
        self.detail_url = f'/bridge/{self.bridge.id}/'

    def test_list_get(self):
        """
        Test GET request for listing all bridges.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.bridge_data['name'])

    def test_list_get_with_filter(self):
        """
        Test GET request for listing bridges with a title filter.
        """
        response = self.client.get(self.list_url, {'title': 'Golden Gate'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.bridge_data['name'])

    def test_list_post(self):
        """
        Test POST request to create a new bridge.
        """
        new_bridge_data = {
            'name': 'Brooklyn Bridge',
            'location': '0101000020E6100000F2D8C35B7B2D5D039F5A6C0108B9E9A40',
            'inspection_date': '2024-07-01',
            'status': 'Fair',
            'traffic_load': 15000
        }
        response = self.client.post(self.list_url, new_bridge_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bridge.objects.count(), 2)
        self.assertEqual(Bridge.objects.latest('id').name, 'Brooklyn Bridge')

    def test_detail_get(self):
        """
        Test GET request to retrieve a single bridge by ID.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.bridge_data['name'])

    def test_detail_put(self):
        """
        Test PUT request to update an existing bridge.
        """
        updated_data = {
            'name': 'Golden Gate Bridge Updated',
            'location': self.bridge_data['location'],
            'inspection_date': self.bridge_data['inspection_date'],
            'status': 'Poor',
            'traffic_load': 11000
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bridge.refresh_from_db()
        self.assertEqual(self.bridge.name, 'Golden Gate Bridge Updated')
        self.assertEqual(self.bridge.status, 'Poor')

    def test_detail_delete(self):
        """
        Test DELETE request to delete an existing bridge.
        """
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bridge.objects.count(), 0)

    def test_detail_get_not_found(self):
        """
        Test GET request for a bridge that does not exist.
        """
        non_existent_url = '/bridge/999/'
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Bridge not found')

    def test_detail_put_not_found(self):
        """
        Test PUT request for a bridge that does not exist.
        """
        non_existent_url = '/bridge/999/'
        response = self.client.put(non_existent_url, {'name': 'Updated Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Bridge not found')

    def test_detail_delete_not_found(self):
        """
        Test DELETE request for a bridge that does not exist.
        """
        non_existent_url = '/bridge/999/'
        response = self.client.delete(non_existent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Bridge not found')
