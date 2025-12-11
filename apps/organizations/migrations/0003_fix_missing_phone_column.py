from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_organization_administrators_organization_owner_and_more'),
    ]

    operations = [
        # En algunos entornos la columna 'phone' puede faltar aunque el modelo la tenga.
        # Esta migración la añade de forma segura si no existe.
        migrations.AddField(
            model_name='organization',
            name='phone',
            field=models.CharField(
                max_length=10,
                verbose_name='Teléfono',
                blank=True,
                null=True,
            ),
        ),
    ]
