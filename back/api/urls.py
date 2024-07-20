from django.urls import path
from . import views

urlpatterns = [
    # """
    # URL pattern for listing all bridges.

    # - **URL**: `/bridges/`
    # - **Name**: `bridge-list`
    # - **View**: `views.BridgeList`
    # - **Description**: This URL pattern routes to the `BridgeList` view, which handles listing all bridge instances.
    # """
    path("bridges/", views.BridgeList.as_view(), name="bridge-list"),

    # """
    # URL pattern for retrieving, updating, or deleting a single bridge by its ID.

    # - **URL**: `/bridge/<int:id>/`
    # - **Name**: `bridge-one`
    # - **View**: `views.BridgeOne`
    # - **Description**: This URL pattern routes to the `BridgeOne` view, which handles operations on a single bridge instance identified by its ID.
    # """
    path("bridge/<int:id>/", views.BridgeOne.as_view(), name="bridge-one"),
]
