from rest_framework import serializers

from core.main.models import SolutionResult
from django.utils import timezone

class SolutionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionResult
        fields = ["id", "problem", "user", "lead_time", "memory_used", "user_code", "passed"]
        read_only_fields = ('user',) 

    def create(self, validated_data):
        return SolutionResult.objects.create(
            problem=validated_data['problem'],
            user=self.context['user'],
            executed_at=timezone.now(),
            lead_time=validated_data['lead_time'],
            memory_used=validated_data['memory_used'],
            user_code=validated_data['user_code'],
            passed=validated_data['passed']
        )
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        problem = instance.problem
        representation["problem"] = {
            "id_problem": problem.id,
            "title": problem.title
        }
        return representation