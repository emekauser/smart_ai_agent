from django.urls import path
from . import views

urlpatterns = [
    path('documents/', views.document_list),
    path('documents/<int:pk>/', views.document_detail),
    path('documents/reindex/<int:pk>/', views.re_index_document_to_vector_db),
    path('ask/', views.ask_agent),
    path('documents/vector/<int:pk>/', views.get_document_in_vector_db),
]
