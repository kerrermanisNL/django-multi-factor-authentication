from django.conf.urls import url
from django.views import View

urlpatterns = [
    url(r'^$', View.as_view(), name="indexpage"),
]
