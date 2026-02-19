from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

# Semilla de 10 empleados (lista en memoria)
empleados = [
    {"id": 1, "nombre": "Juan", "apellido": "Pérez", "fecha_nacimiento": "1990-01-01", "email": "juan.perez@empresa.com", "telefono": "123456789", "puesto": "Desarrollador", "salario": 50000.0, "activo": True, "departamento": "Tecnología", "fecha_contratacion": "2020-01-01"},
    {"id": 2, "nombre": "María", "apellido": "Gómez", "fecha_nacimiento": "1985-05-12", "email": "maria.gomez@empresa.com", "telefono": "234567890", "puesto": "Analista", "salario": 45000.0, "activo": True, "departamento": "Finanzas", "fecha_contratacion": "2019-03-15"},
    {"id": 3, "nombre": "Luis", "apellido": "Ramírez", "fecha_nacimiento": "1992-07-08", "email": "luis.ramirez@empresa.com", "telefono": "345678901", "puesto": "QA", "salario": 38000.0, "activo": True, "departamento": "Calidad", "fecha_contratacion": "2021-06-01"},
    {"id": 4, "nombre": "Ana", "apellido": "López", "fecha_nacimiento": "1991-11-20", "email": "ana.lopez@empresa.com", "telefono": "456789012", "puesto": "Soporte", "salario": 32000.0, "activo": True, "departamento": "Soporte", "fecha_contratacion": "2018-09-10"},
    {"id": 5, "nombre": "Carlos", "apellido": "Vargas", "fecha_nacimiento": "1988-02-02", "email": "carlos.vargas@empresa.com", "telefono": "567890123", "puesto": "DevOps", "salario": 55000.0, "activo": True, "departamento": "Infraestructura", "fecha_contratacion": "2017-04-22"},
    {"id": 6, "nombre": "Sofía", "apellido": "Martínez", "fecha_nacimiento": "1995-08-30", "email": "sofia.martinez@empresa.com", "telefono": "678901234", "puesto": "Diseñadora", "salario": 41000.0, "activo": True, "departamento": "Diseño", "fecha_contratacion": "2022-01-05"},
    {"id": 7, "nombre": "Pedro", "apellido": "Núñez", "fecha_nacimiento": "1983-12-14", "email": "pedro.nunez@empresa.com", "telefono": "789012345", "puesto": "Gerente", "salario": 80000.0, "activo": True, "departamento": "Operaciones", "fecha_contratacion": "2015-07-18"},
    {"id": 8, "nombre": "Luisa", "apellido": "Cano", "fecha_nacimiento": "1994-03-03", "email": "luisa.cano@empresa.com", "telefono": "890123456", "puesto": "Recursos Humanos", "salario": 47000.0, "activo": True, "departamento": "RRHH", "fecha_contratacion": "2020-10-11"},
    {"id": 9, "nombre": "Mateo", "apellido": "Ortega", "fecha_nacimiento": "1996-09-09", "email": "mateo.ortega@empresa.com", "telefono": "901234567", "puesto": "Intern", "salario": 18000.0, "activo": False, "departamento": "Tecnología", "fecha_contratacion": "2023-05-01"},
    {"id": 10, "nombre": "Elena", "apellido": "Ríos", "fecha_nacimiento": "1989-06-25", "email": "elena.rios@empresa.com", "telefono": "012345678", "puesto": "Arquitecto", "salario": 90000.0, "activo": True, "departamento": "Arquitectura", "fecha_contratacion": "2016-02-29"}
]


def _next_id():
    if not empleados:
        return 1
    return max(e["id"] for e in empleados) + 1


def _find_employee(emp_id):
    return next((e for e in empleados if e["id"] == emp_id), None)


def _validate_required(data):
    required = ["nombre", "apellido", "email"]
    missing = [f for f in required if f not in data or not str(data.get(f)).strip()]
    return missing


@app.route('/')
def index():
    return jsonify({"message": "API Empleados - use /employees endpoint"})


@app.route('/employees', methods=['GET'])
def list_employees():
    return jsonify(empleados)


@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    emp = _find_employee(emp_id)
    if emp is None:
        return make_response(jsonify({"error": "Empleado no encontrado"}), 404)
    return jsonify(emp)


@app.route('/employees', methods=['POST'])
def create_employee():
    data = request.get_json() or {}
    missing = _validate_required(data)
    if missing:
        return make_response(jsonify({"error": "Campos requeridos faltantes", "missing": missing}), 400)
    # email uniqueness
    if any(e["email"] == data.get("email") for e in empleados):
        return make_response(jsonify({"error": "Email ya existe"}), 400)
    emp = {
        "id": _next_id(),
        "nombre": data.get("nombre"),
        "apellido": data.get("apellido"),
        "fecha_nacimiento": data.get("fecha_nacimiento"),
        "email": data.get("email"),
        "telefono": data.get("telefono"),
        "puesto": data.get("puesto"),
        "salario": data.get("salario", 0.0),
        "activo": data.get("activo", True),
        "departamento": data.get("departamento"),
        "fecha_contratacion": data.get("fecha_contratacion")
    }
    empleados.append(emp)
    return make_response(jsonify(emp), 201)


@app.route('/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    emp = _find_employee(emp_id)
    if emp is None:
        return make_response(jsonify({"error": "Empleado no encontrado"}), 404)
    data = request.get_json() or {}
    # If email provided, ensure uniqueness
    if "email" in data and any(e["email"] == data.get("email") and e["id"] != emp_id for e in empleados):
        return make_response(jsonify({"error": "Email ya existe"}), 400)
    # update allowed fields
    for key in ["nombre", "apellido", "fecha_nacimiento", "email", "telefono", "puesto", "salario", "activo", "departamento", "fecha_contratacion"]:
        if key in data:
            emp[key] = data.get(key)
    return jsonify(emp)


@app.route('/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    emp = _find_employee(emp_id)
    if emp is None:
        return make_response(jsonify({"error": "Empleado no encontrado"}), 404)
    empleados.remove(emp)
    return make_response(jsonify({"message": "Empleado eliminado"}), 200)
