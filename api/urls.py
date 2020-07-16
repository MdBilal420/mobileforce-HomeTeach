from django.urls import path
from api.views import CustomUserViewSet, ProfileViewSet, TutorProfileViewSet, StudentProfileViewSet
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'tutor-profiles', TutorProfileViewSet)
router.register(r'student-profiles', StudentProfileViewSet)

urlpatterns = [
    path('submit-request/', views.submit_request),
    path('tutor-requests/', views.list_requests_tutor),
    path('user-requests/', views.list_user_requests),
    path('rate_tutor/', views.rate_tutor),
    path('top-tutors/', views.top_tutors)
]

urlpatterns += router.urls
