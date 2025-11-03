import pandas as pd
import scipy.stats
import streamlit as st
import time
import altair as alt # NOVO: Importe para visualização avançada

# --- Dicionário de Textos (Multi-idioma) ---
TEXTS = {
    'pt': {
        'title': '🪙 Jogando uma moeda',
        'description': "Este experimento simula o lançamento de uma moeda não viciada (probabilidade $P=0.5$). A **Lei dos Grandes Números** diz que, quanto mais lançamentos você fizer, mais a média observada (proporção de Caras) se aproximará do valor esperado teórico de 0.5. Use o controle deslizante para definir o número de tentativas e clique em **Executar** para iniciar.",
        'slider_label': 'Número de tentativas?',
        'execute_button': 'Executar',
        'running_message': '🚀 Executando o Experimento de {n} tentativas.',
        'success_message': '✅ Experimento #{n} concluído. Média: {mean:.4f}',
        'history_header': '📊 Histórico de Resultados Acumulados',
        'download_button': 'Baixar Resultados (CSV)',
        'clear_button': 'Limpar Histórico',
        'caption': 'Ainda não é um aplicativo funcional. Em construção.',
        'graph_title_1': 'Convergência da Média para o Valor Esperado',
        'graph_title_2': '(Lei dos Grandes Números)',
        'x_axis': 'Número de Lançamentos',
        'y_axis': 'Média de Ocorrências',
        'sim_legend': 'Simulação',
        'exp_legend': 'Esperado (Teórico)',
        'clear_toast': 'Histórico de experimentos limpo!',
        'language_button': 'Switch to English 🇺🇸',
        'mean_type_label': 'Tipo de Média' # NOVO: Rótulo da coluna da legenda
    },
    'en': {
        'title': '🪙 Coin Toss Simulation',
        'description': "This experiment simulates the toss of an unbiased coin (probability $P=0.5$). The **Law of Large Numbers** states that the more trials you run, the closer the observed mean (proportion of Heads) will approach the theoretical expected value of 0.5. Use the slider to set the number of trials and click **Execute** to start.",
        'slider_label': 'Number of trials?',
        'execute_button': 'Execute',
        'running_message': '🚀 Running Experiment with {n} trials.',
        'success_message': '✅ Experiment #{n} finished. Mean: {mean:.4f}',
        'history_header': '📊 Accumulated Results History',
        'download_button': 'Download Results (CSV)',
        'clear_button': 'Clear History',
        'caption': 'This is not yet a functional application. Under construction.',
        'graph_title_1': 'Convergence of the Mean to the Expected Value',
        'graph_title_2': '(Law of Large Numbers)',
        'x_axis': 'Number of Tosses',
        'y_axis': 'Mean of Occurrences',
        'sim_legend': 'Simulation',
        'exp_legend': 'Expected (Theoretical)',
        'clear_toast': 'Experiment history cleared!',
        'language_button': 'Mudar para Português 🇧🇷',
        'mean_type_label': 'Mean Type' # NOVO: Rótulo da coluna da legenda
    }
}

# --- Funções de Ajuda para i18n ---
def get_current_language():
    """Retorna o código do idioma atual ('pt' ou 'en')."""
    return st.session_state.get('language', 'pt') # Padrão: Português

def get_text(key):
    """Retorna o texto correspondente à chave no idioma atual."""
    lang = get_current_language()
    return TEXTS[lang].get(key, TEXTS['pt'].get(key, f'MISSING TEXT: {key}'))

def toggle_language():
    """Alterna entre Português e Inglês e força o Streamlit a re-executar."""
    current_lang = get_current_language()
    new_lang = 'en' if current_lang == 'pt' else 'pt'
    st.session_state['language'] = new_lang

# --- Injeção de CSS para Remover Espaço Superior e Ajustar Botão ---
# Isso reduz o padding padrão que o Streamlit coloca no topo da página.
st.markdown("""
<style>
    /* Alvo: container principal da página Streamlit */
    .block-container {
        padding-top: 3rem; /* Reduz o padding superior para um valor menor (1rem = ~16px) */
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    /* Alvo: o elemento que contém o título H1/H2, ajustando sua margem superior */
    h1 {
        margin-top: 0rem; 
        padding-top: 0rem;
    }
    /* NOVO: Reduz a altura dos botões para torná-los menos altos */
    .stButton > button {
        padding-top: 4px !important;
        padding-bottom: 4px !important;
        line-height: 1; /* Ajuda a centralizar o texto após reduzir o padding */
    }
</style>
""", unsafe_allow_html=True)

