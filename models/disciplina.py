class Disciplina:
    def __init__(self, codigo, nome, cr_aula, cr_trab, carga_total,
                 carga_estagio=0, carga_pcc=0, carga_ativ_aprof=0):
        self.codigo = codigo
        self.nome = nome
        self.creditos_aula = cr_aula
        self.creditos_trabalho = cr_trab
        self.carga_total = carga_total
        self.carga_estagio = carga_estagio
        self.carga_pcc = carga_pcc
        self.carga_ativ_aprof = carga_ativ_aprof

    @classmethod
    def from_tr(cls, tr):
        td = tr.find_all("td")
        if len(td) < 5:
            return None  # Não é uma linha válida de disciplina

        try:
            # Código da disciplina
            a_tag = td[0].find("a", class_="disciplina")
            codigo = a_tag.text.strip() if a_tag else td[0].text.strip()

            # Nome da disciplina
            nome = td[1].text.strip()

            # Função auxiliar para converter inteiros, tratando vazios
            def parse_int(text):
                try:
                    return int(text.strip())
                except:
                    return 0

            cr_aula = parse_int(td[2].text)
            cr_trab = parse_int(td[3].text)
            carga_total = parse_int(td[4].text)
            carga_estagio = parse_int(td[5].text) if len(td) > 5 else 0
            carga_pcc = parse_int(td[6].text) if len(td) > 6 else 0
            carga_ativ_aprof = parse_int(td[7].text) if len(td) > 7 else 0

            return cls(codigo, nome, cr_aula, cr_trab, carga_total,
                       carga_estagio, carga_pcc, carga_ativ_aprof)
        except Exception as e:
            print(f"⚠️ Erro ao criar disciplina: {e}")
            return None

    def print(self):
        print(f"Disciplina: {self.codigo} - {self.nome}: {self.creditos_aula}, {self.creditos_trabalho} créditos / Carga Total{self.carga_total}, {self.carga_estagio}, {self.carga_pcc}, {self.carga_ativ_aprof}")

    def __repr__(self):
        return f"<{self.codigo} - {self.nome}>"
