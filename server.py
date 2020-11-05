import flask
import mysql.connector
from flask_login import login_required,logout_user,LoginManager, login_user, current_user, UserMixin
import bcrypt
import datetime

# Para instalar o flask digite no terminal do seu Sistema Operacional: pip install flask

app = flask.Flask(__name__, template_folder='templates', # Todos os arquivos HTML
                            static_folder='static',      # Todos os arquivos JS e CSS
                            static_url_path='')          # URL para acessar a pasta static, '' significa acessar pelo domínio direto

login = LoginManager(app)
login.login_view = '/' # Redireciona o decorator @login_required para a pagina inicial
app.permanent_session_lifetime = datetime.timedelta(seconds=24*3600)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # No cache
app.config['SECRET_KEY'] = '323er0892-9u3410dfn1201208' # Senha de cript do cookie do navegador
senha_cript = b'$2b$08$0kvyLsB5utEvz7OQ5/m8F.' # Senha de cript do banco de dados

@login.user_loader
def user_loader(id):
    return User(id)

class User(UserMixin):
    def __init__(self, username):
        self.id = username

banco_de_dados = mysql.connector.connect(
    host="cadastro-teste.mysql.uhserver.com",
    user="alunos_impacta",
    password="Impacta@10",
    database="cadastro_teste"
)
cursor = banco_de_dados.cursor()

@app.route('/',methods=['GET','POST'])
def login_page(): 

    if flask.request.method == 'GET':

        if current_user.is_authenticated: # Verifica o cookie dentro do seu navegador
            user = current_user.id
            return flask.render_template('home.html',usuario=user)
        else:
            # Não está autenticado ou passou o tempo "permanent_session_lifetime"
            return flask.render_template('login.html')

    elif flask.request.method == 'POST':

        info = flask.request.form.to_dict()
        user = str(info['user'])
        password_login = str(info['pass'])

        if (user == '') | (password_login == ''):
            return flask.render_template('login.html',status_login="Preecha os campos de autenticação")

        # Verifica se o usuário está cadastrado
        sql_select = f'SELECT user,email,nome,pass FROM cadastro WHERE user = "{user}"'
        cursor.execute(sql_select)
        resultado = cursor.fetchall()
        if len(resultado) == 0:
            # Não está cadastrado
            return flask.render_template('login.html',status_login="Usuário não cadastrado")
        else:
            # Está cadastrado
            resultado = resultado[0] # Pegando a primeira linha 
            password_banco_de_dados_cript = resultado[3]
            
            password_login_cript = bcrypt.hashpw(password_login.encode('utf-8'),senha_cript).decode('utf-8')

            if password_banco_de_dados_cript == password_login_cript:
                login_user(User(user)) # Cria um cookie no navegador do usuário
                return flask.render_template('home.html',usuario=user)
            else:
                return flask.render_template('login.html',status_login="Senha incorreta")

@app.route('/cadastrar_usuario', methods=['POST'])
def cadastrar_usuario():

    info = flask.request.form.to_dict()

    user_cad = str(info['user_cad'])
    email_cad = str(info['email_cad'])
    nome_cad = str(info['nome_cad'])
    pass_cad1 = str(info['pass_cad1'])
    pass_cad2 = str(info['pass_cad2'])

    if ((user_cad == '') | (email_cad == '') | (nome_cad == '') | (pass_cad1 == '') | (pass_cad2 == '')):
        return flask.render_template('login.html',status_cadastro="Preecha todos os campos")

    if pass_cad1 != pass_cad2:
        return flask.render_template('login.html',status_cadastro="As senhas são diferentes")

    sql_select = f'SELECT user,email,nome,pass FROM cadastro WHERE user = "{user_cad}"'
    cursor.execute(sql_select)
    resultado = cursor.fetchall()
    if len(resultado) != 0:
        return flask.render_template('login.html',status_cadastro=f"O usuário {user_cad} já está cadastrado")

    sql_select = f'SELECT user,email,nome,pass FROM cadastro WHERE email = "{email_cad}"'
    cursor.execute(sql_select)
    resultado = cursor.fetchall()
    if len(resultado) != 0:
        return flask.render_template('login.html',status_cadastro=f"O email {email_cad} já está cadastrado")

    pass_cad1_cript = bcrypt.hashpw(pass_cad1.encode('utf-8'),senha_cript).decode('utf-8')

    sql_insert = f'INSERT INTO cadastro (user,email,nome,pass) VALUES ("{user_cad}","{email_cad}","{nome_cad}","{pass_cad1_cript}")'
    cursor.execute(sql_insert)
    banco_de_dados.commit()

    return flask.render_template('login.html',status_cadastro=f"Usuário {user_cad} cadastrado com sucesso")


