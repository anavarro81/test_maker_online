from flask import Flask, render_template, request, redirect
import random
import sqlite3

from config import config

app = Flask(__name__)


# Guarda las preguntas y opcione de la base de datos
preguntas = []
# opciones = [ 
# ['Madrid', 'Barcelona', 'Lisboa', 'Berlin'],
# ['Madrid', 'Barcelona', 'Lisboa', 'Berlin'],
# ['Madrid', 'Barcelona', 'Lisboa', 'Berlin'],
# ['Madrid', 'Barcelona', 'Lisboa', 'Berlin'],
# ['Madrid', 'Barcelona', 'Lisboa', 'Berlin']
# ]
opciones = []
respuestas = []


user_aswer = []

key_values = ['a', 'b', 'c', 'd']
tot_preg = 5

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
    return random.sample(range(1,11), 5)
    

def obtener_preguntas_bbdd(mums_pregs):
    #Conectamos con la base de datos. 
    connection = sqlite3.connect('preguntas.db')

    #create cursor to manage bd
    cursor = connection.cursor()

    #  Base de datos de preguntas. 
    #  Selecciono por num_pregu (num= 1...) las generadas aleatoriamente. 
    cursor.execute("select * from preguntas where num_preg in (?, ?, ?, ?, ?)", (mums_pregs))  
    
    selec_prgts = cursor.fetchall()

    for pregunta in selec_prgts:

        #-> Agrego la pregunta de la BBDD a la lista de trabajo.
        preguntas.append(pregunta[1])       
        opciones.append(pregunta[2].split(';'))
        respuestas.append(pregunta[3].split(';'))

    connection.close()

@app.route('/')
def index():

   mums_pregs = generar_num_aleatorio()
   obtener_preguntas_bbdd(mums_pregs)


   return render_template('index.html')


@app.route('/siguiente', methods=['GET', 'POST'])
def siguiente():

    if request.method == 'POST':        
        page = int (request.form['page'])       

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
            print (f'--> Entro por corregir el test')
            rsptas_st = corregir_test()
            return render_template('final_test.html', preguntas=preguntas, opciones=opciones, rsptas_st=rsptas_st, user_aswer=user_aswer)               
            
        
        

    return render_template('siguiente.html', pregunta=pregunta, page=page, habilitado=habilitado, dict_opciones=dict_opciones, tot_preg=tot_preg)
    
def corregir_test():
    
    
    idx_rspta = 0
    score = 0
    rsptas_st = {}

    for respuesta in respuestas:        
        if respuesta[0][0] == user_aswer[idx_rspta][0]:
            score += 1
            rsptas_st[idx_rspta] = 1
        else:
            rsptas_st[idx_rspta] = 0

        idx_rspta += 1

    print (f'Diccionario respuestas = {rsptas_st}')
    return rsptas_st

    

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()