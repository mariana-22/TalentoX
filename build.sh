set -o errexit

pip install -r requirements.txt
find . \
  \( -type d -name "venv" -o -name ".venv" -o -name "env" -o -name ".env" -o -name "virtualenv" \) -prune \
  -o -type d -name "migrations" -exec rm -rf {}/* \;
rm -rf staticfiles/
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py makemigrations users
python manage.py makemigrations skills
python manage.py makemigrations assessments
python manage.py makemigrations results
python manage.py makemigrations certifications
python manage.py makemigrations evidence
python manage.py makemigrations organizations
# First, migrate only the users app (creates the custom User table)
python manage.py migrate users
python manage.py migrate skills
python manage.py migrate assessments
python manage.py migrate results
python manage.py migrate certifications
python manage.py migrate evidence
python manage.py migrate organizations

# Then migrate contenttypes and auth (dependencies)
python manage.py migrate contenttypes
python manage.py migrate auth

# Then migrate admin (creates django_admin_log with FK to users)
python manage.py migrate admin

# Finally, migrate everything else
python manage.py migrate
python scripts/populate_db.py