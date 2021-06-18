from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL
from model_produtos import Produto, Inventario, InventarioTupla
from dao_produtos import ProdutoDAO, InventarioDAO
from functools import wraps
import jsons

app = Flask(__name__)
db = MySQL(app)
app.config.from_pyfile('db_config.py')
produto_dao = ProdutoDAO(db)
inventario_dao = InventarioDAO(db)
#=================================================== AUTENTICAÇÃO ================================ #

def login(f):
   @wraps(f)
   def decorated(*args, **kwargs):
      login = request.authorization
      if login and login.username == 'login' and login.password == 'senha':
         return f(*args, *kwargs)
      else:
         return make_response('Login ou senha incorreto!', 401, {'WWW-Authenticate' : 'Basic realm="Necessario Login"'})
   return decorated

#=================================================== ROTAS ======================================== #


@app.route('/')
@login
def index():
    return jsonify({'API': 'PRODUTOS'})

@app.route('/inventario/buscar/<int:id>')
def inv_buscar(id):
    if verifica_id_cliente(db, id) == None:
        return jsonify('id cliente invalido!')
    else:  
        inventario = filtrar_por_id(db, id)
        a_dict = jsons.dump(inventario)
        return jsonify(a_dict)

@app.route('/inventario/cadastrar', methods=['POST', ])
def inv_cadastrar():
   id_produto = request.json['id_produto']
   quantidade = request.json['quantidade']
   id_cliente = request.json['id_cliente']
   inventario = Inventario(id_produto, quantidade, id_cliente)
   inventario_dao.salvar(inventario)
   return inv_buscar(id_cliente)

@app.route('/produtos/listar')
def prod_listar():
   return jsonify(listar(db))

@app.route('/produtos/buscar/<int:id>')
def prod_buscar(id):
   if verifica_id_produto(db, id) == None:
      return jsonify('id produto invalido')
   else:
      return jsonify(buscar(db, id))

@app.route('/produtos/cadastrar', methods = ['POST', ])
def prod_cadastrar():
   nome = request.json['nome']
   descricao = request.json['descricao']
   preco = request.json['preco']
   contratacao = request.json['contratacao']
   produto = Produto(nome, descricao, preco, contratacao)
   produto_dao.salvar(produto)
   return jsonify('produto cadastrado com sucesso!')

@app.route('/produtos/alterar/<int:id>', methods =['PUT', ])
def prod_alterar(id):
    if verifica_id_produto(db, id) == None:
        return jsonify('id produto invalido')
    else:  
        nome = request.json['nome']
        descricao = request.json['descricao']
        preco = request.json['preco']
        contratacao = request.json['contratacao']
        produto = Produto(nome, descricao, preco, contratacao, id = id)
        produto_dao.alterar(produto, id)
        return jsonify('produto alterado com sucesso')

@app.route('/produtos/deletar/<int:id>', methods = ['DELETE', ])
def prod_deletar(id):
   if verifica_id_produto(db, id) == None:
      return jsonify('id produto invalido')
   else:
      return produto_dao.deletar(id)


#========================================MÉTODOS==============================================#


#LISTAR PRODUTOS
def listar(db):
        cursor = db.connection.cursor()
        cursor.execute('select id, nome, descricao, preco, contratacao from produtos')
        produtos = converte_produto(cursor.fetchall())
        return produtos


#BUSCAR PRODUTOS
def buscar(db, id):
    cursor = db.connection.cursor()
    cursor.execute('select id, nome, descricao, preco, contratacao from produtos where id =%s', (id, ))
    tupla = cursor.fetchone()
    return jsons.dump(Produto(id = tupla[0], nome = tupla[1], descricao = tupla[2], preco = tupla[3], contratacao = tupla[4]))

def converte_produto(produtos):
    def cria_produto_com_tupla(tupla):
        return jsons.dump(Produto(id = tupla[0], nome = tupla[1], descricao = tupla[2], preco = tupla[3], contratacao = tupla[4]))
    return list(map(cria_produto_com_tupla, produtos))

def verifica_id_cliente(db, id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id from clientes where id=%s', (id, ))
    id_cliente = cursor.fetchone()
    return id_cliente

def verifica_id_produto(db, id):
    cursor = db.connection.cursor()
    cursor.execute('SELECT id from produtos where id=%s', (id, ))
    id_cliente = cursor.fetchone()
    return id_cliente

#region INVENTARIO
def filtrar_por_id(db, id):
    cursor = db.connection.cursor()
    cursor.execute('select clientes.nome, clientes.id, produtos.nome, produtos.descricao, produtos.id,\
            inventario.quantidade from produtos inner join inventario on inventario.id_produto = produtos.id \
                inner join clientes_desafio1.clientes on clientes.id = inventario.id_cliente \
                    where clientes.id = %s', (id, ))
    inventario = cursor.fetchall()
    return converte_inventario(inventario)

def converte_inventario(inventarios):
    def cria_inventario_com_tupla(tupla):
        lista = InventarioTupla(nome = tupla[0], id_cliente= tupla[1], nome_produto=tupla[2], produto_desc=tupla[3], id_produto=tupla[4], quantidade=tupla[5])
        return lista
    return list(map(cria_inventario_com_tupla, inventarios))
#endregion

app.run(host='0.0.0.0')