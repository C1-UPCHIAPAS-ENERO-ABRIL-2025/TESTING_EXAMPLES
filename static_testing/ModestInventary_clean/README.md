# ModestInventary Clean

Versión segura y mantenible del proyecto de inventario.

## Qué mejora esta versión

- Elimina inyección de comandos usando copias de archivos con `shutil`.
- Elimina deserialización insegura (`pickle`) usando `json`.
- Elimina credenciales hardcodeadas usando variables de entorno.
- Reduce complejidad ciclomática en el cálculo de descuentos.
- Incluye pruebas automatizadas con `pytest`.

## Variables de entorno

- `INVENTORY_ADMIN_USER`
- `INVENTORY_ADMIN_PASSWORD`

Si no están definidas, `login` siempre falla de forma segura.

## Uso rápido

```bash
python -m inventory_system.cli --help
python -m inventory_system.cli login admin mypassword
python -m inventory_system.cli discount electronics gold 15 --holiday
python -m inventory_system.cli save
python -m inventory_system.cli load
python -m inventory_system.cli backup backups/
```

## Ejecutar pruebas

```bash
pytest -q
```
