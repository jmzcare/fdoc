from django.urls import path, include

from .views import ftrace_api as ftrace_api_v
from .views import index as index_v

from rest_framework.routers import DefaultRouter

app_name = 'ftrace'


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'customer', ftrace_api_v.CustomerViewSet)
router.register(r'customer_nature', ftrace_api_v.Customer_natureViewSet)
router.register(r'source_sector', ftrace_api_v.Source_sectorViewSet)
router.register(r'source', ftrace_api_v.SourceViewSet)
router.register(r'sourceship', ftrace_api_v.SourceshipViewSet)
router.register(r'sourceshipModel', ftrace_api_v.SourceshipModelViewSet)

router.register(r'quata', ftrace_api_v.QuataViewSet)
router.register(r'contact', ftrace_api_v.ContactViewSet)




urlpatterns = [
    path('index', index_v.index, name='index'),
]
