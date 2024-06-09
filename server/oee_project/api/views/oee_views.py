from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from oee_app.models import Machine, ProductionLog
from oee_app.serializers import MachineSerializer, ProductionLogSerializer
import datetime

# OEE Calculation Utility
def calculate_oee(machine):
    logs = ProductionLog.objects.filter(machine=machine)
    print(logs.values('product_total'))
    

    
    # AVAILABLE_TIME = 8 * 3   3 shifts of 8 hours each
    # IDEAL_CYCLE_TIME = 5 / 60   5 minutes in hours
    
    # Constants
    AVAILABLE_TIME = 24
    IDEAL_CYCLE_TIME = 0.083

    if not logs.exists():
        return {
            #log doesn't exist
            'availability': 0,
            'performance': 0,
            'quality': 0,
            'oee': 0,
        }

    total_duration = sum(log.duration for log in logs)
    print(total_duration)
    total_products = sum(log.product_total for log in logs)
    print(total_products)
    good_products = total_products*0.9  #assumption
    print(good_products)
    
    print("first",total_duration,total_products,good_products)

    availability = ((AVAILABLE_TIME - (AVAILABLE_TIME - total_duration)) / AVAILABLE_TIME) * 100
    performance = ((IDEAL_CYCLE_TIME * total_products) / total_duration )* 100
    quality = (good_products / total_products)* 100
    
    print(availability,performance,quality)
    
    
    #oee = (availability * performance * quality)
    
    #oee in percentage
    oee = (availability * performance * quality)/10000 
    
    
    return {
        'availability': availability,
        'performance': performance,
        'quality': quality,
        'oee': oee,
    }

@api_view(['GET'])
def machine_oee(request, machine_id=None, start_date=None, end_date=None):
    if machine_id:
        machines = Machine.objects.filter(id=machine_id) #gets me the filtered machine
    else:
        machines = Machine.objects.all()

    if start_date and end_date:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        machines = machines.filter(time__range=(start_date, end_date))

    data = []
    for machine in machines:
        oee_data = calculate_oee(machine)
        data.append({
            'machine': MachineSerializer(machine).data,
            'oee_data': oee_data,
        })

    return Response(data, status=status.HTTP_200_OK)
