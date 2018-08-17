from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, LogoutView
from django.views.generic import TemplateView

from menus.views import HomeView
from profiles.views import ProfileFollowToggle, RegisterView, LogInView, activate_user_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomeView.as_view(), name='restaurant_home'),
    url(r'^activate/(?P<code>[\w-]+)/$', activate_user_view, name='activate'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LogInView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^restaurants/', include('restaurants.urls', namespace='restaurants')),
    url(r'^items/', include('menus.urls', namespace='menus')),
    url(r'^profile-follow/$', ProfileFollowToggle.as_view(), name='follow'),
    url(r'^u/', include('profiles.urls', namespace='profiles')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='restaurant_about'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='restaurant_contact'),
]
