import importlib
import copy
import pytest

# Importar el módulo de la app
app_mod = importlib.import_module("flask_pytest_app.app")

# Copia original de los empleados para restaurar antes de cada test
ORIGINAL_EMPLEADOS = copy.deepcopy(app_mod.empleados)


@pytest.fixture
def client():
    # Restaurar la lista de empleados antes de cada test (in-place)
    app_mod.empleados[:] = copy.deepcopy(ORIGINAL_EMPLEADOS)
    app_mod.app.config["TESTING"] = True
    with app_mod.app.test_client() as client:
        yield client


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "API Empleados" in data.get("message", "")


def test_list_employees(client):
    resp = client.get("/employees")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == len(ORIGINAL_EMPLEADOS)


def test_get_employee_found(client):
    resp = client.get("/employees/1")
    assert resp.status_code == 200
    emp = resp.get_json()
    assert emp["id"] == 1
    assert emp["nombre"] == "Juan"


def test_get_employee_not_found(client):
    resp = client.get("/employees/999")
    assert resp.status_code == 404
    assert resp.get_json().get("error") == "Empleado no encontrado"


def test_create_employee_success_defaults(client):
    nuevo = {"nombre": "Test", "apellido": "User", "email": "test.user@empresa.com"}
    resp = client.post("/employees", json=nuevo)
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["nombre"] == "Test"
    assert data["email"] == "test.user@empresa.com"
    assert data["salario"] == 0.0
    assert data["activo"] is True


def test_create_employee_missing_required(client):
    nuevo = {"nombre": "SinEmail", "apellido": "User"}
    resp = client.post("/employees", json=nuevo)
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("error") == "Campos requeridos faltantes"
    assert "email" in data.get("missing", [])


def test_create_employee_duplicate_email(client):
    dup = {"nombre": "Dup", "apellido": "User", "email": ORIGINAL_EMPLEADOS[0]["email"]}
    resp = client.post("/employees", json=dup)
    assert resp.status_code == 400
    assert resp.get_json().get("error") == "Email ya existe"


def test_update_employee_success(client):
    payload = {"nombre": "Juanito", "email": "juanito.nuevo@empresa.com"}
    resp = client.put("/employees/1", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["id"] == 1
    assert data["nombre"] == "Juanito"
    assert data["email"] == "juanito.nuevo@empresa.com"


def test_update_employee_not_found(client):
    resp = client.put("/employees/999", json={"nombre": "NoExiste"})
    assert resp.status_code == 404
    assert resp.get_json().get("error") == "Empleado no encontrado"


def test_update_employee_duplicate_email(client):
    # Intentar asignar el email del empleado 2 al empleado 1
    email_2 = ORIGINAL_EMPLEADOS[1]["email"]
    resp = client.put("/employees/1", json={"email": email_2})
    assert resp.status_code == 400
    assert resp.get_json().get("error") == "Email ya existe"


def test_delete_employee_success(client):
    resp = client.delete("/employees/1")
    assert resp.status_code == 200
    assert resp.get_json().get("message") == "Empleado eliminado"
    # Verificar que ya no exista
    resp2 = client.get("/employees/1")
    assert resp2.status_code == 404


def test_delete_employee_not_found(client):
    resp = client.delete("/employees/999")
    assert resp.status_code == 404
    assert resp.get_json().get("error") == "Empleado no encontrado"
