import flask
import mysql.connector

# Para instalar o flask digite no terminal do seu Sistema Operacional: pip install flask

app = flask.Flask(__name__, template_folder='templates', # Todos os arquivos HTML
                            static_folder='static',      # Todos os arquivos JS e CSS
                            static_url_path='')          # URL para acessar a pasta static, '' significa acessar pelo domínio direto

banco_de_dados = mysql.connector.connect(
    host="cadastro-teste.mysql.uhserver.com",
    user="alunos_impacta",
    password="Impacta@10",
    database="cadastro_teste"
)
cursor = banco_de_dados.cursor()

@app.route('/',methods=['GET'])
def home(): 
    return flask.render_template('home.html')

@app.route('/cadastrar',methods=['POST'])
def salvar_dados():
    info = flask.request.form.to_dict()

    rg = info['rg']
    p_nome = info['primeiro_nome']
    u_nome = info['ultimo_nome']
    telefone = info['telefone']
    email = info['email']
    comentarios = info['comentarios']

    if ((rg == "") | (p_nome == "") | (u_nome == "") | (telefone == "") | (email == "") | (comentarios == "")):
        return flask.render_template('home.html',status="Preencha todos os campos")
    
    sql_select = f'SELECT * FROM formulario1 WHERE rg = "{rg}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()
    if len(resultado) != 0:
        return flask.render_template('home.html',status=f"RG: {rg} já cadastrado")
    else:
        sql_insert = f'INSERT INTO formulario1 (email,rg,comentarios, primeiro_nome, telefone, ultimo_nome) VALUES ("{email}","{rg}","{comentarios}","{p_nome}",{telefone},"{u_nome}")'
        cursor.execute(sql_insert)
        banco_de_dados.commit()

    # try:
    #     sql_insert = f'INSERT INTO formulario1 (email,rg,comentarios, primeiro_nome, telefone, ultimo_nome) VALUES ("{email}","{rg}","{comentarios}","{p_nome}",{telefone},"{u_nome}")'
    #     cursor.execute(sql_insert)
    #     banco_de_dados.commit()
    # except mysql.connector.errors.IntegrityError:
    #     return flask.render_template('home.html',status=f"RG: {rg} já cadastrado")

    return flask.render_template('home.html',status=f"RG: {rg} cadastrado com sucesso")

@app.route('/consultar_rg',methods=['POST'])
def consultar_dados():
    
    info = flask.request.form.to_dict()
    rg_consulta = info['rg_consulta']

    if rg_consulta == '':
        return flask.render_template('home.html',status="Preencha todos os campos")

    if rg_consulta == '*':
        sql_select = f'SELECT rg,primeiro_nome,ultimo_nome,telefone,email,comentarios FROM formulario1' 
    else:
        sql_select = f'SELECT rg,primeiro_nome,ultimo_nome,telefone,email,comentarios FROM formulario1 WHERE rg = "{rg_consulta}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        if rg_consulta == '*':
            return flask.render_template('home.html',status=f'Nenhum RG cadastrado')
        else:
            return flask.render_template('home.html',status=f'RG: {rg_consulta} não encontrado')

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
    return flask.render_template('home.html',resultado=resultado_final)

@app.route('/consultar_email',methods=['POST'])
def consultar_email():
    
    info = flask.request.form.to_dict()
    email_consulta = info['email_consulta']

    if email_consulta == '':
        return flask.render_template('home.html',status="Preencha todos os campos")

    sql_select = f'SELECT rg,primeiro_nome,ultimo_nome,telefone,email,comentarios FROM formulario1 WHERE email = "{email_consulta}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        return flask.render_template('home.html',status=f'Email: {email_consulta} não encontrado')

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
    return flask.render_template('home.html',resultado=resultado_final)

@app.route('/alterar',methods=['POST'])
def alterar_dados():
    info = flask.request.form.to_dict()

    rg = info['rg_alt']
    p_nome = info['primeiro_nome_alt']
    u_nome = info['ultimo_nome_alt']
    telefone = info['telefone_alt']
    email = info['email_alt']
    comentarios = info['comentarios_alt']

    if (rg == ""):
        return flask.render_template('home.html',status="Preencha todos os campos")
    
    sql_select = f'SELECT * FROM formulario1 WHERE rg = "{rg}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        return flask.render_template('home.html',status="RG não cadastrado")
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
        return flask.render_template('home.html',status=f"RG: {rg} alterado com sucesso")

@app.route('/deletar',methods=['POST'])
def deletar_dados():
    info = flask.request.form.to_dict()
    rg = info['rg_del']

    if rg == '':
        return flask.render_template('home.html',status="Preencha todos os campos")
    
    if rg == '*':
        sql_delete = f'DELETE FROM formulario1'
        cursor.execute(sql_delete)
        banco_de_dados.commit()
        return flask.render_template('home.html',status=f"Todos os RGs foram deletados com sucesso")

    sql_select = f'SELECT * FROM formulario1 WHERE rg = "{rg}"' 
    cursor.execute(sql_select)
    resultado = cursor.fetchall()

    if len(resultado) == 0:
        return flask.render_template('home.html',status=f"RG: {rg} não cadastrado")
    else:
        sql_delete = f'DELETE FROM formulario1 WHERE rg = "{rg}"'
        cursor.execute(sql_delete)
        banco_de_dados.commit()
        return flask.render_template('home.html',status=f"RG: {rg} deletado sucesso")

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
    

    



