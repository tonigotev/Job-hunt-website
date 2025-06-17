from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('seekers', '0001_initial'),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='experience',
            field=models.ForeignKey(
                to='seekers.experience',
                on_delete=django.db.models.deletion.SET_NULL,
                null=True,
                blank=True,
                related_name='applications',
            ),
        ),
    ] 