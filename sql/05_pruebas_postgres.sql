-- ==================================================================
-- 05_pruebas_postgres.sql
-- Comprobación de los 14 procedimientos y los triggers en PostgreSQL.
-- Usa los mismos datos de prueba que el documento original (ids 9001).
-- Requiere que existan la sección 1, la feria 1, el lugar 1 y el
-- propietario 1 (ajusta esos números si en tu base son otros).
-- Ejecutar DESPUÉS de 03 y 04. Al final hay un bloque para limpiar.
-- ==================================================================

-- 1 a 9: registros
CALL sp_registrar_lugar(9001, 'Lugar de Prueba', 'Centro', 'Av. de Prueba 123');
CALL sp_registrar_feria(9001, 'Feria de Prueba', 'Sabado y Domingo', 'Prueba del procedimiento');
CALL sp_registrar_propietario(9001, 70000001, 'Propietario de Prueba', 'Persona natural');
CALL sp_registrar_stand(1, 9001, 'Stand de Prueba', 'Comercial', 1, 1, 1);
CALL sp_registrar_producto(9001, 'Producto de Prueba', 25.50, 'Producto creado para verificar el procedimiento');
CALL sp_registrar_vendedor(9001, 'Vendedor de Prueba', DATE '2000-05-15', '70000002', 1, 9001);
CALL sp_asociar_producto_stand(9001, 1, 9001);
CALL sp_actualizar_precio_producto(9001, 39.90);
CALL sp_asignar_feria_lugar(9001, 9001);

SELECT * FROM stand    WHERE idSeccion = 1 AND nro_stand = 9001;
SELECT * FROM producto WHERE idProducto = 9001;   -- precio debe ser 39.90
SELECT * FROM vendedor WHERE idVendedor = 9001;
SELECT * FROM ofrece   WHERE idProducto = 9001;
SELECT * FROM se_expone WHERE idFeria = 9001 AND idLugar = 9001;

-- 10, 11, 13, 14: funciones que devuelven tabla
SELECT * FROM fn_listar_stands_por_feria(1);
SELECT * FROM fn_buscar_productos_precio(10, 50);
SELECT * FROM fn_obtener_vendedores_stand(1, 9001);
SELECT * FROM fn_resumen_seccion();

-- 12: organizador (necesita un organizador existente; cambia el 1 si hace falta)
-- CALL sp_organizar_feria(1, 9001, 9001);

-- Triggers: cada operación anterior debe haber dejado una fila aquí
SELECT * FROM bitacora_ferias ORDER BY id_bitacora DESC;

-- ------------------------------------------------------------------
-- LIMPIEZA (opcional, en este orden por las claves foráneas)
-- ------------------------------------------------------------------
-- DELETE FROM ofrece     WHERE idProducto = 9001;
-- DELETE FROM vendedor   WHERE idVendedor = 9001;
-- DELETE FROM stand      WHERE idSeccion = 1 AND nro_stand = 9001;
-- DELETE FROM se_expone  WHERE idFeria = 9001 AND idLugar = 9001;
-- DELETE FROM producto   WHERE idProducto = 9001;
-- DELETE FROM propietario WHERE idPropietario = 9001;
-- DELETE FROM feria      WHERE idFeria = 9001;
-- DELETE FROM lugar      WHERE idLugar = 9001;
