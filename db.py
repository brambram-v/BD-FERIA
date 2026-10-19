import os
from datetime import date, datetime
from decimal import Decimal
from dotenv import load_dotenv

# Lee el archivo .env (si existe) con las credenciales de la base de datos
load_dotenv()

# ============================================
# CONFIGURACIÓN (se cambia desde el archivo .env)
# ============================================
# Gestores soportados: postgres, mysql, sqlserver, oracle
GESTOR = os.getenv("DB_GESTOR", "postgres").lower()

# Valores por defecto según el gestor
PUERTOS = {"postgres": 5432, "mysql": 3306, "sqlserver": 1433, "oracle": 1521}
USUARIOS = {"postgres": "postgres", "mysql": "root", "sqlserver": "sa", "oracle": "system"}

HOST = os.getenv("DB_HOST", "localhost")
PUERTO = int(os.getenv("DB_PORT", PUERTOS.get(GESTOR, 0)))
NOMBRE = os.getenv("DB_NAME", "ferias")      # En Oracle es el nombre del servicio (ej: XEPDB1)
USUARIO = os.getenv("DB_USER", USUARIOS.get(GESTOR, ""))
CLAVE = os.getenv("DB_PASSWORD", "")

# Solo para SQL Server: nombre del driver ODBC instalado en la computadora
SQLSERVER_DRIVER = os.getenv("DB_SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server")


# ============================================
# CONEXIÓN
# ============================================
def get_connection():
    """Devuelve una conexión nueva al gestor elegido en DB_GESTOR."""
    if GESTOR == "postgres":
        import psycopg2
        return psycopg2.connect(host=HOST, port=PUERTO, dbname=NOMBRE,
                                user=USUARIO, password=CLAVE)

    if GESTOR in ("mysql", "mariadb"):
        import pymysql
        return pymysql.connect(host=HOST, port=PUERTO, database=NOMBRE,
                               user=USUARIO, password=CLAVE)

    if GESTOR == "sqlserver":
        import pyodbc
        cadena = (f"DRIVER={{{SQLSERVER_DRIVER}}};SERVER={HOST},{PUERTO};"
                  f"DATABASE={NOMBRE};UID={USUARIO};PWD={CLAVE};"
                  f"TrustServerCertificate=yes")
        return pyodbc.connect(cadena)

    if GESTOR == "oracle":
        import oracledb
        return oracledb.connect(user=USUARIO, password=CLAVE,
                                dsn=f"{HOST}:{PUERTO}/{NOMBRE}")

    raise ValueError(f"Gestor no soportado: {GESTOR}")


# ============================================
# FUNCIONES AUXILIARES
# ============================================
def adaptar_sql(sql):
    """En app.py escribimos los parámetros como %s. Aquí los convertimos
    al formato que usa cada gestor."""
    if GESTOR == "sqlserver":
        return sql.replace("%s", "?")            # pyodbc usa ?

    if GESTOR == "oracle":
        partes = sql.split("%s")                  # oracledb usa :1, :2, :3 ...
        resultado = partes[0]
        for i in range(1, len(partes)):
            resultado += f":{i}" + partes[i]
        return resultado

    return sql                                    # postgres y mysql usan %s


def limpiar_valor(valor):
    """Convierte fechas y decimales a tipos que jsonify entiende."""
    if isinstance(valor, (datetime, date)):
        return valor.isoformat()
    if isinstance(valor, Decimal):
        return float(valor)
    return valor


def a_fecha(texto):
    """Convierte un texto 'AAAA-MM-DD' en fecha (la entienden todos los gestores)."""
    return datetime.strptime(texto, "%Y-%m-%d").date()


# ============================================
# FUNCIONES QUE USA app.py
# ============================================
def consultar(sql, params=()):
    """Ejecuta un SELECT y devuelve una lista de diccionarios.
    Las claves siempre salen en minúscula (Oracle las devuelve en mayúscula)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(adaptar_sql(sql), params)
    columnas = [col[0].lower() for col in cursor.description]
    filas = []
    for fila in cursor.fetchall():
        filas.append({col: limpiar_valor(valor) for col, valor in zip(columnas, fila)})
    cursor.close()
    conn.close()
    return filas


def ejecutar(sql, params=()):
    """Ejecuta un INSERT, UPDATE o DELETE y confirma los cambios (commit).
    Devuelve la cantidad de filas afectadas."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(adaptar_sql(sql), params)
    conn.commit()
    afectadas = cursor.rowcount
    cursor.close()
    conn.close()
    return afectadas
