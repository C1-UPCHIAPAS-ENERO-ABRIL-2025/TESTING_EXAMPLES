## Proyecto de comparación: Pytest (funcional) vs Unittest (orientado a objetos)

Este repositorio contiene dos pequeñas aplicaciones Flask que implementan
un CRUD para la entidad `Empleado` (semilla de 10 empleados). El objetivo es
comparar la experiencia de pruebas rápidas y ágiles con `pytest` frente a la
rigidez y verbosidad de `unittest`.

Estructura relevante
- `flask_pytest_app/`
  - `app.py` : implementación simple (funcional) y lista en memoria `empleados`.
  - `test_app.py` : pruebas con `pytest` (funciones y fixture que restaura la semilla).
- `flask_unittest_app/`
  - `app.py` : implementación orientada a objetos (`Employee`, `EmployeeStore`).
  - `test_unittest.py` : pruebas con `unittest.TestCase` usando `setUp` y `tearDown`.

Requisitos
- Python 3.8+
- Un entorno virtual (recomendado)

Comandos (PowerShell)

1) Crear y activar entorno virtual (opcional pero recomendado):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Instalar dependencias:

```powershell
pip install --upgrade pip
pip install Flask pytest
```

3) Ejecutar la suite `pytest` (rápida, funciones):

```powershell
.venv\Scripts\python -m pytest -q flask_pytest_app
```

4) Ejecutar la suite `unittest` (verbosa, orientada a objetos):

```powershell
.venv\Scripts\python -m unittest discover -v flask_unittest_app
```

Ejecutar ambas y comparar

```powershell
.venv\Scripts\python -m pytest -q flask_pytest_app > pytest-output.txt
.venv\Scripts\python -m unittest discover -v flask_unittest_app > unittest-output.txt
```

Breve explicación de las sesiones de prueba
- Pytest (`flask_pytest_app/test_app.py`):
  - Tests escritos como funciones independientes.
  - Fixture `client` crea el `test_client()` de Flask y restaura la lista en memoria
    (`empleados[:] = deepcopy(seed)`) antes de cada test.
  - Ventaja: sintaxis concisa, muy rápida para escribir y ejecutar.

- Unittest (`flask_unittest_app/test_unittest.py`):
  - Caso de prueba implementado como clase `unittest.TestCase`.
  - `setUp` hace backup profundo del estado del `EmployeeStore` y crea `test_client()`;
    `tearDown` restaura el estado (in-place) garantizando aislamiento estricto.
  - Ventaja: más explícito y controlado; más verboso y estructurado.

Notas y recomendaciones
- Ambas implementaciones usan almacenamiento en memoria (no persistente) para
  simplificar la comparación y mantener la actividad ligera.
- Mantén la venv activa al ejecutar los comandos para asegurar que se usen las
  dependencias correctas.
- Si quieres, puedo añadir un script `run_tests.ps1` que ejecute ambas suites y
  muestre un resumen comparativo.

Archivos clave
- [flask_pytest_app/app.py](flask_pytest_app/app.py#L1)
- [flask_pytest_app/test_app.py](flask_pytest_app/test_app.py#L1)
- [flask_unittest_app/app.py](flask_unittest_app/app.py#L1)
- [flask_unittest_app/test_unittest.py](flask_unittest_app/test_unittest.py#L1)

---
Generado para una actividad rápida de comparación entre frameworks de pruebas.
