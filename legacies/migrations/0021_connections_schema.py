from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legacies', '0020_legacy_archive_id'),
    ]

    operations = [
        # ── Place ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('name_om', models.CharField(blank=True, default='', help_text='Name in Afaan Oromo', max_length=200)),
                ('slug', models.SlugField(max_length=220, unique=True)),
                ('place_type', models.CharField(
                    choices=[
                        ('city', 'City / Town'),
                        ('village', 'Village / Kebele'),
                        ('region', 'Region / Zone'),
                        ('prison', 'Prison / Detention Center'),
                        ('battlefield', 'Battlefield / Conflict Site'),
                        ('institution', 'Institution / Building'),
                        ('grave', 'Grave / Memorial Site'),
                        ('other', 'Other'),
                    ],
                    default='other',
                    max_length=20,
                )),
                ('zone', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='places', to='legacies.zone',
                )),
                ('description', models.TextField(blank=True, default='')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),

        # ── Organization ───────────────────────────────────────────────────
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('name_om', models.CharField(blank=True, default='', max_length=200)),
                ('slug', models.SlugField(max_length=220, unique=True)),
                ('org_type', models.CharField(
                    choices=[
                        ('political', 'Political Party / Movement'),
                        ('military', 'Military / Armed Group'),
                        ('cultural', 'Cultural / Self-Help Association'),
                        ('religious', 'Religious Organization'),
                        ('academic', 'Academic / Educational Institution'),
                        ('media', 'Media Organization'),
                        ('government', 'Government Body'),
                        ('ngo', 'NGO / Civil Society'),
                        ('other', 'Other'),
                    ],
                    default='other',
                    max_length=20,
                )),
                ('description', models.TextField(blank=True, default='')),
                ('founded_year', models.IntegerField(blank=True, null=True)),
                ('dissolved_year', models.IntegerField(blank=True, null=True)),
                ('historical_period', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='organizations', to='legacies.historicalperiod',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name']},
        ),

        # ── PersonConnection ───────────────────────────────────────────────
        migrations.CreateModel(
            name='PersonConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_legacy', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='connections_from', to='legacies.legacy',
                )),
                ('to_legacy', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='connections_to', to='legacies.legacy',
                )),
                ('relationship_type', models.CharField(
                    choices=[
                        ('colleague', 'Colleague / Comrade'),
                        ('co_defendant', 'Co-defendant / Co-prisoner'),
                        ('mentor', 'Mentor'),
                        ('student', 'Student / Mentee'),
                        ('family', 'Family Member'),
                        ('commander', 'Commander'),
                        ('subordinate', 'Subordinate'),
                        ('contemporary', 'Contemporary / Peer'),
                        ('collaborator', 'Collaborator'),
                        ('opponent', 'Political Opponent'),
                        ('other', 'Other'),
                    ],
                    max_length=20,
                )),
                ('description', models.CharField(blank=True, default='', max_length=400)),
                ('year_from', models.IntegerField(blank=True, null=True)),
                ('year_to', models.IntegerField(blank=True, null=True)),
            ],
            options={'ordering': ['relationship_type']},
        ),
        migrations.AddConstraint(
            model_name='personconnection',
            constraint=models.UniqueConstraint(
                fields=['from_legacy', 'to_legacy', 'relationship_type'],
                name='personconnection_unique',
            ),
        ),

        # ── LegacyPlace ────────────────────────────────────────────────────
        migrations.CreateModel(
            name='LegacyPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legacy', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='place_connections', to='legacies.legacy',
                )),
                ('place', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='legacy_connections', to='legacies.place',
                )),
                ('connection_type', models.CharField(
                    choices=[
                        ('born', 'Born Here'),
                        ('lived', 'Lived / Resided'),
                        ('died', 'Died Here'),
                        ('imprisoned', 'Imprisoned / Detained'),
                        ('exiled', 'Exiled From / To'),
                        ('organized', 'Organized / Activist Work'),
                        ('buried', 'Buried Here'),
                        ('other', 'Other Connection'),
                    ],
                    max_length=20,
                )),
                ('year_from', models.IntegerField(blank=True, null=True)),
                ('year_to', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=400)),
            ],
            options={'ordering': ['connection_type']},
        ),
        migrations.AddConstraint(
            model_name='legacyplace',
            constraint=models.UniqueConstraint(
                fields=['legacy', 'place', 'connection_type'],
                name='legacyplace_unique',
            ),
        ),

        # ── LegacyOrganization ─────────────────────────────────────────────
        migrations.CreateModel(
            name='LegacyOrganization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legacy', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='org_connections', to='legacies.legacy',
                )),
                ('organization', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='legacy_connections', to='legacies.organization',
                )),
                ('role', models.CharField(
                    blank=True, default='',
                    help_text='e.g. Founder, Secretary, Member',
                    max_length=200,
                )),
                ('year_from', models.IntegerField(blank=True, null=True)),
                ('year_to', models.IntegerField(blank=True, null=True)),
                ('description', models.CharField(blank=True, default='', max_length=400)),
            ],
            options={'ordering': ['organization__name']},
        ),
        migrations.AddConstraint(
            model_name='legacyorganization',
            constraint=models.UniqueConstraint(
                fields=['legacy', 'organization'],
                name='legacyorganization_unique',
            ),
        ),
    ]
