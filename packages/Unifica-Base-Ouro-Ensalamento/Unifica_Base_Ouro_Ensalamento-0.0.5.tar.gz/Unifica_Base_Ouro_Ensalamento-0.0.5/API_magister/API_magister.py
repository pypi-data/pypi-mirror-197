import pandas
import requests
import json
from collections import defaultdict

def Post(df_unificado, access_token, url):

    my_headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    # atributo para mostrar o numero da linha
    row = 0
    qtd_linhas = len(df_unificado)
    print('criando json...')
    new_df_unificado = pandas.DataFrame()
    valores_json = df_unificado.to_json()
    new_df_unificado['emailInstitucional'] = df_unificado['E-mail Institucional']
    new_df_unificado['turmaAluno'] = df_unificado['Turma Aluno']
    new_df_unificado['cursoDisciplina'] = df_unificado['Curso Disciplina']
    new_df_unificado['turmaDisciplina'] = df_unificado['Turma Disciplina']
    new_df_unificado['divisao'] = df_unificado['Divisão']
    new_df_unificado['disciplina'] = df_unificado['Disciplina']
    new_df_unificado['diaSemana'] = df_unificado['Dia da Semana']
    new_df_unificado['horarioInicio'] = df_unificado['Horário de início']
    new_df_unificado['horarioTermino'] = df_unificado['Horário de término']
    new_df_unificado['sala'] = df_unificado['Sala']
    new_df_unificado['professor'] = df_unificado['Professor']

    valores_json = new_df_unificado.to_json(orient ='records')

    '''for data in df_unificado.iterrows():
        # valores
        emailInstitucional = str(data[1]['E-mail Institucional'])
        turmaAluno = str(data[1]['Turma Aluno'])
        cursoDisciplina = str(data[1]['Curso Disciplina'])
        turmaDisciplina = str(data[1]['Turma Disciplina'])
        divisao = str(data[1]['Divisão'])
        disciplina = str(data[1]['Disciplina'])
        diaSemana = str(data[1]['Dia da Semana'])
        horarioInicio = str(data[1]['Horário de início'])
        horarioTermino = str(data[1]['Horário de término'])
        sala = str(data[1]['Sala'])
        professor = str(data[1]['Professor'])

        # criando dict
        dict_valores = {
            'emailInstitucional': emailInstitucional,
            'turmaAluno': turmaAluno,
            'cursoDisciplina': cursoDisciplina,
            'turmaDisciplina': turmaDisciplina,
            'divisao': divisao,
            'disciplina': disciplina,
            'diaSemana': diaSemana,
            'horarioInicio': horarioInicio,
            'horarioTermino': horarioTermino,
            'sala': sala,
            'professor': professor,
        }

        #formatando o json
        if row == 0:
            valores_json = f'[{json.dumps(dict_valores)},'
        elif row == qtd_linhas - 1:
            valores_json += f'{json.dumps(dict_valores)}]'
        else:
            valores_json += f'{json.dumps(dict_valores)},'

        row += 1'''

    print(valores_json)
    print('enviando...')

    # enviando
    response = requests.post(url, headers=my_headers, data=valores_json)

    # retornando status
    print(response.headers)
    print(response.text)
    print(f'retornou codigo: 'f'{response.status_code} ({response.reason})')


if __name__ == '__main__':

    Post()
