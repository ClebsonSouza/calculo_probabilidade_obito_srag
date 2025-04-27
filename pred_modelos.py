#pip install pyexcel
#pip install pyexcel-xls

import pyexcel as p
import pandas as pd
import numpy as np
import statistics
import streamlit as st
from io import BytesIO
from unidecode import unidecode
import os
import re
from zipfile import ZipFile
import pickle

import time
import streamlit as st

dir_modelos = 'modelos'

with open(f'{dir_modelos}/modelo_dtc.pkl', 'rb') as arquivo_dtc:
    modelo_dtc = pickle.load(arquivo_dtc)

with open(f'{dir_modelos}/modelo_rfc.pkl', 'rb') as arquivo_rfc:
    modelo_rfc = pickle.load(arquivo_rfc)

with open(f'{dir_modelos}/modelo_xgb.pkl', 'rb') as arquivo_xgb:
    modelo_xgb = pickle.load(arquivo_xgb)

with open(f'{dir_modelos}/modelo_lgbm.pkl', 'rb') as arquivo_lgbm:
    modelo_lgbm = pickle.load(arquivo_lgbm)

# with open(f'{dir_modelos}/modelo_rna.pkl', 'rb') as arquivo_rna:
#     modelo_rna = pickle.load(arquivo_rna)

def probabilidade(idade, branca, diarreia, nosocomial, tosse, desc_resp,  
                  fator_risco, uti, sup_vent_inv, sup_vent_n_inv,
                  class_n_srag, vacina_cov):

    prob = (1)/(1 + np.exp(-(-4.9152 + 0.0315 * idade - 0.4581 * branca + 0.4929 * diarreia + 0.6228 * nosocomial
                             - 0.4022 * tosse + 0.5676 * desc_resp + 
                             0.5289 * fator_risco + 1.2039 * uti +
                             2.6350 * sup_vent_inv + 0.6366 * sup_vent_n_inv + 1.8717 * class_n_srag - 0.2315 * vacina_cov)))

    return prob

def df_X(idade, branca, diarreia, nosocomial, tosse, desc_resp, 
                  fator_risco, uti, sup_vent_inv, sup_vent_n_inv,
                  class_n_srag, vacina_cov):
    
    data = {'IDADE_AJUS': [idade],
            'CS_RACA_BRANCA_SIM': [branca],
            'DIARREIA_SIM': [diarreia],
            'NOSOCOMIAL_SIM': [nosocomial],
            'TOSSE_SIM': [tosse],
            'DESC_RESP_SIM': [desc_resp],            
            'UTI_SIM': [uti],
            'SUPORT_VEN_INVASIVO': [sup_vent_inv],
            'SUPORT_VEN_NAO_INVASIVO': [sup_vent_n_inv],
            'CLASSI_FIN_SRAG_OUTRO_AGENTE_ETIOLOGICO': [class_n_srag],
            'FATOR_RISC_SIM': [fator_risco],
            'VACINA_COV_SIM': [vacina_cov]}

    df = pd.DataFrame(data)

    return df

#############

# Função para autenticação com múltiplos usuários
def autenticar_usuario(usuario, senha):
    # Dicionário com usuários e suas respectivas senhas
    credenciais = {
        "clebson": "123",
        "admin": "123",
        "teste": "4321",
        # Adicione mais usuários aqui
    }
    
    # Verifica se o usuário está no dicionário e se a senha está correta
    if usuario in credenciais and credenciais[usuario] == senha:
        return True
    else:
        return False

# Verifica se o usuário já está autenticado
if 'autenticado' not in st.session_state:
    st.session_state['autenticado'] = False
    

