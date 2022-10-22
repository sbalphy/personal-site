Projeto de site pessoal.

A intenção é que ele seja dividido em várias páginas subordinadas a uma hierarquia de diretórios, com uma árvore
representando onde a página atual está nessa hierarquia no topo de cada página. Baseado na wiki pessoal da
artista deuveir, a partir da qual esse repositório foi forkado.

TODO:
1. Decidir o visual das páginas.
	Eu gostaria de um visual mais escuro. Uma inspiração talvez seria a capa do "monograph", do monochromia.
	
2. Achar um jeito de automatizar a criação de páginas novas na hierarquia. 
	A minha ideia atual seria guardar uma representação da hierarquia num arquivo e escrever um script no python
	que, ao receber o nome de uma nova página na hierarquia (e.g. $ createpage.py index/pesquisa/jogos), lê o
	arquivo contendo a hierarquia, modifica ele para conter a nova página e cria uma página (e.g. jogos.html)
	com o boilerplate base (incluindo a representação da hierarquia no topo da página).