from rest_framework import serializers

from django.db.models import Count, F, Window
from django.db.models.functions import RowNumber

from core.auth_.models import User
from core.main.models import SolutionResult

class UserProfileSerializer(serializers.ModelSerializer):
    solved_problems = serializers.SerializerMethodField()
    was_complited_problems = serializers.SerializerMethodField()
    rank = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "was_complited_problems", "solved_problems", "rank"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_ranks = {}
        self.calculate_user_ranks()

    def calculate_user_ranks(self):
        ranked_users = User.objects.annotate(
            solved_problems_count=Count("results"),
            rank=Window(
                expression=RowNumber(),
                order_by=F('solved_problems_count').desc()
            )
        ).values('id', 'rank')
        self.user_ranks = {user['id']: user['rank'] for user in ranked_users}

    def get_rank(self, obj):
        return self.user_ranks.get(obj.id, None)

    def get_solved_problems(self, obj):
        solved_problems = SolutionResult.objects.filter(user=obj, passed=True).order_by("-executed_at")
        return UserProfileSolutionResultSerializer(solved_problems, many=True).data

    def get_was_complited_problems(self, obj):
        unique_solved_problems_count = SolutionResult.objects.filter(user=obj, passed=True).values('problem').distinct().count()
        return unique_solved_problems_count


class UserProfileSolutionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionResult
        fields = ["id", "executed_at", "lead_time", "memory_used", "passed"]

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        problem = obj.problem
        representation['problem'] = {
            "id": problem.id,
            "title": problem.title,
        }
        return representation


class TopUserSerializer(serializers.ModelSerializer):
    position = serializers.IntegerField()
    solved_problems = serializers.SerializerMethodField() 

    class Meta:
        model = User
        fields = ["position", "id", "username", "solved_problems"]

    def get_solved_problems(self, obj):
        unique_solved_problems_count = SolutionResult.objects.filter(user=obj, passed=True).values('problem').distinct().count()
        return unique_solved_problems_count