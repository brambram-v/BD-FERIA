from flask import Flask, request, jsonify
from db import consultar, ejecutar, a_fecha, GESTOR

# ============================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================
app = Flask(__name__)
# NOTA: la conexión a la base de datos está en db.py
# (todavía sin autenticación JWT ni conexión al frontend)


# ============================================
# FUNCIÓN AUXILIAR PARA LOS PATCH
# ============================================
# PATCH modifica SOLO los campos que lleguen en el JSON.
# Esta función arma la parte "campo1 = %s, campo2 = %s" del UPDATE.
def armar_set(data, campos):
    partes = []
    valores = []
    for campo in campos:
        if campo in data:
            partes.append(f"{campo} = %s")
            if campo.startswith("fecha"):
                valores.append(a_fecha(data[campo]))
            else:
                valores.append(data[campo])
    return ", ".join(partes), valores


# ============================================
# PRUEBA DE CONEXIÓN
# ============================================
@app.route('/', methods=['GET'])
def inicio():
    return jsonify({"mensaje": "API de Ferias funcionando", "gestor": GESTOR}), 200

@app.route('/prueba-conexion', methods=['GET'])
def prueba_conexion():
    resultado = consultar("SELECT COUNT(*) AS total FROM feria")
    return jsonify({"gestor": GESTOR, "total_ferias": resultado[0]["total"]}), 200


# ============================================
# CRUD DE FERIAS
# ============================================
@app.route('/ferias', methods=['GET'])
def listar_ferias():
    ferias = consultar("SELECT * FROM feria")
    return jsonify(ferias), 200

@app.route('/ferias/<int:id>', methods=['GET'])
def obtener_feria(id):
    feria = consultar("SELECT * FROM feria WHERE idferia = %s", (id,))
    if not feria:
        return jsonify({"mensaje": f"No existe la feria con id {id}"}), 404
    return jsonify(feria[0]), 200

@app.route('/ferias', methods=['POST'])
def crear_feria():
    data = request.get_json()
    idferia = data.get("idferia")
    nombre = data.get("nombre")
    dias = data.get("dias")
    motivo = data.get("motivo")
    sql = "INSERT INTO feria (idferia, nombre, dias, motivo) VALUES (%s, %s, %s, %s)"
    ejecutar(sql, (idferia, nombre, dias, motivo))
    return jsonify({"mensaje": "Feria creada correctamente"}), 201

@app.route('/ferias/<int:id>', methods=['PUT'])
def actualizar_feria(id):
    data = request.get_json()
    nombre = data.get("nombre")
    dias = data.get("dias")
    motivo = data.get("motivo")
    sql = "UPDATE feria SET nombre=%s, dias=%s, motivo=%s WHERE idferia=%s"
    ejecutar(sql, (nombre, dias, motivo, id))
    return jsonify({"mensaje": f"Feria con id {id} actualizada correctamente"}), 200

@app.route('/ferias/<int:id>', methods=['PATCH'])
def modificar_feria(id):
    data = request.get_json()
    set_sql, valores = armar_set(data, ["nombre", "dias", "motivo"])
    if not set_sql:
        return jsonify({"mensaje": "No se envió ningún campo para modificar"}), 400
    valores.append(id)
    ejecutar(f"UPDATE feria SET {set_sql} WHERE idferia=%s", tuple(valores))
    return jsonify({"mensaje": f"Feria con id {id} modificada correctamente"}), 200

@app.route('/ferias/<int:id>', methods=['DELETE'])
def eliminar_feria(id):
    ejecutar("DELETE FROM feria WHERE idferia=%s", (id,))
    return jsonify({"mensaje": "Feria eliminada correctamente"}), 200


# ============================================
# CRUD DE LUGARES
# ============================================
@app.route('/lugares', methods=['GET'])
def listar_lugares():
    lugares = consultar("SELECT * FROM lugar")
    return jsonify(lugares), 200

