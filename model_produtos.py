class Produto:
    def __init__(self, nome, descricao, preco, contratacao, id=None):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.contratacao = contratacao
        self.id = id

class InventarioTupla:
    def __init__(self, nome, id_cliente, nome_produto, produto_desc, id_produto, quantidade):
        self.nome = nome
        self.id_cliente = id_cliente
        self.nome_produto = nome_produto
        self.produto_desc = produto_desc
        self.id_produto = id_produto
        self.quantidade = quantidade

class Inventario:
    def __init__(self, id_produto, quantidade, id_cliente):
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.id_cliente = id_cliente