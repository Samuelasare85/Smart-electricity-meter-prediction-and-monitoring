from django.urls import path
from accounts import views
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'smart_app'

urlpatterns = [
    # path('home/', views.homepage, name='home'),
    path('register/', views.signup_view, name='signup'),
    path('login/', views.signin_view, name='signin'),
    path('logout/', views.logout_view, name='logout'),
]
