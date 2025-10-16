# Sistema de Gestión de Biblioteca - TDD Workshop

Sistema completo de gestión de biblioteca desarrollado siguiendo metodología TDD (Test-Driven Development).

## 🔧 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 📁 Estructura del Proyecto

```
biblioteca/
│
├── src/                       # Código fuente
│   ├── __init__.py
│   ├── libro.py               # Clase Libro
│   ├── usuario.py             # Clase Usuario
│   ├── prestamo.py            # Clase Prestamo
│   └── biblioteca.py          # Clase Biblioteca (CRUD)
│
├── test/                     # Suite de pruebas
│   ├── __init__.py
│   ├── test_libro.py          # Tests unitarios de Libro
│   ├── test_usuario.py        # Tests unitarios de Usuario
│   ├── test_prestamo.py       # Tests unitarios de Prestamo
│   ├── test_biblioteca.py     # Tests CRUD de Biblioteca
│   ├── test_prestamos.py      # Tests gestión de préstamos
│   └── test_integracion.py    # Tests de integración
│
└── README.md                  # Este archivo
```

## 🚀 Instalación

### Paso 1: Instalar Python

Descarga e instala Python desde: https://python.org/downloads/

Verifica la instalación:
```bash
python --version
# o
python3 --version
```
### Paso 2: Instalar dependencias

```bash
pip install pytest pytest-cov
```


## 🧪 Ejecución de Tests

### Ejecutar todos los tests

```bash
pytest test/ -v
```

### Ejecutar tests con cobertura

```bash
pytest test/ -v --cov=src --cov-report=html
```

Esto generará un reporte HTML en `htmlcov/index.html`

### Ejecutar tests específicos

```bash
# Tests de una clase específica
pytest test/test_libro.py -v

# Un test específico
pytest test/test_libro.py::TestLibro::test_crear_libro_exitoso -v

```

### Ver cobertura en terminal

```bash
pytest test/ -v --cov=src --cov-report=term-missing
```

## 📊 Cobertura de Tests

Al ejecutar `pytest test/ -v --cov=src --cov-report=html`:

```
<img width="615" height="353" alt="image" src="https://github.com/user-attachments/assets/ec0a1475-d46f-4285-8d8a-42d42dafbbc2" />

```

## ⏱️ Comparativa: Testing Manual vs Automatizado

### 🔴 Escenario Manual (Tradicional)

Durante las pruebas manuales, cada módulo requiere ejecución y verificación individual con ingreso manual de datos y observación de resultados.

| Actividad | Tiempo estimado |
|-----------|-----------------|
| Configuración del entorno | 10 min |
| Pruebas de registro y búsqueda | 8 min |
| Pruebas de préstamos y devoluciones | 12 min |
| Validación de errores y casos límite | 10 min |
| **TOTAL** | **≈ 40 minutos** |

**Problemas del testing manual:**
- ❌ Propenso a errores humanos
- ❌ No repetible consistentemente
- ❌ Difícil de escalar
- ❌ Sin trazabilidad automática
- ❌ Requiere re-ejecución completa ante cambios

---

### 🟢 Escenario Automatizado (pytest)

Con **pytest**, las **70 pruebas** se ejecutan automáticamente en menos de 1 segundo, con reporte instantáneo de cobertura.

| Actividad | Tiempo estimado |
|-----------|-----------------|
| Instalación inicial (una vez) | 1 min |
| Ejecución de 70 tests | 0.68 seg |
| Generación de reporte HTML | 2 seg |
| **TOTAL** | **≈ 1 minuto** |

**Ventajas del testing automatizado:**
- ✅ **97.5% más rápido** que testing manual
- ✅ Repetible y consistente
- ✅ Detecta regresiones inmediatamente
- ✅ Cobertura de código medible
- ✅ Integrable con CI/CD
- ✅ Documentación viva del comportamiento del sistema

---

## 📈 Casos de Prueba Implementados

### Tests Unitarios
- Creación y validación de entidades
- Métodos de búsqueda (ISBN, título, autor)
- Agregar/remover libros y usuarios
- Validación de restricciones de negocio
- Manejo de excepciones

### Tests de Integración
- Flujo completo de préstamo y devolución
- Múltiples usuarios con múltiples libros
- Límites de préstamos por usuario
- Búsquedas parametrizadas
- Estadísticas del sistema
- Detección de retrasos con fechas simuladas

### Tests Parametrizados
- Búsquedas con diferentes queries
- Diferentes escenarios de retraso (0, 5, 14, 15, 20 días)
- Creación de múltiples instancias

---

## 🎓 Conceptos de Testing Demostrados

- ✅ **Tests unitarios** - Pruebas aisladas de componentes
- ✅ **Tests de integración** - Pruebas de interacción entre módulos
- ✅ **Fixtures** - Preparación de datos de prueba reutilizables
- ✅ **Parametrización** - Tests con múltiples entradas
- ✅ **Assertions** - Validaciones de comportamiento esperado
- ✅ **Manejo de excepciones** - Validación de errores controlados
- ✅ **Cobertura de código** - Medición de líneas ejecutadas
- ✅ **Mocking de fechas** - Simulación de escenarios temporales

---
