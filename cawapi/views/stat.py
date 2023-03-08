from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cawapi.models import Survey, Stat, Journal

class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = ('id', 'journal', 'survey', 'rating')
        depth = 1


class StatView(ViewSet):
    """Requests for Stat"""
    def retrieve(self, request, pk):
        try:
            stat = Stat.objects.get(pk=pk)
            serializer = StatSerializer(stat)
            return Response(serializer.data)
        except Stat.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Get requests for Stats"""
        stat = Stat.objects.all()
        journal = self.request.query_params.get('journal_id', None)

        if journal is not None:
            stat = stat.filter(journal_id=journal)

        serializer = StatSerializer(stat, many=True)
        return Response(serializer.data)

    def create(self, request):
        """POST for Stats"""
        journal = Journal.objects.get(pk=request.data['journal'])
        survey = Survey.objects.get(pk=request.data['survey'])

        stat = Stat.objects.create(
            journal = journal,
            survey = survey,
            rating = request.data["rating"],
        )

        serializer = StatSerializer(stat)
        return Response(serializer.data)

    def update(self, request, pk):
        stat = Stat.objects.get(pk=pk)
        stat.rating = request.data["rating"]
        stat.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        stat = Stat.objects.get(pk=pk)
        stat.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
