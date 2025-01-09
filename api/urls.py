from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
