import pandas as pd
from jinja2 import Environment, FileSystemLoader
from flask import url_for
import numpy as np


# funções pra colorir as tabelas
def _color_correction(data):
    df = data.copy()
    df.loc[df['Sua resposta'] == df['Gabarito'], :] = 'background-color: lightgreen'
    df.loc[df['Sua resposta'] != df['Gabarito'], :] = 'background-color: #d48585'
    return df

def _color_table_every_other(data):
    df = data.copy()
    n = len(df)
    df.iloc[range(0,n,2), :] = 'background-color: #f5f5dc'
    df.iloc[range(1,n,2), :] = 'background-color: #f0f0ce'
    df.iloc[-1,:] += '; font-weight: bold'
    
    return df

# carrega os DataFrames com os dados de questoes, notas pessoais e notas gerais
df_q = pd.read_pickle('dados-relatorio-alunos\data.pkl')
df_q = df_q.rename(columns={'resposta':'Sua resposta', 'gabarito':'Gabarito'})
df_q['Sua resposta'] = df_q['Sua resposta'].str.upper()
df_q['Gabarito'] = df_q['Gabarito'].str.upper()

df_n = pd.read_pickle('dados-relatorio-alunos/acertos_aluno.pkl')
df_n['Média Individual'] = df_n['Média Individual'].apply(lambda x: str(round(x,3)*100)+'%')
df_n['Media Geral'] = df_n['Media Geral'].apply(lambda x: str(round(x,3)*100)+'%')

# df_g = pd.read_pickle('df_notas_geral.pkl').rename(columns={'Nota':'Média geral'})
# df_g['Média geral'] = df_g['Média geral'].apply(lambda x: str(round(x,1))+'%')

df_r = pd.read_pickle('dados-relatorio-alunos\dados_redacao.pkl')

relatorio_alunos = {}


# /!\ IMPORTANTE /!\
# aqui carrega o template HTML que vai ser usado pelo Jinja
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("SIMULINHO/simulinho_aluno_template.html")

# cria um dicionário com as variáveis pro template
doc = {
    'document_title': 'Correção SIMULINHO 2021'
}

# pra cada aluno
for aluno in df_q.index.get_level_values(0).unique():
    # print(aluno)

    # a cada iteração, ele pega os dados correspondente ao 'aluno'
    doc['nome'] = aluno # nome do aluno
    doc['materias'] = []
    df_q_aluno = df_q.loc[aluno, :]
    # print(df_q_aluno)
    
    
    df_q_aluno['questao'] = df_q_aluno.index.get_level_values(1)
    df_q_aluno = df_q_aluno[['questao','Sua resposta','Gabarito','assunto']]
    
    # pra cada matéria:
    for materia in df_q_aluno.index.get_level_values(0).unique():
        doc['materias'].append({
            'materia':materia,
            'df':df_q_aluno.loc[materia, :].style.apply(
                _color_correction,
                axis=None
            ).set_properties(
                **{'text-align':'center',
                   'font-family':'Roboto',
                   'border-color':'black',
                   'border-style' :'solid',
                   'border-width': '1px',
                   'border-collapse':'collapse'}
            ).set_table_styles(
                [{'props':[('color','#533884'),
                           ('font-family','Roboto')]}]
            ).hide_index().render()
        })

    



    df_n_aluno = df_n.loc[aluno, :]
    df_n_aluno['Matéria'] = df_n_aluno.index
    df_n_aluno.loc[:, 'Total de Acertos'] = df_n_aluno['Total de Acertos']# .apply(lambda x: str(int(x))) + '/' + df_n_aluno['Contagem'].apply(lambda x: str(int(x)))
    df_n_aluno.loc[:, 'Média Individual'] = df_n_aluno['Média Individual']# .apply(lambda x: str(round(x,1))+'%')
    df_n_aluno.loc[:, 'Media Geral'] = df_n_aluno['Media Geral']
    
    
    df_n_aluno = df_n_aluno[['Matéria','Total de Acertos', 'Média Individual',  'Media Geral']]
    ## print(df_n_aluno)
    #vprint(df_n_aluno)
    # a proxima linha não é necessária, o valor da média individual de cada aluno já vem com a media geral
    #  df_n_aluno = df_n_aluno.join(df_g)



    doc['notas'] = df_n_aluno.style.apply(
                _color_table_every_other,
                axis=None
            ).set_properties(
                **{'text-align':'center',
                   'font-family':'Roboto',
                   'border-color':'black',
                   'border-style' :'solid',
                   'border-width': '1px',
                   'border-collapse':'collapse'}
            ).set_table_styles(
                [{'props':[('color','#533884'), ('font-family','Roboto')]}]
            ).hide_index().render()

	


    # redacao
    # red_aluno = df_r.loc[aluno, :]
    red_aluno = df_r.loc[df_r['nome'] == aluno]
    red_aluno = red_aluno.drop(columns=['nome', 'cpf']) # .transpose()
   #  print(doc['notas'])
    doc['redacao'] = red_aluno
    
    redacao = red_aluno.to_dict()
    print(redacao)

    
    # path pro grafico
    # não tem gráfico para alunos
    # doc['grafico_path'] = f'/home/pedro/einstein/simenem/graficos/total_{aluno.replace(" ","_")}.png'
    

    # renderiza o html a partir do template e com as informações do dicionário
    html_out = template.render(doc)
    with open(f"html-alunos/{aluno.replace(' ', '_')}.html",'w') as file:
        file.write(html_out)



