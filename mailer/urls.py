from django.urls import path
from . import views

urlpatterns = [
    path("", views.compose_email, name="compose_email"),

    path("recipients/", views.recipient_list, name="recipient_list"),
    path("recipients/add/", views.recipient_create, name="recipient_create"),
    path("recipients/<int:pk>/edit/", views.recipient_update, name="recipient_update"),
    path("recipients/<int:pk>/delete/", views.recipient_delete, name="recipient_delete"),
    path("recipients/delete-selected/", views.recipient_delete_selected, name="recipient_delete_selected"),

    path("drafts/", views.draft_list, name="draft_list"),
    path("drafts/<int:pk>/delete/", views.draft_delete, name="draft_delete"),
    path("drafts/delete-selected/", views.draft_delete_selected, name="draft_delete_selected"),
]
