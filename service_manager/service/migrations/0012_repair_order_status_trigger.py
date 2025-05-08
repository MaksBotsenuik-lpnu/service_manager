from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('service', '0010_merge_20250508_1612'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL
            sql="""
            DROP TRIGGER IF EXISTS repair_order_status_trigger ON service_repairorder;
            DROP FUNCTION IF EXISTS update_repair_order_status();

            CREATE OR REPLACE FUNCTION update_repair_order_status()
            RETURNS TRIGGER AS $$
            DECLARE
                service_record RECORD;
                part_record RECORD;
                service_part_record RECORD;
                update_needed BOOLEAN := FALSE;
            BEGIN
                -- Validate status transition
                IF NOT (
                    -- pending transitions
                    (OLD.status = 'pending' AND NEW.status IN ('in_progress', 'waiting_for_parts', 'cancelled')) OR
                    -- in_progress transitions
                    (OLD.status = 'in_progress' AND NEW.status IN ('waiting_for_parts', 'completed', 'pending')) OR
                    -- waiting_for_parts transitions
                    (OLD.status = 'waiting_for_parts' AND NEW.status IN ('in_progress', 'pending', 'cancelled'))
                ) THEN
                    RAISE EXCEPTION 'Invalid status transition from % to %', OLD.status, NEW.status;
                END IF;

                -- Handle transition to in_progress
                IF (OLD.status IN ('pending', 'waiting_for_parts') AND NEW.status = 'in_progress') THEN
                    -- Check all services and their parts
                    FOR service_record IN 
                        SELECT * FROM service_repairorderservice WHERE repair_order_id = NEW.id
                    LOOP
                        -- Check each part in the service
                        FOR service_part_record IN 
                            SELECT * FROM service_servicetopart WHERE service_id = service_record.service_id
                        LOOP
                            -- Get current part status
                            SELECT * INTO part_record FROM service_part WHERE id = service_part_record.part_id;
                            
                            -- Check if we have enough parts
                            IF part_record.stock_quantity < service_part_record.part_amount THEN
                                -- Not enough parts, set status back to waiting_for_parts
                                NEW.status := 'waiting_for_parts';
                                RETURN NEW;
                            END IF;
                            
                            -- Update part quantities
                            UPDATE service_part 
                            SET 
                                stock_quantity = stock_quantity - service_part_record.part_amount,
                                reserved_parts = reserved_parts + service_part_record.part_amount
                            WHERE id = service_part_record.part_id;
                        END LOOP;
                    END LOOP;
                
                -- Handle transition from in_progress to completed
                ELSIF OLD.status = 'in_progress' AND NEW.status = 'completed' THEN
                    -- Release reserved parts
                    FOR service_record IN 
                        SELECT * FROM service_repairorderservice WHERE repair_order_id = NEW.id
                    LOOP
                        FOR service_part_record IN 
                            SELECT * FROM service_servicetopart WHERE service_id = service_record.service_id
                        LOOP
                            UPDATE service_part 
                            SET reserved_parts = reserved_parts - service_part_record.part_amount
                            WHERE id = service_part_record.part_id;
                        END LOOP;
                    END LOOP;

                -- Handle transition from in_progress to pending
                ELSIF OLD.status = 'in_progress' AND NEW.status = 'pending' THEN
                    -- Release reserved parts
                    FOR service_record IN 
                        SELECT * FROM service_repairorderservice WHERE repair_order_id = NEW.id
                    LOOP
                        FOR service_part_record IN 
                            SELECT * FROM service_servicetopart WHERE service_id = service_record.service_id
                        LOOP
                            UPDATE service_part 
                            SET 
                                reserved_parts = reserved_parts - service_part_record.part_amount,
                                stock_quantity = stock_quantity + service_part_record.part_amount
                            WHERE id = service_part_record.part_id;
                        END LOOP;
                    END LOOP;

                -- Handle transition to cancelled
                ELSIF NEW.status = 'cancelled' THEN
                    -- If parts were reserved, release them
                    IF OLD.status = 'in_progress' THEN
                        FOR service_record IN 
                            SELECT * FROM service_repairorderservice WHERE repair_order_id = NEW.id
                        LOOP
                            FOR service_part_record IN 
                                SELECT * FROM service_servicetopart WHERE service_id = service_record.service_id
                            LOOP
                                UPDATE service_part 
                                SET 
                                    reserved_parts = reserved_parts - service_part_record.part_amount,
                                    stock_quantity = stock_quantity + service_part_record.part_amount
                                WHERE id = service_part_record.part_id;
                            END LOOP;
                        END LOOP;
                    END IF;
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;

            CREATE TRIGGER repair_order_status_trigger
                BEFORE UPDATE OF status
                ON service_repairorder
                FOR EACH ROW
                EXECUTE FUNCTION update_repair_order_status();
            """,
            # Reverse SQL
            reverse_sql="""
            DROP TRIGGER IF EXISTS repair_order_status_trigger ON service_repairorder;
            DROP FUNCTION IF EXISTS update_repair_order_status();
            """
        ),
    ] 