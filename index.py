
from flask import Flask, render_template, request
from flask_mysqldb import MySQL
#importar url_For y redicect para enviar a otro template al usuario cuando se realice una accion 
app = Flask(__name__)
#servidor virtual gratuito
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_PASSWORD']='Rode7991'
app.config['MYSQL_DB']='rode'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('tableroControl.html')

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
    
@app.route('/CrearRRHH')  
def CrearRRHH( ):
    return render_template('crearRecursoHumano.html')

@app.route('/crearOperario')
def crearOperario():
     return render_template('crearOperario.html')

@app.route('/crearJO')
def crearJO():
     return render_template('crearJO.html')

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
            render_template('crearRecursoHumano.html')
        elif tipoUsuario=='2':
            render_template('crearOperario.html')     
        elif tipoUsuario=='3':
             render_template('crearJO.html')

     
        #Sentencia
        cur.execute("INSERT INTO `usuario`(`IdUsuario`,`Contraseña`, `Usuario`,`tipo`) VALUES (%s,%s,%s,%s)", (dni, 5465456, nombreUsuario, tipoUsuario))
       #cargo la sentencia con un commit
        mysql.connection.commit()

    return render_template('tableroControl.html')


@app.route('/CrearObra', methods=['POST'])
def crearobra():
    if request.method=='POST':
   #crear metodo cargar obra
     return render_template('tableroControl.html')



if __name__ == '__main__':
        app.run(debug=True)




