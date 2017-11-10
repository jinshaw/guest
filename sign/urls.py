from django.conf.urls import url
from sign import view_if

urlpatternts={
    url(r'^user_sign/',view_if.user_sign,name='user_sign'),

}