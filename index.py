
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
#importar url_For y redicect para enviar a otro template al usuario cuando se realice una accion 
app = Flask(__name__)
#servidor virtual gratuito
app.config['MYSQL_USER']= 'sql10371101'
app.config['MYSQL_HOST']='sql10.freemysqlhosting.net'
app.config['MYSQL_PASSWORD']='QciftIsB3J'
app.config['MYSQL_DB']= 'sql10371101'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('CrearUsuario.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route("/login")
def login():
        return render_template('login.html')

@app.route('/tableroControl')
def tcontrol():
        return render_template('tableroControl.html')

@app.route('/asistencia')
def asist():
    return render_template('asistencia.html')

@app.route('/CrearUsuario')
def CrearUsuario():
    return render_template('crearUsuario.html')

@app.route('/crearOperario')
def crearOperario():
     return render_template('/CrearOperario.html')

@app.route('/metodoCrearUsuario', methods=['POST'])
def metCrearUsuario():

    if request.method == 'POST':
        #pido todos los daots desde el formulario y los instancio para cargar la sentencia luego

        nombreUsuario = request.form ['nombreUsuario']
        dni = request.form['dni']
        tipoUsuario = request.form.get('seleccionado')
   #Conecto a mysql y instancio el cursor
        cur = mysql.connection.cursor()
        #realizo la comprobacion para renderizar una diferente pantalla segun el tipo de usuario a crear
        if tipoUsuario=='1':
          render_template('crearOpeario.html')
        elif tipoUsuario=='2':
            print('rrhh')         
        elif tipoUsuario=='3':
            print('ope')

     
        #Sentencia
        cur.execute("INSERT INTO `usuario`(`IdUsuario`,`Contraseña`, `Usuario`,`tipo`) VALUES (%s,%s,%s,%s)", (dni, nombreUsuario, 2132123,tipoUsuario))
       #cargo la sentencia con un commit
        mysql.connection.commit()

    return render_template('tableroControl.html')


@app.route('/CrearObra', methods=['POST'])
def crearobra():
    if request.method== 'POST':
   #crear metodo cargar obra

            return render_template('tableroControl.html')



if __name__ == '__main__':
        app.run(debug=True)




