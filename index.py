from flask import Flask, redirect, render_template, request, url_for, flash, session, send_file 
from flask_mysqldb import MySQL
from datetime import date, datetime
import locale, time
from flask_bcrypt import Bcrypt

# condiciones para la ejecucion de lcodigo 
#   Se necita instalar todas estas dependencias importadas arriba (FLASK,FLASK_MYSQLDB,DATETIME,FLASK_BCRYPT) 
#       Ademas se debe utilziar python 3.7.0 para poder correr flask_mysqldb 
#          Tambien se debe tener la base de datos funcionando y editar las app.config de MSQL deacuerdo a su configuracion 

app = Flask(__name__)
# Servidor MSQL Local-configuracion de conexiones de base de datos
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Rode7991*"
app.config["MYSQL_DB"] = "rode"

# Variable para el cursor de la base de datos
mysql= MySQL(app)
# Variable para hasheo
bcrypt = Bcrypt()
#Clave secreta
app.secret_key = "kYp3s6v9y$B&E)H@McQfTjWnZq4t7w!z"

@app.route("/")
def home():
    return render_template("login.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/loginIn", methods=["POST"])
def loginIn():
    if request.method == "POST":
        # Carga el nombre del usuario y realizo la busqueda del usuario en la base de datos
        usrlogin = request.form["usuario"]
        pasw = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM rode.usuario WHERE usuario="'+usrlogin+'";')
        userdata = cur.fetchall()
        if userdata:
            userdata = userdata[0]
            if usrlogin == userdata[1] and bcrypt.check_password_hash(
                userdata[2], pasw ):
                # almaceno en el diccionario de sessiones mi usuarrio para validaro luego en otros metodos
                session["idusuario"] = userdata[0]
                session["nombreusr"] = userdata[1]
                session["tipousr"] = userdata[3]
                return redirect(url_for("tcontrol"))
            else:
                mensajeError = (
                    "A ocurrido un error con tu contraseña, intentalo nuevamente"
                )
                flash(mensajeError)
                return redirect(url_for("login"))
        else:
            mensajeError = "A ocurrido un error con tu usuario, intentalo nuevamente"
            flash(mensajeError)
            return redirect(url_for("login"))
    return redirect(url_for("login"))


@app.route("/logOut")
def logout():
    session.clear()
    mensajeSession = "Se cerro la session."
    flash(mensajeSession)
    return redirect(url_for("login"))


@app.route("/tableroControl")
def tcontrol():
    # validar que  el  usuario que ingreso sea admin, de ser  asi redireccionarlo a  tablero de lo contrario a marcacion  de horario
    if "tipousr" in session:
        if session["tipousr"] == 1:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM horario")
            horarios = cur.fetchall()
            return render_template("tableroControl.html",horarios=horarios)
        else:
            flash("Bienvenido " + session["nombreusr"])
            return redirect(url_for("MHorario"))
    return redirect(url_for("login"))


# poner en el metodo que  espera un parametro para utilizarlo en la busqueda de horarios solo del operario que esta por marcar asistencia


@app.route("/MarcarHorario")
def MHorario():
    if "tipousr" in session:
        if session["tipousr"] == 3:
            idOpe = session["idusuario"]
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM horario")
            horarios = cur.fetchall()
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM operario WHERE IdOperario=" + str(idOpe))
            datousr = cur.fetchall()
            return render_template(
                "marcarHorario.html", datousr=datousr, horarios=horarios
            )
        flash(
            "No es posible utilizar el marcado de horarios para este usuario en particular"
        )
    return redirect(url_for("tcontrol"))


@app.route("/verHorarios")
def verHorarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM horario")
    horarios = cur.fetchall()
    return render_template("verHorarios.html", horarios=horarios)


