from django.urls import path

from . import views

urlpatterns = [
    path('', views.front_page_view, name='front_page'),
    path("add/", views.add_publication_view),
    path("delete/<int:id>", views.delete_publication)
]