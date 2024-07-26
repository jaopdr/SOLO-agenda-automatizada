# Agenda Automatizada

## Descrição do Projeto

O projeto **Agenda Automatizada** é uma aplicação para gerenciamento de eventos, desenvolvida com a biblioteca Tkinter para a interface gráfica e SQLite para armazenamento de dados. A aplicação permite aos usuários adicionar, atualizar, excluir e pesquisar eventos em uma agenda, facilitando o acompanhamento de compromissos e eventos importantes.

## Que Problema Resolve

A aplicação resolve a necessidade de uma ferramenta prática e intuitiva para gerenciar eventos e compromissos. Ela proporciona uma interface gráfica amigável onde usuários podem:
- Adicionar novos eventos.
- Atualizar informações de eventos existentes.
- Excluir eventos.
- Buscar eventos por nome.
- Visualizar eventos por data utilizando um calendário interativo.

## Funcionalidades

- **Adição de Eventos:** Permite o cadastro de novos eventos com detalhes como tipo, nome, cerimonialista, data, telefone, entre outros.
- **Atualização de Eventos:** Possibilita a modificação de eventos já existentes na agenda.
- **Exclusão de Eventos:** Remove eventos da agenda.
- **Pesquisa por Nome:** Permite a busca de eventos específicos pelo nome do evento.
- **Visualização por Data:** Mostra eventos programados para uma data específica selecionada em um calendário.
- **Exibição de Todos os Eventos:** Permite visualizar todos os eventos registrados, independentemente da data selecionada.

## Stacks Utilizadas

- **Tkinter:** Biblioteca para a construção da interface gráfica.
- **tkcalendar:** Biblioteca para o widget de calendário.
- **SQLite:** Banco de dados para armazenamento dos eventos.

## Instalação

### Como Clonar o Repositório

1. Abra o terminal (ou prompt de comando).
2. Navegue até o diretório onde deseja clonar o repositório.
3. Execute o comando:

   ```bash
   git clone https://github.com/seu-usuario/agenda-automatizada.git
   ```
### Como Criar e Ativar o Ambiente Virtual

#### Navegue até o diretório do projeto clonado:

```bash
cd agenda-automatizada
```
#### Crie um ambiente virtual:

```bash
python -m venv venv
```
#### Ative o ambiente virtual:

No Windows:
```bash
venv\Scripts\activate
```

No macOS e Linux:
```bash
source venv/bin/activate
Como Instalar as Dependências
```

###Com o ambiente virtual ativado, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

Observação: O arquivo requirements.txt deve conter as bibliotecas necessárias, como tkcalendar e qualquer outra que o projeto utilize.

## Como Usar

### Como Executar a Automação

Certifique-se de que o ambiente virtual está ativado.

Execute o script principal para iniciar a aplicação:

```bash
python src/main.py
```

### Como Usar a Interface Gráfica

- **Adicionar Evento:** Preencha os campos de entrada com as informações do evento e clique no botão "Adicionar".
- **Atualizar Evento:** Selecione um evento na tabela, modifique os campos de entrada e clique no botão "Atualizar".
- **Excluir Evento:** Selecione um evento na tabela e clique no botão "Excluir". Confirme a exclusão quando solicitado.
- **Buscar Evento:** Digite o nome do evento no campo de pesquisa e clique no botão "Procurar" para encontrar eventos correspondentes.
- **Visualizar Eventos por Data:** Selecione uma data no calendário para ver os eventos programados para essa data. Use o botão "Mostrar Todos" para exibir todos os eventos.
