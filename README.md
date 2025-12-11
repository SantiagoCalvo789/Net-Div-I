# Network Device Inventory

Proyecto web diseñado para registrar, administrar y consultar dispositivos de red.  
El sistema está dividido en Frontend, Backend (FastAPI) y Base de Datos (PostgreSQL).

---

## Objetivo del Proyecto

Crear una plataforma centralizada para:
- Registrar dispositivos de red como switches, routers, puntos de acceso y firewalls.
- Guardar su ubicación, modelo, IP, responsable y estado.
- Consultar, actualizar y eliminar dispositivos.
- Generar vistas filtradas y ordenadas.
- Mantener un inventario confiable de la infraestructura de red.

---

## Arquitectura General

El sistema sigue una arquitectura de tres capas: Frontend, Backend y Base de Datos.

```mermaid
graph TD
    A[Frontend - React] --> B[Backend API - FastAPI]
    B --> C[Base de Datos - PostgreSQL]

/
├── backend/
│   ├── app/
│   │   ├── api/           # Rutas de la API
│   │   ├── core/          # Configuración principal
│   │   ├── models/        # Modelos Pydantic y ORM
│   │   ├── main.py        # Punto de entrada del backend
│   │   └── __init__.py
│   ├── requirements.txt   # Dependencias del backend
│   └── tests/             # Pruebas automáticas
│
├── frontend/              # Proyecto de React (por configurar)
│
├── db/
│   ├── schema.sql         # Script SQL inicial del modelo de datos
│   └── migrations/        # Migraciones futuras
│
├── docs/
│   ├── architecture.md    # Documentación técnica del sistema
│   └── api.md             # Documentación de la API
│
└── README.md