# bhorarios y busuarios son metodos se deberian mover a otro lado
@app.route("/buscarHorarios", methods=["POST"])
def Buscarhorario():
    if request.method == "POST":
        id = request.form["busqueda"]
        if id == "":
            mensajeError = (
                "Error en la busqueda, no se escrbio ningun dato o no existen ningun dato con"
                + id
                + ". Se muestran todos los datos"
            )
            flash(mensajeError)
            return redirect(url_for("verHorarios"))
        else:
            # mensajeExito= "Estos son los resultados de  su busqueeda:"+id
            cur = mysql.connection.cursor()
            # Hago la consulta para la busqueda en la db, donde el dni del operario sea como el id que le paso
            cur.execute(
                'SELECT * FROM rode.horario WHERE DniOperario LIKE "%'
                + id
                + '%"or Ubicacion LIKE "%'
                + id
                + '%";'
            )
            horarioid = cur.fetchall()
            # flash(mensajeExito)
        return render_template("verHorarios.html", horarios=horarioid)
    return redirect(url_for("verHorarios"))


@app.route("/verUsuarios")
def verUsr():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM rode.usuario")
    datausuario = cur.fetchall()
    return render_template("/verUsuarios.html", usuarios=datausuario)


@app.route("/buscarUsuarios", methods=["POST"])
def buscarusuario():
    if request.method == "POST":
        id = request.form["busqueda"]
        if id:
            cur = mysql.connection.cursor()
            cur.execute(
                'SELECT * FROM rode.usuario WHERE IdUsuario LIKE "%'
                + id
                + '%"or Usuario LIKE "%'
                + id
                + '%";'
            )
            datausuario = cur.fetchall()
            if datausuario:
                return render_template("/verUsuarios.html", usuarios=datausuario)
            else:
                mensajeError = (
                    "Error en la busqueda, no se escrbio ningun dato o no existen ningun dato con "
                    + id
                    + ". Se muestran todos los datos"
                )
                flash(mensajeError)
                return redirect(url_for("verUsr"))
        else:
            mensajeError = "Error en la busqueda, no se escrbio ningun dato"
            flash(mensajeError)
            return redirect(url_for("verUsr"))

    return redirect(url_for("verUsr"))

