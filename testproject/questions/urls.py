from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/', views.answers, name='answers'),
    path('create/', views.create, name='create'),
    path('<int:question_id>/create_answer/', views.create_answer, name='create_answer'),
    path('<int:question_id>/edit/', views.edit, name='edit'),
    path('<int:question_id>/delete/', views.delete, name='delete'),
    path('<int:question_id>/edit_answer/', views.edit_answer, name='edit_answer'),
    path('<int:question_id>/delete_answer/', views.delete_answer, name='delete_answer'),
    path('<int:question_id>/rating/', views.rating, name='rating'),
    path('<int:question_id>/rating_answer/', views.rating_answer, name='rating_answer'),
    path('<int:question_id>/solution/', views.solution, name='solution'),
    path('<int:question_id>/solution_answer/', views.solution_answer, name='solution_answer'),
    path('search/', views.search, name='search'),
]
