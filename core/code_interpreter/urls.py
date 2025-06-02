from django.urls import path
from .views import RunCodeView, SubmitCodeView, TaskStatusView, SaveSolutionResultView


urlpatterns = [
    path('run-code/<int:id_problem>/', RunCodeView.as_view(), name='run_code'),
    path('submit-code/<int:id_problem>/', SubmitCodeView.as_view(), name='submit_code'), 
    path('task-status/<str:task_id>/', TaskStatusView.as_view(), name='task_status'),
    path("save-solution/<int:problem_id>/", SaveSolutionResultView.as_view(), name='save_solution'),
]