# 📚 Guía de Uso de la API TalentoX

## 🚀 Inicio Rápido

### 1. Poblar la Base de Datos

```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar el script de población
python manage.py shell < scripts/populate_db.py
```

### 2. Iniciar el Servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000`

---

## 🔐 Autenticación

### Credenciales de Prueba

| Rol | Usuario | Contraseña | Permisos |
|-----|---------|------------|----------|
| Admin | `admin` | `Admin123!` | Acceso total |
| Empresa | `techcorp` | `Empresa123!` | Evaluar y gestionar |
| Aprendiz | `juan_dev` | `Aprendiz123!` | Solo lectura |

### Endpoints de Autenticación

#### 📝 Registrar Usuario
```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "nuevo_usuario",
    "email": "nuevo@email.com",
    "password": "MiPassword123!",
    "role": "aprendiz"
  }'
```

#### 🔑 Iniciar Sesión (Obtener Token)
```bash
curl -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "juan_dev",
    "password": "Aprendiz123!"
  }'
```

**Respuesta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### 🔄 Refrescar Token
```bash
curl -X POST http://127.0.0.1:8000/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "TU_REFRESH_TOKEN"
  }'
```

---

## 📖 Uso de Endpoints (con Token)

**Importante:** Todos los endpoints (excepto auth) requieren el header:
```
Authorization: Bearer TU_ACCESS_TOKEN
```

### Definir variable de entorno para facilitar:
```bash
# Obtener token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}' | jq -r '.access')

echo $TOKEN
```

---

## 👥 Usuarios (`/users/`)

### Listar Usuarios (Admin/Empresa)
```bash
curl -X GET http://127.0.0.1:8000/users/ \
  -H "Authorization: Bearer $TOKEN"
```

### Ver Perfil Propio
```bash
curl -X GET http://127.0.0.1:8000/users/me/ \
  -H "Authorization: Bearer $TOKEN"
```

### Actualizar Mi Perfil
```bash
curl -X PUT http://127.0.0.1:8000/users/me/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan Carlos",
    "last_name": "Pérez García"
  }'
```

---

## 🎯 Habilidades (`/skills/`)

### Listar Categorías
```bash
curl -X GET http://127.0.0.1:8000/skills/categories/ \
  -H "Authorization: Bearer $TOKEN"
```

### Listar Todas las Habilidades
```bash
curl -X GET http://127.0.0.1:8000/skills/skills/ \
  -H "Authorization: Bearer $TOKEN"
```

### Filtrar Habilidades por Categoría
```bash
curl -X GET "http://127.0.0.1:8000/skills/skills/?category__id=1" \
  -H "Authorization: Bearer $TOKEN"
```

### Buscar Habilidades
```bash
curl -X GET "http://127.0.0.1:8000/skills/skills/?search=python" \
  -H "Authorization: Bearer $TOKEN"
```

### Crear Habilidad (Solo Admin)
```bash
curl -X POST http://127.0.0.1:8000/skills/skills/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "FastAPI",
    "slug": "fastapi",
    "description": "Framework moderno para APIs en Python",
    "category": 1
  }'
```

### Ver Niveles de Habilidad
```bash
curl -X GET http://127.0.0.1:8000/skills/skill-levels/ \
  -H "Authorization: Bearer $TOKEN"
```

### Ver Top Usuarios por Habilidad
```bash
curl -X GET http://127.0.0.1:8000/skills/skills/1/top-users/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📝 Evaluaciones (`/assessments/`)

### Listar Evaluaciones
```bash
curl -X GET http://127.0.0.1:8000/assessments/ \
  -H "Authorization: Bearer $TOKEN"
```

### Filtrar por Dificultad
```bash
curl -X GET "http://127.0.0.1:8000/assessments/?difficulty=2" \
  -H "Authorization: Bearer $TOKEN"
```

### Ver Detalle de Evaluación
```bash
curl -X GET http://127.0.0.1:8000/assessments/1/ \
  -H "Authorization: Bearer $TOKEN"
```

### Crear Evaluación (Admin/Empresa)
```bash
curl -X POST http://127.0.0.1:8000/assessments/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Evaluación de Git",
    "description": "Conocimientos de control de versiones",
    "difficulty": 2,
    "time_limit": 1200
  }'
```

### Iniciar Evaluación (Obtener Preguntas)
```bash
curl -X GET http://127.0.0.1:8000/assessments/1/start/ \
  -H "Authorization: Bearer $TOKEN"
```

### Enviar Respuesta
```bash
curl -X POST http://127.0.0.1:8000/assessments/1/submit/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": 1,
    "option_id": 1
  }'
```

### Ver Preguntas de una Evaluación
```bash
curl -X GET http://127.0.0.1:8000/assessments/1/questions/ \
  -H "Authorization: Bearer $TOKEN"
```

### Crear Pregunta (Admin/Empresa)
```bash
curl -X POST http://127.0.0.1:8000/assessments/1/questions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "¿Qué comando se usa para clonar un repositorio?",
    "order": 6,
    "options": [
      {"text": "git clone", "is_correct": true},
      {"text": "git copy", "is_correct": false},
      {"text": "git download", "is_correct": false},
      {"text": "git pull", "is_correct": false}
    ]
  }'
