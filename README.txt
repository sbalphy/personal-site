Projeto de site pessoal.

Esse site consiste num site normal (about.html e curriculo.html) e uma wiki (pasta wiki) que pretendo expandir no futuro.
O design das páginas da wiki foi baseado na página pessoal do artista Oliver Shore: https://github.com/deuveir/deuveir.github.io

A pasta utils contém um utilitário para gerenciamento das páginas da wiki, o pagemanager.py.
Ele requer Python e as bibliotecas anytree e jinja2. A sua função é gerenciar a hierarquia de diretórios da wiki (salva em files.json)
e criar novas páginas usando a templating engine Jinja.

Comandos:

python pagemanager.py add path/to/node
	Cria a página node na localização especificada na hierarquia de diretórios da wiki. Não cria o arquivo .html -- é útil se
	você quer adicionar várias páginas de uma vez.

python pagemanager.py remove path/to/node
	Remove a página node na localização especificada na hierarquia de diretórios da wiki. Não apaga o arquivo .html, se existir.

python pagemanager.py create path/to/node
	Cria um arquivo node.html referente ao nó path/to/node, adicionando o nó na árvore (via add) caso não exista. O arquivo
	é salvo na pasta utils/output e está nas especificações da template template-fresh.html. 

python pagemanager.py update path/to/node
	Updata o arquivo wiki/node.html, de acordo com a template template-renew.html. A nova versão é salva na pasta utils/output.
	Honestamente não vejo muita utilidade, dados os próximos comandos.

python pagemanager.py update-all
	Updata todos os arquivos na hierarquia de diretório contidos na pasta wiki, de acordo com a template template-renew.html.
	Salvos em utils/output. Útil se você fez alguma mudança no boilerplate da template e quer updatar todos os arquivos com ela.

python pagemanager.py update-dependents path/to/node
	Updata wiki/node.html e todos os seus filhos imediatos, de acordo com a template template-renew.html. Salvos em utils/output.
	Útil se você acrescentou um filho à node e quer updatar o header de todos os afetados.
