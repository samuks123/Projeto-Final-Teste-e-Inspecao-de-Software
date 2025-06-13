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

    scraper = USPScraper(limite_unidades)
    scraper.executar()

if __name__ == "__main__":
    main()