from flask import jsonify

class ProdutoDAO:
    def __init__(self, db):
        self.__db = db

    def salvar(self, produto):
        cursor = self.__db.connection.cursor()
        cursor.execute('insert into produtos (nome, descricao, preco, contratacao) values (%s, %s, %s, %s)', (produto.nome, produto.descricao, produto.preco, produto.contratacao))
        return produto

    def alterar(self, produto, id):
        cursor = self.__db.connection.cursor()
        cursor.execute('update produtos set nome=%s, descricao=%s, preco=%s, contratacao=%s where id = %s', (produto.nome, produto.descricao, produto.preco, produto.contratacao, id))
        return produto

    def deletar(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute('delete from produtos where id = %s', (id, ))
        return jsonify('produto deletado com sucesso!')

class InventarioDAO:
    def __init__(self, db):
        self.__db = db

    def salvar(self, inventario):
        cursor = self.__db.connection.cursor()
        cursor.execute('insert into clientes_desafio1.inventario (id_produto, quantidade, id_cliente) values (%s, %s, %s)', (inventario.id_produto, inventario.quantidade, inventario.id_cliente))
        return inventario


