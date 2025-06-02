from rest_framework import serializers
from core.main.models import SolutionResult, Problem
from django.utils import timezone

class SolutionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionResult
        fields = ["id", "problem", "user", "lead_time", "memory_used", "user_code", "passed"]
        read_only_fields = ['id', 'user', 'problem']

    def create(self, validated_data):
        problem_id = self.context.get('problem_id')
        user = self.context.get('user')
        if not problem_id:
            raise serializers.ValidationError("Problem ID is required.")
        if not user:
            raise serializers.ValidationError("User is required.")
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            raise serializers.ValidationError(f"Problem with ID {problem_id} does not exist.")

        return SolutionResult.objects.create(
            problem=problem,
            user=user,
            executed_at=timezone.now(),
            **validated_data 
        )    

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        problem = instance.problem
        representation["problem"] = {
            "id_problem": problem.id,
            "title": problem.title
        }
        return representation