from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0010_restore_hero_stories'),
    ]

    operations = [
        migrations.AddField(
            model_name='legacy',
            name='quote',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
    ]
