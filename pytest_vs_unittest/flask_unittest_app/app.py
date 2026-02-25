from flask import Flask, request, jsonify, make_response
from copy import deepcopy

app = Flask(__name__)


class Employee:
    def __init__(self, id, nombre, apellido, email, fecha_nacimiento=None, telefono=None, puesto=None, salario=0.0, activo=True, departamento=None, fecha_contratacion=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.puesto = puesto
        self.salario = salario
        self.activo = activo
        self.departamento = departamento
        self.fecha_contratacion = fecha_contratacion

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_nacimiento": self.fecha_nacimiento,
            "email": self.email,
            "telefono": self.telefono,
            "puesto": self.puesto,
            "salario": self.salario,
            "activo": self.activo,
            "departamento": self.departamento,
            "fecha_contratacion": self.fecha_contratacion,
        }


class EmployeeStore:
    def __init__(self, seed=None):
        self.employees = []
        if seed:
            for d in seed:
                emp = Employee(**d)
                self.employees.append(emp)

    def _next_id(self):
        if not self.employees:
            return 1
        return max(e.id for e in self.employees) + 1

    def list(self):
        return [e.to_dict() for e in self.employees]

    def find(self, emp_id):
        return next((e for e in self.employees if e.id == emp_id), None)

    def exists_email(self, email, exclude_id=None):
        return any(e.email == email and (exclude_id is None or e.id != exclude_id) for e in self.employees)

    def create(self, data):
        required = ["nombre", "apellido", "email"]
        missing = [f for f in required if f not in data or not str(data.get(f)).strip()]
        if missing:
            return {"error": "Campos requeridos faltantes", "missing": missing}, 400
        if self.exists_email(data.get("email")):
            return {"error": "Email ya existe"}, 400
        emp = Employee(
            id=self._next_id(),
            nombre=data.get("nombre"),
            apellido=data.get("apellido"),
            email=data.get("email"),
            fecha_nacimiento=data.get("fecha_nacimiento"),
            telefono=data.get("telefono"),
            puesto=data.get("puesto"),
            salario=data.get("salario", 0.0),
            activo=data.get("activo", True),
            departamento=data.get("departamento"),
            fecha_contratacion=data.get("fecha_contratacion"),
        )
        self.employees.append(emp)
        return emp.to_dict(), 201

    def update(self, emp_id, data):
        emp = self.find(emp_id)
        if emp is None:
            return {"error": "Empleado no encontrado"}, 404
        if "email" in data and self.exists_email(data.get("email"), exclude_id=emp_id):
            return {"error": "Email ya existe"}, 400
        for key in ["nombre", "apellido", "fecha_nacimiento", "email", "telefono", "puesto", "salario", "activo", "departamento", "fecha_contratacion"]:
            if key in data:
                setattr(emp, key, data.get(key))
        return emp.to_dict(), 200

    def delete(self, emp_id):
        emp = self.find(emp_id)
        if emp is None:
            return {"error": "Empleado no encontrado"}, 404
        self.employees.remove(emp)
        return {"message": "Empleado eliminado"}, 200


# Seed data - same structure keys expected by Employee
SEED = [
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


# Create store and expose as module-level variable for tests to manipulate
store = EmployeeStore(seed=SEED)


@app.route("/")
def index():
    return jsonify({"message": "API Empleados (OO) - use /employees endpoint"})


@app.route("/employees", methods=["GET"])
def list_employees():
    return jsonify(store.list())


@app.route("/employees/<int:emp_id>", methods=["GET"])
def get_employee(emp_id):
    emp = store.find(emp_id)
    if emp is None:
        return make_response(jsonify({"error": "Empleado no encontrado"}), 404)
    return jsonify(emp.to_dict())


@app.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json() or {}
    result, code = store.create(data)
    return make_response(jsonify(result), code)


@app.route("/employees/<int:emp_id>", methods=["PUT"])
def update_employee(emp_id):
    data = request.get_json() or {}
    result, code = store.update(emp_id, data)
    return make_response(jsonify(result), code)


@app.route("/employees/<int:emp_id>", methods=["DELETE"])
def delete_employee(emp_id):
    result, code = store.delete(emp_id)
    return make_response(jsonify(result), code)
