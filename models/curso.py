from bs4 import BeautifulSoup
from models.disciplina import Disciplina

class Curso:
    def __init__(self, nome, unidade, duracao_ideal=None, duracao_min=None, duracao_max=None):
        self.nome = nome
        self.unidade = unidade
        self.duracao_ideal = duracao_ideal
        self.duracao_min = duracao_min
        self.duracao_max = duracao_max
        self.disciplinas_obrigatorias = []
        self.disciplinas_optativas_livres = []
        self.disciplinas_optativas_eletivas = []

    @classmethod
    def from_html(cls, html, unidade):
        soup = BeautifulSoup(html, 'html.parser')

        # Extrai o nome do curso
        nome = soup.find('span', class_='curso').text

        ideal = soup.find('span', class_='duridlhab').text
        minima = soup.find('span', class_='durminhab').text
        maxima = soup.find('span', class_='durmaxhab').text

        curso = cls(nome, unidade.nome, ideal, minima, maxima)

        div_grade = soup.find("div", id="gradeCurricular")

        # Encontra todas as tabelas dentro dessa div
        tabelas = div_grade.find_all("table")

        for idx, tabela in enumerate(tabelas):
            # Heurística para decidir o tipo de disciplina
            tipo = "obrigatoria" if idx == 0 else "eletiva"

            linhas = tabela.find_all("tr", attrs={"style": "height: 20px;"})

            for tr in linhas:
                disciplina = Disciplina.from_tr(tr)
                if disciplina:
                    curso.adicionar_disciplina(disciplina, tipo)

        print("Curso: ", nome, unidade.nome, ideal, minima, maxima)

        return curso

    def adicionar_disciplina(self, disciplina, tipo):
        if tipo == "obrigatoria":
            self.disciplinas_obrigatorias.append(disciplina)
        elif tipo == "livre":
            self.disciplinas_optativas_livres.append(disciplina)
        elif tipo == "eletiva":
            self.disciplinas_optativas_eletivas.append(disciplina)
