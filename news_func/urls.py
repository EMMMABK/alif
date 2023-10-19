from django.urls import path
from .views import NewsListCreateView, NewsRetrieveUpdateDeleteView, NewsCreateView, NewsDeleteView

urlpatterns = [
    path('news/', NewsListCreateView.as_view(), name='news-list'),
    path('news/<int:pk>/', NewsRetrieveUpdateDeleteView.as_view(), name='news-detail'),
    path('news/create/', NewsCreateView.as_view(), name='name-create'),
    path('news/delete/<int:pk>/', NewsDeleteView.as_view(), name='news-delete')
]
