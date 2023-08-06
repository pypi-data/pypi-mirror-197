import numpy as np
import pandas
import API_magister

class Ensalamento:
    def __init__(self, curso_disciplina, cod_disciplina, turma_disciplina
                 , divisao, escola_disciplina, disciplina, dia, hora_inicio, hora_fim, sala, professor):
        self.curso_disciplina = curso_disciplina
        self.cod_disciplina = cod_disciplina
        self.turma_disciplina = turma_disciplina
        self.divisao = divisao

        self.escola_disciplina = escola_disciplina
        self.disciplina = disciplina
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim
        self.sala = sala
        self.professor = professor


def trata_coluna_turmas_disciplinas(dado):
    dado = dado.split('-')[1:]
    #retirando o formato lista
    dado = str(dado).replace("'","").replace("[","").replace("]","").replace(',',"-")
    return dado

def trata_coluna_disciplinas(dado):
    dado = dado.replace(',', '|')

    dado = dado.split(' ')[2:]

    dado = str(dado).replace("'", "").replace("[", "").replace("]", "").replace(',','').replace('|',',')
    return dado

def trata_coluna_sala(dado):

    lista_replace = ['CHVC', 'GIN', 'LBCS','LBMO']

    dado = dado.replace(';','|')

    for salas_replace in lista_replace:

        if dado.__contains__(salas_replace):
            dado = dado.replace('CHVC', 'Clínica Veterinária').replace('GIN', 'Ginásio').replace('LBCS', 'LABCOM').replace('LBMO', 'Laboratório de Modelos')


    return dado

def gera_lista_ensalamento(df_ensalamento):
    lista_ensalamento = []
    dict_ensalamento = {}

    for data_en in df_ensalamento.iterrows():
        list_aux = []

        # chaves
        curso_disciplina_en = data_en[1]['Curso']
        cod_disciplina_en = data_en[1]['Nome disciplina'].split(' ')[0]
        turma_disciplina_en = data_en[1]['Turma Prime']
        divisao_en = data_en[1]['Divisão']

        # valores ensalamento
        escola_disciplina = data_en[1]['Escola']
        disciplina = data_en[1]['Nome disciplina']
        dia = data_en[1]['Dia da Semana']
        hora_inicio = data_en[1]['Horário de início']
        hora_fim = data_en[1]['Horário de término']
        sala = data_en[1]['Sala']
        professor = data_en[1]['Professor']

        if turma_disciplina_en.__contains__('LEA -'):
            part1 = turma_disciplina_en.split(' ')[0]
            part2 = turma_disciplina_en.split(' ')[1]
            part3 = turma_disciplina_en.split(' ')[2]
            part4 = turma_disciplina_en.split(' ')[3]
            part5 = turma_disciplina_en.split(' ')[4]
            part6 = turma_disciplina_en.split(' ')[5]
            part6 = part6.replace('-','')
            turma_disciplina_en = f"{part1} {part2} {part3} {part4} {part6}"

        objeto = Ensalamento(curso_disciplina_en, cod_disciplina_en, turma_disciplina_en,
                             divisao_en, escola_disciplina, disciplina, dia, hora_inicio, hora_fim, sala, professor)

        key_en = f"{cod_disciplina_en, turma_disciplina_en, divisao_en}".upper()

        list_aux.append(objeto)

        if key_en in dict_ensalamento.keys():

            dict_ensalamento[key_en] += list_aux
        else:
            dict_ensalamento[key_en] = list_aux

    return dict_ensalamento


def trata_base_ouro(caminho_base_ouro):
    df_divisao1 = pandas.read_excel(caminho_base_ouro)
    df_divisao2 = pandas.read_excel(caminho_base_ouro)
    df_divisao_vazia = pandas.read_excel(caminho_base_ouro)

    # tratando colunas
    df_divisao1.drop("DIVISAO2", axis=1, inplace=True)
    df_divisao2.drop("DIVISAO", axis=1, inplace=True)
    df_divisao_vazia.drop(["DIVISAO", "DIVISAO2"], axis=1, inplace=True)

    # criando coluna para divisões vazias
    df_divisao_vazia['DIVISAO'] = "-"

    # renomeando colunas para concatenar
    df_divisao2.rename(columns={'DIVISAO2': 'DIVISAO'}, inplace=True)

    df_base_ouro = pandas.concat([df_divisao1, df_divisao2, df_divisao_vazia])
    df_base_ouro = df_base_ouro.drop_duplicates()

    # writer = pandas.ExcelWriter("C:/Users\m.rosa1\Downloads/teste.xlsx", engine='xlsxwriter')
    # df_base_ouro.to_excel(writer, index=False, sheet_name="Sheet1")
    # writer.close()
    return df_base_ouro


