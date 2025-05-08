from django.db import migrations

def create_part_status_trigger(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("""
            CREATE OR REPLACE FUNCTION update_part_status()
            RETURNS TRIGGER AS $$
            BEGIN
                IF NEW.stock_quantity = 0 THEN
                    NEW.status = 'out_of_stock';
                ELSIF NEW.stock_quantity > 0 AND NEW.stock_quantity < 5 THEN
                    NEW.status = 'low_stock';
                ELSIF NEW.stock_quantity >= 5 THEN
                    NEW.status = 'available';
                END IF;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            DROP TRIGGER IF EXISTS part_status_trigger ON service_part;
            CREATE TRIGGER part_status_trigger
                BEFORE INSERT OR UPDATE OF stock_quantity
                ON service_part
                FOR EACH ROW
                EXECUTE FUNCTION update_part_status();
        """)

def remove_part_status_trigger(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        schema_editor.execute("""
            DROP TRIGGER IF EXISTS part_status_trigger ON service_part;
            DROP FUNCTION IF EXISTS update_part_status();
        """)

class Migration(migrations.Migration):
    dependencies = [
        ('service', '0006_partusage'),
    ]

    operations = [
        migrations.RunPython(create_part_status_trigger, remove_part_status_trigger),
    ] 