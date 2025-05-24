from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser

from django.core.cache import cache

from core.auth_.models import User
from core.auth_.permissions import CustomIsAdminPermission, CustomIsAuthenticatedPermission
from core.main.models import Problem, Rate, SolutionResult, TestCase
from core.main.serializers import ProblemSerializer, TestCaseSerializer
from core.utils.file_validator import file_is_valid 
from core.utils.json_convertor import read_and_convert_file_to_json
from core.utils.custom_paginator import CustomPagination


class ProblemListView(generics.ListAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    pagination_class = CustomPagination
 
    def get_quryset(self):
        cache_key = "all_problems"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        else:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data)


class ProblemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ProblemCreateView(APIView):
    permission_classes = [CustomIsAdminPermission]
    def post(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        serializer = ProblemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    
class TestCaseView(APIView):
    permission_classes = [CustomIsAdminPermission]
    def post(self, request, *args, **kwargs):
        problem_id = request.data.get('problem')
        user = self.request.user
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return Response({"error": "Problem does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if problem.author != user:
            return Response({"error": "You are not the author of this problem."}, status=status.HTTP_403_FORBIDDEN)
        serializer = TestCaseSerializer(data=request.data, context={'id_problem': problem_id})  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class TestCasesListView(generics.ListAPIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    serializer_class = TestCaseSerializer
    def get(self, request, *args, **kwargs):
        id_problem = self.kwargs["id"]
        not_full = request.query_params.get("not_full")

        if not_full:
            queryset = TestCase.objects.filter(problem_id=id_problem)[:3]
        else:
            queryset = TestCase.objects.filter(problem_id=id_problem)

        serializater = self.get_serializer(queryset, many=True)

        return Response(serializater.data)
    

class LikeProblemView(APIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    def post(self, request, problem_id, user_id):
        try:
            problem = Problem.objects.get(pk=problem_id)
            user = User.objects.get(pk=user_id)
        except (Problem.DoesNotExist, User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not SolutionResult.objects.filter(problem=problem, user=user).exists():
            return Response({"error": "You need to solve this problem to decide whether you like it or not"}, status=status.HTTP_400_BAD_REQUEST)
        
        rate, created = Rate.objects.get_or_create(user=user, problem=problem)
        
        if created or rate.rate_type != Rate.LIKE:
            rate.rate_type = Rate.LIKE
            rate.save()
            if not created:
                return Response(status=status.HTTP_205_RESET_CONTENT)
            return Response(status=status.HTTP_201_CREATED)
        else:
            rate.delete()
            return Response(status=status.HTTP_200_OK)


class DislikeProblemView(APIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    def post(self, request, problem_id, user_id):
        try:
            problem = Problem.objects.get(pk=problem_id)
            user = User.objects.get(pk=user_id)
        except (Problem.DoesNotExist, User.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)

        if not SolutionResult.objects.filter(problem=problem, user=user).exists():
            return Response({"error": "You need to solve this problem to decide whether you like it or not"}, status=status.HTTP_400_BAD_REQUEST)

        rate, created = Rate.objects.get_or_create(user=user, problem=problem)

        if created or rate.rate_type != Rate.DISLIKE:
            rate.rate_type = Rate.DISLIKE
            rate.save()
            if not created:
                return Response(status=status.HTTP_205_RESET_CONTENT)
            return Response(status=status.HTTP_201_CREATED)
        else:
            rate.delete()
            return Response(status=status.HTTP_200_OK)

class LoadTestCasesView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [CustomIsAdminPermission]
    def post(self, request, *args, **kwargs):
        problem_id = kwargs.get("id")
        user = self.request.user
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return Response({"error": "Problem does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if problem.author != user:
            return Response({"error": "You are not the author of this problem."}, status=status.HTTP_403_FORBIDDEN)

        if 'file' not in request.data:
            return Response({"error": "No file provided"}, status=400)
        
        file = request.data['file']
        file_name = file.name
    
        if file_is_valid(file, file_name):
            testcases = read_and_convert_file_to_json(file, problem_id)
            if testcases is False:
                return Response({"error": "Invalid format in file"}, status=400)
            test_cases = [TestCase(**data) for data in testcases]
            non_serialized_data = TestCase.objects.bulk_create(test_cases)
            serialized_data = TestCaseSerializer(non_serialized_data, many=True)
            return Response({"message": "Test cases uploaded successfully", "testcases": serialized_data.data})
        else:
            return Response({"error": "Invalid file"}, status=400)