@app.route('/lugares/<int:id>', methods=['GET'])
def obtener_lugar(id):
    lugar = consultar("SELECT * FROM lugar WHERE idlugar = %s", (id,))
    if not lugar:
        return jsonify({"mensaje": f"No existe el lugar con id {id}"}), 404
    return jsonify(lugar[0]), 200

@app.route('/lugares', methods=['POST'])
def crear_lugar():
    data = request.get_json()
    idlugar = data.get("idlugar")
    nombre_lugar = data.get("nombre_lugar")
    macrodistrito = data.get("macrodistrito")
    direccion = data.get("direccion")
    sql = """INSERT INTO lugar (idlugar, nombre_lugar, macrodistrito, direccion)
             VALUES (%s, %s, %s, %s)"""
    ejecutar(sql, (idlugar, nombre_lugar, macrodistrito, direccion))
    return jsonify({"mensaje": "Lugar creado correctamente"}), 201

@app.route('/lugares/<int:id>', methods=['PUT'])
def actualizar_lugar(id):
    data = request.get_json()
    nombre_lugar = data.get("nombre_lugar")
    macrodistrito = data.get("macrodistrito")
    direccion = data.get("direccion")
    sql = """UPDATE lugar
             SET nombre_lugar=%s, macrodistrito=%s, direccion=%s
             WHERE idlugar=%s"""
    ejecutar(sql, (nombre_lugar, macrodistrito, direccion, id))
    return jsonify({"mensaje": f"Lugar con id {id} actualizado correctamente"}), 200

@app.route('/lugares/<int:id>', methods=['PATCH'])
def modificar_lugar(id):
    data = request.get_json()
    set_sql, valores = armar_set(data, ["nombre_lugar", "macrodistrito", "direccion"])
    if not set_sql:
        return jsonify({"mensaje": "No se envió ningún campo para modificar"}), 400
    valores.append(id)
    ejecutar(f"UPDATE lugar SET {set_sql} WHERE idlugar=%s", tuple(valores))
    return jsonify({"mensaje": f"Lugar con id {id} modificado correctamente"}), 200

@app.route('/lugares/<int:id>', methods=['DELETE'])
def eliminar_lugar(id):
    ejecutar("DELETE FROM lugar WHERE idlugar=%s", (id,))
    return jsonify({"mensaje": "Lugar eliminado correctamente"}), 200


# ============================================
# CRUD DE ORGANIZADORES
# ============================================
@app.route('/organizadores', methods=['GET'])
def listar_organizadores():
    organizadores = consultar("SELECT * FROM organizador")
    return jsonify(organizadores), 200

@app.route('/organizadores/<int:id>', methods=['GET'])
def obtener_organizador(id):
    organizador = consultar("SELECT * FROM organizador WHERE idorganizador = %s", (id,))
    if not organizador:
        return jsonify({"mensaje": f"No existe el organizador con id {id}"}), 404
    return jsonify(organizador[0]), 200

@app.route('/organizadores', methods=['POST'])
def crear_organizador():
    data = request.get_json()
    idorganizador = data.get("idorganizador")
    nombre = data.get("nombre")
    contacto = data.get("contacto")
    sql = "INSERT INTO organizador (idorganizador, nombre, contacto) VALUES (%s, %s, %s)"
    ejecutar(sql, (idorganizador, nombre, contacto))
    return jsonify({"mensaje": "Organizador creado correctamente"}), 201

@app.route('/organizadores/<int:id>', methods=['PUT'])
def actualizar_organizador(id):
    data = request.get_json()
    nombre = data.get("nombre")
    contacto = data.get("contacto")
    sql = "UPDATE organizador SET nombre=%s, contacto=%s WHERE idorganizador=%s"
    ejecutar(sql, (nombre, contacto, id))
    return jsonify({"mensaje": f"Organizador con id {id} actualizado correctamente"}), 200

