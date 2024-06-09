from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from oee_app.models import ProductionLog
from oee_app.serializers import ProductionLogSerializer

@api_view(['GET', 'POST'])
def productionlog_list_create(request):
    if request.method == 'GET':
        logs = ProductionLog.objects.all()
        serializer = ProductionLogSerializer(logs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductionLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
