from django.conf.urls import url
from django.contrib.auth import views as auth_views

from app import views as app_views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    # Authentication
    url(r'^login/$', auth_views.login, {'template_name': 'app/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),

    url(r'^.*\.html', app_views.all_html, name='all_html'),

    # The home page
    url(r'^$', app_views.channels, name='index'),

    # Channels page
    url(r'^channels', app_views.channels, name='channels'),

    # Channels page
    url(r'^sats', app_views.sats, name='sats'),

    # Profile page
    url(r'^profile', app_views.profile, name='profile'),

    # Home page
    url(r'^home', app_views.index, name='home'),

    # Home page
    url(r'^interfaces', app_views.interfaces, name='interfaces'),


    url(r'^init_work$', app_views.init_work),
    url(r'^poll_state$', app_views.poll_state, name="poll_state"),
    url(r'^ajax/refresh_dvb_list/$', app_views.sats_ajax, name='sats_ajax'),
    url(r'^ajax/post_config/$', app_views.post_config_ajax, name='post_config_ajax'),

]

handler404 = app_views.error_404
