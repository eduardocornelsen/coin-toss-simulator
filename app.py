import pandas as pd
import scipy.stats
import streamlit as st
import time
import altair as alt # NOVO: Importe para visualização avançada

# --- Variáveis Persistentes (Session State) ---
# Estas variáveis são preservadas à medida que o Streamlit executa novamente este script
if 'experiment_no' not in st.session_state:
    # Inicializa o contador de experimentos
    st.session_state['experiment_no'] = 0 

if 'df_experiment_results' not in st.session_state:
    # Inicializa o DataFrame para armazenar os resultados
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

# --- Função de Callback para Limpar Resultados ---
def clear_results():
    """Limpa o contador e o DataFrame de resultados no Session State."""
    st.session_state['experiment_no'] = 0
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])
    st.toast('Histórico de experimentos limpo!', icon='🗑️')

# --- Função de Criação do Gráfico Altair ---
def create_altair_chart(data_points):
    """Cria o gráfico Altair com linha pontilhada para o valor teórico."""
    
    # 1. Prepara o DataFrame para Altair
    # Transforma a lista de dicionários em DataFrame e adiciona a coluna de índice (Iteração)
    df_chart = pd.DataFrame(data_points).reset_index().rename(columns={'index': 'Iteração'})
    
    # Derrete (melt) o DataFrame para ter as colunas 'Simulação' e 'Esperado' na mesma coluna 'Tipo de Média'
    df_melted = df_chart.melt(
        id_vars=['Iteração'], 
        value_vars=['Simulação', 'Esperado (Teórico)'],
        var_name='Tipo de Média', 
        value_name='Valor'
    )

    # 2. Configuração Base do Gráfico
    base = alt.Chart(df_melted).encode(
        # CORREÇÃO AQUI: Adicionado format='d' para forçar o eixo X a usar formato de inteiro
        x=alt.X('Iteração:Q', axis=alt.Axis(title='Número de Lançamentos', format='d')),
        y=alt.Y('Valor:Q', scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(title='Média de Ocorrências')),
        color='Tipo de Média:N' # Usa a coluna 'Tipo de Média' para diferenciar as cores
    ).properties(
        # Título dividido em duas linhas para evitar truncamento
        title=[
            'Convergência da Média para o Valor Esperado (Lei dos Grandes Números)'
        ],
        height=500,
        width=20  # Define uma altura fixa de 600 pixels
    )

    # 3. Estilização da Linha (aqui entra o pontilhado)
    line = base.mark_line().encode(
        # Condição que aplica o estilo tracejado/pontilhado à linha 'Esperado (Teórico)'
        strokeDash=alt.condition(
            alt.datum['Tipo de Média'] == 'Esperado (Teórico)',
            alt.value([5, 5]), # [tamanho do traço, tamanho do espaço]
            alt.value([0])     # Linha sólida para Simulação
        )
    ).interactive()
    
    # 4. Configuração da Legenda (Move a legenda para a parte inferior)
    line = line.configure_legend(
        orient='bottom'        # Define a orientação para a parte inferior
        # REMOVIDO: titleOrient='bottom' para evitar conflito com o título superior.
    )
    
    return line


# --- Interface do Usuário ---
st.header('🪙 Jogando uma moeda')

# NOVO: Descrição do Experimento
st.markdown(
    """
    Este experimento simula o lançamento de uma moeda não viciada (probabilidade $P=0.5$). 
    A **Lei dos Grandes Números** diz que, quanto mais lançamentos você fizer, mais a média 
    observada (proporção de Caras) se aproximará do valor esperado teórico de 0.5.
    
    Use o controle deslizante para definir o número de tentativas e clique em **Executar** para iniciar.
    """
)

# NOVO: Cria um placeholder para o gráfico Altair. O gráfico será renderizado DEPOIS da simulação.
chart_placeholder = st.empty()

