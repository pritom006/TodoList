
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import TodoItem
from .serializers import TodoItemSerializer
from rest_framework.response import Response
from rest_framework import status
class TodoItemViewSet(viewsets.ModelViewSet):
    queryset = TodoItem.objects.all().order_by('-created_at')
    serializer_class = TodoItemSerializer

    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_fields = ['is_completed']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        response_data = dict()
        if serializer.is_valid():
            serializer.save()
            response_data['data'] = serializer.data
            response_data['message'] = "Create New Todo object"
            response_data['status'] = status.HTTP_201_CREATED
        else:
            response_data['message'] = "Fillup all input data"
            response_data['status'] = status.HTTP_400_BAD_REQUEST
            
        return Response(response_data,status=response_data['status'])

    def update(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(instance=queryset,data = request.data)
        response_data = dict()
        if serializer.is_valid():
            serializer.save()
            response_data['data'] = serializer.data
            response_data['message'] = "Update this todo object informations"
            response_data['status'] = status.HTTP_202_ACCEPTED
        else:
            response_data['message'] = "Bad Request"
            response_data['status'] = status.HTTP_400_BAD_REQUEST
        return Response(response_data,status=response_data['status'])
    def destroy(self, request, *args, **kwargs):
        object_data = self.get_object()
        response_data = dict()
        if object_data:
            object_data.delete()
            response_data['message'] = "Delete this information"
            response_data['status'] = status.HTTP_202_ACCEPTED
        else:
            response_data['message'] = "invalid information"
            response_data['status'] = status.HTTP_400_BAD_REQUEST

        return Response(response_data,status=response_data['status'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(instance = queryset,many=True)
        response_data = dict()
        response_data['data'] = serializer.data
        response_data['message'] = 'Todo list'
        response_data['status'] = status.HTTP_200_OK
        return Response(response_data,status=response_data['status'])