# Generated by Django 4.2.9 on 2024-06-05 15:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("agents", "0002_agent_target_ip"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agent",
            name="target_ip",
        ),
    ]