# --- Variáveis Persistentes (Session State) ---
# Inicializa o estado do idioma se não existir
if 'language' not in st.session_state:
    st.session_state['language'] = 'pt' 
    
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
    st.toast(get_text('clear_toast'), icon='🗑️')

# --- Função de Criação do Gráfico Altair ---
def create_altair_chart(data_points):
    """Cria o gráfico Altair com linha pontilhada para o valor teórico."""
    
    # 1. Prepara o DataFrame para Altair
    # Transforma a lista de dicionários em DataFrame e adiciona a coluna de índice (Iteração)
    df_chart = pd.DataFrame(data_points).reset_index().rename(columns={'index': 'Iteração'})
    
    # Mapeia as legendas do gráfico de acordo com o idioma
    df_chart = df_chart.rename(columns={
        'Simulação': get_text('sim_legend'),
        'Esperado (Teórico)': get_text('exp_legend')
    })

    # NOVO: Obtém o nome da coluna de média traduzido
    mean_type_column_name = get_text('mean_type_label')

    # Derrete (melt) o DataFrame para ter as colunas na mesma coluna 'Tipo de Média'
    df_melted = df_chart.melt(
        id_vars=['Iteração'], 
        value_vars=[get_text('sim_legend'), get_text('exp_legend')],
        var_name=mean_type_column_name, # CORRIGIDO: Usa o nome traduzido da coluna
        value_name='Valor'
    )

    # 2. Configuração Base do Gráfico
    base = alt.Chart(df_melted).encode(
        # CORREÇÃO AQUI: Adicionado format='d' para forçar o eixo X a usar formato de inteiro
        x=alt.X('Iteração:Q', axis=alt.Axis(title=get_text('x_axis'), format='d')),
        y=alt.Y('Valor:Q', scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(title=get_text('y_axis'))),
        color=f'{mean_type_column_name}:N' # CORRIGIDO: Usa a coluna traduzida na codificação de cor
    ).properties(
        # Título agora é dinâmico
        title=[
            get_text('graph_title_1'), 
            get_text('graph_title_2')
        ],
        height=450 # NOVO: Define uma altura fixa de 450 pixels
    )

    # 3. Estilização da Linha (aqui entra o pontilhado)
    line = base.mark_line().encode(
        # Condição que aplica o estilo tracejado/pontilhado à linha 'Esperado (Teórico)' (usando o texto dinâmico)
        strokeDash=alt.condition(
            alt.datum['Tipo de Média'] == get_text('exp_legend'),
            alt.value([5, 5]), # [tamanho do traço, tamanho do espaço]
            alt.value([0])     # Linha sólida para Simulação
        )
    ).interactive()
    
    # 4. Configuração da Legenda (Move a legenda para a parte inferior)
    line = line.configure_legend(
        orient='bottom'        # Define a orientação para a parte inferior
    )
    
    return line


# --- Interface do Usuário ---

# 1. Título (mantido fora de colunas)
st.header(get_text('title'))

# 2. Botão de Idioma (Menos alto, mais largo, alinhado à esquerda)
# Usamos colunas para controlar a largura, mantendo o alinhamento esquerdo
col_lang_wide, _ = st.columns([1.5, 5]) # Coluna 1.5 para o botão, 5 para o espaço vazio

with col_lang_wide:
    st.button(
        get_text('language_button'), 
        on_click=toggle_language, 
        use_container_width=True # Garante que ele ocupe a largura da coluna 1.5
    )

# 3. Descrição do Experimento agora é dinâmica
st.markdown(get_text('description'))

# NOVO: Cria um placeholder para o gráfico Altair. O gráfico será renderizado DEPOIS da simulação.
chart_placeholder = st.empty()

# Inicializa o placeholder com um gráfico simples para exibição
chart_placeholder.altair_chart(
    create_altair_chart([{'Simulação': 0.5, 'Esperado (Teórico)': 0.5}]),
    use_container_width=True
)

