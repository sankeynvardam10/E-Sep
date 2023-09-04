from django.urls import path
from .views import *

urlpatterns = [
    path('register',EmployeeRegisterView.as_view()),
    path('register/<int:employee_id>/', EmployeeDetailedView.as_view()),

    path('login',EmployeeLoginView.as_view()),
    path('login/<int:pk>/',EmployeeLoginView.as_view()),
    path('login/<str:resignation_status>/',EmployeeLoginView.as_view()),
    path('login/<str:resignation_status>/<int:pk>/',EmployeeLoginView.as_view()),

    path('resignation',EmployeeResignationView.as_view(), name='resignation'),
    path('resignation/<int:resignation_id>/', ResignationDetailedView.as_view()),
]
