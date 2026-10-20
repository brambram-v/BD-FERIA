-- ==================================================================
-- 03_procedimientos_postgres.sql
-- BDFERIA26 · Versión PostgreSQL de los 14 procedimientos (originales en Oracle)
--
-- Ejecutar conectado a la base de ferias:
--   psql -U postgres -d NOMBRE_BASE -f 03_procedimientos_postgres.sql
--
-- Cambios respecto a Oracle:
--   * NUMBER -> INTEGER / NUMERIC, VARCHAR2 -> VARCHAR
--   * Se quitó el COMMIT interno: lo hace el backend (ejecutar()) o psql
--   * Los procedimientos 10, 11 y 13 (SYS_REFCURSOR) pasan a ser FUNCIONES
--     que devuelven una tabla; se consultan con SELECT * FROM fn_...()
--   * El 14 (DBMS_OUTPUT) pasa a ser una función que devuelve filas
-- ==================================================================

-- 1. Registro de un nuevo Lugar
CREATE OR REPLACE PROCEDURE sp_registrar_lugar (
    p_idLugar        INTEGER,
    p_nombre_lugar   VARCHAR,
    p_macrodistrito  VARCHAR,
    p_direccion      VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO lugar (idLugar, nombre_lugar, macrodistrito, direccion)
    VALUES (p_idLugar, p_nombre_lugar, p_macrodistrito, p_direccion);
END;
$$;

-- 2. Registro de una nueva Feria
CREATE OR REPLACE PROCEDURE sp_registrar_feria (
    p_idFeria  INTEGER,
    p_nombre   VARCHAR,
    p_dias     VARCHAR,
    p_motivo   VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO feria (idFeria, nombre, dias, motivo)
    VALUES (p_idFeria, p_nombre, p_dias, p_motivo);
END;
$$;

-- 3. Registro de un Propietario de Stand
CREATE OR REPLACE PROCEDURE sp_registrar_propietario (
    p_idPropietario    INTEGER,
    p_fono             NUMERIC,
    p_razon_social     VARCHAR,
    p_tipo_propietario VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO propietario (idPropietario, fono, razon_social, tipo_propietario)
    VALUES (p_idPropietario, p_fono, p_razon_social, p_tipo_propietario);
END;
$$;

-- 4. Registro de un Stand (entidad débil)
CREATE OR REPLACE PROCEDURE sp_registrar_stand (
    p_idSeccion     INTEGER,
    p_nro_stand     INTEGER,
    p_nombre        VARCHAR,
    p_tipo          VARCHAR,
    p_idFeria       INTEGER,
    p_idLugar       INTEGER,
    p_idPropietario INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO stand (idSeccion, nro_stand, nombre, tipo, idFeria, idLugar, idPropietario)
    VALUES (p_idSeccion, p_nro_stand, p_nombre, p_tipo, p_idFeria, p_idLugar, p_idPropietario);
END;
$$;

-- 5. Registro de un Producto
CREATE OR REPLACE PROCEDURE sp_registrar_producto (
    p_idProducto  INTEGER,
    p_nombre      VARCHAR,
    p_precio      NUMERIC,
    p_descripcion VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO producto (idProducto, nombre, precio, descripcion)
    VALUES (p_idProducto, p_nombre, p_precio, p_descripcion);
END;
$$;

-- 6. Registro de un Vendedor
CREATE OR REPLACE PROCEDURE sp_registrar_vendedor (
    p_idVendedor INTEGER,
    p_nombre     VARCHAR,
    p_fecha_nac  DATE,
    p_contacto   VARCHAR,
    p_idSeccion  INTEGER,
    p_nro_stand  INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO vendedor (idVendedor, nombre, fecha_nac, contacto, idSeccion, nro_stand)
    VALUES (p_idVendedor, p_nombre, p_fecha_nac, p_contacto, p_idSeccion, p_nro_stand);
END;
$$;

-- 7. Asociación de Producto a Stand (OFRECE)
CREATE OR REPLACE PROCEDURE sp_asociar_producto_stand (
    p_idProducto INTEGER,
    p_idSeccion  INTEGER,
    p_nro_stand  INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO ofrece (idProducto, idSeccion, nro_stand)
    VALUES (p_idProducto, p_idSeccion, p_nro_stand);
END;
$$;

-- 8. Actualización de precio de un producto
CREATE OR REPLACE PROCEDURE sp_actualizar_precio_producto (
    p_idProducto   INTEGER,
    p_nuevo_precio NUMERIC
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE producto
    SET precio = p_nuevo_precio
    WHERE idProducto = p_idProducto;
END;
$$;

-- 9. Relación de exposición (SE_EXPONE)
CREATE OR REPLACE PROCEDURE sp_asignar_feria_lugar (
    p_idFeria INTEGER,
    p_idLugar INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO se_expone (idFeria, idLugar)
    VALUES (p_idFeria, p_idLugar);
END;
$$;

-- 10. Stands por feria  (Oracle: SYS_REFCURSOR -> Postgres: función que devuelve tabla)
CREATE OR REPLACE FUNCTION fn_listar_stands_por_feria (p_idFeria INTEGER)
RETURNS TABLE (
    idseccion     INTEGER,
    nro_stand     INTEGER,
    nombre        VARCHAR,
    tipo          VARCHAR,
    nombre_lugar  VARCHAR
)
LANGUAGE sql
AS $$
    SELECT s.idSeccion::INTEGER,
           s.nro_stand::INTEGER,
           s.nombre::VARCHAR,
           s.tipo::VARCHAR,
           l.nombre_lugar::VARCHAR
    FROM stand s
    JOIN lugar l ON s.idLugar = l.idLugar
    WHERE s.idFeria = p_idFeria;
$$;

-- 11. Productos por rango de precios
CREATE OR REPLACE FUNCTION fn_buscar_productos_precio (
    p_precio_min NUMERIC,
    p_precio_max NUMERIC
)
RETURNS TABLE (
    idproducto  INTEGER,
    nombre      VARCHAR,
    precio      NUMERIC,
    descripcion VARCHAR
)
LANGUAGE sql
AS $$
    SELECT p.idProducto::INTEGER,
           p.nombre::VARCHAR,
           p.precio::NUMERIC,
           p.descripcion::VARCHAR
    FROM producto p
    WHERE p.precio BETWEEN p_precio_min AND p_precio_max;
$$;

-- 12. Asignación de Organizador a Feria
CREATE OR REPLACE PROCEDURE sp_organizar_feria (
    p_idOrganizador INTEGER,
    p_idFeria       INTEGER,
    p_idLugar       INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO organiza (idOrganizador, idFeria, idLugar)
    VALUES (p_idOrganizador, p_idFeria, p_idLugar);
END;
$$;

-- 13. Vendedores por stand
CREATE OR REPLACE FUNCTION fn_obtener_vendedores_stand (
    p_idSeccion INTEGER,
    p_nro_stand INTEGER
)
RETURNS TABLE (
    idvendedor INTEGER,
    nombre     VARCHAR,
    fecha_nac  DATE,
    contacto   VARCHAR
)
LANGUAGE sql
AS $$
    SELECT v.idVendedor::INTEGER,
           v.nombre::VARCHAR,
           v.fecha_nac::DATE,
           v.contacto::VARCHAR
    FROM vendedor v
    WHERE v.idSeccion = p_idSeccion
      AND v.nro_stand = p_nro_stand;
$$;

-- 14. Resumen por sección (cursor explícito; Oracle imprimía con DBMS_OUTPUT,
--     aquí devuelve una fila por sección)
CREATE OR REPLACE FUNCTION fn_resumen_seccion ()
RETURNS TABLE (
    idseccion       INTEGER,
    nombre_seccion  VARCHAR,
    total_stands    BIGINT,
    total_productos BIGINT
)
LANGUAGE plpgsql
AS $$
DECLARE
    c_secciones CURSOR FOR
        SELECT sec.idSeccion AS id_sec, sec.nombre_seccion AS nom_sec
        FROM seccion sec;
    reg RECORD;
BEGIN
    FOR reg IN c_secciones LOOP
        idseccion      := reg.id_sec;
        nombre_seccion := reg.nom_sec;

        SELECT COUNT(*) INTO total_stands
        FROM stand st
        WHERE st.idSeccion = reg.id_sec;

        SELECT COUNT(DISTINCT o.idProducto) INTO total_productos
        FROM ofrece o
        JOIN stand st ON o.idSeccion = st.idSeccion AND o.nro_stand = st.nro_stand
        WHERE st.idSeccion = reg.id_sec;

        RETURN NEXT;
    END LOOP;
END;
$$;
