# Generated by Django 5.0.4 on 2024-04-15 13:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("watchlist_app", "0005_review_review_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="watchlist",
            name="average_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="watchlist",
            name="num_of_ratings",
            field=models.IntegerField(default=0),
        ),
    ]