@app.route('/organizadores/<int:id>', methods=['PATCH'])
def modificar_organizador(id):
    data = request.get_json()
    set_sql, valores = armar_set(data, ["nombre", "contacto"])
    if not set_sql:
        return jsonify({"mensaje": "No se envió ningún campo para modificar"}), 400
    valores.append(id)
    ejecutar(f"UPDATE organizador SET {set_sql} WHERE idorganizador=%s", tuple(valores))
    return jsonify({"mensaje": f"Organizador con id {id} modificado correctamente"}), 200

@app.route('/organizadores/<int:id>', methods=['DELETE'])
def eliminar_organizador(id):
    ejecutar("DELETE FROM organizador WHERE idorganizador=%s", (id,))
    return jsonify({"mensaje": "Organizador eliminado correctamente"}), 200


# ============================================
# CRUD DE PROMOTORES
# ============================================
@app.route('/promotores', methods=['GET'])
def listar_promotores():
    promotores = consultar("SELECT * FROM promotor")
    return jsonify(promotores), 200

@app.route('/promotores/<int:id>', methods=['GET'])
def obtener_promotor(id):
    promotor = consultar("SELECT * FROM promotor WHERE idpromotor = %s", (id,))
    if not promotor:
        return jsonify({"mensaje": f"No existe el promotor con id {id}"}), 404
    return jsonify(promotor[0]), 200

@app.route('/promotores', methods=['POST'])
def crear_promotor():
    data = request.get_json()
    idpromotor = data.get("idpromotor")
    nombre = data.get("nombre")
    contacto = data.get("contacto")
    sql = "INSERT INTO promotor (idpromotor, nombre, contacto) VALUES (%s, %s, %s)"
    ejecutar(sql, (idpromotor, nombre, contacto))
    return jsonify({"mensaje": "Promotor creado correctamente"}), 201

@app.route('/promotores/<int:id>', methods=['PUT'])
def actualizar_promotor(id):
    data = request.get_json()
    nombre = data.get("nombre")
    contacto = data.get("contacto")
    sql = "UPDATE promotor SET nombre=%s, contacto=%s WHERE idpromotor=%s"
    ejecutar(sql, (nombre, contacto, id))
    return jsonify({"mensaje": f"Promotor con id {id} actualizado correctamente"}), 200

@app.route('/promotores/<int:id>', methods=['PATCH'])
def modificar_promotor(id):
    data = request.get_json()
    set_sql, valores = armar_set(data, ["nombre", "contacto"])
    if not set_sql:
        return jsonify({"mensaje": "No se envió ningún campo para modificar"}), 400
    valores.append(id)
    ejecutar(f"UPDATE promotor SET {set_sql} WHERE idpromotor=%s", tuple(valores))
    return jsonify({"mensaje": f"Promotor con id {id} modificado correctamente"}), 200

@app.route('/promotores/<int:id>', methods=['DELETE'])
def eliminar_promotor(id):
    ejecutar("DELETE FROM promotor WHERE idpromotor=%s", (id,))
    return jsonify({"mensaje": "Promotor eliminado correctamente"}), 200


# ============================================
# CRUD DE PROPIETARIOS
# ============================================
@app.route('/propietarios', methods=['GET'])
def listar_propietarios():
    propietarios = consultar("SELECT * FROM propietario")
    return jsonify(propietarios), 200

@app.route('/propietarios/<int:id>', methods=['GET'])
def obtener_propietario(id):
    propietario = consultar("SELECT * FROM propietario WHERE idpropietario = %s", (id,))
    if not propietario:
        return jsonify({"mensaje": f"No existe el propietario con id {id}"}), 404
    return jsonify(propietario[0]), 200

@app.route('/propietarios', methods=['POST'])
def crear_propietario():
    data = request.get_json()
    idpropietario = data.get("idpropietario")
    fono = data.get("fono")
    razon_social = data.get("razon_social")
    tipo_propietario = data.get("tipo_propietario")
    sql = """INSERT INTO propietario (idpropietario, fono, razon_social, tipo_propietario)
             VALUES (%s, %s, %s, %s)"""
    ejecutar(sql, (idpropietario, fono, razon_social, tipo_propietario))
    return jsonify({"mensaje": "Propietario creado correctamente"}), 201