def unificado(caminho_base_ouro, caminho_ensalamento, caminho_arquivo):
    df_ensalamento = pandas.read_excel(caminho_ensalamento)
    df_base = trata_base_ouro(caminho_base_ouro)

    df_base['DIVISAO'] = df_base['DIVISAO'].replace(np.nan, '-')

    dict_excel = {}

    dict_ensalamento = gera_lista_ensalamento(df_ensalamento)

    chaves_n_encontradas = []
    key_aux = 0
    contagem_n_encontradas = 0
    for data in df_base.iterrows():

        # chaves base
        curso_disciplina = data[1]['Curso_Disciplina']
        cod_disciplina = data[1]['DISCIPLINA'].split(' ')[0]
        turma_disciplina = data[1]['TURMA_DISCIPLINA']
        divisao = str(data[1]['DIVISAO']).replace("NAN", "-")

        # todo chave base
        key_base = f"{cod_disciplina, turma_disciplina, divisao}".upper()

        # valores
        cpf = data[1]['CPF']
        matricula = data[1]['Matrícula']
        nome_completo = data[1]['Nome Completo']
        email = data[1]['E-mail']
        email_institucional = data[1]['E-mail Institucional']
        escola = data[1]['Escola']
        curso_aluno = data[1]['Curso Aluno']
        turma_aluno = data[1]['Turma Aluno']

        try:
            lista_valores = dict_ensalamento[key_base]
        except:
            chaves_n_encontradas.append(key_base)
            contagem_n_encontradas += 1
            continue

        for valor in lista_valores:
            # valores ensalamento
            escola_disciplina = valor.escola_disciplina
            disciplina = valor.disciplina
            dia = valor.dia
            hora_inicio = valor.hora_inicio
            hora_fim = valor.hora_fim
            sala = valor.sala
            professor = valor.professor

            dict_excel[key_aux] = {
                'CPF': cpf,
                'Matrícula': matricula,
                'Nome Completo': nome_completo,
                'E-mail': email,
                'E-mail Institucional': email_institucional,
                'Escola': escola,
                'Curso Aluno': curso_aluno,
                'Turma Aluno': turma_aluno,
                'Escola Disciplina': escola_disciplina,
                'Curso Disciplina': curso_disciplina,
                'Turma Disciplina': turma_disciplina,
                'Divisão': divisao,
                'Disciplina': disciplina,
                'Dia da Semana': dia,
                'Horário de início': hora_inicio,
                'Horário de término': hora_fim,
                'Sala': sala,
                'Professor': professor,
            }

            key_aux += 1

    contagem_chaves_n_encontradas = 0
    chaves_n_encontradas = list(set(chaves_n_encontradas))
    for chaves in chaves_n_encontradas:
        contagem_chaves_n_encontradas += 1



    df = pandas.DataFrame(data=dict_excel)
    df = (df.T)
    df = df.drop_duplicates()

    df['Turma Disciplina'] = df.apply(lambda x: trata_coluna_turmas_disciplinas(x['Turma Disciplina']), axis=1)
    df['Disciplina'] = df.apply(lambda x: trata_coluna_disciplinas(x['Disciplina']), axis=1)
    df['Sala'] = df.apply(lambda x: trata_coluna_sala(x['Sala']), axis=1)

    writer = pandas.ExcelWriter(caminho_arquivo, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name="Sheet1")

    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    row = len(df.index)
    worksheet.add_table(0, 0, row, 17, {'style': 'Table Style Light 1', 'columns': [
        {'header': 'CPF'},
        {'header': 'Matrícula'},
        {'header': 'Nome Completo'},
        {'header': 'E-mail'},
        {'header': 'E-mail Institucional'},
        {'header': 'Escola'},
        {'header': 'Curso Aluno'},
        {'header': 'Turma Aluno'},
        {'header': 'Escola disciplina'},
        {'header': 'Curso Disciplina'},
        {'header': 'Turma Disciplina'},
        {'header': 'Divisão'},
        {'header': 'Disciplina'},
        {'header': 'Dia da Semana'},
        {'header': 'Horário de inicio'},
        {'header': 'Horário de Término'},
        {'header': 'Sala'},
        {'header': 'Professor'}
    ]})

    # Formatação da Largura da Tabela
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 50)
    worksheet.set_column('D:D', 40)
    worksheet.set_column('E:E', 40)
    worksheet.set_column('F:F', 25)
    worksheet.set_column('G:G', 15)
    worksheet.set_column('H:H', 45)
    worksheet.set_column('I:I', 30)
    worksheet.set_column('J:J', 35)
    worksheet.set_column('K:K', 20)
    worksheet.set_column('L:L', 10)
    worksheet.set_column('M:M', 60)
    worksheet.set_column('N:N', 15)
    worksheet.set_column('O:O', 15)
    worksheet.set_column('P:P', 15)
    worksheet.set_column('Q:Q', 30)
    worksheet.set_column('R:R', 30)

    writer.close()

    #print('Chaves não encontradas: ', contagem_chaves_n_encontradas)
    #print('Linhas não encontradas:', contagem_n_encontradas)
    return df


def gerarUnificado(caminho_base_ouro, caminho_ensalamento, caminho_arquivo):
    print('gerando unificado base ouro + ensalamento...')
    df = unificado(caminho_base_ouro, caminho_ensalamento, caminho_arquivo)

    access_token = "CJs1PSyZYDQxjxK9B8mkFzn5pTf4a2eTs9umAB2WGC5oAHtq0ZJl3A0ld2jwVKV8R9j8TdMfWaabzCAkTjcCSiKvf9SyUCbtiajwSKoQj1xPAtH3sXs4qsOBNRbzl0Yh"

    # urls
    #homologacao
    #url = "https://magister-hom.pucpr.br/radix/v1/ensalamentoalunotemp/inserir"
    #producao
    url = "https://magister.pucpr.br/radix/v1/ensalamentoalunotemp/inserir"
    print('enviando para o Magister...')
    API_magister.Post(df,access_token,url)

if __name__ == '__main__':

    gerarUnificado()



