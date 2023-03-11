"""View module for handling requests about users"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from cawapi.models import User

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for Users"""
    class Meta:
        model = User
        fields = ('id', 'uid', 'first_name', 'last_name', 'email', 'profile_image_url', 'created_on')

class UserView(ViewSet):
  """User View"""
  
  def retrieve(self, request, pk):
        """Handles Single User"""
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
    
        except User.DoesNotExist as exception:
            return Response({'message': exception.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
  def list(self, request):
    """Handle GET requests to get all users"""
    
    users = User.objects.all()
    uid_query = request.query_params.get('uid', None)
    if uid_query is not None:
            users = users.filter(uid=uid_query)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
  
  def create(self, request):
    
    user = User.objects.create(
      uid = request.data["uid"],
      first_name = request.data["first_name"],
      last_name = request.data["last_name"],
      email = request.data["email"],
      profile_image_url = request.data["profile_image_url"],
      created_on = request.data["created_on"],
    )
    serializer = UserSerializer(user)
    return Response(serializer.data)

  def update(self, request, pk):
        """Handle PT requests for users
       Returns:
        Response -- Empty body with 204 status code
      """
        user = User.objects.get(pk=pk)
    
        user.uid = request.data["uid"]
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.email = request.data["email"]
        user.profile_image_url = request.data["profile_image_url"]
        user.created_on = request.data["created_on"]
    
        user.save()
    
        return Response(None, status=status.HTTP_204_NO_CONTENT)
  
  def destroy(self, request, pk):
        """DELETE User"""
    
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