# Tela de login com formulário para permitir envio com "Enter"
if not st.session_state['autenticado']:
    st.title("Cálculo da probabilidade do Óbito (SRAG)")
    st.write("*usuário: teste, senha: 4321")    
        
    # Formulário de login
    with st.form("login_form"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        # Botão de enviar (submit), que também é acionado ao pressionar "Enter"
        submit_button = st.form_submit_button("Entrar")
    
    # Verifica se o formulário foi enviado
    if submit_button:
        if autenticar_usuario(usuario, senha):
            st.session_state['autenticado'] = True  # Marca o estado de autenticação como verdadeiro

            st.success(f"Login bem-sucedido! Bem-vindo, {usuario}!")

            time.sleep(1)

            st.rerun()          
            
        else:
            st.error("Usuário ou senha incorretos.")  # Exibe erro se a autenticação falhar
else:    
    # Aplicação principal que é exibida após o login bem-sucedido
    st.sidebar.title("PROBABILIDADE DE ÓBITO PARA SÍNDROME RESPIRATÓRIA AGUDA GRAVE (SRAG)")    

    st.sidebar.write("Calcula a probabilidade do evento 'Óbito' a partir de modelos de inteligência artificial com base em dados do sistema SIVEP Gripe")

    st.sidebar.write("-------------------------------------")

    st.sidebar.write("A aplicação foi desenvolvida exclusivamente para fins didáticos, servindo como uma das diversas formas de aplicação prática da pesquisa em questão.")

    st.sidebar.write("-------------------------------------")

    st.title("CÁLCULO DA PROBABILIDADE DO EVENTO ÓBITO PARA SRAG")

    coluna_1, coluna_2 = st.columns(2, gap = 'large', vertical_alignment='center')

    # Estado inicial para as variáveis
    if 'reset' not in st.session_state:
        st.session_state['reset'] = 'Não'
    
    #idade = st.slider('Idade (anos)', 0, 120, 1)

    
    with coluna_1:

        idade = st.number_input("Idade (anos)", min_value=0, max_value= 120, value=30, key="idade_reset")
        # Entradas para variáveis binárias com "Sim" ou "Não"
        branca = st.selectbox("Cor ou raça declarada pelo paciente é Branca?", ['Não', 'Sim'], key="branca_reset" if st.session_state['reset'] else "branca")    
        diarreia = st.selectbox("Paciente apresentou diarreia?", ['Não', 'Sim'], key='diarreia_key')
        nosocomial = st.selectbox("Caso de SRAG com infecção adquirida após internação (Nosocomial)?", ['Não', 'Sim'], key="nosocomial_reset" if st.session_state['reset'] else "nosocomial")
        tosse = st.selectbox("Paciente apresentou tosse?", ['Não', 'Sim'], key="tosse_reset" if st.session_state['reset'] else "tosse")
        desc_resp = st.selectbox("Paciente apresentou desconforto respiratório?  ", ['Não', 'Sim'], key="desc_resp_reset" if st.session_state['reset'] else "dispneia")
        
    
    with coluna_2:

        fator_risco = st.selectbox("Paciente apresenta algum fator de risco?", ['Não', 'Sim'], key="fator_risco_reset" if st.session_state['reset'] else "fator_risco")
        uti = st.selectbox("Foi internado na UTI?", ['Não', 'Sim'], key="uti_reset" if st.session_state['reset'] else "uti")
        sup_vent_inv = st.selectbox("O paciente fez uso de Suporte Ventilatório Invasivo?", ['Não', 'Sim'], key="sup_vent_inv_reset" if st.session_state['reset'] else "sup_vent_inv")

        if sup_vent_inv == 'Sim':
            sup_vent_n_inv = st.selectbox("O paciente fez uso de Suporte Ventilatório Não Invasivo?", ['Não'], key="sup_vent_n_inv", disabled=True)
        else:
            sup_vent_n_inv = st.selectbox("O paciente fez uso de Suporte Ventilatório Não Invasivo?", ['Não', 'Sim'], key="sup_vent_n_inv", disabled=False)

        #sup_vent_u_inv = st.selectbox("O paciente fez uso de Suporte Ventilatório Invasivo?", ['Não', 'Sim'], key="sup_vent_u_inv_reset" if st.session_state['reset'] else "sup_vent_u_inv")
        class_n_srag = st.selectbox("Classificação Final (outro agente etiológico)?", ['Não', 'Sim'], key="class_outro_agen_reset" if st.session_state['reset'] else "class_outro_agen")
        vacina_cov = st.selectbox("Recebeu vacina COVID-19?", ['Não', 'Sim'], key="vacina_cov_reset" if st.session_state['reset'] else "vacina_cov")
            
    # Converter as respostas "Sim" e "Não" em 0 e 1

    branca = 1 if branca == 'Sim' else 0
    diarreia = 1 if diarreia == 'Sim' else 0
    nosocomial = 1 if nosocomial == 'Sim' else 0
    tosse = 1 if tosse == 'Sim' else 0
    desc_resp = 1 if desc_resp == 'Sim' else 0       
    fator_risco = 1 if fator_risco == 'Sim' else 0
    uti = 1 if uti == 'Sim' else 0
    sup_vent_inv = 1 if sup_vent_inv == 'Sim' else 0
    sup_vent_n_inv = 1 if sup_vent_n_inv == 'Sim' else 0
    class_n_srag = 1 if class_n_srag == 'Sim' else 0
    vacina_cov = 1 if vacina_cov == 'Sim' else 0   

    # Botão para calcular a probabilidade
    if st.button("Calcular probabilidade do óbito"):
        # Cálculo da probabilidade
        prob = probabilidade(idade, diarreia, branca, nosocomial, tosse, desc_resp,
                            fator_risco, uti, sup_vent_inv, sup_vent_n_inv,
                            class_n_srag, vacina_cov)

        # Exibir resultado
        st.success(f"Logit Regression: {prob * 100:.2f}%")        

        df = df_X(idade, diarreia, branca, nosocomial, tosse, desc_resp, 
                            fator_risco, uti, sup_vent_inv, sup_vent_n_inv,
                            class_n_srag, vacina_cov)       

        st.success(f"Decision Tree: {(modelo_dtc.predict_proba(df)[:, -1][0]):.2%}")
        st.success(f"Random Forest: {(modelo_rfc.predict_proba(df)[:, -1][0]):.2%}")
        st.success(f"XGBoost: {(modelo_xgb.predict_proba(df)[:, -1][0]):.2%}")
        st.success(f"LightGBM: {(modelo_lgbm.predict_proba(df)[:, -1][0]):.2%}")
        #st.success(f"Rede Neural: {float(modelo_rna.predict(df)[0][0]):.6f}")
        #st.success(f"Rede Neural: {np.squeeze(modelo_rna.predict(df)):.6f}")

        #df.to_excel('teste_X.xlsx', index = False)

    # Botão para limpar os dados e voltar às configurações originais
    if st.button("Limpar"):
        st.session_state['reset'] = False        
        st.rerun()       

    # Adiciona um botão de logout
    if st.button("Sair"):
        st.session_state['autenticado'] = False  # Reseta o estado de autenticação
        st.rerun()

####################################################################################
####################################################################################