@app.route('/propietarios/<int:id>', methods=['PUT'])
def actualizar_propietario(id):
    data = request.get_json()
    fono = data.get("fono")
    razon_social = data.get("razon_social")
    tipo_propietario = data.get("tipo_propietario")
    sql = """UPDATE propietario
             SET fono=%s, razon_social=%s, tipo_propietario=%s
             WHERE idpropietario=%s"""
    ejecutar(sql, (fono, razon_social, tipo_propietario, id))
    return jsonify({"mensaje": f"Propietario con id {id} actualizado correctamente"}), 200

@app.route('/propietarios/<int:id>', methods=['PATCH'])
def modificar_propietario(id):
    data = request.get_json()
    set_sql, valores = armar_set(data, ["fono", "razon_social", "tipo_propietario"])
    if not set_sql:
        return jsonify({"mensaje": "No se envió ningún campo para modificar"}), 400
    valores.append(id)
    ejecutar(f"UPDATE propietario SET {set_sql} WHERE idpropietario=%s", tuple(valores))
    return jsonify({"mensaje": f"Propietario con id {id} modificado correctamente"}), 200

@app.route('/propietarios/<int:id>', methods=['DELETE'])
def eliminar_propietario(id):
    ejecutar("DELETE FROM propietario WHERE idpropietario=%s", (id,))
    return jsonify({"mensaje": "Propietario eliminado correctamente"}), 200


# ============================================
# CRUD DE VENDEDORES
# ============================================
# La fecha de nacimiento se envía como texto "AAAA-MM-DD"
@app.route('/vendedores', methods=['GET'])
def listar_vendedores():
    vendedores = consultar("SELECT * FROM vendedor")
    return jsonify(vendedores), 200

@app.route('/vendedores/<int:id>', methods=['GET'])
def obtener_vendedor(id):
    vendedor = consultar("SELECT * FROM vendedor WHERE idvendedor = %s", (id,))
    if not vendedor:
        return jsonify({"mensaje": f"No existe el vendedor con id {id}"}), 404
    return jsonify(vendedor[0]), 200

