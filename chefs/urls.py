from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.get_collection),
    path('<int:user_id>/', views.Index.as_view()),
]
