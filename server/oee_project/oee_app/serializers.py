from rest_framework import serializers
from oee_app.models import Machine, ProductionLog

class ProductionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionLog
        fields = '__all__'

class MachineSerializer(serializers.ModelSerializer):
    production_logs = ProductionLogSerializer(many=True, read_only=True)

    class Meta:
        model = Machine
        fields = '__all__'
