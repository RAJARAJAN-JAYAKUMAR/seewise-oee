from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from oee_app.models import Machine
from oee_app.serializers import MachineSerializer

@api_view(['GET', 'POST'])
def machine_list_create(request):
    if request.method == 'GET':
        machines = Machine.objects.all()
        serializer = MachineSerializer(machines, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = MachineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
