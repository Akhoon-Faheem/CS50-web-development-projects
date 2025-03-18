from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.title_page, name="title" ),
    path("search/", views.search, name="look"),
    path('create_page/', views.create_page, name="create_page"),
    path("wiki/<str:namy>/edit/",views.edit, name="edit"),
    path('random_page/',views.random_generator, name="random")
]
