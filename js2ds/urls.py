from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^js2ds-index/$', views.index, name='js2ds-index'),
    url(r'^js2ds-schema/$', views.schema, name='js2ds-schema'),
    url(r'^js2ds-meta-schema/$', views.meta_schema, name='js2ds-meta_schema'),
    url(r'^js2ds/$', views.js2ds, name='js2ds'),
]
