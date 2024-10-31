from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, BookViewSet

router = DefaultRouter()
router.register(r'client', ClientViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
