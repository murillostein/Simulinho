import pandas as pd
import numpy as np
import streamlit as st
import PIL

data = pd.read_pickle('dados-relatorio-alunos/data.pkl')
# 


st.title('Relatório Docentes')

st.write('Olá Docente!')
st.write("Este é o seu relatório do Simulinho 2021. Aqui você encontra dados sobre a prova geral e dados específicos para cada disciplina.")
# ! dados gerais !

# número de inscritos
# total_presentes = data.Index(['nome'])
# print(total_presentes.value_counts())
total_presentes = 12
# media de pontuação total e porcentagem de acerto
pontuacao_total = pd.read_pickle('dados-relatorio-alunos/pontuacao_total.pkl')

media_pontuacao_total = round(pontuacao_total['Nota total'].mean(),1)

# a media da % de acerto da prova é justamente a média de acerto, dividida pela quantidade total de pontos possíveis
# como a redação vale 1000, e as questçoes objetivas 500, basta dividir por 500
media_porcem_total = str(round(media_pontuacao_total / 1500, 1)*100) + '%'
# media_porcem_total = media_porcem_total.astype()
# print(media_porcem_total)
st.header("**1. Dados sobre a Prova Geral**")
dados = {
    'Total de Inscritos': [total_presentes],
    'Média de Pontuação Total':[media_pontuacao_total],
    'Média da Porcentagem de Acerto': [media_porcem_total]
}
st.table(data=dados)
st.write(pd.DataFrame(dados))
# media e % das objetivas 
media_acerto_materia = pd.read_pickle('dados-relatorio-docentes/media_acerto_materia.pkl')
media_acertos_obj = media_acerto_materia['correcao'].mean()

# print(media_acertos_obj)
st.subheader("**1.1 Dados sobre as Questões Objetivas**")

st.write("A média de acertos da prova objetiva foi: ", str(round(media_acertos_obj, 1)*100)+'%')
st.write(pd.DataFrame({
   'Média de acertos': [media_acertos_obj],
}))
# media geral de acertos por materia
def get_media_a_m():
    path = 'dados-relatorio-docentes/media_acerto_materia.pkl'
    return pd.read_pickle(path)
    

st.markdown("**Média de acertos por matéria (em %)**")

media_acerto_materia = get_media_a_m()
media_acerto_materia = media_acerto_materia.reset_index()


# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
media_acerto_materia.set_index('materia',inplace=True)


st.write(pd.DataFrame({
   'Média de acertos': media_acerto_materia['correcao']*100
}))

media_acerto_materia = get_media_a_m()

# print(media_acerto_materia)

# gráfico com a média de acerto de cada matéria

media_acerto_materia = media_acerto_materia.reset_index()
media_acerto_materia = media_acerto_materia.set_index('correcao')

st.bar_chart(data=media_acerto_materia[["materia"]])

# media e % da redação
media_redacao = pd.read_pickle('dados-relatorio-docentes/media_redacao.pkl')
# print(media_redacao)

# tabela com os dados coletados acima
st.subheader("**1.2 Dados sobre a Redação**")
st.write(pd.DataFrame({
    'Nota Média': media_redacao
}))


# tabela com a colocação dos alunos

colocacao = pd.read_pickle('dados-relatorio-alunos/colocacao.pkl')
st.subheader("**1.3   Colocação dos alunos do Einstein**")
colocacao.set_index('Colocação',inplace=True)
st.write(pd.DataFrame({
    'Nome': colocacao['nome'],
    'Pontos': colocacao['Nota total'],
    "Porcentagem de Acerto": colocacao['% de acerto']*100
}))





#  ! dados específicos por matéria  ! 




#### para cada materia

# questões separadas por materia e por assunto
# # tem o total de acertos, total de alunos que responderam e média de acerto

# print(media_acerto_materia)
media_acerto_materia = get_media_a_m()
media_acerto_materia = media_acerto_materia.reset_index()