@app.route('/vendedores', methods=['POST'])
def crear_vendedor():
    data = request.get_json()
    idvendedor = data.get("idvendedor")
    nombre = data.get("nombre")
    fecha_nac = a_fecha(data.get("fecha_nac"))
    contacto = data.get("contacto")
    idseccion = data.get("idseccion")
    nro_stand = data.get("nro_stand")
    sql = """INSERT INTO vendedor (idvendedor, nombre, fecha_nac, contacto, idseccion, nro_stand)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    ejecutar(sql, (idvendedor, nombre, fecha_nac, contacto, idseccion, nro_stand))
    return jsonify({"mensaje": "Vendedor creado correctamente"}), 201

@app.route('/vendedores/<int:id>', methods=['PUT'])
def actualizar_vendedor(id):
    data = request.get_json()
    nombre = data.get("nombre")
    fecha_nac = a_fecha(data.get("fecha_nac"))
    contacto = data.get("contacto")
    idseccion = data.get("idseccion")
    nro_stand = data.get("nro_stand")
    sql = """UPDATE vendedor
             SET nombre=%s, fecha_nac=%s, contacto=%s, idseccion=%s, nro_stand=%s
             WHERE idvendedor=%s"""
    ejecutar(sql, (nombre, fecha_nac, contacto, idseccion, nro_stand, id))
    return jsonify({"mensaje": f"Vendedor con id {id} actualizado correctamente"}), 200

@app.route('/vendedores/<int:id>', methods=['PATCH'])
def modificar_vendedor(id):
    data = request.get_json()
    set_sql, valores = armar_set(data, ["nombre", "fecha_nac", "contacto", "idseccion", "nro_stand"])
    if not set_sql:
        return jsonify({"mensaje": "No se envió ningún campo para modificar"}), 400
    valores.append(id)
    ejecutar(f"UPDATE vendedor SET {set_sql} WHERE idvendedor=%s", tuple(valores))
    return jsonify({"mensaje": f"Vendedor con id {id} modificado correctamente"}), 200

@app.route('/vendedores/<int:id>', methods=['DELETE'])
def eliminar_vendedor(id):
    ejecutar("DELETE FROM vendedor WHERE idvendedor=%s", (id,))
    return jsonify({"mensaje": "Vendedor eliminado correctamente"}), 200


# ============================================
# CRUD DE STANDS (clave primaria compuesta: idseccion + nro_stand)
# ============================================
@app.route('/stands', methods=['GET'])
def listar_stands():
    stands = consultar("SELECT * FROM stand")
    return jsonify(stands), 200

@app.route('/stands/<int:id_seccion>/<int:nro_stand>', methods=['GET'])
def obtener_stand(id_seccion, nro_stand):
    stand = consultar("SELECT * FROM stand WHERE idseccion = %s AND nro_stand = %s",
                      (id_seccion, nro_stand))
    if not stand:
        return jsonify({"mensaje": f"No existe el stand {nro_stand} de la sección {id_seccion}"}), 404
    return jsonify(stand[0]), 200

@app.route('/stands', methods=['POST'])
def crear_stand():
    data = request.get_json()
    idseccion = data.get("idseccion")
    nro_stand = data.get("nro_stand")
    nombre = data.get("nombre")
    tipo = data.get("tipo")
    idferia = data.get("idferia")
    idlugar = data.get("idlugar")
    idpropietario = data.get("idpropietario")
    sql = """INSERT INTO stand (idseccion, nro_stand, nombre, tipo, idferia, idlugar, idpropietario)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    ejecutar(sql, (idseccion, nro_stand, nombre, tipo, idferia, idlugar, idpropietario))
    return jsonify({"mensaje": "Stand creado correctamente"}), 201

@app.route('/stands/<int:id_seccion>/<int:nro_stand>', methods=['PUT'])
def actualizar_stand(id_seccion, nro_stand):
    data = request.get_json()
    nombre = data.get("nombre")
    tipo = data.get("tipo")
    idferia = data.get("idferia")
    idlugar = data.get("idlugar")
    idpropietario = data.get("idpropietario")
    sql = """UPDATE stand
             SET nombre=%s, tipo=%s, idferia=%s, idlugar=%s, idpropietario=%s
             WHERE idseccion=%s AND nro_stand=%s"""
    ejecutar(sql, (nombre, tipo, idferia, idlugar, idpropietario, id_seccion, nro_stand))
    return jsonify({"mensaje": f"Stand {nro_stand} de la sección {id_seccion} actualizado correctamente"}), 200

@app.route('/stands/<int:id_seccion>/<int:nro_stand>', methods=['PATCH'])
def modificar_stand(id_seccion, nro_stand):
    data = request.get_json()
    set_sql, valores = armar_set(data, ["nombre", "tipo", "idferia", "idlugar", "idpropietario"])
    if not set_sql:
        return jsonify({"mensaje": "No se envió ningún campo para modificar"}), 400
    valores.append(id_seccion)
    valores.append(nro_stand)
    ejecutar(f"UPDATE stand SET {set_sql} WHERE idseccion=%s AND nro_stand=%s", tuple(valores))
    return jsonify({"mensaje": f"Stand {nro_stand} de la sección {id_seccion} modificado correctamente"}), 200

@app.route('/stands/<int:id_seccion>/<int:nro_stand>', methods=['DELETE'])
def eliminar_stand(id_seccion, nro_stand):
    ejecutar("DELETE FROM stand WHERE idseccion=%s AND nro_stand=%s", (id_seccion, nro_stand))
    return jsonify({"mensaje": "Stand eliminado correctamente"}), 200


# ============================================
# PUNTO DE ENTRADA DE LA APLICACIÓN
# ============================================
if __name__ == "__main__":
    app.run(debug=True)
