from django.urls import path
from . import views

urlpatterns = [
    path("bridges/", views.BridgeList.as_view(), name="bridge-list"),
    path("bridge/<int:id>/", views.BridgeOne.as_view(), name= "bridge-one"),
]
