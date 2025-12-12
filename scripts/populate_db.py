"""
Script para poblar la base de datos con datos de ejemplo.
Ejecutar con: python manage.py shell < scripts/populate_db.py
O copiar y pegar en: python manage.py shell
"""

from django.contrib.auth import get_user_model
from apps.assessments.models import Assessment, Question, Option
from apps.skills.models import Category, Skill, SkillLevel
from apps.results.models import Result, UserScore
from apps.certifications.models import Certification
from apps.organizations.models import Organization, Team
from apps.evidence.models import Evidence
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

print("🚀 Iniciando población de base de datos...")

# ==================== USUARIOS ====================
print("\n📝 Creando usuarios...")

# Admin
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@talentox.com',
        'first_name': 'Carlos',
        'last_name': 'Administrador',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
    }
)
if created:
    admin_user.set_password('Admin123!')
    admin_user.save()
    print(f"  ✅ Admin creado: {admin_user.username}")

# Empresas (evaluadores)
empresas_data = [
    {'username': 'techcorp', 'email': 'rrhh@techcorp.com', 'first_name': 'María', 'last_name': 'González'},
    {'username': 'innovasoft', 'email': 'talento@innovasoft.com', 'first_name': 'Roberto', 'last_name': 'Martínez'},
    {'username': 'dataworks', 'email': 'seleccion@dataworks.com', 'first_name': 'Ana', 'last_name': 'Rodríguez'},
]

empresa_users = []
for data in empresas_data:
    user, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': 'empresa',
        }
    )
    if created:
        user.set_password('Empresa123!')
        user.save()
        print(f"  ✅ Empresa creada: {user.username}")
    empresa_users.append(user)

# Aprendices (talentos)
aprendices_data = [
    {'username': 'juan_dev', 'email': 'juan@email.com', 'first_name': 'Juan', 'last_name': 'Pérez'},
    {'username': 'laura_fullstack', 'email': 'laura@email.com', 'first_name': 'Laura', 'last_name': 'Sánchez'},
    {'username': 'miguel_data', 'email': 'miguel@email.com', 'first_name': 'Miguel', 'last_name': 'López'},
    {'username': 'sofia_ux', 'email': 'sofia@email.com', 'first_name': 'Sofía', 'last_name': 'Hernández'},
    {'username': 'andres_backend', 'email': 'andres@email.com', 'first_name': 'Andrés', 'last_name': 'García'},
    {'username': 'camila_frontend', 'email': 'camila@email.com', 'first_name': 'Camila', 'last_name': 'Torres'},
]

aprendiz_users = []
for data in aprendices_data:
    user, created = User.objects.get_or_create(
        username=data['username'],
        defaults={
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': 'aprendiz',
        }
    )
    if created:
        user.set_password('Aprendiz123!')
        user.save()
        print(f"  ✅ Aprendiz creado: {user.username}")
    aprendiz_users.append(user)

# ==================== CATEGORÍAS Y HABILIDADES ====================
print("\n🎯 Creando categorías y habilidades...")

