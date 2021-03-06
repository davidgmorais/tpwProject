# TPW Project

Projeto criado no âmbito da cadeira de Tecnologias e Programação Web que consiste numa loja de compra e venda de itens gerido por um user admin.
Servidor: Django
Cliente: AngularJS

## Funcionalidades
**Utilizador anónimo:**
- Listagem de todos os produtos disponiveis (com paginação)
- Procurar produtos
- Listagem de produtos por categoria, promoções e novidades (com paginação) 
- Ordenação e filtragem de produtos
- Login e registo
- Além dos cards nos levarem aos itens, têm a categoria que nos leva para a página da catergoria

**Utilizador com conta:**
- todas as funcionalidades do utilizador anónimo
- comprar produtos (adicionando ao carrinho)
	-> usar icone de carrinho para ver o cart em qualquer página
- propor venda de produtos
- descontar dinheiro acumulado
- gestão de conta
	- eliminar conta
- criar, editar e eliminar comentários em items

**Utilizador Admin**
- todas as funcionalidades do utilizador com conta
- criar, editar e eliminar itens
	- Com uma secção para só adicionar mais quantidade (out of order, acedida através do dashboard)
- criar, editar e eliminar categorias e subcategorias
- aceitar ou negar propostas de vendas
- estatisticas do negócio

**Nota:** Todos os items aparecem a NEW porque foram adicionados através da interface que criamos para o admin, após 2 semanas ficavam sem essa 'propriedade'

## Contas
Conta admin
- username: admin
- password: djangoPass

**Conta cliente**
- username: example1
- password: djangoPass

## Link do deployment
https://proj-tpw-g5.herokuapp.com/

## Notas para correr localmente
Instalar (além das da aula):`pip install django-rest-authtoken` e `pip install djangorestframework-recursive`

Além de fazer as migrações normais, fazer também `python3 manage.py migrate authtoken`.


## Membros do projeto
Inês Pinho Leite, 92928
David Gomes Morais, 93147
