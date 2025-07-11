# Generated by Django 5.2 on 2025-05-05 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_remove_repairorder_service_part_service_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='part',
            name='service',
        ),
        migrations.RemoveField(
            model_name='repairorder',
            name='services',
        ),
        migrations.CreateModel(
            name='ServiceToPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_amount', models.PositiveIntegerField(default=1)),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_services', to='service.part')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_parts', to='service.service')),
            ],
            options={
                'verbose_name': 'Service to Part',
                'verbose_name_plural': 'Service to Parts',
                'unique_together': {('service', 'part')},
            },
        ),
        migrations.AddField(
            model_name='service',
            name='parts',
            field=models.ManyToManyField(related_name='services', through='service.ServiceToPart', to='service.part'),
        ),
        migrations.CreateModel(
            name='RepairOrderService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repair_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_services', to='service.repairorder')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_orders', to='service.service')),
            ],
            options={
                'verbose_name': 'Repair Order Service',
                'verbose_name_plural': 'Repair Order Services',
                'unique_together': {('repair_order', 'service')},
            },
        ),
    ]