materia_escolhida = st.sidebar.selectbox("Escolha a materia", media_acerto_materia['materia'])

dados_materia_escolhida = media_acerto_materia[(media_acerto_materia['materia'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
dados_materia_escolhida.set_index('materia',inplace=True)

st.header("**2. Dados sobre a Matéria Selecionada**")


# st.write("A média em ", str(dados_materia_escolhida.index), " foi ", dados_materia_escolhida['correcao'])
st.write(pd.DataFrame({
    "Média Acertos(em %)": dados_materia_escolhida['correcao']*100
}))



# todas as questões separadas por matéria
# #  tem o total de acertos, total de alunos que responderam e média de acerto
media_acerto_questao = pd.read_pickle('dados-relatorio-docentes/media_acerto_questao.pkl')

st.subheader("**2.1   Média de acertos por questao**")
st.write("Nesta seção são discretizados os acertos por questão")
media_acerto_questao = media_acerto_questao.reset_index()
questao_materia_escolhida = media_acerto_questao[(media_acerto_questao['materia'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
questao_materia_escolhida.set_index('questao',inplace=True)


print(questao_materia_escolhida)
# st.table(data=questao_materia_escolhida[['assunto','dificuldade', 'Média']])


st.write(pd.DataFrame({
    "Assunto": questao_materia_escolhida['assunto'],
    "Dificuldade": questao_materia_escolhida['dificuldade'],
    "Total Acertos": questao_materia_escolhida['Total Acertos'],
    'Média (em %)': round(questao_materia_escolhida['Média']*100, 1)
}))

grafico_questoes = questao_materia_escolhida['correcao','Média']
grafico_questoes = grafico_questoes.reset_index()
grafico_questoes['questao'] = grafico_questoes['questao'].astype(str)
grafico_questoes["media"] = grafico_questoes['correcao','Média']
# grafico_questoes = grafico.drop(columns=('correcao','Média'))
grafico_questoes.set_index('questao',inplace=True)

st.bar_chart(data=grafico_questoes['media'])


# questões separadas por materia e por assunto
# #  tem o total de acertos, total de alunos que responderam e média de acerto

def get_media_p_a():
    path = 'dados-relatorio-docentes/media_por_assunto.pkl'
    return pd.read_pickle(path)
media_por_assunto = get_media_p_a()
# print(media_por_assunto)

media_por_assunto = media_por_assunto.reset_index()
assuntos_materia_escolhida = media_por_assunto[(media_por_assunto['materia'] == materia_escolhida)]

# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
assuntos_materia_escolhida.set_index('assunto',inplace=True)

st.subheader("**2.2   Média de acertos por assunto**")

st.write(pd.DataFrame({
    "Total Acertos": assuntos_materia_escolhida['correcao','Total Acertos'],
    'Total Respostas': assuntos_materia_escolhida['correcao','Total Respostas'],
    'Média (em %)': round(assuntos_materia_escolhida['correcao','Média']*100,3)
}))



# analise dos acertos por dificuldade
media_por_dificuldade = pd.read_pickle('dados-relatorio-docentes/media_por_dificuldade.pkl')

st.subheader("**2.3   Média de acertos por dificuldade**")

media_por_dificuldade = media_por_dificuldade.reset_index()
dificuldade_materia_escolhida = media_por_dificuldade[(media_por_dificuldade['materia'] == materia_escolhida)]


# para nao mostrar on indices do dataframe na tabela do streamlit, podemos mudar o indice
dificuldade_materia_escolhida.set_index('dificuldade',inplace=True)

st.write(pd.DataFrame({
    "Total Acertos": dificuldade_materia_escolhida['correcao','Total Acertos'],
    'Total Respostas': dificuldade_materia_escolhida['correcao','Total Respostas'],
    'Média (em %)': round(dificuldade_materia_escolhida['correcao','Média']*100,3)		
}))