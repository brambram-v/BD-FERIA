-- ==================================================================
-- 04_bitacora_triggers_postgres.sql
-- BDFERIA26 · Tabla BITACORA_FERIAS y los 10 triggers en PostgreSQL
--
-- Ejecutar conectado a la base de ferias:
--   psql -U postgres -d NOMBRE_BASE -f 04_bitacora_triggers_postgres.sql
--
-- En Oracle cada trigger tenía su propio cuerpo. En Postgres un trigger
-- necesita una FUNCIÓN de trigger, así que se usa una sola función
-- (fn_registrar_bitacora) que toma el nombre de la tabla y la operación
-- automáticamente, y 10 CREATE TRIGGER que la llaman.
-- Son triggers de SENTENCIA (FOR EACH STATEMENT), igual que los de Oracle.
-- ==================================================================

CREATE TABLE IF NOT EXISTS bitacora_ferias (
    id_bitacora     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tabla_afectada  VARCHAR(50),
    operacion       VARCHAR(20),
    usuario_bd      VARCHAR(100),
    fecha_operacion TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_registrar_bitacora ()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO bitacora_ferias (tabla_afectada, operacion, usuario_bd, fecha_operacion)
    VALUES (UPPER(TG_TABLE_NAME), TG_OP, current_user, CURRENT_TIMESTAMP);
    RETURN NULL;   -- en triggers AFTER de sentencia el valor devuelto se ignora
END;
$$;

-- Trigger 1. Inserción de una feria
DROP TRIGGER IF EXISTS trg_insert_feria ON feria;
CREATE TRIGGER trg_insert_feria
AFTER INSERT ON feria
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 2. Modificación de una feria
DROP TRIGGER IF EXISTS trg_update_feria ON feria;
CREATE TRIGGER trg_update_feria
AFTER UPDATE ON feria
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 3. Eliminación de una feria
DROP TRIGGER IF EXISTS trg_delete_feria ON feria;
CREATE TRIGGER trg_delete_feria
AFTER DELETE ON feria
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 4. Inserción de un lugar
DROP TRIGGER IF EXISTS trg_insert_lugar ON lugar;
CREATE TRIGGER trg_insert_lugar
AFTER INSERT ON lugar
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 5. Modificación de un lugar
DROP TRIGGER IF EXISTS trg_update_lugar ON lugar;
CREATE TRIGGER trg_update_lugar
AFTER UPDATE ON lugar
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 6. Inserción de un stand
DROP TRIGGER IF EXISTS trg_insert_stand ON stand;
CREATE TRIGGER trg_insert_stand
AFTER INSERT ON stand
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 7. Modificación de productos
DROP TRIGGER IF EXISTS trg_update_producto ON producto;
CREATE TRIGGER trg_update_producto
AFTER UPDATE ON producto
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 8. Inserción de vendedores
DROP TRIGGER IF EXISTS trg_insert_vendedor ON vendedor;
CREATE TRIGGER trg_insert_vendedor
AFTER INSERT ON vendedor
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 9. Eliminación de productos ofrecidos
DROP TRIGGER IF EXISTS trg_delete_ofrece ON ofrece;
CREATE TRIGGER trg_delete_ofrece
AFTER DELETE ON ofrece
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();

-- Trigger 10. Modificación de propietarios
DROP TRIGGER IF EXISTS trg_update_propietario ON propietario;
CREATE TRIGGER trg_update_propietario
AFTER UPDATE ON propietario
FOR EACH STATEMENT EXECUTE FUNCTION fn_registrar_bitacora();