categorias_skills = {
    'Desarrollo Backend': [
        ('Python', 'Lenguaje de programación versátil para backend, ciencia de datos y automatización'),
        ('Django', 'Framework web de alto nivel para Python'),
        ('Node.js', 'Entorno de ejecución de JavaScript del lado del servidor'),
        ('APIs REST', 'Diseño e implementación de APIs RESTful'),
        ('Bases de Datos SQL', 'Gestión de bases de datos relacionales'),
        ('PostgreSQL', 'Sistema de gestión de bases de datos relacional'),
    ],
    'Desarrollo Frontend': [
        ('JavaScript', 'Lenguaje de programación para desarrollo web'),
        ('React', 'Biblioteca de JavaScript para interfaces de usuario'),
        ('Vue.js', 'Framework progresivo de JavaScript'),
        ('HTML/CSS', 'Fundamentos de estructura y estilos web'),
        ('TypeScript', 'Superset tipado de JavaScript'),
        ('Tailwind CSS', 'Framework de CSS utilitario'),
    ],
    'DevOps y Cloud': [
        ('Docker', 'Plataforma de contenedorización'),
        ('Kubernetes', 'Orquestación de contenedores'),
        ('AWS', 'Amazon Web Services - plataforma cloud'),
        ('CI/CD', 'Integración y despliegue continuo'),
        ('Linux', 'Sistema operativo y administración de servidores'),
        ('Git', 'Control de versiones'),
    ],
    'Ciencia de Datos': [
        ('Machine Learning', 'Aprendizaje automático y modelos predictivos'),
        ('Pandas', 'Biblioteca de análisis de datos en Python'),
        ('SQL Avanzado', 'Consultas complejas y optimización'),
        ('Visualización de Datos', 'Creación de gráficos y dashboards'),
        ('Estadística', 'Fundamentos estadísticos para análisis'),
    ],
    'Habilidades Blandas': [
        ('Comunicación', 'Habilidad para transmitir ideas claramente'),
        ('Trabajo en Equipo', 'Colaboración efectiva con otros'),
        ('Resolución de Problemas', 'Análisis y solución de desafíos'),
        ('Liderazgo', 'Capacidad de guiar y motivar equipos'),
        ('Gestión del Tiempo', 'Organización y priorización de tareas'),
    ],
}

