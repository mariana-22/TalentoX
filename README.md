# Plataforma TalentoX

## 🧠 Descripción de – **TalentoX**
TalentoX es una plataforma inteligente que evalúa habilidades reales mediante pruebas, retos prácticos y evidencias.
El objetivo es medir competencias reales, no títulos, generando un “pasaporte digital de habilidades”.

## ⭐ Descripción General del Proyecto
Talentox permite:

- Evaluar habilidades mediante ***micro-pruebas***.
- Medir niveles y puntajes dinámicos.
- Recomendar nuevas habilidades y pruebas.
- Generar certificaciones inteligentes.
- Consultar información desde Swagger o vía API.

El sistema está dividido en módulos (apps) para cada parte del proceso: `usuarios`, `empresas`, `habilidades`, `evaluaciones`, `resultados`, `certificaciones` y `recomendaciones`.

## 🏗️ Arquitectura
```bash
skillbridge/
├── config/
│   └── settings/
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── apps/
│   ├── users/
│   ├── organizations/
│   ├── skills/
│   ├── evidence/
│   ├── assessments/
│   ├── results/
│   ├── certifications/
│   └── recommendations/
│
└── manage.py
```
- settings/base.py → Configuración general (apps, DRF, JWT, middleware).
- settings/dev.py → Configuración para desarrollo (debug, sqlite/mysql local).
- settings/prod.py → Seguridad, CORS, logs, base de datos real.

## 🔐 Autenticación JWT

Incluye:
- `Registro`
- `Login`
- `Token Access / Refresh`
- `Vista /users/me/ para perfil propio`
- `Permisos personalizados por rol`
Roles principales:
- `admin`
- `empresa`
- `aprendiz`

## 🔒 Permisos Personalizados
- Solo empresas pueden ver sus equipos.
- Solo el propio usuario puede editar su perfil.
- Administradores tienen acceso global.

## 🔍 Filtros
El backend incluye filtros para:
- ***Usuarios***
- ***Equipos***
- ***Habilidades***
- ***Niveles***
- ***Evidencias***
- ***Resultados***

Uso estándar con django-filter:
```bash
/skills/?category=1
/assessments/?difficulty=high
```

## ❤️ Health Check


## 🔄 Transacciones
- Operaciones críticas usan transacciones atómicas:
- Enviar prueba `/assessments/{id}/submit/`
- Generar certificación
- Procesar resultados
- Garantiza que los datos no queden incompletos.

## 🧪 Pruebas
El proyecto incluye pruebas para:
- Autenticación
- Endpoints principales
- Lógica de resultados
- Permisos
- Habilidades
- Evidencias

Se ejecutan con:
```bash
python manage.py test
```

## 📘 Swagger + API Deploy
Incluye documentación automática:
```bash
/swagger/
/api/schema/
/redoc/
```
Desde Swagger se pueden probar:
- login
- registro
- CRUDs
- pruebas
- resultados
- evidencias

## 🧩 Módulos del Proyecto

### 👤 ***Integrante 1*** – App **users** (Usuarios y Roles)
- **Funcionalidades**
- Registro e inicio de sesión con JWT.
- Perfiles de usuario.
- Roles (admin, empresa, aprendiz).
- Permisos personalizados.

- **Modelos**
- User (extends AbstractUser)
- Profile

- **Endpoints principales**
`/users/me/`
`/users/{id}/skills/`

### 🏢 ***Integrante 1*** – App **organizations** (Empresas y Equipos)
- **Funcionalidad**

Gestión de:
- Empresas
- Equipos de trabajo
- Miembros
- Administradores internos

- **Modelos**
- Organization
- Team (ManyToMany con Users)

- **Endpoints principales**
`/organizations/{id}/members/`
`/organizations/
