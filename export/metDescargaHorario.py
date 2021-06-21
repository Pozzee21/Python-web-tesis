
def MetDescargarHorarios():
    q = 'select * from 9deC7T4LsG.horario'
    cur = mysql.connection.cursor()
    cur.execute(q)
    #Creo las variables para asignarle un nombre unico al archivo que se cree
    fecha = str(date.today())
    tiempo = datetime.now()
    hora = tiempo.strftime(" %H-%M-%S")
    nombreArchivo= fecha+hora+" Horarios.csv"
    #Creo la variable del path para descargar el archivo
    filepath = f'{here}/{nombreArchivo}'
    #creo el archivo
    pd.DataFrame(cur.fetchall()).to_csv(filepath, index=False)
    try:
        return send_file(filename_or_fp=filepath, as_attachment=True, attachment_filename=nombreArchivo)
    except:
        return "Algo salio mas vuelve atras"   