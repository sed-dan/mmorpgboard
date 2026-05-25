from django.urls import path
from .views import user_profile, SignUpView, Verification


urlpatterns = [
  path('profile/', user_profile, name='user_profile'),
  path('signup/', SignUpView.as_view(), name = 'signup_page'),
  path('verification/', Verification.as_view(), name = 'verification'),
]