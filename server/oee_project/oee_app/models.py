from django.db import models

class Machine(models.Model):
    machine_name = models.CharField(max_length=100)
    machine_serial_no = models.CharField(max_length=100, unique=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.machine_name

class ProductionLog(models.Model):
    cycle_no = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100, unique=True)
    material_name = models.CharField(max_length=100)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.FloatField()  # Duration in hours
    product_total = models.IntegerField()

    def __str__(self):
        return self.cycle_no
