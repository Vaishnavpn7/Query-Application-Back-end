from django.shortcuts import render
from api.models import Questions, Answers
from rest_framework.response import Response
from rest_framework import viewsets
from api.serializer import UserSerialize, QuestionSerialize, AnswerSerialize
from rest_framework import authentication, permissions
from rest_framework.decorators import action


class UserView(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):

        serializer = UserSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerialize
    queryset = Questions.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = QuestionSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def query_set(self, ):
        return Questions.objects.all().exclude(user=self.request.user)

    @action(methods=['POST'], detail=True)
    def add_answer(self, request, *args, **kw):
        id = kw.get('pk')
        object = Questions.objects.get(id=id)
        serializer = AnswerSerialize(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user, question=object)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


from rest_framework import serializers


class AnswerView(viewsets.ModelViewSet):
    serializer_class = AnswerSerialize
    queryset = Answers.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise serializers.ValidationError('method not allowed')

    def list(self, request, *args, **kw):
        raise serializers.ValidationError('method not allowed')

    def destroy(self, request, *args, **kwargs):
        object = self.get_object()
        if request.user == object.user:
            object.delete()
            return Response(data='Deleated')
        else:
            raise serializers.ValidationError('permission denied for this user')

    @action(methods=['POST'], detail=True)
    def upvote(self, request, *args, **kwargs):
        object = self.get_object()
        user = request.user
        object.upvote.add(user)
        return Response(data='up voted')
