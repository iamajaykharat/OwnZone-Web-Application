# Generated by Django 3.0.6 on 2020-06-15 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('subcategory', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('desc', models.TextField()),
                ('pub_date', models.DateField()),
                ('image', models.ImageField(upload_to='shop/images')),
            ],
        ),
    ]