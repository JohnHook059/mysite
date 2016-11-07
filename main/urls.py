from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^logout_page$', views.logout_page, name='logout_page'),
    url(r'^chat/(?P<chat_name>.+)/$', views.chat),
    url(r'^chats$', views.chats, name='chats'),
    url(r'^invites$', views.invites, name='invites'),
]