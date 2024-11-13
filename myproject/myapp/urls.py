from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NsaResourceView, UserViewSet, RegisterView, LoginView, LogoutView, CategoryViewSet, PostViewSet, CommentViewSet, InformationViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'information', InformationViewSet, basename='information')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('nsa-resource/', NsaResourceView.as_view(), name='nsa-resource'),
]
