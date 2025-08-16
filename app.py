from flask import Flask, render_template, request, redirect
from database import db
from models import Usuario

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db.init_app(app)

tarefas = []

@app.route('/')
def login():
    return render_template('login.html', body_class='login-page')

@app.route('/home')
def home():
    return render_template('home.html',
                            tarefas=tarefas, body_class='home-page')


@app.route('/adicionar_tarefa', methods=['POST'])
def adicionar_tarefa():
    nova_tarefa = request.form['tarefa']
    tarefas.append(nova_tarefa)  # Adiciona a tarefa na lista
    return redirect('/home')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'GET':
        return render_template('cadastrar.html', body_class='cadastrar-page')
    elif request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmar_senha')

        if senha != confirmar_senha:
            return "Erro: senhas diferentes!"

        try:
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()
            # Redireciona para a rota do login (com body_class correto lá)
            return redirect('/')
        except Exception as e:
            return f"Erro ao cadastrar: {e}"


@app.route('/deletar_tarefa/<int:index>', methods=['POST'])
def deletar_tarefa(index):
    if 0 <= index < len(tarefas):  # garante que o índice existe
        tarefas.pop(index)         # remove a tarefa
    return redirect('/home')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
