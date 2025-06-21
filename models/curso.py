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
        self.dados_validos = True

    @classmethod
    def from_html(cls, html, unidade):
        soup = BeautifulSoup(html, 'html.parser')

        nome = soup.find('span', class_='curso').text
        ideal = soup.find('span', class_='duridlhab').text
        minima = soup.find('span', class_='durminhab').text
        maxima = soup.find('span', class_='durmaxhab').text

        curso = cls(nome, unidade.nome, ideal, minima, maxima)
        
        # Se chegamos aqui, os dados são válidos.
        # Apenas para garantir, mantemos como True.
        curso.dados_validos = True

        div_grade = soup.find("div", id="gradeCurricular")
        if not div_grade:
            curso.dados_validos = False
            return curso

        tabelas = div_grade.find_all("table")

        for idx, tabela in enumerate(tabelas):
            tipo = "obrigatoria" if idx == 0 else "eletiva"
            linhas = tabela.find_all("tr", attrs={"style": "height: 20px;"})
            for tr in linhas:
                disciplina = Disciplina.from_tr(tr)
                if disciplina:
                    curso.adicionar_disciplina(disciplina, tipo)

        return curso

    def print(self):
        print("="*50)
        print(f"Curso: {self.nome} - Unidade: {self.unidade}")
        # Verifica se os dados são válidos antes de imprimir os detalhes
        if not self.dados_validos:
            print("  !! Dados da grade curricular não encontrados ou indisponíveis. !!")
            return
            
        print(f"  Duração Ideal: {self.duracao_ideal}, Mínima: {self.duracao_min}, Máxima: {self.duracao_max}\n")
        
        # As impressões das disciplinas para depuração
        # print("  Disciplinas Obrigatórias:")
        # for d in self.disciplinas_obrigatorias:
        #     d.print()

    def adicionar_disciplina(self, disciplina, tipo):
        if tipo == "obrigatoria":
            self.disciplinas_obrigatorias.append(disciplina)
        elif tipo == "livre":
            self.disciplinas_optativas_livres.append(disciplina)
        elif tipo == "eletiva":
            self.disciplinas_optativas_eletivas.append(disciplina)