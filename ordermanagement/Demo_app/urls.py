from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomerCreateView, ProductListView, OrderViewSet

router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    path("customers/", CustomerCreateView.as_view(), name="customers-create"),
    path("products/", ProductListView.as_view(), name="products-list"),
    path("", include(router.urls)),
]