@app.route("/logout",methods=['GET'])
@login_required
def logout():
    logout_user()
    return flask.render_template('login.html')
    
@app.route('/cadastrar',methods=['POST'])
@login_required
def salvar_dados():

    user = current_user.id

    info = flask.request.form.to_dict()

    rg = info['rg']
    p_nome = info['primeiro_nome']
    u_nome = info['ultimo_nome']
    telefone = info['telefone']
    email = info['email']
    comentarios = info['comentarios']

    if ((rg == "") | (p_nome == "") | (u_nome == "") | (telefone == "") | (email == "") | (comentarios == "")):
        return flask.render_template('home.html',status="Preencha todos os campos",usuario=user)
    
    sql_select = f'SELECT * FROM formulario1 WHERE rg = "{rg}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()
    if len(resultado) != 0:
        return flask.render_template('home.html',status=f"RG: {rg} já cadastrado",usuario=user)
    else:
        sql_insert = f'INSERT INTO formulario1 (email,rg,comentarios, primeiro_nome, telefone, ultimo_nome) VALUES ("{email}","{rg}","{comentarios}","{p_nome}",{telefone},"{u_nome}")'
        cursor.execute(sql_insert)
        banco_de_dados.commit()

    # try:
    #     sql_insert = f'INSERT INTO formulario1 (email,rg,comentarios, primeiro_nome, telefone, ultimo_nome) VALUES ("{email}","{rg}","{comentarios}","{p_nome}",{telefone},"{u_nome}")'
    #     cursor.execute(sql_insert)
    #     banco_de_dados.commit()
    # except mysql.connector.errors.IntegrityError:
    #     return flask.render_template('home.html',status=f"RG: {rg} já cadastrado",usuario=user)

    return flask.render_template('home.html',status=f"RG: {rg} cadastrado com sucesso",usuario=user)

@app.route('/consultar_rg',methods=['POST'])
@login_required
def consultar_dados():
    
    user = current_user.id

    info = flask.request.form.to_dict()
    rg_consulta = info['rg_consulta']

    if rg_consulta == '':
        return flask.render_template('home.html',status="Preencha todos os campos",usuario=user)

    if rg_consulta == '*':
        sql_select = f'SELECT rg,primeiro_nome,ultimo_nome,telefone,email,comentarios FROM formulario1' 
    else:
        sql_select = f'SELECT rg,primeiro_nome,ultimo_nome,telefone,email,comentarios FROM formulario1 WHERE rg = "{rg_consulta}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        if rg_consulta == '*':
            return flask.render_template('home.html',status=f'Nenhum RG cadastrado',usuario=user)
        else:
            return flask.render_template('home.html',status=f'RG: {rg_consulta} não encontrado',usuario=user)

    # Função ZIP():
    # lista1 = [1,2,3,4]
    # lista2 = ['a','b','c','d']
    # list(zip(lista1,lista2)) é [[1,'a'],[2,'b'],[3,'c'],[4,'d']]

    campos = ['RG','Primeiro nome','Ultimo nome','Telefone','E-mail','Comentários']
    resultado_final = []
    for i in resultado:
        resultado_final.append(list(zip(campos,i)))

    # Transformamos 
    # [('123', 'carlos', 'silva', 9876, 'kevin.zezel@hotmail.com', 'ok'),
    # ('123456', 'kevin', 'zezel', 123456, 'kevin.zezel@hotmail.com', 'ok')]
    # em
    # [[('RG', '123'), ('Primeiro nome', 'carlos'), ('Ultimo nome', 'silva'), ('Telefone', 9876), ('E-mail', 'kevin.zezel@hotmail.com'), ('Comentários', 'ok')], 
    # [('RG', '123456'), ('Primeiro nome', 'kevin'), ('Ultimo nome', 'zezel'), ('Telefone', 123456), ('E-mail', 'kevin.zezel@hotmail.com'), ('Comentários', 'ok')]]

    # return flask.render_template('bloco_resultado.html',resultado=resultado_final,usuario=user)
    return flask.render_template('home.html',resultado=resultado_final,usuario=user)

