import sys
from scraper.usp_scraper import USPScraper

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <quantidade_de_unidades>")
        return

    try:
        limite_unidades = int(sys.argv[1])
    except ValueError:
        print("O argumento deve ser um número inteiro.")
        return

    net = input("Sua Internet está rápida? (s/n): ").strip().lower()

    scraper = USPScraper(limite_unidades, tempo=0.1 if net == 's' else 0.5)
    scraper.executar()

    print("Scraping concluído.")

    unidades = scraper.get_unidades()
    cursos = scraper.get_cursos()
    disciplinas = scraper.get_disciplinas()

    char = ''

    while char != 'q':
        char = input("Informa a ação desejada (q para sair): \n"
                    " 1. Lista de cursos por unidades\n"
                    " 2. Dados de um determinado curso\n"
                    " 3. Dados de todos os cursos\n"
                    " 4. Dados de uma disciplina, inclusive quais cursos ela faz parte\n"
                    " 5. Disciplinas que são usadas em mais de um curso\n"
                    " 6. Outras consultas que você ache relevantes.\n").strip().lower()
        match char:
            case '1':
                print("Lista de cursos por unidades:")
                
                for unidade in unidades:
                    print(f"\nUnidade: {unidade.nome}")
                    for curso in unidade.cursos:
                        print(f"  Curso: {curso.codigo} - {curso.nome}")
            case '2':
                print("Dados de um determinado curso:")
                nome_curso = input("Digite o nome do curso: ").strip()
                curso_encontrado = next((curso for curso in cursos if curso.nome == nome_curso), None)
                if curso_encontrado:
                    curso_encontrado.print()
                else:
                    print(f"Curso com nome {nome_curso} não encontrado.")
            case '3':
                print("Dados de todos os cursos:")
                for curso in cursos:
                    curso.print()
            case '4':
                print("Dados de uma disciplina, inclusive quais cursos ela faz parte:")
                # Implementar lógica para mostrar dados de uma disciplina específica
            case '5':
                print("Disciplinas que são usadas em mais de um curso:")
                # Implementar lógica para mostrar disciplinas usadas em mais de um curso
            case '6':
                print("Outras consultas que você ache relevantes.")
                # Implementar outras consultas relevantes
            case 'q':
                print("Saindo...")
            case _:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()