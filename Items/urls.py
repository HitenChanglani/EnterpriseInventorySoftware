from django.urls import path
from . import views

urlpatterns = [
    path("item/", views.item_views),
    path("category/", views.category_views),
    path("tag/", views.tag_views)
]