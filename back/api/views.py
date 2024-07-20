from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Bridge
from .serializers import BridgeSerializer

from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Bridge
from .serializers import BridgeSerializer

class BridgeList(APIView):
    """
    API view to retrieve and create bridges.

    Methods:
        get(request): Retrieves a list of all bridges or filters them by title.
        post(request): Creates a new bridge with the provided data.
    """

    def get(self, request):
        """
        Retrieve a list of bridges.

        Query Parameters:
            - title (str): Optional. Filter bridges by title using case-insensitive partial match.

        Responses:
            - 200 OK: Returns a list of bridges in JSON format.
            - 500 Internal Server Error: If an unexpected error occurs.

        Example:
            GET /bridges/?title=Golden Gate
        """
        try:
            title = request.query_params.get('title', None)
            if title:
                bridges = Bridge.objects.filter(name__icontains=title)
            else:
                bridges = Bridge.objects.all()

            serializer = BridgeSerializer(bridges, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new bridge.

        Request Data:
            - name (str): The name of the bridge.
            - location (str): The location of the bridge.
            - inspection_date (date): The inspection date of the bridge.
            - status (str): The status of the bridge. Must be one of 'Good', 'Fair', 'Poor', or 'Bad'.
            - traffic_load (int): The traffic load of the bridge.

        Responses:
            - 201 Created: Returns the created bridge data in JSON format.
            - 400 Bad Request: If the provided data is invalid.
            - 500 Internal Server Error: If an unexpected error occurs.

        Example:
            POST /bridges/
                {
                    "name": "Brooklyn Bridge",
                    "location": "0101000020E61000004182E2C7988F5DC0F46C567DAE064140",
                    "inspection_date": "2023-02-15",
                    "status": "Fair",
                    "traffic_load": 10000
                }
        """
        try:
            serializer = BridgeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BridgeOne(APIView):
    """
    API view to retrieve, update, or delete a single bridge by ID.

    Methods:
        get(request, id): Retrieves a single bridge by ID.
        put(request, id): Updates the bridge with the provided ID.
        delete(request, id): Deletes the bridge with the provided ID.
    """

    def get(self, request, id):
        """
        Retrieve a single bridge by ID.

        Parameters:
            - id (int): The ID of the bridge to retrieve.

        Responses:
            - 200 OK: Returns the bridge data in JSON format.
            - 404 Not Found: If the bridge with the given ID does not exist.
            - 500 Internal Server Error: If an unexpected error occurs.

        Example:
            GET /bridge/1/
        """
        try:
            bridge = Bridge.objects.get(id=id)
        except Bridge.DoesNotExist:
            return Response({"error": "Bridge not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = BridgeSerializer(bridge)
        return Response(serializer.data)

    def put(self, request, id):
        """
        Update an existing bridge by ID.

        Parameters:
            - id (int): The ID of the bridge to update.

        Request Data:
            - name (str): The name of the bridge.
            - location (str): The location of the bridge.
            - inspection_date (date): The inspection date of the bridge.
            - status (str): The status of the bridge.
            - traffic_load (int): The traffic load of the bridge.

        Responses:
            - 200 OK: Returns the updated bridge data in JSON format.
            - 400 Bad Request: If the provided data is invalid.
            - 404 Not Found: If the bridge with the given ID does not exist.
            - 500 Internal Server Error: If an unexpected error occurs.

        Example:
            PUT /bridge/1/
            {
                "name": "Golden Gate Bridge Updated",
                "location": "0101000020E610000050FC1873D79A5EC0D0D556EC2FE34240",
                "inspection_date": "2023-01-01",
                "status": "Poor",
                "traffic_load": 11000
            }
        """
        try:
            bridge = Bridge.objects.get(id=id)
        except Bridge.DoesNotExist:
            return Response({"error": "Bridge not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = BridgeSerializer(bridge, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        """
        Delete a bridge by ID.

        Parameters:
            - id (int): The ID of the bridge to delete.

        Responses:
            - 204 No Content: Indicates successful deletion.
            - 404 Not Found: If the bridge with the given ID does not exist.
            - 500 Internal Server Error: If an unexpected error occurs.

        Example:
            DELETE /bridge/1/
        """
        try:
            bridge = Bridge.objects.get(id=id)
        except Bridge.DoesNotExist:
            return Response({"error": "Bridge not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        bridge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
