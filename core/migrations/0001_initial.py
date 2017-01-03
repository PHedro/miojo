# -*- coding: utf-8 -*-

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BreadCrumbs',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(default=None)),
                ('deleted', models.BooleanField(default=False)),
                (
                    'user',
                    models.CharField(
                        blank=True, db_index=True, max_length=300, null=True
                    )
                ),
                (
                    'user_agent',
                    models.CharField(blank=True, max_length=500, null=True)
                ),
                (
                    'ip',
                    models.CharField(
                        blank=True, db_index=True, max_length=100, null=True
                    )
                ),
                (
                    'method',
                    models.CharField(
                        blank=True, db_index=True, max_length=10, null=True
                    )
                ),
                (
                    'url',
                    models.CharField(blank=True, max_length=1000, null=True)
                ),
                (
                    'referer',
                    models.CharField(blank=True, max_length=1000, null=True)
                ),
                ('get', models.TextField(blank=True, null=True)),
                ('post', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
