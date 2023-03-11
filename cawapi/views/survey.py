from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cawapi.models import Survey

class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ('id', 'question', 'answer')
        depth = 1

class SurveyView(ViewSet):
    """Request Handlers for Surveys"""
    def retrieve(self, request, pk):
        try:
            survey = Survey.objects.get(pk=pk)
            serializer = SurveySerializer(survey)

            return Response(serializer.data)
        except Survey.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET Handlers for Survey"""
        surveys = Survey.objects.all()
        id_query = request.query_params.get('id', None)
        if id_query is not None:
            surveys = surveys.filter(survey=id_query)

        serializer = SurveySerializer(surveys, many = True)
        return Response(serializer.data)

    def create(self, request):
        """POST request for Survey"""
        survey = Survey.objects.create(
          question = request.data["question"],
          answer = request.data["answer"],
        )
        serializer = SurveySerializer(survey)
        return Response(serializer.data)

    def update(self, request, pk):
        """PUT requests for Survey"""
        survey = Survey.objects.get(pk=pk)

        survey.question = request.data["question"]
        survey.answer = request.data["answer"]
        survey.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """DELETE Survey"""
        survey = Survey.objects.get(pk=pk)
        survey.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
