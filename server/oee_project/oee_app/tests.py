from django.test import TestCase
from .models import Machine, ProductionLog
from django.utils import timezone
from datetime import timedelta

class MachineModelTestCase(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(
            machine_name="Test Machine",
            machine_serial_no="12345"
        )

    def test_machine_creation(self):
        self.assertEqual(self.machine.machine_name, "Test Machine")
        self.assertEqual(self.machine.machine_serial_no, "12345")
        self.assertTrue(self.machine.time)

    def test_machine_str(self):
        self.assertEqual(str(self.machine), "Test Machine")

class ProductionLogModelTestCase(TestCase):
    def setUp(self):
        self.machine = Machine.objects.create(
            machine_name="Test Machine",
            machine_serial_no="12345"
        )
        self.production_log = ProductionLog.objects.create(
            cycle_no="CN001",
            unique_id="UID001",
            material_name="Material 1",
            machine=self.machine,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            duration=1.0
        )

    def test_production_log_creation(self):
        self.assertEqual(self.production_log.cycle_no, "CN001")
        self.assertEqual(self.production_log.unique_id, "UID001")
        self.assertEqual(self.production_log.material_name, "Material 1")
        self.assertEqual(self.production_log.machine, self.machine)
        self.assertTrue(self.production_log.start_time)
        self.assertTrue(self.production_log.end_time)
        self.assertEqual(self.production_log.duration, 1.0)

    def test_production_log_str(self):
        self.assertEqual(str(self.production_log), "CN001")
