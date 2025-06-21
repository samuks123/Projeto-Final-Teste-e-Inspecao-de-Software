# scraper/usp_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from models.unidade import Unidade
from models.curso import Curso
import time

class USPScraper:
    
    def __init__(self, limite_unidades, tempo=0.1):
        
        self.tempo = tempo
        self.limite_unidades = limite_unidades
        self.unidades = []

        options = Options()
        
        options.add_argument('--log-level=3') 
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.driver = webdriver.Chrome(options=options)

    def executar(self):
        url = "https://uspdigital.usp.br/jupiterweb/jupCarreira.jsp?codmnu=8275"
        self.driver.get(url)
        
        body = self.driver.find_element(By.TAG_NAME, 'body')

        select_element_unidade = self.driver.find_element(By.ID, "comboUnidade")
        select_unidade = Select(select_element_unidade)
        time.sleep(self.tempo)
        opcoes_unidades = select_unidade.options[1:]
        print(f"Total de unidades encontradas: {len(opcoes_unidades)}")

        for i, opcao_unidade in enumerate(opcoes_unidades):
            
            if i >= self.limite_unidades:
                break

            nome_unidade = opcao_unidade.text.strip()
            print(f"[{i+1}] Selecionando unidade: {nome_unidade}")
            select_unidade.select_by_index(i + 1)
            time.sleep(self.tempo)

            unidade = Unidade(nome_unidade)
            self.unidades.append(unidade)
            
            opcoes_cursos = Select(self.driver.find_element(By.ID, "comboCurso")).options[1:]
            print(f"Total de cursos encontrados para a unidade {unidade.nome}: {len(opcoes_cursos)}")

            for j, opcao_curso in enumerate(opcoes_cursos):
                Select(self.driver.find_element(By.ID, "comboUnidade")).select_by_index(i + 1)
                time.sleep(self.tempo)
                
                select_curso_iter = Select(self.driver.find_element(By.ID, "comboCurso"))
                codigo_curso = select_curso_iter.options[j + 1].get_attribute("value")
                nome_curso = select_curso_iter.options[j + 1].text.strip()
                print(f"  [{j+1}] Selecionando curso: {nome_curso} ({codigo_curso})")
                select_curso_iter.select_by_index(j + 1)

                check_input = self.driver.find_element(By.ID, "enviar")
                check_input.click()

                wait = WebDriverWait(self.driver, 3)
                
                try:
                    overlay_locator = (By.CSS_SELECTOR, ".ui-widget-overlay, .blockOverlay")
                    wait.until(EC.invisibility_of_element_located(overlay_locator))

                    tab_grade = wait.until(EC.element_to_be_clickable((By.ID, "step4-tab")))
                    tab_grade.click()
                    
                    time.sleep(self.tempo * 3)
                    
                    curso = Curso.from_html(self.driver.page_source, unidade)
                    unidade.adicionar_curso(curso)

                except (TimeoutException, ElementClickInterceptedException):
                    print(f"    --- Dados da grade não encontrados para o curso: {nome_curso}. Marcando como inválido.")

                    curso_invalido = Curso(nome_curso, unidade.nome)
                    curso_invalido.dados_validos = False
                    unidade.adicionar_curso(curso_invalido)
                    
                    body.send_keys(Keys.ESCAPE)
                    time.sleep(0.5)
                
                except Exception as e:
                    print(f"------ Ocorreu um erro desconhecido e não tratado ao processar o curso {nome_curso}: {e}")

                finally:

                    try:
                        overlay_locator = (By.CSS_SELECTOR, ".ui-widget-overlay, .blockOverlay")
                        wait.until(EC.invisibility_of_element_located(overlay_locator))
                    except TimeoutException:
                        body.send_keys(Keys.ESCAPE)
                        time.sleep(0.5)

                    tab_busca = self.driver.find_element(By.ID, "step1-tab")
                    tab_busca.click()
                    time.sleep(self.tempo)

        print("\nFim da coleta de unidades.")

    def get_unidades(self):
        return self.unidades

    def get_cursos(self):
        cursos = []
        for unidade in self.unidades:
            cursos.extend(unidade.cursos)
        return cursos

    def get_disciplinas(self):
        disciplinas = []
        for unidade in self.unidades:
            for curso in unidade.cursos:
                disciplinas.extend(curso.disciplinas_obrigatorias)
                disciplinas.extend(curso.disciplinas_optativas_livres)
                disciplinas.extend(curso.disciplinas_optativas_eletivas)
        return disciplinas

    def finalizar(self):
        self.driver.quit()