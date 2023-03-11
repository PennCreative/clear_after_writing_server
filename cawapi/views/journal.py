from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cawapi.models import User, Journal, Survey, Stat
from rest_framework.decorators import action
from rest_framework import generics
from django.utils import timezone
from django.db.models import Avg

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ('id', 'writer', 'date', 'goal_entry', 'affirmation', 'distraction', 'significant', 'entry', 'overall_rating')
        depth = 1

class JournalView(ViewSet):
    """Request Handlers for Journals"""
    def retrieve(self, request, pk):
        try:
            journal = Journal.objects.get(pk=pk)
            ratings = Stat.objects.filter(journal=journal)
            if ratings:
                overall_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            else:
                overall_rating = None
            journal.overall_rating = overall_rating
            serializer = JournalSerializer(journal)

            return Response(serializer.data)
        except Journal.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """GET Handlers for Journal"""
        journals = Journal.objects.all()
        id_query = request.query_params.get('id', None)

        if id_query is not None:
            journals = journals.filter(journal=id_query)

        serializer = JournalSerializer(journals, many = True)
        return Response(serializer.data)

    def create(self, request):
        """POST request for Journal"""
        writer = User.objects.get(id=request.data["writer_id"])
        journal = Journal.objects.create(
          writer = writer,
          date = request.data["date"],
          goal_entry = request.data["goal_entry"],
          affirmation = request.data["affirmation"],
          distraction = request.data["distraction"],
          significant = request.data["significant"],
          entry = request.data["entry"]
        )
        
        # Retrieve survey ratings for the journal and calculate the overall rating
        ratings = Stat.objects.filter(journal=journal)
        if ratings:
            overall_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        else:
            overall_rating = None
        
        # Update the journal with the overall rating
        journal.overall_rating = overall_rating
        journal.save()

        serializer = JournalSerializer(journal)
        return Response(serializer.data)

    def update(self, request, pk):
        """PUT requests for Journal"""
        journal = Journal.objects.get(pk=pk)

        journal.date = request.data["date"]
        journal.goal_entry = request.data["goal_entry"]
        journal.affirmation = request.data["affirmation"]
        journal.distraction = request.data["distraction"]
        journal.significant = request.data["significant"]
        journal.entry = request.data["entry"]
        journal.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """DELETE Journal"""
        journal = Journal.objects.get(pk=pk)
        journal.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class todaysJournalView(generics.ListCreateAPIView):
    serializer_class = JournalSerializer

    def get_queryset(self):
        today = timezone.now().date()
        
        date = self.kwargs['date']
        if date == 'today':
            return Journal.objects.filter(date=today)
        else:
            return Journal.objects.filter(date=date)
class WriterJournalView(ViewSet):
    """Request Handlers for Journals filtered by writer's id"""
    serializer_class = JournalSerializer
    
    @action(detail=False, methods=['get'])
    def list_by_writer_id(self, request):
        writer_id = request.query_params.get('writer_id')
        if not writer_id:
            return Response({'message': 'writer_id query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        journals = Journal.objects.filter(writer__id=writer_id)
        serializer = self.serializer_class(journals, many=True)
        return Response(serializer.data)
