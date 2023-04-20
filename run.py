from flask import Flask, render_template, request
import random
import sqlite3

from config import config

app = Flask(__name__)


# Guarda las preguntas y opcione de la base de datos
preguntas = []
opciones = []
respuestas = []


user_aswer = []

key_values = ['a', 'b', 'c', 'd']


tot_preg = len(preguntas)

print (f'Total preguntas = {tot_preg}')

# Diccionario para habilitar o desabilizar los botones de paginación
habilitado = {'prev': "", 
              'next': ""}


def estado_nav(page):  

    if page == 1:
       habilitado['prev'] = 'disabled'
       habilitado['next'] = ''
    else:
        habilitado['prev'] = ''
        habilitado['next'] = ''
    
    return habilitado

def generar_num_aleatorio():
    return random.sample(range(10), 5)
    

def obtener_preguntas_bbdd(mums_pregs):
    #Conectamos con la base de datos. 
    connection = sqlite3.connect('preguntas.db')

    #create cursor to manage bd
    cursor = connection.cursor()

    #  Base de datos de preguntas. 
    cursor.execute("select * from preguntas where num_preg in (5, 8, 3)")   


    preguntas_all = cursor.fetchall()

    connection.close()

    return preguntas_all


@app.route('/')
def index():

   mums_pregs = generar_num_aleatorio()
   
   preguntas_bbdd = obtener_preguntas_bbdd(mums_pregs)

   print (preguntas_bbdd)

   return render_template('index.html')


@app.route('/siguiente', methods=['GET', 'POST'])
def siguiente():

    if request.method == 'POST':        
        page = int (request.form['page'])

        

        print (f'/siguiente | page = {page}')

        # Si vengo de index (st)
        if 'start_game' in request.form or 'siguiente'  in request.form:
            page      = page + 1        
        elif 'anterior' in request.form:            
            page = page - 1

        habilitado = estado_nav(page)

        # Guardo la opción dada por el usuario: 
        if 'opcion' in request.form:
            opc = request.form['opcion']           
            user_aswer.insert(page, opc)
        
        
        
        if page <= tot_preg:
            pregunta = preguntas[page-1]
            dict_opciones = dict(zip(key_values, opciones[page-1]))         
        else: 
            return render_template('final_test.html', preguntas=preguntas, opciones=opciones, n_pregunta=0)

        

    return render_template('siguiente.html', pregunta=pregunta, page=page, habilitado=habilitado, dict_opciones=dict_opciones)
    

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()