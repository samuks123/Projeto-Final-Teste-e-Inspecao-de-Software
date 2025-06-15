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
                    " 5. Disciplinas que são usadas em mais de um curso\n").strip().lower()
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


if __name__ == "__main__":
    main()