@app.route("/editarUsuario/<string:id>", methods=["POST"])
def editarUsuario(id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM rode.usuario WHERE idUsuario="+id+";")
        datausuario = cur.fetchall()
        #consigo solo unaa tupla con este siguiente codigo si no trae 2 items y uno  esta vacio
        datausuario=  datausuario[0]
        return render_template("/editarUsuario.html",usuario=datausuario)


@app.route("/borrarUsuario/<string:id>", methods=["POST"])
def borrarUsuario(id):
        cur = mysql.connection.cursor()
        olddniusr=id
        newIdUsuario=request.form['dni']
        newUsuario=request.form['nombreUsuario']
        newTipo=request.form.get('seleccionado')
        hash= bcrypt.generate_password_hash(id)
        data=(newIdUsuario,newUsuario,hash,newTipo,olddniusr)
        query=""" UPDATE rode.usuario
                SET IdUsuario = %s,
                    Usuario=%s,
                    contraseña= %s,
                    Tipo= %s
                WHERE idUsuario = %s """
        cur.execute(query,data)    
        mysql.connection.commit()  
        return redirect(url_for("verUsr"))
        

@app.route("/verOperariosPorObra")
def verOpeObra():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM obra;")
    dataObra = cur.fetchall()
    cur.execute("SELECT * FROM operario;")
    dataOper = cur.fetchall()
    return render_template("verOperariosPorObra.html", obra=dataObra, operario=dataOper)


@app.route("/buscarOperarioObra", methods=["POST"])
def buscarOpeObra():
    if request.method == "POST":
        indexObra = request.form.get("DropdownObra")
        if indexObra:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM obra;")
            dataObra = cur.fetchall()
            cur.execute("SELECT * FROM operario WHERE idObra=" + indexObra + ";")
            dataOpe = cur.fetchall()
            return render_template("verOperariosPorObra.html", obra=dataObra, operario=dataOpe)
        else:
            mensajeError = "Error en la seleccion de obra intentelo de nuevo"
            flash(mensajeError)
            return redirect(url_for("verOpeObra"))
    mensajeError = "Error en la seleccion de obra intentelo de nuevo, o recargue la pagina "
    flash(mensajeError)
    return redirect(url_for("verOpeObra"))

#este memtodo no esta siendo bien implementado no estaba en el alcance del prototipo pero estara implementado para la exposición si todo sale bien 
@app.route("/asistencia")
def asist():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario")
    datos = cur.fetchall()
    return render_template("asistencia.html", datos=datos)


@app.route("/CrearUsuario")
def CrearUsuario():
    return render_template("crearUsuario.html")


@app.route("/CrearRRHH")
def CrearRRHH():
    flash("Usuario creado exitosamente")
    return redirect(url_for("tcontrol"))


@app.route("/crearOperario")
def crearOperario():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario Where Tipo=3")
    # lleno la variable datos con  la informacion  de  usuarios que tengan como tipo 1
    datos = cur.fetchall()
    cur.execute("SELECT * FROM obra")
    obras = cur.fetchall()
    return render_template("crearOperario.html", datos=datos, obras=obras)


@app.route("/crearJO")
def crearJO():
    # creo el cursor para hacer el llamado a la base de datos y obtener el listado de  Jefes y jefas de obra
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario Where Tipo=2")
    datos = cur.fetchall()

    cur.execute("SELECT * FROM obra")
    obras = cur.fetchall()

    return render_template("crearJO.html", datos=datos, obras=obras)


@app.route("/crearObra")
def crearObra():
    # creo el cursor para hacer el llamado a la base de datos y obtener el listado de usuarios para ver  con que usuario puedo crear una obra
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jefejefaobra")
    datos = cur.fetchall()
    return render_template("crearObra.html", datos=datos)


@app.route("/metodoCrearUsuario", methods=["POST"])
def metCrearUsuario():

    if request.method == "POST":
        # pido todos los datos desde el formulario y los instancio para cargar la sentencia luego
        nombreUsuario = request.form["nombreUsuario"]
        dni = request.form["dni"]
        # hasheo el dni para almacenarlo en la base como contraseña luego el  usuario podria cambiarla
        contraseña = bcrypt.generate_password_hash(dni)
        tipoUsuario = request.form.get("seleccionado")
        # Conecto a mysql y instancio el cursor
        cur = mysql.connection.cursor()
        # Sentencia
        cur.execute(
            "INSERT INTO `usuario`(`IdUsuario`,`Contraseña`, `Usuario`,`tipo`) VALUES (%s,%s,%s,%s)",
            (dni, contraseña, nombreUsuario, tipoUsuario),
        )
        # cargo la sentencia con un commit
        mysql.connection.commit()

        # realizo la comprobacion para renderizar una diferente pantalla segun el tipo de usuario a crear
        if tipoUsuario == "1":
            # redirigo al usuario a la creacion del usuario que corresponda
            return redirect(url_for("tcontrol"))
        elif tipoUsuario == "2":
            return redirect(url_for("crearJO"))
        elif tipoUsuario == "3":
            return redirect(url_for("crearOperario"))
    # si algo sale mal se redirige a la pantalla de inicio
    return redirect(url_for("tcontrol"))

@app.route("/metodoEditarUsuario/<string:id>",  methods=["POST"])
def metEditarUsuario(id):
        
        cur = mysql.connection.cursor()
        olddniusr=id
        newIdUsuario=request.form['dni']
        newUsuario=request.form['nombreUsuario']
        newTipo=request.form.get('seleccionado')
        hash= bcrypt.generate_password_hash(id)
        data=(newIdUsuario,newUsuario,hash,newTipo,olddniusr)
        query=""" UPDATE rode.usuario
                SET IdUsuario = %s,
                    Usuario=%s,
                    contraseña= %s,
                    Tipo= %s
                WHERE idUsuario = %s """
        cur.execute(query,data)    
        mysql.connection.commit()  
        return redirect(url_for("verUsr"))

@app.route("/metodoCrearObra", methods=["POST"])
def crearobra():

    if request.method == "POST":
        # crear metodo cargar obra
        # pido  los datos desde el form para asignalo a variables temp para poder cargar la sentencia luego
        nombreObra = request.form["nombreObra"]
        ubicacion = request.form["ubicacion"]
        centroCosto = request.form["centroCosto"]
        encargado = request.form.get("seleccionado")
        sentencia = (nombreObra, ubicacion, centroCosto, encargado)
        # creo el cursor para realizar sentencias en la base de datos
        cur = mysql.connection.cursor()
        # Sentencia
        cur.execute(
            "INSERT INTO `rode`.`obra` (`NombreObra`,`Ubicacion`,`CentroCosto`,`idJefeJefaObra`) VALUES (%s,%s,%s,%s)",
            sentencia,
        )
        # cargo la sentencia con un commit
        mysql.connection.commit()

    return render_template("tableroControl.html")


@app.route("/metodoCrearRecursoHumano", methods=["POST"])
def crearRRHH():
    return redirect(url_for("tcontrol"))


@app.route("/metodoCrearJO", methods=["POST"])
def MetJO():
    if request.method == "POST":
        NombreJO = request.form["NombreJO"]
        ApellidoJO = request.form["ApellidoJO"]
        tel = request.form["Tel"]
        usuario = request.form.get("usr")
        seleccionado = "3"
        sentencia = (usuario, NombreJO, ApellidoJO, tel, seleccionado)
        # creo el cursor para realizar sentencias en la base de datos
        cur = mysql.connection.cursor()
        # Sentencia
        cur.execute(
            "INSERT INTO `rode`.`jefejefaobra` (`IdJefeJefaObra`,`Nombre`,`Apellido`,`Telefono`,`obra`) VALUES (%s,%s,%s,%s,%s)",
            sentencia,
        )
        # cargo la sentencia con un commit
        mysql.connection.commit()
    return redirect(url_for("tcontrol"))


@app.route("/metodoCrearOp", methods=["POST"])
def MetCrearOp():
    if request.method == "POST":
        NombreOP = request.form["NombreOpe"]
        ApellidoOp = request.form["ApellidoOpe"]
        TelefonoOp = request.form["TelOpe"]
        seleccionUsr = request.form.get("DropdownUsuario")
        seleccionObra = request.form.get("DropdownObra")
        sentencia = (seleccionUsr, NombreOP, ApellidoOp, TelefonoOp, seleccionObra)
    # creo el cursor para realizar sentencias en la base de datos
    cur = mysql.connection.cursor()
    # Sentencia
    cur.execute(
        "INSERT INTO `rode`.`operario` (`IdOperario`,`Nombre`,`Apellido`,`Telefono`,`IdObra`) VALUES (%s,%s,%s,%s,%s)",
        sentencia,
    )
    # cargo la sentencia con un commit
    mysql.connection.commit()
    return redirect(url_for("tcontrol"))


@app.route("/metodoCargarIngreso/<string:Id>")
def metodoCargarIngreso(Id):
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM rode.operario WHERE IdOperario=" + str(session["idusuario"])
    )
    usrData = cur.fetchall()
    usrData = usrData[0]
    #Cambio la variable local para que me muestre los dias en español
    locale.setlocale(locale.LC_TIME, "es_ES")
    #guardo el nombre del dia en la variable dia 
    dia = time.strftime("%A")
    dniOpe = session["idusuario"]
    # FALTA AGREGAR LA OBRA QUE TRAIGA DESDE DONDE ESTA MARCANDO O DESDE LOS DATOS DEL USUARIO MISMO
    location = usrData[4]
    tipo = "Ingreso"
    # tiempo actual
    tiempo = datetime.now()
    hora = tiempo.strftime("%H:%M:%S")
    # fecha en aaaa-mm-dd
    fecha = str(date.today())
    sentencia = (dia, hora, fecha, dniOpe, location, tipo)
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO `rode`.`horario` (`Dia`, `Hora`, `Fecha`, `DniOperario`, `Ubicacion`, `Tipo`) VALUES (%s,%s,%s,%s,%s,%s)",
        sentencia
    )
    mysql.connection.commit()
    return redirect(url_for("MHorario"))


