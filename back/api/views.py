from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Bridge
from .serializers import BridgeSerializer

from rest_framework.views import APIView

class BridgeList(APIView):
    def get(self, request):
        try:
            title = request.query_params.get('title', None)
            if title:
                bridges = Bridge.objects.filter(title__icontains=title)
            else:
                bridges = Bridge.objects.all()

            serializer = BridgeSerializer(bridges, many=True)
            print(serializer.data)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = BridgeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class BridgeOne(APIView):
    def get(self, request, id):
        try:
            bridge = Bridge.objects.get(id=id)
        except Bridge.DoesNotExist:
            return Response({"error": "Bridge not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = BridgeSerializer(bridge)
        return Response(serializer.data)

    def put(self, request, id):
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
        try:
            bridge = Bridge.objects.get(id=id)
        except Bridge.DoesNotExist:
            return Response({"error": "Bridge not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        bridge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
