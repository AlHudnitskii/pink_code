from rest_framework import serializers

from core.main.models import Problem, TestCase


class ProblemSerializer(serializers.ModelSerializer):
    count_solutions = serializers.SerializerMethodField()
    
    class Meta:
        model = Problem
        fields = [
            "id", "author", "title", "type", "subtitle", "description", "difficulty", "count_solutions", "fst_line"
        ]
    def get_count_solutions(self, obj):
        return obj.get_count_solutions_of_problem()
    
    def to_representation(self, instance: Problem):
        representation = super().to_representation(instance)
        rates = instance.get_rates()
        representation["rates"] = {
            "likes": rates["likes"],
            "dislikes": rates["dislikes"],
        }
        return representation


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input_data', 'expected_output']
        read_only_fields = ['id']

    def create(self, validated_data):
        id_problem = self.context.get('id_problem')
        if id_problem is None:
            raise serializers.ValidationError("Problem ID is required to create a test case.")
        try:
            problem = Problem.objects.get(id=id_problem)
        except Problem.DoesNotExist:
            raise serializers.ValidationError(f"Problem with ID {id_problem} does not exist.")

        test_case = TestCase.objects.create(problem=problem, **validated_data)
        return test_case    