@app.route("/metodoCargarSalida/<string:Id>")
def metodoCargarSalida(Id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM rode.operario WHERE IdOperario=" + str(session["idusuario"]))
    usrData = cur.fetchall()
    usrData = usrData[0]
    locale.setlocale(locale.LC_TIME, "es_ES")
    dia = time.strftime("%A")
    dniOpe = session["idusuario"]
    # FALTA AGREGAR LA OBRA QUE TRAIGA DESDE DONDE ESTA MARCANDO O DESDE LOS DATOS DEL USUARIO MISMO
    location = usrData[4]
    tipo = "Salida"
    # tiempo actual
    tiempo = datetime.now()
    hora = tiempo.strftime("%H:%M:%S")
    # fecha en aaaa-mm-dd
    fecha = str(date.today())
    sentencia = (dia, hora, fecha, dniOpe, location, tipo)
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO `rode`.`horario` (`Dia`, `Hora`, `Fecha`, `DniOperario`, `Ubicacion`, `Tipo`) VALUES (%s,%s,%s,%s,%s,%s)",
        sentencia,
    )
    mysql.connection.commit()

    return redirect(url_for("MHorario"))

@app.route("/metodoDescargarUsuarios")
def MetDescargarUsr():
    #creo las variables para asignarle un nombre unico al archivo que se cree
    fecha = str(date.today())
    tiempo = datetime.now()
    hora = tiempo.strftime(" %H-%M-%S")
    nombreArchivo="C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/"+fecha+hora+"Usuarios.csv"
    cur = mysql.connection.cursor()
    #guardo el archivo en el servidor
    cur.execute("""SELECT * FROM rode.usuario INTO OUTFILE '"""+nombreArchivo+""" ' FIELDS TERMINATED BY ','ENCLOSED BY '"' LINES TERMINATED BY '\n';""") 
    #se retorna el archivo como descarga y se redirecciona al tablero de control
    return send_file(nombreArchivo, attachment_filename=""+fecha+hora+' Usuarios.csv', as_attachment="true"), redirect(url_for("tcontrol"))

@app.route("/metodoDescargarHorarios")
def MetDescargarHorarios():
    #creo las variables para asignarle un nombre unico al archivo que se cree
    fecha = str(date.today())
    tiempo = datetime.now()
    hora = tiempo.strftime(" %H-%M-%S")
    #puede colapsar por espacio si se piden muchas descargas, pero los .csv son muy livianos, y no consideran una preocupacion a pequeña escala 
    nombreArchivo="C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/"+fecha+hora+"Horarios.csv"
    cur = mysql.connection.cursor()
    #guardo el archivo en el servidor
    cur.execute("""SELECT * FROM rode.Horario INTO OUTFILE '"""+nombreArchivo+""" ' FIELDS TERMINATED BY ','ENCLOSED BY '"' LINES TERMINATED BY '\n';""") 
    #se retorna el archivo como descarga y se redirecciona al tablero de control
    return send_file(nombreArchivo, attachment_filename=""+fecha+hora+' Horarios.csv', as_attachment="true"), redirect(url_for("tcontrol"))   

#seteo la aplicacion en debug para poder ver cambios en el codigo sin reiniciar
if __name__ == "__main__":
    app.run(debug=True)