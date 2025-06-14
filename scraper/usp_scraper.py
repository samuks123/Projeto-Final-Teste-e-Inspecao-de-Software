from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from models.unidade import Unidade
from models.curso import Curso
import time

class USPScraper:
    def __init__(self, limite_unidades):
        self.limite_unidades = limite_unidades
        self.unidades = []

        #options = Options()
        #options.add_argument("--headless")  # ou remova para visualizar o navegador
        self.driver = webdriver.Chrome()

    def executar(self):
        url = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
        self.driver.get(url)

        # Encontra o menu suspenso de unidades
        select_element = self.driver.find_element(By.ID, "comboUnidade")
        select = Select(select_element)

        time.sleep(0.5)

        # Coleta todas as opções (ignorando a primeira: "Selecione")
        opcoes_unidades = select.options[1:]  # Ignora a primeira opção
        print(f"Total de unidades encontradas: {len(opcoes_unidades)}")

        for i, opcao in enumerate(opcoes_unidades):
            if i >= self.limite_unidades:
                break

            codigo = opcao.get_attribute("value")
            nome = opcao.text.strip()

            print(f"[{i+1}] Selecionando unidade: {nome} ({codigo})")

            # Seleciona a unidade no menu
            select.select_by_index(i + 1)
            time.sleep(0.5)  # Tempo para o site carregar os cursos (ajuste conforme necessário)

            unidade = Unidade(nome)
            self.unidades.append(unidade)

            select_element = self.driver.find_element(By.ID, "comboCurso")
            select = Select(select_element)

            opcoes_cursos = select.options[1:]  # Ignora a primeira opção
            print(f"Total de cursos encontrados para a unidade {unidade}: {len(opcoes_cursos)}")

            for i, opcao in enumerate(opcoes_cursos):
                codigo_curso = opcao.get_attribute("value")
                nome_curso = opcao.text.strip()

                print(f"  [{i+1}] Selecionando curso: {nome_curso} ({codigo_curso})")

                # Seleciona o curso no menu
                select.select_by_index(i + 1)

                check_input = self.driver.find_element(By.ID, "enviar")
                check_input.click()

                time.sleep(1)

                tab_grade = self.driver.find_element(By.ID, "step4-tab")
                tab_grade.click()

                time.sleep(3)

                curso = Curso.from_html(self.driver.page_source, unidade)
                unidade.adicionar_curso(curso)

                tab_busca = self.driver.find_element(By.ID, "step1-tab")
                tab_busca.click()

                time.sleep(1)

        print("\nFim da coleta de unidades.")

    def finalizar(self):
        self.driver.quit()
