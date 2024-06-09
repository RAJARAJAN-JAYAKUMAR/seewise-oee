from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from oee_app.models import Machine, ProductionLog

class MachineViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.machine = Machine.objects.create(machine_name='Test Machine', machine_serial_no='12345')

    def test_get_machines(self):
        response = self.client.get(reverse('machine-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['machine_name'], 'Test Machine')

    def test_create_machine(self):
        data = {'machine_name': 'New Machine', 'machine_serial_no': '67890'}
        response = self.client.post(reverse('machine-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Machine.objects.count(), 2)
        self.assertEqual(Machine.objects.get(id=response.data['id']).machine_name, 'New Machine')
        
class ProductionLogViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.machine = Machine.objects.create(machine_name='Test Machine', machine_serial_no='12345')
        self.production_log = ProductionLog.objects.create(
            cycle_no='CN001',
            unique_id='UID001',
            material_name='Material1',
            machine=self.machine,
            start_time='2023-01-01T00:00:00Z',
            end_time='2023-01-01T01:00:00Z',
            duration=1.0,
            product_total=100  # Provide a value for the product_total field
        )

    def test_get_production_logs(self):
        response = self.client.get(reverse('log-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['cycle_no'], 'CN001')

    def test_create_production_log(self):
        data = {
            'cycle_no': 'CN002',
            'unique_id': 'UID002',
            'material_name': 'Material2',
            'machine': self.machine.id,
            'start_time': '2023-01-01T02:00:00Z',
            'end_time': '2023-01-01T03:00:00Z',
            'duration': 1.0,
            'product_total': 50  # Provide a value for the product_total field
        }
        response = self.client.post(reverse('log-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductionLog.objects.count(), 2)
        self.assertEqual(ProductionLog.objects.get(id=response.data['id']).cycle_no, 'CN002')

# class MachineOeeTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.machine = Machine.objects.create(machine_name='Test Machine', machine_serial_no='12345')
#         self.production_log_1 = ProductionLog.objects.create(
#             cycle_no='CN001',
#             unique_id='UID001',
#             material_name='Material1',
#             machine=self.machine,
#             start_time='2023-01-01T00:00:00Z',
#             end_time='2023-01-01T00:05:00Z',
#             duration=5/60  # 5 minutes in hours
#         )
#         self.production_log_2 = ProductionLog.objects.create(
#             cycle_no='CN002',
#             unique_id='UID002',
#             material_name='Material2',
#             machine=self.machine,
#             start_time='2023-01-01T00:10:00Z',
#             end_time='2023-01-01T00:20:00Z',
#             duration=10/60  # 10 minutes in hours
#         )

#     def test_get_machine_oee(self):
#         response = self.client.get(reverse('machine_oee', kwargs={'machine_id': self.machine.id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         oee_data = response.data[0]['oee_data']
#         self.assertIn('availability', oee_data)
#         self.assertIn('performance', oee_data)
#         self.assertIn('quality', oee_data)
#         self.assertIn('oee', oee_data)

#     def test_get_machine_oee_with_date_range(self):
#         response = self.client.get(reverse('machine_oee', kwargs={
#             'machine_id': self.machine.id,
#             'start_date': '2023-01-01',
#             'end_date': '2023-01-02'
#         }))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         oee_data = response.data[0]['oee_data']
#         self.assertIn('availability', oee_data)
#         self.assertIn('performance', oee_data)
#         self.assertIn('quality', oee_data)
#         self.assertIn('oee', oee_data)

#     def test_get_machine_oee_no_data(self):
#         # Create a new machine without any production logs
#         machine_without_logs = Machine.objects.create(machine_name='Test Machine 2', machine_serial_no='54321')

#         response = self.client.get(reverse('machine_oee', kwargs={'machine_id': machine_without_logs.id}))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         oee_data = response.data[0]['oee_data']
#         # Check that all OEE metrics are zero
#         self.assertEqual(oee_data['availability'], 0)
#         self.assertEqual(oee_data['performance'], 0)
#         self.assertEqual(oee_data['quality'], 0)
#         self.assertEqual(oee_data['oee'], 0)

#     def test_get_machine_oee_invalid_date_range(self):
#         # Provide an invalid date range where end_date is before start_date
#         response = self.client.get(reverse('machine_oee', kwargs={
#             'machine_id': self.machine.id,
#             'start_date': '2023-01-02',
#             'end_date': '2023-01-01'
#         }))
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MachineOeeTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.machine = Machine.objects.create(machine_name='Test Machine', machine_serial_no='12345')
        self.production_log_1 = ProductionLog.objects.create(
            cycle_no='CN001',
            unique_id='UID001',
            material_name='Material1',
            machine=self.machine,
            start_time='2023-01-01T00:00:00Z',
            end_time='2023-01-01T00:05:00Z',
            duration=5/60,  # 5 minutes in hours
            product_total=100  # Adjust the product total value as needed
        )
        self.production_log_2 = ProductionLog.objects.create(
            cycle_no='CN002',
            unique_id='UID002',
            material_name='Material2',
            machine=self.machine,
            start_time='2023-01-01T00:10:00Z',
            end_time='2023-01-01T00:20:00Z',
            duration=10/60,  # 10 minutes in hours
            product_total=200  # Adjust the product total value as needed
        )

    def test_get_machine_oee(self):
        response = self.client.get(reverse('machine_oee_detail', kwargs={'machine_id': self.machine.id}))
        print('firsttttttttttttttt', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        oee_data = response.data[0]['oee_data']
        self.assertIn('availability', oee_data)
        self.assertIn('performance', oee_data)
        self.assertIn('quality', oee_data)
        self.assertIn('oee', oee_data)

    def test_get_machine_oee_with_date_range(self):
        response = self.client.get(reverse('machine_oee_filter', kwargs={
            'machine_id': self.machine.id,
            'start_date': '2023-01-01',
            'end_date': '2023-01-02'
        }))
        print('secondddddddddddddddd', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        oee_data = response.data[0]['oee_data']
        self.assertIn('availability', oee_data)
        self.assertIn('performance', oee_data)
        self.assertIn('quality', oee_data)
        self.assertIn('oee', oee_data)
