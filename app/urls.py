from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, FriendshipViewSet, get_friends, verify_user, add_friend, edit_username, delete_user, remove_friend

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'friend', FriendshipViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verfiy/', verify_user),
    path('get/<int:id>/', get_friends),
    path('add/', add_friend),
    path('edit/', edit_username),
    path('delete/<int:id>/<int:friendid>/',remove_friend),
    path('delete/<int:id>/',delete_user)
]