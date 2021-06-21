import os

import pandas as pd
from flask import Flask, send_file
from flask_mysqldb import MySQL

here = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
# Servidor MSQL Local-configuracion de conexiones de base de datos
app.config["MYSQL_HOST"] = "remotemysql.com"
app.config["MYSQL_USER"] = "9deC7T4LsG"
app.config["MYSQL_PASSWORD"] = "xhE0VledMn"
app.config["MYSQL_DB"] = "9deC7T4LsG"
app.config["CLIENT_CSV"] = here

# Variable para el cursor de la base de datos
mysql= MySQL(app)


@app.route('/export')
def export():
    q = 'select * from 9deC7T4LsG.horario'
    cur = mysql.connection.cursor()
    cur.execute(q)
    filename = 'usuarios.csv'
    filepath = f'{here}/{filename}'
    pd.DataFrame(cur.fetchall()).to_csv(filepath, index=False)
    return send_file(filename_or_fp=filepath, as_attachment=True, attachment_filename=filename)

app.run(host='0.0.0.0', debug=True, port=8888)
