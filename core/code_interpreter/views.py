import json
#import custom_json_serializer 

from rest_framework.views import APIView, status
from rest_framework.response import Response

from django.core import serializers

from celery.result import AsyncResult

from core.auth_.permissions import CustomIsAuthenticatedPermission
from core.code_interpreter.serializers import SolutionResultSerializer
from core.executor.tasks import run_user_code
from core.main.models import TestCase

class RunCodeView(APIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    def post(self, request, id_problem):
        user_code = request.data.get('code')
        try:
            testcases = serializers.serialize('json', TestCase.objects.filter(problem_id=id_problem)[:3])
        except Exception:
            return Response({"No problem with such id"})
        
        #task = run_user_code.delay(str(request.user.id), user_code, custom_json_serializer.deserialize(testcases))
        task = run_user_code.delay(str(request.user.id), user_code, json.loads(testcases))

        return Response({"task_id": task.id})



class SubmitCodeView(APIView):
    permission_classes = [CustomIsAuthenticatedPermission] 
    def post(self, request, id_problem):
        user_code = request.data.get('code')
        try:
            testcases = serializers.serialize('json', TestCase.objects.filter(problem_id=id_problem))
        except Exception:
            return Response({"No problem with such id"})
        #task = run_user_code.delay(str(request.user.id), user_code, custom_json_serializer.deserialize(testcases))
        task = run_user_code.delay(str(request.user.id), user_code, json.loads(testcases))

        return Response({"task_id": task.id})
    
    
class TaskStatusView(APIView):
    def get(self, request, task_id, *args, **kwargs):
        task = AsyncResult(task_id)

        response_data = {
            'state': task.state,
            'result': None
        }

        if task.state == 'PENDING':
            response_data['result'] = 'Task is still pending...'
        elif task.state == 'SUCCESS':
            response_data['result'] = task.result
        elif task.state == 'FAILURE':
            response_data['result'] = str(task.info)
        elif task.state == 'REVOKED':
            response_data['result'] = 'Task was revoked.'
        
        return Response(response_data)
    

class SaveSolutionResultView(APIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    def post(self, request, problem_id, *args, **kwargs):
        serializer = SolutionResultSerializer(data=request.data, context={'user': request.user, 'problem_id': problem_id})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)