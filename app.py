from flask import Flask, render_template, request, redirect

app = Flask(__name__)

tarefas = []

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html',
                            tarefas=tarefas)


@app.route('/adicionar_tarefa', methods=['POST'])
def adicionar_tarefa():
    nova_tarefa = request.form['tarefa']
    tarefas.append(nova_tarefa)  # Adiciona a tarefa na lista
    return redirect('/home')



if __name__ == '__main__':
    app.run(debug=True)