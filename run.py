from flask import Flask, render_template, request

from config import config

app = Flask(__name__)

preguntas = [
    '¿Cuál es la capital de Francia?',
    '¿Cuál es la capital de España?',
    '¿Cuál es la capital de Portugal?',
    '¿Cuá es la capital de Alemania?'
    ]

# Diccionario para habilitar o desabilizar los botones de paginación
habilitado = {'prev': "", 
              'next': ""}

def estado_nav(page):

    print ('== estado_nav ')
    print (f'page = {page}')
    
    if page == 0:
        habilitado['prev'] = "disabled"
        habilitado['next'] = ""
    elif page == len(preguntas):
        habilitado['prev'] = ""
        habilitado['next'] = "disabled"
    else:
        habilitado['prev'] = ""
        habilitado['next'] = ""
    
    return habilitado

@app.route('/')
def index():
    return render_template('index.html', page=0)


@app.route('/siguiente', methods=['GET', 'POST'])
def siguiente():



    page = int (request.args.get('page')) 

    habilitado = estado_nav(page)
    
    if page < len(preguntas):   
        pregunta = preguntas[page]
        page += 1
    else: 
        pregunta = 'No hay mas preguntas'

    return render_template('siguiente.html', pregunta=pregunta, page=page, habilitado=habilitado)
    
@app.route('/anterior', methods=['GET', 'POST'])
def anterior():

    page = int (request.args.get('page'))

    print (f'anterior | page (antes)= {page}')

    habilitado = estado_nav(page)    

    if page > 0:
        page -= 1
        pregunta = preguntas[page]        
    else: 
        pregunta = 'Esta en la primera pregunta'

    habilitado = estado_nav(page)

    print (f'anterior | page (despues)= {page}') 

    return render_template('siguiente.html', pregunta=pregunta, page=page, habilitado=habilitado)


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()