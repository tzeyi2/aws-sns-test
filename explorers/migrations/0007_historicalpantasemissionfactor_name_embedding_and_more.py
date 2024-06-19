# Generated by Django 4.1.10 on 2024-03-08 08:58

from django.db import migrations
import pgvector.django


class Migration(migrations.Migration):

    dependencies = [
        ("explorers", "0006_historicalregiongeocode_country_and_more"),
    ]

    operations = [
        pgvector.django.VectorExtension(),
        migrations.AddField(
            model_name="historicalpantasemissionfactor",
            name="name_embedding",
            field=pgvector.django.VectorField(
                blank=True, dimensions=1024, null=True),
        ),
        migrations.AddField(
            model_name="pantasemissionfactor",
            name="name_embedding",
            field=pgvector.django.VectorField(
                blank=True, dimensions=1024, null=True),
        ),
    ]
