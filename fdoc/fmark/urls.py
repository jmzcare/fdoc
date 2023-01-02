from django.urls import path, include

from .views import fmark_api as fmark_api_v
from .views import index as index_v

from rest_framework.routers import DefaultRouter

app_name = 'fmark'


# # Create a router and register our viewsets with it.
router = DefaultRouter()
# router.register(r'customer', ftrace_api_v.CustomerViewSet)


urlpatterns = [
    path('index/<pk>/', index_v.index, name='index'),
]
