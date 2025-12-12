[Link del despliegue](https://talentox.onrender.com/schema/swagger-ui/)

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
TalentoX/                               # Proyecto principal
├── config/                                # Configuración global de Django
│   └── settings/                           # Ajustes separados por entorno
│       ├── base.py                         # Configuración base (común a todo)
│       ├── dev.py                          # Configuración para desarrollo
│       └── prod.py                         # Configuración para producción
│
├── apps/                                   # Todas las aplicaciones del proyecto
│   ├── users/                              # Gestión de usuarios, roles, perfiles y autenticación
│   ├── organizations/                      # Empresas, equipos y relación con usuarios
│   ├── skills/                             # Habilidades, categorías y niveles
│   ├── evidence/                           # Evidencias, archivos y portafolios de usuarios
│   ├── assessments/                        # Pruebas, retos y preguntas
│   ├── results/                            # Resultados, puntajes y mejoras del usuario
│   ├── certifications/                     # Certificaciones dinámicas basadas en desempeño
│   └── recommendations/                    # Motor recomendador de nuevas habilidades / rutas
│
└── manage.py                               # Comando principal para ejecutar Django
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
- 
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
Incluye endpoint:
```bash
/health/
```

```bash
{
  "status": "ok",
  "database": "connected",
  "version": "1.0.0"
}

```

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
python manage.py runserver
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

## 👤 ***Integrante 1*** – App **users** (Usuarios y Roles)
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
`/organizations/`

## 🎯 ***Integrante 2*** – App **skills** (Habilidades, Categorías, Niveles)
- **Gestiona**
- Categorías
- Habilidades
- Niveles del usuario

- **Modelos**
- Category
- Skill
- SkillLevel ***(User + Skill + nivel dinámico)***

- **Endpoints especiales**
`/skills/{id}/top-users/`
`/skills/{id}/levels/`

### 📁 ***Integrante 2*** – App **evidence** (Evidencias / Portafolio)
- **Permite subir:**
- Fotos
- Videos
- Archivos
- Links externos

- **Modelos**
- Evidence
- MediaFile

- **Endpoints**
`/evidence/user/{id}/`
`/evidence/skill/{id}/`

## 📝 ***Integrante 3*** – App **assessments** (Pruebas y Retos)
- **Gestiona:**
- Pruebas
- Preguntas
- Opciones
- Retos adaptativos

- **Modelos**
- Assessment
- Question
- Option

- **Endpoints**
`/assessments/{id}/start/`
`/assessments/{id}/submit/` (transacción atómica)

### 📊 ***Integrante 3*** – App **results** (Resultados y Puntajes)
- **Procesa:**
- Puntajes
- Tiempos
- Nivel ganado
- Sugerencias de mejora

- **Modelos**
- Result
- UserScore

- **Endpoints**
`/results/user/{id}/history/`
`/results/user/{id}/improvements/`

## 🎓 ***Integrante 4**** – App **certifications** (Certificaciones inteligentes)
- **Genera certificaciones basadas en:**
- Evidencias
- Resultados
- Habilidades del usuario

- **Modelo**
- Certification

- **Endpoints**
`/certifications/{user_id}/generate/`
`/certifications/{user_id}/history/`

### 🤖 ***Integrante 4*** – App **recommendations** (Motor de Recomendación)
- **Genera:**
- Nuevas habilidades recomendadas
- Pruebas sugeridas
- Rutas de aprendizaje personalizadas

- **Modelos**
- Recommendation

- **Endpoints**
`/recommendations/{user_id}/next-skills/`
`/recommendations/{user_id}/learning-path/`
