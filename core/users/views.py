from django.db.models import Count, Window, F, Q
from django.db.models.functions import RowNumber

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from core.auth_.models import User
from core.auth_.permissions import CustomIsAuthenticatedPermission
from core.code_interpreter.serializers import SolutionResultSerializer
from core.main.models import SolutionResult
from core.users.serializers import TopUserSerializer, UserProfileSerializer
from core.utils.custom_paginator import CustomPagination


class ProfileView(APIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(instance=user)
        return Response(serializer.data)
    
class SolutionView(generics.RetrieveAPIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    serializer_class = SolutionResultSerializer
    queryset = SolutionResult.objects.all()
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TopUsersListView(generics.ListAPIView):
    permission_classes = [CustomIsAuthenticatedPermission]
    serializer_class = TopUserSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        top_users = User.objects.annotate(
            solved_problems=Count(
                'results__problem',
                filter=Q(results__passed=True),
                distinct=True
            ),
            position=Window(
                expression=RowNumber(),
                order_by=[F('solved_problems').desc(), F('username').asc()]
            )
        ).order_by('-solved_problems', 'username')
        return top_users