# Inicializa o placeholder com um gráfico simples para exibição
chart_placeholder.altair_chart(
    create_altair_chart([{'Simulação': 0.5, 'Esperado (Teórico)': 0.5}]),
    use_container_width=True
)

# --- Função Principal de Simulação (agora coleta dados E renderiza) ---
def toss_coin(n, chart_placeholder, progress_bar): # Adicionado progress_bar
    """Simula o lançamento de moeda, coleta a média e renderiza o gráfico progressivamente."""
    
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    
    # MUDANÇA AQUI: Começa a lista de pontos com o estado inicial (0 iterações)
    data_points = [{'Simulação': 0.5, 'Esperado (Teórico)': 0.5}]
    
    outcome_no = 0
    outcome_1_count = 0
    
    # Define a frequência de renderização para simular a animação (máximo 50 updates)
    RENDER_FREQUENCY = max(1, n // 50) 

    # Itera sobre os resultados
    for i, r in enumerate(trial_outcomes):
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
            
        mean = outcome_1_count / outcome_no 
        
        # Armazena o ponto
        data_points.append({'Simulação': mean, 'Esperado (Teórico)': 0.5})

        # NOVO: Renderiza o gráfico periodicamente
        if i == n - 1 or (i + 1) % RENDER_FREQUENCY == 0:
            chart_placeholder.altair_chart(
                create_altair_chart(data_points), 
                use_container_width=True
            )
            # ATUALIZAÇÃO SINCRONIZADA DA BARRA DE PROGRESSO
            progress = (i + 1) / n
            progress_bar.progress(progress, text=f"Lançamento {i+1} de {n}...")
            
            time.sleep(0.1) # Pausa para desacelerar a animação

    return mean, data_points # Retorna a média final E a lista de pontos


# Slider para selecionar o número de tentativas
number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
# Botão para iniciar o experimento
start_button = st.button('Executar')

# --- Lógica de Execução e Armazenamento ---
if start_button:
    # 1. Mensagem inicial
    st.write(f'🚀 Executando o Experimento de {number_of_trials} tentativas.')
    
    # 2. Incrementa o contador de experimento (persistente)
    st.session_state['experiment_no'] += 1

    # 3. Adiciona a barra de progresso antes da simulação
    # Esta barra será controlada pela função toss_coin
    progress_bar = st.progress(0, text="Preparando Simulação...")
    
    # 4. Executa a simulação e obtém a média final e os dados de plotagem
    # NOTE: Passando o progress_bar como argumento
    mean, data_points = toss_coin(number_of_trials, chart_placeholder, progress_bar) 

    # 5. Limpa a barra de progresso
    progress_bar.empty()

    # 6. Cria o registro de um único experimento
    new_result = pd.DataFrame(
        [[st.session_state['experiment_no'], number_of_trials, mean]],
        columns=['no', 'iterations', 'mean']
    )
    
    # 7. Concatena o novo resultado com o DataFrame persistente
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_result],
        ignore_index=True 
    )
    
    st.success(f'✅ Experimento #{st.session_state["experiment_no"]} concluído. Média: {mean:.4f}')


# --- Exibição dos Resultados e Opções ---
st.write('---')
st.subheader('📊 Histórico de Resultados Acumulados')

# Exibe o DataFrame salvo na sessão
st.dataframe(st.session_state['df_experiment_results'], hide_index=True)

# Contêiner para os botões de Download e Limpar
col_download, col_clear, _ = st.columns([1, 1, 3])

# 8. Adiciona o botão de download
with col_download:
    csv_data = st.session_state['df_experiment_results'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Baixar Resultados (CSV)",
        data=csv_data,
        file_name='resultados_moeda.csv',
        mime='text/csv',
        disabled=st.session_state['experiment_no'] == 0
    )

# 9. Adiciona o botão para limpar o histórico
with col_clear:
    st.button(
        'Limpar Histórico', 
        on_click=clear_results,
        disabled=st.session_state['experiment_no'] == 0
    )

st.write('\n')
st.caption('Ainda não é um aplicativo funcional. Em construção.')
