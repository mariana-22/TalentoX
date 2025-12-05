# TalentoX

---

### 📘 **Bitácora del Proyecto TalentoX (Proyección a Futuro)**

**Día 1 – Definición del concepto**
Durante este día se **identificará** la necesidad de que TalentoX evalúe habilidades reales por encima de títulos académicos.
Se **definirá** el enfoque principal de la plataforma, basado en micro-pruebas, retos prácticos y evidencias verificables.
Además, se **creará** el concepto central del sistema: el **Pasaporte de Habilidades de TalentoX**, que será el eje de certificación.

---

**Día 2 – Análisis del problema y la solución**
Se **documentarán** los problemas del modelo tradicional de certificación frente al objetivo de TalentoX.
Se **establecerán** los tipos de evaluaciones que la plataforma ofrecerá:

* Micro-pruebas inteligentes
* Retos prácticos
* Evidencias verificables

También se **definirán** los indicadores de evaluación que utilizará TalentoX: dificultad, tiempo, exactitud, evidencias y consistencia.

---

**Día 3 – Diseño del sistema de puntajes**
Se **creará** la estructura de asignación de puntajes de TalentoX, basada en: dificultad del reto, tiempo de respuesta, correctitud, evidencias y consistencia.
Además, se **establecerá** la escala oficial de niveles de habilidad del proyecto, que irá de 0 a 5.

---

**Día 4 – Modelado funcional**
Se **desarrollarán** ejemplos concretos de retos y pruebas usados por TalentoX.
Se **describirán** los parámetros que se evaluarán en cada tipo de prueba.
Finalmente, se **definirá** el flujo adaptativo de evaluación que permitirá ajustar las pruebas según el desempeño del usuario.

---

**Día 5 – Documentación del perfil del usuario**
Se **construirá** la estructura del **Perfil de Habilidades TalentoX**, que incluirá:

* Habilidad
* Nivel
* Última evaluación
* Puntaje total
* Evidencias

También se **documentará** el funcionamiento del **Pasaporte de Habilidades TalentoX** y su actualización progresiva.

---

**Día 6 – Integración y limpieza del README**
Se **organizará** toda la información del proyecto TalentoX.
Se **redactará** el README final con un formato claro, ordenado y adecuado para publicación.
Este documento **incluirá** la explicación del problema, la solución propuesta, el modelo de evaluación, ejemplos y datos simulados generados por la plataforma.

---


**Distribución de Aplicaciones**
| Integrante | App | Descripción / Responsabilidades | Modelos | Endpoints especiales |
|------------|-----|--------------------------------|---------|----------------------|
| **Angelica** (Integrante 1) | **users** | Registro e inicio de sesión con JWT, Roles (admin, empresa, aprendiz), Perfil, Permisos personalizados | User (extends AbstractUser), Profile | `/users/me/`<br>`/users/{id}/skills/` |
| | **organizations** | Gestión de empresas, equipos de trabajo y administradores internos | Organization, Team (ManyToMany con Users) | `/organizations/{id}/members/`<br>`/organizations/{id}/teams/` |
| **Sara** (Integrante 2) | **skills** | Categorías, habilidades y niveles dinámicos | Category, Skill, SkillLevel (User + Skill con nivel dinámico) | `/skills/{id}/top-users/`<br>`/skills/{id}/levels/` |
| | **evidence** | Gestión de evidencias del usuario: fotos, snippets, archivos y links | Evidence, MediaFile | `/evidence/user/{id}/`<br>`/evidence/skill/{id}/` |
| **Mariana** (Integrante 3) | **assessments** | Pruebas inteligentes, retos, preguntas, opciones | Assessment, Question, Option | `/assessments/{id}/start/`<br>`/assessments/{id}/submit/` (atomic) |
| | **results** | Procesa puntajes, tiempo, dificultad y recomendaciones | Result, UserScore | `/results/user/{id}/history/`<br>`/results/user/{id}/improvements/` |
| **Jeonardo** (Integrante 4) | **certifications** | Certificaciones basadas en evidencias, resultados y nivel del usuario | Certification | `/certifications/{user_id}/generate/`<br>`/certifications/{user_id}/history/` |

Una vez finalizada la implementación de estas apps, se realizara el despliegue por parte de todos los miembros, pues es importante que todos tengan la capacidad de explicar como funciona y como se hizo.