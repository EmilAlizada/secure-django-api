from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .auth_views import (
    RegisterView,
    ThrottledTokenObtainPairView,
    ThrottledTokenRefreshView,
)
from .views import HealthView, MeView, NoteViewSet

router = DefaultRouter()
router.register("notes", NoteViewSet, basename="note")

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", ThrottledTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", ThrottledTokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]
