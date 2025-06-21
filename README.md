# Coletor e Analisador de Dados de Cursos da USP

## 📖 Sobre o Projeto

Este projeto consiste em um programa de software livre, desenvolvido em **Python** e orientado a objetos, que realiza a coleta automatizada (_web scraping_) de dados sobre todos os cursos de graduação oferecidos pela **Universidade de São Paulo (USP)**, a partir do sistema público **JúpiterWeb**.

O programa navega pelo site, extrai informações detalhadas sobre as unidades, os cursos e as grades curriculares, e ao final, permite que o usuário realize diversas consultas sobre os dados coletados através de um menu interativo.

---

## ✨ Funcionalidades

Após a coleta dos dados, o programa oferece um menu interativo com as seguintes consultas:

1. **Lista de cursos por unidades**: Exibe todas as unidades processadas e os respectivos cursos oferecidos por cada uma.  
2. **Dados de um determinado curso**: Mostra informações detalhadas de um curso específico, pesquisado pelo nome.  
3. **Dados de todos os cursos**: Itera sobre todos os cursos coletados e exibe suas informações.  
4. **Dados de uma disciplina**: Exibe detalhes de uma disciplina (créditos, carga horária, etc.) e em quais cursos ela é utilizada.  
5. **Disciplinas em mais de um curso**: Lista todas as disciplinas que fazem parte da grade curricular de mais de um curso.  
6. **Top Cursos por Carga Horária**: Apresenta um ranking dos cursos com maior carga horária total, somando as disciplinas obrigatórias.  
7. **Análise de Cursos (Teórico vs. Prático)**: Classifica os cursos com maior foco em atividades práticas ou teóricas, com base na proporção de créditos-trabalho e créditos-aula.  

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3  
- **Web Scraping**:
  - **Selenium**: Para automação e controle do navegador web.  
  - **Beautiful Soup**: Para extração de dados (_parsing_) do conteúdo HTML das páginas.  

---

## 📂 Estrutura de Arquivos

```bash
.
├── main.py                 # Ponto de entrada da aplicação, gerencia o menu interativo
├── scraper/
│   └── usp_scraper.py      # Contém a classe e a lógica principal do web scraper
├── models/
│   ├── unidade.py          # Modelo da classe Unidade
│   ├── curso.py            # Modelo da classe Curso
│   └── disciplina.py       # Modelo da classe Disciplina
└── README.md               # Este arquivo
```

---

## ⚙️ Instalação

Siga os passos abaixo para configurar o ambiente e executar o projeto.

### Clone o repositório:

```bash
git clone https://github.com/samuks123/Projeto-Final-Teste-e-Inspecao-de-Software
cd Projeto-Final-Teste-e-Inspecao-de-Software
```

### Instale as dependências de sistema:

- **Google Chrome**: É necessário ter o navegador instalado.
- **ChromeDriver**: O Selenium precisa do driver correspondente à sua versão do Google Chrome.

Para Linux (Debian/Ubuntu):

```bash
sudo apt install chromium-chromedriver
```

### Instale as dependências do Python:

```bash
pip install selenium beautifulsoup4
```

---

## 🚀 Execução

Para iniciar o programa, execute o arquivo `main.py` a partir do seu terminal, passando como argumento o número de unidades da USP que você deseja analisar.

### Exemplos:

#### Para analisar apenas as 3 primeiras unidades da lista:

```bash
python main.py 3
```

#### Para analisar todas as 47 unidades (pode levar vários minutos):

```bash
python main.py 47
```

Ao iniciar, o programa perguntará sobre a velocidade da sua conexão para ajustar os tempos de espera e, em seguida, começará o processo de coleta.

---

## 📋 Menu Interativo

Após a conclusão da coleta, o menu interativo será exibido:

```
Scraping concluído.

Informa a ação desejada (q para sair):
 1. Lista de cursos por unidades
 2. Dados de um determinado curso
 3. Dados de todos os cursos
 4. Dados de uma disciplina, inclusive quais cursos ela faz parte
 5. Disciplinas que são usadas em mais de um curso
 6. Top Cursos por Carga Horária
 7. Análise de Cursos (Teórico vs. Prático)
```

---

## 🏆 Exemplo da Opção 6: Top Cursos por Carga Horária

```
6
==================================================
Top Cursos por Carga Horária:
Deseja ver o ranking de quantos cursos? Digite um número: 5

--- Top 5 Cursos por Carga Horária (Disciplinas Obrigatórias) ---
  - Medicina - integral: 8130 horas
  - Medicina - integral: 8040 horas
  - Arquitetura e Urbanismo - integral: 5895 horas
  - Engenharia Civil - integral: 4995 horas
  - Arquitetura e Urbanismo - integral: 4920 horas
```

---

## 🔍 Exemplo da Opção 7: Análise de Cursos Práticos

```
7
==================================================
Análise de Cursos (Teórico vs. Prático):
Deseja ver os cursos mais 'teoricos' ou 'praticos'? praticos
Deseja ver o ranking de quantos cursos mais praticos? 5

--- Top 5 Cursos Mais Praticos (Proporção Créditos Trabalho/Aula) ---
  - Medicina - integral (Ratio: 0.94)
  - Música - Licenciatura - integral (Ratio: 0.76)
  - Bacharelado em Comunicação Social (Habilitação em Editoração) - matutino (Ratio: 0.55)
  - Fonoaudiologia - integral (Ratio: 0.54)
  - Bacharelado em Jornalismo - matutino (Ratio: 0.53)
```