```

---

## 📊 Resultados (`/results/`)

### Ver Mis Resultados (Aprendiz)
```bash
curl -X GET http://127.0.0.1:8000/results/ \
  -H "Authorization: Bearer $TOKEN"
```

### Ver Todos los Resultados (Admin/Empresa)
```bash
curl -X GET http://127.0.0.1:8000/results/ \
  -H "Authorization: Bearer $TOKEN"
```

### Filtrar por Usuario
```bash
curl -X GET "http://127.0.0.1:8000/results/?user=2" \
  -H "Authorization: Bearer $TOKEN"
```

### Filtrar por Puntaje Mínimo
```bash
curl -X GET "http://127.0.0.1:8000/results/?score_min=80" \
  -H "Authorization: Bearer $TOKEN"
```

### Crear Resultado (Admin/Empresa)
```bash
curl -X POST http://127.0.0.1:8000/results/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 2,
    "assessment": 1,
    "score": 85.5,
    "correct_answers": 4,
    "total_questions": 5,
    "time_taken": 900
  }'
```

---

## 🎓 Certificaciones (`/certifications/`)

### Ver Mis Certificaciones (Aprendiz)
```bash
curl -X GET http://127.0.0.1:8000/certifications/ \
  -H "Authorization: Bearer $TOKEN"
```

### Generar Certificación (Admin/Empresa)
```bash
curl -X POST http://127.0.0.1:8000/certifications/2/generate/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Desarrollador Python Junior",
    "description": "Certificación de competencias en Python"
  }'
```

### Ver Historial de Usuario
```bash
curl -X GET http://127.0.0.1:8000/certifications/2/history/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📎 Evidencias (`/evidence/`)

### Listar Evidencias
```bash
curl -X GET http://127.0.0.1:8000/evidence/ \
  -H "Authorization: Bearer $TOKEN"
```

### Crear Evidencia
```bash
curl -X POST http://127.0.0.1:8000/evidence/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Mi Proyecto Personal",
    "description": "Aplicación web completa con Django y React",
    "skill": 1,
    "external_link": "https://github.com/miusuario/proyecto",
    "code_snippet": "def main():\n    print(\"Hola mundo\")"
  }'
```

### Ver Evidencias por Usuario
```bash
curl -X GET http://127.0.0.1:8000/evidence/user/2/ \
  -H "Authorization: Bearer $TOKEN"
```

### Ver Evidencias por Habilidad
```bash
curl -X GET http://127.0.0.1:8000/evidence/skill/1/ \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🏢 Organizaciones (`/organizations/`)

### Listar Organizaciones
```bash
curl -X GET http://127.0.0.1:8000/organizations/ \
  -H "Authorization: Bearer $TOKEN"
```

### Ver Detalle de Organización
```bash
curl -X GET http://127.0.0.1:8000/organizations/1/ \
  -H "Authorization: Bearer $TOKEN"
```

### Crear Organización (Admin/Empresa)
```bash
curl -X POST http://127.0.0.1:8000/organizations/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Empresa",
    "description": "Descripción de la empresa",
    "industry": "Tecnología",
    "size": "small",
    "city": "Bogotá",
    "country": "Colombia"
  }'
```

---

## 📚 Documentación Interactiva

- **Swagger UI:** http://127.0.0.1:8000/schema/swagger-ui/
- **ReDoc:** http://127.0.0.1:8000/schema/redoc/
- **Schema JSON:** http://127.0.0.1:8000/schema/

---

## 🔍 Filtros y Búsqueda Disponibles

### Parámetros Comunes

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `search` | Búsqueda en texto | `?search=python` |
| `ordering` | Ordenar resultados | `?ordering=-created_at` |
| `page` | Número de página | `?page=2` |
| `page_size` | Resultados por página | `?page_size=20` |

### Filtros Específicos por Recurso

**Evaluaciones:**
- `difficulty` - Nivel de dificultad (1-5)
- `difficulty_min`, `difficulty_max` - Rango de dificultad
- `time_limit_min`, `time_limit_max` - Rango de tiempo

**Resultados:**
- `user` - ID del usuario
- `assessment` - ID de la evaluación
- `score_min`, `score_max` - Rango de puntaje

**Certificaciones:**
- `user` - ID del usuario
- `level` - Nivel de certificación
- `status` - Estado (pending, active, expired, revoked)

---

## 📋 Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| 200 | Éxito |
| 201 | Creado exitosamente |
| 204 | Eliminado exitosamente |
| 400 | Error en los datos enviados |
| 401 | No autenticado (falta token) |
| 403 | No autorizado (sin permisos) |
| 404 | Recurso no encontrado |

---

## 🛡️ Matriz de Permisos

| Recurso | Admin | Empresa | Aprendiz |
|---------|-------|---------|----------|
| Usuarios | CRUD | Listar/Ver | Solo perfil propio |
| Evaluaciones | CRUD | CRUD | Ver + Responder |
| Resultados | CRUD | CRUD | Ver propios |
| Certificaciones | CRUD | CRUD + Generar | Ver propias |
| Habilidades | CRUD | Ver | Ver |
| Evidencias | CRUD | CRUD | Crear propias + Ver |
| Organizaciones | CRUD | Propias | Ver asignadas |