@app.route('/consultar_email',methods=['POST'])
@login_required
def consultar_email():
    
    user = current_user.id

    info = flask.request.form.to_dict()
    email_consulta = info['email_consulta']

    if email_consulta == '':
        return flask.render_template('home.html',status="Preencha todos os campos",usuario=user)

    sql_select = f'SELECT rg,primeiro_nome,ultimo_nome,telefone,email,comentarios FROM formulario1 WHERE email = "{email_consulta}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        return flask.render_template('home.html',status=f'Email: {email_consulta} não encontrado',usuario=user)

    # Função ZIP():
    # lista1 = [1,2,3,4]
    # lista2 = ['a','b','c','d']
    # list(zip(lista1,lista2)) é [[1,'a'],[2,'b'],[3,'c'],[4,'d']]

    campos = ['RG','Primeiro nome','Ultimo nome','Telefone','E-mail','Comentários']
    resultado_final = []
    for i in resultado:
        resultado_final.append(list(zip(campos,i)))

    # Transformamos 
    # [('123', 'carlos', 'silva', 9876, 'kevin.zezel@hotmail.com', 'ok'),
    # ('123456', 'kevin', 'zezel', 123456, 'kevin.zezel@hotmail.com', 'ok')]
    # em
    # [[('RG', '123'), ('Primeiro nome', 'carlos'), ('Ultimo nome', 'silva'), ('Telefone', 9876), ('E-mail', 'kevin.zezel@hotmail.com'), ('Comentários', 'ok')], 
    # [('RG', '123456'), ('Primeiro nome', 'kevin'), ('Ultimo nome', 'zezel'), ('Telefone', 123456), ('E-mail', 'kevin.zezel@hotmail.com'), ('Comentários', 'ok')]]

    # return flask.render_template('bloco_resultado.html',resultado=resultado_final)
    return flask.render_template('home.html',resultado=resultado_final,usuario=user)

@app.route('/alterar',methods=['POST'])
@login_required
def alterar_dados():

    user = current_user.id

    info = flask.request.form.to_dict()

    rg = info['rg_alt']
    p_nome = info['primeiro_nome_alt']
    u_nome = info['ultimo_nome_alt']
    telefone = info['telefone_alt']
    email = info['email_alt']
    comentarios = info['comentarios_alt']

    if (rg == ""):
        return flask.render_template('home.html',status="Preencha todos os campos",usuario=user)
    
    sql_select = f'SELECT * FROM formulario1 WHERE rg = "{rg}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        return flask.render_template('home.html',status="RG não cadastrado",usuario=user)
    else:
        
        # Não altera se tiver vazio
        campos = ['primeiro_nome','ultimo_nome','telefone','email','comentarios']
        dados = [p_nome,u_nome,telefone,email,comentarios]

        sql_update = 'UPDATE formulario1 SET '
        for idx,valor in enumerate(dados):
            if valor != '':
                if campos[idx] == 'telefone':
                    sql_update = sql_update + f'{campos[idx]} = {valor},'
                else:
                    sql_update = sql_update + f'{campos[idx]} = "{valor}",'

        sql_update = sql_update[:-1]        
        sql_update = sql_update + f' WHERE rg = "{rg}"'

        # Altera tudo
        # sql_update = f"""
        #         UPDATE formulario1 SET email = "{email}", comentarios = "{comentarios}", 
        #         primeiro_nome = "{p_nome}",  ultimo_nome = "{u_nome}", 
        #         telefone = {telefone} WHERE rg = "{rg}"
        # """ 
        cursor.execute(sql_update)
        banco_de_dados.commit()
        return flask.render_template('home.html',status=f"RG: {rg} alterado com sucesso",usuario=user)

@app.route('/deletar',methods=['POST'])
@login_required
def deletar_dados():

    user = current_user.id

    info = flask.request.form.to_dict()
    rg = info['rg_del']

    if rg == '':
        return flask.render_template('home.html',status="Preencha todos os campos",usuario=user)
    
    if rg == '*':
        sql_delete = f'DELETE FROM formulario1'
        cursor.execute(sql_delete)
        banco_de_dados.commit()
        return flask.render_template('home.html',status=f"Todos os RGs foram deletados com sucesso",usuario=user)

    sql_select = f'SELECT * FROM formulario1 WHERE rg = "{rg}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        return flask.render_template('home.html',status=f"RG: {rg} não cadastrado",usuario=user)
    else:
        sql_delete = f'DELETE FROM formulario1 WHERE rg = "{rg}"'
        cursor.execute(sql_delete)
        banco_de_dados.commit()
        return flask.render_template('home.html',status=f"RG: {rg} deletado sucesso",usuario=user)

if __name__ == "__main__":
    # localhost = 127.0.0.1
    # Porta 80: HTTP
    # Porta 443: HTTPS

    # Acesso somente pelo seu PC
    app.run(host="localhost",port=9999)

    # Acesso somente pela sua INTRAnet
    # app.run(host="localhost",port=9999)

    # Acesso externo 
    # Liberar antivirus (desativar o firewall)
    # Redirecionar a porta 9999 ou qualquer outra porta do seu roteador para o IP que está rodando o flask
    # app.run(host="0.0.0.0",port=9999)
    

    