all_skills = []
for cat_name, skills in categorias_skills.items():
    category, _ = Category.objects.get_or_create(
        name=cat_name,
        defaults={'slug': cat_name.lower().replace(' ', '-').replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')}
    )
    print(f"  📁 Categoría: {cat_name}")
    
    for skill_name, skill_desc in skills:
        skill, created = Skill.objects.get_or_create(
            name=skill_name,
            category=category,
            defaults={
                'slug': skill_name.lower().replace(' ', '-').replace('.', '').replace('/', '-'),
                'description': skill_desc
            }
        )
        all_skills.append(skill)
        if created:
            print(f"    ✅ Skill: {skill_name}")

# ==================== NIVELES DE HABILIDAD POR USUARIO ====================
print("\n📊 Asignando niveles de habilidad a usuarios...")

import random

for user in aprendiz_users:
    # Asignar 5-10 habilidades aleatorias a cada aprendiz
    selected_skills = random.sample(all_skills, random.randint(5, 10))
    for skill in selected_skills:
        level = random.randint(1, 5)
        SkillLevel.objects.get_or_create(
            user=user,
            skill=skill,
            defaults={'level': level}
        )
    print(f"  ✅ Habilidades asignadas a {user.username}")

# ==================== EVALUACIONES ====================
print("\n📝 Creando evaluaciones...")

assessments_data = [
    {
        'title': 'Fundamentos de Python',
        'description': 'Evaluación de conocimientos básicos e intermedios de Python',
        'difficulty': 2,
        'time_limit': 1800,  # 30 minutos
        'questions': [
            {
                'text': '¿Cuál es la forma correcta de declarar una lista en Python?',
                'order': 1,
                'options': [
                    ('lista = []', True),
                    ('lista = ()', False),
                    ('lista = {}', False),
                    ('list lista = new List()', False),
                ]
            },
            {
                'text': '¿Qué método se usa para agregar un elemento al final de una lista?',
                'order': 2,
                'options': [
                    ('add()', False),
                    ('append()', True),
                    ('insert()', False),
                    ('push()', False),
                ]
            },
            {
                'text': '¿Cuál es la salida de: print(type([]))?',
                'order': 3,
                'options': [
                    ("<class 'list'>", True),
                    ("<class 'array'>", False),
                    ("<class 'tuple'>", False),
                    ("<class 'dict'>", False),
                ]
            },
            {
                'text': '¿Cómo se define una función en Python?',
                'order': 4,
                'options': [
                    ('function mi_funcion():', False),
                    ('def mi_funcion():', True),
                    ('func mi_funcion():', False),
                    ('fn mi_funcion():', False),
                ]
            },
            {
                'text': '¿Qué palabra clave se usa para manejar excepciones en Python?',
                'order': 5,
                'options': [
                    ('catch', False),
                    ('except', True),
                    ('handle', False),
                    ('error', False),
                ]
            },
        ]
    },
    {
        'title': 'JavaScript Esencial',
        'description': 'Evaluación de fundamentos de JavaScript moderno',
        'difficulty': 2,
        'time_limit': 1800,
        'questions': [
            {
                'text': '¿Cuál es la diferencia entre let y var?',
                'order': 1,
                'options': [
                    ('No hay diferencia', False),
                    ('let tiene alcance de bloque, var tiene alcance de función', True),
                    ('var es más moderno que let', False),
                    ('let solo funciona con números', False),
                ]
            },
            {
                'text': '¿Qué método convierte un JSON string a objeto JavaScript?',
                'order': 2,
                'options': [
                    ('JSON.parse()', True),
                    ('JSON.stringify()', False),
                    ('JSON.toObject()', False),
                    ('JSON.convert()', False),
                ]
            },
            {
                'text': '¿Qué es una Promise en JavaScript?',
                'order': 3,
                'options': [
                    ('Un tipo de variable', False),
                    ('Un objeto que representa un valor futuro', True),
                    ('Una función especial', False),
                    ('Un método de arrays', False),
                ]
            },
            {
                'text': '¿Cómo se declara una arrow function?',
                'order': 4,
                'options': [
                    ('function => {}', False),
                    ('() => {}', True),
                    ('arrow() {}', False),
                    ('=> function() {}', False),
                ]
            },
            {
                'text': '¿Qué método se usa para iterar sobre un array?',
                'order': 5,
                'options': [
                    ('forEach()', True),
                    ('each()', False),
                    ('iterate()', False),
                    ('loop()', False),
                ]
            },
        ]
    },
    {
        'title': 'Fundamentos de SQL',
        'description': 'Evaluación de conocimientos en bases de datos SQL',
        'difficulty': 2,
        'time_limit': 1500,
        'questions': [
            {
                'text': '¿Cuál comando se usa para obtener datos de una tabla?',
                'order': 1,
                'options': [
                    ('GET', False),
                    ('SELECT', True),
                    ('FETCH', False),
                    ('RETRIEVE', False),
                ]
            },
            {
                'text': '¿Qué cláusula se usa para filtrar resultados?',
                'order': 2,
                'options': [
                    ('FILTER', False),
                    ('WHERE', True),
                    ('HAVING', False),
                    ('CONDITION', False),
                ]
            },
            {
                'text': '¿Qué tipo de JOIN devuelve solo las filas coincidentes?',
                'order': 3,
                'options': [
                    ('LEFT JOIN', False),
                    ('INNER JOIN', True),
                    ('OUTER JOIN', False),
                    ('FULL JOIN', False),
                ]
            },
            {
                'text': '¿Cuál comando elimina todos los registros de una tabla?',
                'order': 4,
                'options': [
                    ('DELETE FROM tabla', True),
                    ('REMOVE * FROM tabla', False),
                    ('CLEAR tabla', False),
                    ('DROP tabla', False),
                ]
            },
        ]
    },
    {
        'title': 'React Avanzado',
        'description': 'Evaluación de conceptos avanzados de React',
        'difficulty': 4,
        'time_limit': 2400,
        'questions': [
            {
                'text': '¿Qué hook se usa para manejar efectos secundarios?',
                'order': 1,
                'options': [
                    ('useState', False),
                    ('useEffect', True),
                    ('useContext', False),
                    ('useReducer', False),
                ]
            },
            {
                'text': '¿Qué es el Virtual DOM?',
                'order': 2,
                'options': [
                    ('Una copia del DOM real en memoria', True),
                    ('Un navegador virtual', False),
                    ('Una librería de React', False),
                    ('Un tipo de componente', False),
                ]
            },
            {
                'text': '¿Para qué sirve useCallback?',
                'order': 3,
                'options': [
                    ('Memorizar funciones', True),
                    ('Crear callbacks', False),
                    ('Manejar eventos', False),
                    ('Crear estados', False),
                ]
            },
            {
                'text': '¿Qué patrón usa Redux para manejar estado?',
                'order': 4,
                'options': [
                    ('MVC', False),
                    ('Flux', True),
                    ('Observer', False),
                    ('Singleton', False),
                ]
            },
        ]
    },
    {
        'title': 'DevOps y CI/CD',
        'description': 'Evaluación de prácticas DevOps y pipelines',
        'difficulty': 3,
        'time_limit': 2100,
        'questions': [
            {
                'text': '¿Qué es Docker?',
                'order': 1,
                'options': [
                    ('Un sistema operativo', False),
                    ('Una plataforma de contenedorización', True),
                    ('Un lenguaje de programación', False),
                    ('Una base de datos', False),
                ]
            },
            {
                'text': '¿Qué archivo define los servicios en Docker Compose?',
                'order': 2,
                'options': [
                    ('Dockerfile', False),
                    ('docker-compose.yml', True),
                    ('config.yml', False),
                    ('services.json', False),
                ]
            },
            {
                'text': '¿Qué significa CI en CI/CD?',
                'order': 3,
                'options': [
                    ('Code Integration', False),
                    ('Continuous Integration', True),
                    ('Complete Installation', False),
                    ('Cloud Infrastructure', False),
                ]
            },
            {
                'text': '¿Qué herramienta se usa comúnmente para orquestar contenedores?',
                'order': 4,
                'options': [
                    ('Docker', False),
                    ('Kubernetes', True),
                    ('Jenkins', False),
                    ('Nginx', False),
                ]
            },
        ]
    },
]

created_assessments = []
for assessment_data in assessments_data:
    assessment, created = Assessment.objects.get_or_create(
        title=assessment_data['title'],
        defaults={
            'description': assessment_data['description'],
            'difficulty': assessment_data['difficulty'],
            'time_limit': assessment_data['time_limit'],
        }
    )
    created_assessments.append(assessment)
    
    if created:
        print(f"  ✅ Evaluación: {assessment.title}")
        
        for q_data in assessment_data['questions']:
            question = Question.objects.create(
                assessment=assessment,
                text=q_data['text'],
                order=q_data['order']
            )
            
            for opt_text, is_correct in q_data['options']:
                Option.objects.create(
                    question=question,
                    text=opt_text,
                    is_correct=is_correct
                )

# ==================== RESULTADOS ====================
print("\n📈 Creando resultados de evaluaciones...")

for user in aprendiz_users[:4]:  # Solo los primeros 4 aprendices
    for assessment in random.sample(created_assessments, random.randint(2, 4)):
        total_questions = assessment.questions.count()
        correct = random.randint(int(total_questions * 0.5), total_questions)
        score = round((correct / total_questions) * 100, 2)
        time_taken = random.randint(300, assessment.time_limit)
        
        Result.objects.get_or_create(
            user=user,
            assessment=assessment,
            defaults={
                'score': score,
                'correct_answers': correct,
                'total_questions': total_questions,
                'time_taken': time_taken,
            }
        )
    print(f"  ✅ Resultados creados para {user.username}")

# ==================== PUNTAJES GLOBALES ====================
print("\n🏆 Calculando puntajes globales...")

for user in aprendiz_users:
    results = Result.objects.filter(user=user)
    if results.exists():
        avg_score = sum(r.score for r in results) / results.count()
        total_correct = sum(r.correct_answers for r in results)
        total_questions = sum(r.total_questions for r in results)
        
        UserScore.objects.update_or_create(
            user=user,
            defaults={
                'global_score': round(avg_score, 2),
                'total_assessments': results.count(),
                'total_correct': total_correct,
                'total_questions': total_questions,
            }
        )
        print(f"  ✅ Puntaje global para {user.username}: {round(avg_score, 2)}%")

# ==================== CERTIFICACIONES ====================
print("\n🎓 Generando certificaciones...")

for user in aprendiz_users[:3]:
    user_score = UserScore.objects.filter(user=user).first()
    if user_score and user_score.global_score >= 60:
        level = 1
        if user_score.global_score >= 90:
            level = 5
        elif user_score.global_score >= 80:
            level = 4
        elif user_score.global_score >= 70:
            level = 3
        elif user_score.global_score >= 60:
            level = 2
        
        Certification.objects.get_or_create(
            user=user,
            title=f'Certificación en Desarrollo de Software - Nivel {level}',
            defaults={
                'description': f'Certificación que acredita competencias en desarrollo de software',
                'level': level,
                'total_score': user_score.global_score,
                'status': 'active',
                'issued_at': timezone.now(),
                'expires_at': timezone.now() + timedelta(days=365),
            }
        )
        print(f"  ✅ Certificación nivel {level} para {user.username}")

# ==================== ORGANIZACIONES ====================
print("\n🏢 Creando organizaciones...")

org_data = [
    {
        'name': 'TechCorp Solutions',
        'description': 'Empresa líder en desarrollo de software empresarial',
        'industry': 'Tecnología',
        'size': 'large',
        'city': 'Bogotá',
        'country': 'Colombia',
        'website': 'https://techcorp.example.com',
        'phone': '3001234567',
        'email': 'contacto@techcorp.com',
    },
    {
        'name': 'InnovaSoft',
        'description': 'Startup de innovación tecnológica',
        'industry': 'Software',
        'size': 'medium',
        'city': 'Medellín',
        'country': 'Colombia',
        'website': 'https://innovasoft.example.com',
        'phone': '3009876543',
        'email': 'info@innovasoft.com',
    },
    {
        'name': 'DataWorks Analytics',
        'description': 'Consultoría especializada en análisis de datos',
        'industry': 'Consultoría',
        'size': 'small',
        'city': 'Cali',
        'country': 'Colombia',
        'website': 'https://dataworks.example.com',
        'phone': '3005551234',
        'email': 'contacto@dataworks.com',
    },
]

for i, data in enumerate(org_data):
    org, created = Organization.objects.get_or_create(
        name=data['name'],
        defaults={
            **data,
            'owner': empresa_users[i] if i < len(empresa_users) else empresa_users[0],
        }
    )
    if created:
        print(f"  ✅ Organización: {org.name}")

# ==================== EVIDENCIAS ====================
print("\n📎 Creando evidencias...")

evidencias_data = [
    {'title': 'Proyecto API REST con Django', 'description': 'Desarrollo completo de una API REST usando Django REST Framework', 'external_link': 'https://github.com/example/django-api'},
    {'title': 'Dashboard con React', 'description': 'Aplicación de dashboard interactivo con React y Chart.js', 'external_link': 'https://github.com/example/react-dashboard'},
    {'title': 'Script de Automatización', 'description': 'Scripts de Python para automatizar tareas repetitivas', 'code_snippet': 'import os\nimport shutil\n\ndef backup_files(src, dst):\n    shutil.copytree(src, dst)'},
    {'title': 'Configuración Docker', 'description': 'Configuración de contenedores para aplicación web', 'code_snippet': 'FROM python:3.11\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt'},
]

for user in aprendiz_users[:3]:
    user_skills = SkillLevel.objects.filter(user=user)
    if user_skills.exists():
        for ev_data in random.sample(evidencias_data, 2):
            skill = random.choice(user_skills).skill
            Evidence.objects.get_or_create(
                user=user,
                title=ev_data['title'],
                skill=skill,
                defaults={
                    'description': ev_data['description'],
                    'external_link': ev_data.get('external_link', ''),
                    'code_snippet': ev_data.get('code_snippet', ''),
                }
            )
        print(f"  ✅ Evidencias creadas para {user.username}")

print("\n" + "="*60)
print("✅ ¡Base de datos poblada exitosamente!")
print("="*60)
print("\n📋 RESUMEN DE CREDENCIALES:")
print("-"*40)
print("👑 ADMIN:")
print("   Usuario: admin")
print("   Contraseña: Admin123!")
print("\n🏢 EMPRESAS:")
print("   Usuarios: techcorp, innovasoft, dataworks")
print("   Contraseña: Empresa123!")
print("\n👨‍💻 APRENDICES:")
print("   Usuarios: juan_dev, laura_fullstack, miguel_data,")
print("            sofia_ux, andres_backend, camila_frontend")
print("   Contraseña: Aprendiz123!")
print("-"*40)
