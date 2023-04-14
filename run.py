from flask import Flask, render_template, request

from config import config

app = Flask(__name__)

preguntas = [
    'SOF',
    '¿Cuál es la capital de Francia?',
    '¿Cuál es la capital de España?',
    '¿Cuál es la capital de Portugal?',
    '¿Cuá es la capital de Alemania?',
    ]

opciones = [
    ['Madrid', 'Lisboa', 'París', 'Berlín'],
    ['Madrid', 'Lisboa', 'París', 'Berlín'],
    ['Madrid', 'Lisboa', 'París', 'Berlín'],
    ['Madrid', 'Lisboa', 'París', 'Berlín'],
]

respuestas = [
    ['c', 'a', 'b', 'd']
]

user_aswer = []

key_values = ['a', 'b', 'c', 'd']


tot_preg = len(preguntas) - 1

print (f'Total preguntas = {tot_preg}')



# Diccionario para habilitar o desabilizar los botones de paginación
habilitado = {'prev': "", 
              'next': ""}

def estado_nav(page):

    print ('->estado_nav | page = {p} ')

    if page == 1:
       habilitado['prev'] = 'disabled'
       habilitado['next'] = ''
    else:
        habilitado['prev'] = ''
        habilitado['next'] = ''
    
    return habilitado

@app.route('/')
def index():
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
            pregunta = preguntas[page]
            dict_opciones = dict(zip(key_values, opciones[page-1]))         
        else: 
            return render_template('final_test.html')

        

    return render_template('siguiente.html', pregunta=pregunta, page=page, habilitado=habilitado, dict_opciones=dict_opciones)
    

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()