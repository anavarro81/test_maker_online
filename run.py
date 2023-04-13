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

tot_preg = len(preguntas) - 1

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

@app.route('/')
def index():
    return render_template('index.html', page=0)


@app.route('/siguiente', methods=['GET', 'POST'])
def siguiente():

    page = int (request.args.get('page')) 
    habilitado = estado_nav(page)

    if page <= tot_preg:
        pregunta = preguntas[page]        
    else: 
        return render_template('final_test.html')

    return render_template('siguiente.html', pregunta=pregunta, page=page, habilitado=habilitado)
    
@app.route('/anterior', methods=['GET', 'POST'])
def anterior():

    page = int (request.args.get('page'))       
    pregunta = preguntas[page]
    habilitado = estado_nav(page)

    return render_template('siguiente.html', pregunta=pregunta, page=page, habilitado=habilitado)


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()