from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    connection = sqlite3.connect('novo_escola.db') 
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            disciplina TEXT
        )
    ''')
    connection.commit()
    connection.close()

@app.route('/professores', methods=['GET', 'POST']) #LEMBRANDO QUE TEMOS DOIS TIPOS DE METODOS DE ENVIO DE INFORMAÇÕES
# EM HTML, O GET E O POST
def professores():
    connection = sqlite3.connect('novo_escola.db') #CONEXÃO COM O SQL - USE SEMPRE O MESMO DATABASE
    cursor = connection.cursor()

    if request.method == 'POST':
        # AQUI ELE MANDA VIA POST O NOME E A DISCIPLINA DO PROFESSOR
        nome = request.form['nome']
        disciplina = request.form['disciplina']
        
        # AQUI FAZ A INSERÇÃO DAS INFORMAÇÕES 
        cursor.execute("INSERT INTO Professores (nome, disciplina) VALUES (?, ?)", (nome, disciplina))
        connection.commit()

        # AQUI ELE FAZ UM RETURN -> VOLTA PARA A MESMA PÁGINA PROFESSORES.HTML DEPOIS DE INSERIR NOVOS PROFESSORES
        return redirect(url_for('professores'))

    # FAZ A BUSCA COM O SELECT * FROM. LEMBREM QUE QUANDO UTILIZAMOS O * SIGNIFICA QUE IRÁ PUXAR TODAS
    # AS COLUNAS DA MINHA TABELA, SE EU QUERO ALGUMA COLUNA EM ESPECIFICO, USO O NOME DA COLUNA
    # NO LUGAR DO *
    cursor.execute("SELECT * FROM Professores")
    professores = cursor.fetchall()
    connection.close()

   # AQUI VEM O HTML COM O CSS INTEGRADO
    html_code = '''
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Professores do Colégio Estadual Protásio de Carvalho</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; }
            table { width: 50%; margin: auto; border-collapse: collapse; }
            th, td { padding: 8px 12px; border: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
            form { margin: 20px auto; width: 300px; text-align: left; }
            input[type="text"] { width: 100%; padding: 8px; margin: 5px 0; }
            input[type="submit"] { padding: 8px 12px; background-color: #4CAF50; color: white; border: none; }
        </style>
    </head>
    <body>
        <h2>Formulário: Adicionar Professor</h2>
        <form method="POST">
            <label for="nome">Nome:</label><br>
            <input type="text" id="nome" name="nome" required><br>
            <label for="disciplina">Disciplina:</label><br>
            <input type="text" id="disciplina" name="disciplina" required><br><br>
            <input type="submit" value="Adicionar Professor">
        </form>

        <h2>Lista de Professores</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Disciplina</th>
                </tr>
            </thead>
            <tbody>
                {% for professor in professores %}
                <tr>
                    <td>{{ professor[0] }}</td>
                    <td>{{ professor[1] }}</td>
                    <td>{{ professor[2] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    '''
    return render_template_string(html_code, professores=professores)

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