# --- Função Principal de Simulação (agora coleta dados E renderiza) ---
def toss_coin(n, chart_placeholder):
    """Simula o lançamento de moeda, coleta a média e renderiza o gráfico progressivamente."""
    
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    
    # MUDANÇA AQUI: Começa a lista de pontos com o estado inicial (0 iterações)
    data_points = [{'Simulação': 0.5, 'Esperado (Teórico)': 0.5}]
    
    outcome_no = 0
    outcome_1_count = 0
    
    # Define a frequência de renderização para simular a animação (máximo 50 updates)
    # RENDER_FREQUENCY garante que o gráfico não tente renderizar a cada lançamento em n=1000
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
        # Renderiza no último ponto ou quando atingir a frequência definida
        # O índice (i) aqui se refere ao trial_outcomes (0 a n-1).
        if i == n - 1 or (i + 1) % RENDER_FREQUENCY == 0:
            chart_placeholder.altair_chart(
                create_altair_chart(data_points), 
                use_container_width=True
            )
            time.sleep(0.1) # Pausa aumentada para 0.1s para desacelerar a animação

    return mean, data_points # Retorna a média final E a lista de pontos


# --- Interface do Usuário (Slider e Botão Lado a Lado) ---

# 1. Cria duas colunas para o slider e o botão
col_slider, col_button = st.columns([4, 1])

with col_slider:
    # Slider para selecionar o número de tentativas (rótulo dinâmico)
    number_of_trials = st.slider(get_text('slider_label'), 1, 1000, 10)

with col_button:
    # Botão para iniciar o experimento, alinhado com o slider (rótulo dinâmico)
    st.write(" ") # Adiciona um pequeno espaço para alinhamento vertical
    start_button = st.button(get_text('execute_button'), use_container_width=True)


# --- Lógica de Execução e Armazenamento ---
if start_button:
    # 1. Mensagem inicial (dinâmica)
    st.write(get_text('running_message').format(n=number_of_trials))
    
    # 2. Incrementa o contador de experimento (persistente)
    st.session_state['experiment_no'] += 1

    # 3. Adiciona a barra de progresso antes da simulação
    progress_bar = st.progress(0, text="Simulando Lançamentos...")
    
    # Simulação Rápida da barra de progresso (visual imediato)
    for i in range(10):
        time.sleep(0.02)
        progress_bar.progress(min(100, (i + 1) * 10))
    
    # 4. Executa a simulação e obtém a média final e os dados de plotagem
    mean, data_points = toss_coin(number_of_trials, chart_placeholder) 

    # 5. Limpa a barra de progresso
    progress_bar.empty()

    # 6. Cria o registro de um único experimento
    new_result = pd.DataFrame(
        [[st.session_state['experiment_no'], number_of_trials, mean]],
        # As colunas internas do DataFrame devem permanecer fixas
        columns=['no', 'iterations', 'mean']
    )
    
    # 7. Concatena o novo resultado com o DataFrame persistente
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_result],
        ignore_index=True 
    )
    
    # Mensagem de sucesso (dinâmica)
    st.success(get_text('success_message').format(n=st.session_state["experiment_no"], mean=mean))


# --- Exibição dos Resultados e Opções ---
st.write('---')
# Subcabeçalho dinâmico
st.subheader(get_text('history_header'))

# Exibe o DataFrame salvo na sessão
st.dataframe(st.session_state['df_experiment_results'], hide_index=True)

# Contêiner para os botões de Download e Limpar
col_download, col_clear, _ = st.columns([1, 1, 3])

# 8. Adiciona o botão de download (rótulo dinâmico)
with col_download:
    csv_data = st.session_state['df_experiment_results'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label=get_text('download_button'),
        data=csv_data,
        file_name='resultados_moeda.csv',
        mime='text/csv',
        disabled=st.session_state['experiment_no'] == 0
    )

# 9. Adiciona o botão para limpar o histórico (rótulo dinâmico)
with col_clear:
    st.button(
        get_text('clear_button'), 
        on_click=clear_results,
        disabled=st.session_state['experiment_no'] == 0
    )

st.write('\n')
st.caption(get_text('caption'))
