from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0012_seed_hero_quotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='legacy',
            name='photo_enhanced',
            field=models.ImageField(blank=True, null=True, upload_to='legacy_photos/'),
        ),
        migrations.AddField(
            model_name='legacy',
            name='photo_enhancement_status',
            field=models.CharField(
                max_length=20,
                default='none',
                choices=[
                    ('none', 'Not enhanced'),
                    ('pending', 'Enhancement in progress'),
                    ('done', 'Enhanced'),
                    ('failed', 'Enhancement failed'),
                ],
            ),
        ),
    ]
