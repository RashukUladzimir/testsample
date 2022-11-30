from django.urls import path

from .views import index, AdCreateView, add_and_save, AdDetailView, AdListView, AdDeleteView, detail_view
app_name = 'bboard'

urlpatterns = [
    path('', index, name='index'),
    path('add/', AdCreateView.as_view(), name='add'),
    path('detail/<int:pk>', detail_view, name='detail'),
    path('delete/<int:pk>', AdDeleteView.as_view(), name='delete'),
]


