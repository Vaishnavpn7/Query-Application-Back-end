from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Questions, Answers


class UserSerialize(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AnswerSerialize(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    question = serializers.CharField(read_only=True)
    upvote = serializers.CharField(read_only=True)
    upvote_count = serializers.CharField(read_only=True)

    class Meta:
        model = Answers
        fields = '__all__'


class QuestionSerialize(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    question_answer = AnswerSerialize(read_only=True, many=True)

    class Meta:
        model = Questions
        fields = '__all__'
