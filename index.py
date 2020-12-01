from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL

# importar url_For y redicect para enviar a otro template al usuario cuando se realice una accion
app = Flask(__name__)
# servidor Local Gratuito  configuracion de conexiones de base de datos
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_PASSWORD"] = "Rode7991"
app.config["MYSQL_DB"] = "rode"

mysql = MySQL(app)


@app.route("/")
def home():

    return render_template("tableroControl.html")


@app.route("/about")
def about():

    return render_template("about.html")


@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/tableroControl")
def tcontrol():
    return render_template("tableroControl.html")
    
#poner en el metodo que  espera un parametro para utilizarlo en la busqueda de horarios solo del operario que esta por marcar asistencia
@app.route("/MarcarHorario")
def MHorario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM horario')
    horarios=cur.fetchall()
    return render_template("marcarHorario.html",horarios=horarios)

@app.route("/asistencia")
def asist():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario')
    datos= cur.fetchall()

    return render_template("asistencia.html", datos=datos)


@app.route("/CrearUsuario")
def CrearUsuario():
    return render_template("crearUsuario.html")


@app.route("/CrearRRHH")
def CrearRRHH():
    #creo el cursor para hacer el llamado a la base de datos y obtener el listado de  usuarios para crear ese usr
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario Where Tipo=1')
    #lleno la variable datos con  la informacion  de  usuarios que tengan como tipo 1 
    datos= cur.fetchall()       
    return render_template("crearRecursoHumano.html", datos=datos)


@app.route("/crearOperario")
def crearOperario():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario Where Tipo=3')
    #lleno la variable datos con  la informacion  de  usuarios que tengan como tipo 1 
    datos= cur.fetchall() 
    cur.execute('SELECT * FROM obra')
    obras=cur.fetchall()
    return render_template("crearOperario.html",datos=datos,obras=obras)


@app.route("/crearJO")
def crearJO():
    #creo el cursor para hacer el llamado a la base de datos y obtener el listado de  Jefes y jefas de obra
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario Where Tipo=2')
    datos= cur.fetchall()

    cur.execute('SELECT * FROM obra')
    obras=cur.fetchall()

    return render_template("crearJO.html",datos=datos,obras=obras)

@app.route("/crearObra")
def crearObra():
    #creo el cursor para hacer el llamado a la base de datos y obtener el listado de usuarios para ver  con que usuario puedo crear una obra
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM jefejefaobra')
    datos= cur.fetchall()
    return render_template("crearObra.html",datos=datos)

@app.route("/metodoCrearUsuario", methods=["POST"])
def metCrearUsuario():

    if request.method == "POST":
        # pido todos los datos desde el formulario y los instancio para cargar la sentencia luego
        nombreUsuario = request.form["nombreUsuario"]
        #hacer la contraseña para que se cree mediante el dni
        dni = request.form["dni"]
        contraseña=dni
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
            #redirigo al usuario a la creacion del usuario que corresponda
           return redirect(url_for("tcontrol"))
        elif tipoUsuario == "2":
            return redirect(url_for("crearJO"))
        elif tipoUsuario == "3":
            return redirect(url_for("crearOperario"))

#si algo sale mal se redirige a la pantalla de inicio
    return redirect(url_for("tcontrol"))


@app.route("/metodoCrearObra", methods=["POST"])
def crearobra():
    
    if request.method == "POST":
        # crear metodo cargar obra
        #pido  los datos desde el form para asignalo a variables temp para poder cargar la sentencia luego
        nombreObra = request.form["nombreObra"]
        ubicacion = request.form["ubicacion"]
        centroCosto = request.form["centroCosto"]
        encargado = request.form.get("seleccionado")
        sentencia = (nombreObra,ubicacion,centroCosto,encargado)
        #creo el cursor para realizar sentencias en la base de datos
        cur = mysql.connection.cursor()
        # Sentencia
        cur.execute(
           "INSERT INTO `rode`.`obra` (`NombreObra`,`Ubicacion`,`CentroCosto`,`idJefeJefaObra`) VALUES (%s,%s,%s,%s)", sentencia)
        # cargo la sentencia con un commit
        mysql.connection.commit()

    return render_template("tableroControl.html")

@app.route("/metodoCrearRecursoHumano", methods=["POST"])
def crearRRHH():
    return redirect(url_for("tcontrol"))

@app.route("/metodoCrearJO", methods=["POST"])
def MetJO():
    if request.method=='POST':
        NombreJO = request.form["NombreJO"]
        ApellidoJO = request.form["ApellidoJO"]
        tel = request.form["Tel"]
        usuario = request.form.get("usr")
        seleccionado= "3"
        sentencia = (usuario, NombreJO, ApellidoJO, tel,seleccionado )
        print(sentencia)
        #creo el cursor para realizar sentencias en la base de datos
        cur = mysql.connection.cursor()
        # Sentencia
        cur.execute( "INSERT INTO `rode`.`jefejefaobra` (`IdJefeJefaObra`,`Nombre`,`Apellido`,`Telefono`,`obra`) VALUES (%s,%s,%s,%s,%s)", sentencia )
        # cargo la sentencia con un commit
        mysql.connection.commit()
    return redirect(url_for("tcontrol"))

@app.route("/metodoCrearOp",methods=["POST"])
def MetCrearOp():
    if request.method=="POST":
        NombreOP= request.form['NombreOpe']
        ApellidoOp=request.form['ApellidoOpe']
        TelefonoOp=request.form['TelOpe']
        seleccionUsr= request.form.get("DropdownUsuario")
        seleccionObra=request.form.get("DropdownObra")
        sentencia=(seleccionUsr,NombreOP,ApellidoOp,TelefonoOp,seleccionObra)
        print(sentencia)
    #creo el cursor para realizar sentencias en la base de datos
    cur = mysql.connection.cursor()
    # Sentencia
    cur.execute( "INSERT INTO `rode`.`operario` (`IdOperario`,`Nombre`,`Apellido`,`Telefono`,`IdObra`) VALUES (%s,%s,%s,%s,%s)", sentencia )
    # cargo la sentencia con un commit
    mysql.connection.commit()
    return redirect(url_for(tcontrol))


if __name__ == "__main__":
    app.run(debug=True)
