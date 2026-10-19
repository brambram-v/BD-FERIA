-- ============================================================
-- FERIAS DE FIN DE SEMANA - LA PAZ (GRUPO 3)
-- Creacion de tablas para PostgreSQL
-- Equivalente al script de Oracle (creacion_tablas.sql)
--
-- Cambios respecto a Oracle:
--   NUMBER        -> INTEGER / BIGINT / NUMERIC(10,2)
--   VARCHAR2(n)   -> VARCHAR(n)
--   BEGIN ... EXECUTE IMMEDIATE ... END;  -> sentencias CREATE TABLE normales
-- ============================================================

-- Limpieza: permite volver a ejecutar el script desde cero.
-- (borra las tablas si ya existen, en orden de dependencia)
DROP TABLE IF EXISTS ofrece, vendedor, stand, producto, propietario, seccion,
                     promueve, promotor, organiza, organizador, se_expone,
                     feria, lugar CASCADE;

-- ENTIDADES FUERTES Y AGREGACION FERIA-LUGAR
CREATE TABLE lugar (
    idLugar       INTEGER PRIMARY KEY,
    nombre_lugar  VARCHAR(100) NOT NULL,
    macrodistrito VARCHAR(50)  NOT NULL,
    direccion     VARCHAR(150) NOT NULL
);

CREATE TABLE feria (
    idFeria INTEGER PRIMARY KEY,
    nombre  VARCHAR(100) NOT NULL,
    dias    VARCHAR(50)  NOT NULL,
    motivo  VARCHAR(150) NOT NULL
);

CREATE TABLE se_expone (
    idFeria INTEGER,
    idLugar INTEGER,
    PRIMARY KEY (idFeria, idLugar),
    CONSTRAINT fk_seexpone_feria FOREIGN KEY (idFeria) REFERENCES feria(idFeria),
    CONSTRAINT fk_seexpone_lugar FOREIGN KEY (idLugar) REFERENCES lugar(idLugar)
);

-- ORGANIZADOR Y PROMOTOR (RELACIONES M:N CON LA AGREGACION)
CREATE TABLE organizador (
    idOrganizador INTEGER PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    contacto      VARCHAR(50)  NOT NULL
);

CREATE TABLE organiza (
    idOrganizador INTEGER,
    idFeria       INTEGER,
    idLugar       INTEGER,
    PRIMARY KEY (idOrganizador, idFeria, idLugar),
    CONSTRAINT fk_organiza_org      FOREIGN KEY (idOrganizador) REFERENCES organizador(idOrganizador),
    CONSTRAINT fk_organiza_seexpone FOREIGN KEY (idFeria, idLugar) REFERENCES se_expone(idFeria, idLugar)
);

CREATE TABLE promotor (
    idPromotor INTEGER PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    contacto   VARCHAR(50)  NOT NULL
);

CREATE TABLE promueve (
    idPromotor INTEGER,
    idFeria    INTEGER,
    idLugar    INTEGER,
    PRIMARY KEY (idPromotor, idFeria, idLugar),
    CONSTRAINT fk_promueve_prom     FOREIGN KEY (idPromotor) REFERENCES promotor(idPromotor),
    CONSTRAINT fk_promueve_seexpone FOREIGN KEY (idFeria, idLugar) REFERENCES se_expone(idFeria, idLugar)
);

-- AGREGACION SECCION-STAND (STAND ES ENTIDAD DEBIL)
CREATE TABLE seccion (
    idSeccion      INTEGER PRIMARY KEY,
    nombre_seccion VARCHAR(100) NOT NULL
);

CREATE TABLE propietario (
    idPropietario    INTEGER PRIMARY KEY,
    fono             BIGINT       NOT NULL,
    razon_social     VARCHAR(150) NOT NULL,
    tipo_propietario VARCHAR(50)  NOT NULL
);

CREATE TABLE stand (
    idSeccion     INTEGER,
    nro_stand     INTEGER,
    nombre        VARCHAR(100) NOT NULL,
    tipo          VARCHAR(50)  NOT NULL,
    idFeria       INTEGER NOT NULL,
    idLugar       INTEGER NOT NULL,
    idPropietario INTEGER NOT NULL,
    PRIMARY KEY (idSeccion, nro_stand),
    CONSTRAINT fk_stand_seccion     FOREIGN KEY (idSeccion) REFERENCES seccion(idSeccion),
    CONSTRAINT fk_stand_seexpone    FOREIGN KEY (idFeria, idLugar) REFERENCES se_expone(idFeria, idLugar),
    CONSTRAINT fk_stand_propietario FOREIGN KEY (idPropietario) REFERENCES propietario(idPropietario)
);

-- VENDEDOR, PRODUCTO Y OFRECE
CREATE TABLE vendedor (
    idVendedor INTEGER PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    fecha_nac  DATE         NOT NULL,
    contacto   VARCHAR(50)  NOT NULL,
    idSeccion  INTEGER NOT NULL,
    nro_stand  INTEGER NOT NULL,
    CONSTRAINT fk_vendedor_stand FOREIGN KEY (idSeccion, nro_stand) REFERENCES stand(idSeccion, nro_stand)
);

CREATE TABLE producto (
    idProducto  INTEGER PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL,
    precio      NUMERIC(10, 2) NOT NULL,
    descripcion VARCHAR(200)
);

CREATE TABLE ofrece (
    idProducto INTEGER,
    idSeccion  INTEGER,
    nro_stand  INTEGER,
    PRIMARY KEY (idProducto, idSeccion, nro_stand),
    CONSTRAINT fk_ofrece_producto FOREIGN KEY (idProducto) REFERENCES producto(idProducto),
    CONSTRAINT fk_ofrece_stand    FOREIGN KEY (idSeccion, nro_stand) REFERENCES stand(idSeccion, nro_stand)
);
