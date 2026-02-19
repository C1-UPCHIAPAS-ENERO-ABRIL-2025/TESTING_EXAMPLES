import copy
import unittest
from flask import json

import importlib

# Importar el módulo de la app orientada a objetos
app_mod = importlib.import_module("flask_unittest_app.app")


class TestEmpleadoCRUD(unittest.TestCase):
    """Pruebas CRUD para la API de Empleados (orientada a objetos).

    Estas pruebas usan `setUp` y `tearDown` para restaurar el estado
    compartido de `store.employees` antes y después de cada caso, demostrando
    la rigidez y el control de `unittest`.
    """

    def setUp(self):
        # Backup profundo del estado original
        self._backup = copy.deepcopy(app_mod.store.employees)
        app_mod.app.testing = True
        self.client = app_mod.app.test_client()

    def tearDown(self):
        # Restaurar el estado original (in-place)
        app_mod.store.employees[:] = self._backup

    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn('API Empleados', data.get('message', ''))

    def test_list_employees(self):
        resp = self.client.get('/employees')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), len(self._backup))

    def test_get_employee_found(self):
        resp = self.client.get('/employees/1')
        self.assertEqual(resp.status_code, 200)
        emp = resp.get_json()
        self.assertEqual(emp['id'], 1)
        self.assertEqual(emp['nombre'], 'Juan')

    def test_get_employee_not_found(self):
        resp = self.client.get('/employees/999')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.get_json().get('error'), 'Empleado no encontrado')

    def test_create_employee_success(self):
        nuevo = {'nombre': 'UnitTest', 'apellido': 'User', 'email': 'unittest.user@empresa.com'}
        resp = self.client.post('/employees', data=json.dumps(nuevo), content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data['nombre'], 'UnitTest')
        self.assertEqual(data['email'], 'unittest.user@empresa.com')
        self.assertEqual(data['salario'], 0.0)

    def test_create_employee_missing_required(self):
        nuevo = {'nombre': 'NoEmail', 'apellido': 'User'}
        resp = self.client.post('/employees', data=json.dumps(nuevo), content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        data = resp.get_json()
        self.assertEqual(data.get('error'), 'Campos requeridos faltantes')
        self.assertIn('email', data.get('missing', []))

    def test_create_employee_duplicate_email(self):
        dup = {'nombre': 'Dup', 'apellido': 'User', 'email': self._backup[0].email}
        # Duplicate uses email from seed
        resp = self.client.post('/employees', data=json.dumps({'nombre': 'Dup','apellido':'User','email': self._backup[0].email}), content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json().get('error'), 'Email ya existe')

    def test_update_employee_success(self):
        payload = {'nombre': 'Modificado', 'email': 'modificado@empresa.com'}
        resp = self.client.put('/employees/1', data=json.dumps(payload), content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['nombre'], 'Modificado')

    def test_update_employee_not_found(self):
        resp = self.client.put('/employees/999', data=json.dumps({'nombre': 'X'}), content_type='application/json')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.get_json().get('error'), 'Empleado no encontrado')

    def test_update_employee_duplicate_email(self):
        # Attempt to set employee 1's email to the email of employee 2
        email_2 = self._backup[1].email
        resp = self.client.put('/employees/1', data=json.dumps({'email': email_2}), content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.get_json().get('error'), 'Email ya existe')

    def test_delete_employee_success(self):
        resp = self.client.delete('/employees/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json().get('message'), 'Empleado eliminado')
        # Verify removed
        resp2 = self.client.get('/employees/1')
        self.assertEqual(resp2.status_code, 404)

    def test_delete_employee_not_found(self):
        resp = self.client.delete('/employees/999')
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.get_json().get('error'), 'Empleado no encontrado')


if __name__ == '__main__':
    unittest.main(verbosity=2)
