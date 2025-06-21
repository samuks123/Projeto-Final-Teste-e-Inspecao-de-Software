import sys
from scraper.usp_scraper import USPScraper

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <quantidade_de_unidades>")
        return
    elif int(sys.argv[1]) <= 0:
        print("A quantidade de unidades deve ser um número inteiro positivo.")
        return
    if not sys.argv[1].isdigit():
        print("O argumento deve ser um número inteiro positivo.")
        return

    try:
        limite_unidades = int(sys.argv[1])
    except ValueError:
        print("O argumento deve ser um número inteiro.")
        return

    net = input("Sua Internet está rápida? (s/n): ").strip().lower()

    scraper = USPScraper(limite_unidades, tempo=0.2 if net == 's' else 0.5)
    scraper.executar()

    print("Scraping concluído.")

    unidades = scraper.get_unidades()
    cursos = scraper.get_cursos()
    disciplinas = scraper.get_disciplinas()

    char = ''

    while char != 'q':
        
        char = input("\nInforma a ação desejada (q para sair): \n"
                    " 1. Lista de cursos por unidades\n"
                    " 2. Dados de um determinado curso\n"
                    " 3. Dados de todos os cursos\n"
                    " 4. Dados de uma disciplina, inclusive quais cursos ela faz parte\n"
                    " 5. Disciplinas que são usadas em mais de um curso\n"
                    " 6. Top Cursos por Carga Horária\n"
                    " 7. Análise de Cursos (Teórico vs. Prático)\n").strip().lower()
        match char:
            case '1':
                print("=" * 50 + "\nLista de cursos por unidades:")
                for unidade in unidades:
                    print(f"\nUnidade: {unidade.nome}")
                    for curso in unidade.cursos:
                        print(f"  Curso: {curso.nome}")

            case '2':
                print("=" * 50 + "\nDados de um determinado curso:")
                nome_curso = input("Digite o nome do curso: ").strip()
                curso_encontrado = next((curso for curso in cursos if curso.nome == nome_curso), None)
                if curso_encontrado:
                    curso_encontrado.print()
                else:
                    print(f"Curso com nome {nome_curso} não encontrado.")

            case '3':
                print("=" * 50 + "\nDados de todos os cursos:")
                for curso in cursos:
                    curso.print()

            case '4':
                print("=" * 50 + "\nDados de uma disciplina, inclusive quais cursos ela faz parte:")
                codigo_disciplina = input("Digite o código da disciplina: ").strip()
                disciplina_encontrada = next((disciplina for disciplina in disciplinas if disciplina.codigo == codigo_disciplina), None)
                if disciplina_encontrada:
                    disciplina_encontrada.print()
                    disciplina_usada_em_mais_de_um_curso(cursos, 's', disciplina_encontrada.codigo)
                else:
                    print(f"Disciplina com código {codigo_disciplina} não encontrada.")

            case '5':
                print_curso = input("Deseja imprimir os cursos que usam disciplinas em mais de um curso? (s/n): ").strip().lower()
                print("=" * 50 + "\nDisciplinas que são usadas em mais de um curso:")
                disciplina_usada_em_mais_de_um_curso(cursos, print_curso)

            case '6':
                print("=" * 50 + "\nTop Cursos por Carga Horária:")
                top_cursos_por_carga_horaria(cursos)

            case '7':
                print("=" * 50 + "\nAnálise de Cursos (Teórico vs. Prático):")
                analise_cursos_teorico_pratico(cursos)
            
            case 'q':
                print("Saindo...")

            case _:
                print("Opção inválida. Tente novamente.")


def disciplina_usada_em_mais_de_um_curso(cursos, print_curso='s', codigo_alvo=None):
    disciplinas_usadas = {}

    for curso in cursos:
        for disciplina in curso.disciplinas_obrigatorias + curso.disciplinas_optativas_livres + curso.disciplinas_optativas_eletivas:
            if disciplina.codigo not in disciplinas_usadas:
                disciplinas_usadas[disciplina.codigo] = []
            disciplinas_usadas[disciplina.codigo].append(curso)

    if codigo_alvo:
        cursos_usando = disciplinas_usadas.get(codigo_alvo)
        if cursos_usando:
            print(f"Disciplina {codigo_alvo} é usada nos cursos:")
            for curso in cursos_usando:
                print(f"  - {curso.nome}")
        else:
            print(f"Disciplina {codigo_alvo} não foi encontrada em nenhum curso.")
    else:
        disciplinas_repetidas = {codigo: cursos for codigo, cursos in disciplinas_usadas.items() if len(cursos) > 1}
        print("Disciplinas usadas em mais de um curso:")
        for codigo, cursos in disciplinas_repetidas.items():
            if print_curso == 's':
                print(f"Disciplina {codigo} usada nos cursos:")
                for curso in cursos:
                    print(f"  - {curso.nome}")
            else:
                print(f"Disciplina {codigo} usada em {len(cursos)} cursos.")

# Top Cursos por Carga Horária
def top_cursos_por_carga_horaria(cursos):
    
    try:
        n = int(input("Deseja ver o ranking de quantos cursos? Digite um número: ").strip())
    except ValueError:
        print("Entrada inválida. Exibindo os 5 primeiros por padrão.")
        n = 5

    cargas_horarias = []
    for curso in cursos:

        if not curso.dados_validos:
            continue
        
        carga_total_obrigatorias = sum(d.carga_total for d in curso.disciplinas_obrigatorias)
        
        if carga_total_obrigatorias > 0:
            cargas_horarias.append((curso.nome, carga_total_obrigatorias))

    # Ordena os cursos pela carga horária, do maior para o menor
    cargas_horarias.sort(key=lambda x: x[1], reverse=True)

    print(f"\n--- Top {n} Cursos por Carga Horária (Disciplinas Obrigatórias) ---")
    for nome_curso, carga in cargas_horarias[:n]:
        print(f"  - {nome_curso}: {carga} horas")

# Análise de Cursos teorico vs. Prático
def analise_cursos_teorico_pratico(cursos):

    """Calcula a proporção de créditos práticos vs. teóricos e ranqueia os cursos."""

    tipo_analise = input("Deseja ver os cursos mais 'teoricos' ou 'praticos'? ").strip().lower()

    if tipo_analise not in ['teoricos', 'praticos']:
        print("Opção inválida. Por favor, escolha 'teoricos' ou 'praticos'.")
        return

    try:
        n = int(input(f"Deseja ver o ranking de quantos cursos mais {tipo_analise}? ").strip())

    except ValueError:

        print("Entrada inválida. Exibindo os 5 primeiros por padrão.")
        n = 5

    ratios = []
    for curso in cursos:

        if not curso.dados_validos or not curso.disciplinas_obrigatorias:
            continue
        
        total_cr_aula = sum(d.creditos_aula for d in curso.disciplinas_obrigatorias)
        total_cr_trab = sum(d.creditos_trabalho for d in curso.disciplinas_obrigatorias)

        if total_cr_aula > 0:
            ratio = total_cr_trab / total_cr_aula
            ratios.append((curso.nome, ratio))

    reverse_order = True if tipo_analise == 'praticos' else False
    ratios.sort(key=lambda x: x[1], reverse=reverse_order)

    print(f"\n--- Top {n} Cursos Mais {tipo_analise.capitalize()} (Proporção Créditos Trabalho/Aula) ---")
    for nome_curso, ratio in ratios[:n]:
        print(f"  - {nome_curso} (Ratio: {ratio:.2f})")


if __name__ == "__main__":
    main()