from aluno import Aluno


class GerenciadorAlunos:
    def __init__(self, arquivo="alunos.txt"):
        self.arquivo = arquivo
        self.alunos = []
        self.carregar()

    def carregar(self):
        self.alunos = []

        try:
            with open(self.arquivo, "r", encoding="utf-8") as arquivo:
                for linha in arquivo:
                    dados = linha.rstrip("\n").split(";")

                    if len(dados) == 5:
                        matricula, nome, cpf, email, codigo_curso = dados
                        self.alunos.append(
                            Aluno(matricula, nome, cpf, email, codigo_curso)
                        )
        except FileNotFoundError:
            pass

    def salvar(self):
        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            for aluno in self.alunos:
                dados = [
                    aluno.matricula,
                    aluno.nome,
                    aluno.cpf,
                    aluno.email,
                    aluno.codigo_curso
                ]
                arquivo.write(";".join(dados) + "\n")

    def pesquisar(self, termo):
        termo = termo.strip().casefold()

        return [
            aluno for aluno in self.alunos
            if termo == aluno.matricula.casefold()
            or termo in aluno.nome.casefold()
        ]

    def cadastrar(self, matricula, nome, cpf, email, codigo_curso,
                  codigos_cursos):
        if not all(v.strip() for v in (
            matricula, nome, cpf, email, codigo_curso
        )):
            print("Todos os campos são obrigatórios.")
            return

        if any(a.matricula == matricula for a in self.alunos):
            print("Já existe um aluno com essa matrícula.")
            return

        if codigo_curso not in codigos_cursos:
            print("Curso não encontrado. Cadastre o curso primeiro.")
            return

        aluno = Aluno(
            matricula.strip(),
            nome.strip(),
            cpf.strip(),
            email.strip(),
            codigo_curso.strip()
        )

        self.alunos.append(aluno)
        self.salvar()
        print("Aluno cadastrado com sucesso!")

    def listar(self):
        if not self.alunos:
            print("Nenhum aluno cadastrado.")
            return

        for aluno in self.alunos:
            print(aluno)

    def alterar(self, matricula, codigos_cursos):
        resultados = [
            a for a in self.alunos if a.matricula == matricula
        ]

        if not resultados:
            print("Aluno não encontrado.")
            return

        aluno = resultados[0]

        nome = input("Novo nome (Enter mantém): ").strip()
        cpf = input("Novo CPF (Enter mantém): ").strip()
        email = input("Novo e-mail (Enter mantém): ").strip()
        codigo = input("Novo código do curso (Enter mantém): ").strip()

        if codigo and codigo not in codigos_cursos:
            print("Curso não encontrado. Alteração cancelada.")
            return

        if nome:
            aluno.nome = nome
        if cpf:
            aluno.cpf = cpf
        if email:
            aluno.email = email
        if codigo:
            aluno.codigo_curso = codigo

        self.salvar()
        print("Aluno alterado com sucesso!")

    def excluir(self, matricula):
        resultados = [
            a for a in self.alunos if a.matricula == matricula
        ]

        if not resultados:
            print("Aluno não encontrado.")
            return

        self.alunos.remove(resultados[0])
        self.salvar()
        print("Aluno excluído com sucesso!")