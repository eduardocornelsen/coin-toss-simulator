import pandas as pd
import scipy.stats
import streamlit as st
import time
import altair as alt # Import for advanced visualization

# --- Text Dictionary (Multi-language) ---
TEXTS = {
    'pt': {
        'title': '🪙 Jogando uma moeda',
        'description': "Este experimento simula o lançamento de uma moeda não viciada (probabilidade $P=0.5$). A **Lei dos Grandes Números** diz que, quanto mais lançamentos você fizer, mais a média observada (**Proporção de Caras**) se aproximará do valor esperado teórico de 0.5. Use o controle deslizante para definir o número de tentativas e clique em **Executar** para iniciar.",
        'slider_label': 'Número de tentativas?',
        'execute_button': 'Executar',
        'running_message': '🚀 Executando o Experimento de {n} tentativas...',
        'success_message': '✅ Experimento #{n} concluído. Proporção de Caras: {mean:.4f}',
        'history_header': '📊 Histórico de Resultados Acumulados',
        'download_button': 'Baixar Resultados (CSV)',
        'clear_button': 'Limpar Histórico',
        'caption': 'Ainda não é um aplicativo funcional. Em construção.',
        # ÊNFASE NOS GRÁFICOS E EIXOS PARA 'PROPORÇÃO DE CARAS'
        'graph_title_1': 'Convergência da Proporção de Caras para o Valor Esperado',
        'graph_title_2': '(Lei dos Grandes Números)',
        'x_axis': 'Número de Lançamentos',
        'y_axis': 'Proporção de Caras (Média)',
        'sim_legend': 'Simulação (Caras)',
        'exp_legend': 'Esperado (Teórico)',
        # NOVO: Chaves para Contadores e Tabela
        'result_counts_header': 'Contagem Final do Último Experimento',
        'heads_label': 'Caras (Heads)',
        'tails_label': 'Coroas (Tails)',
        'no_col': 'No.',
        'iterations_col': 'Tentativas',
        'mean_col': 'Proporção (Caras)',
        'heads_col': 'Caras',
        'tails_col': 'Coroas',
        'clear_toast': 'Histórico de experimentos limpo!',
        'language_button': 'Switch to English 🇬🇧',
        'mean_type_label': 'Tipo de Proporção'
    },
    'en': {
        'title': '🪙 Coin Toss Simulation',
        'description': "This experiment simulates the toss of an unbiased coin (probability $P=0.5$). The **Law of Large Numbers** states that the more trials you run, the closer the observed mean (**Heads Proportion**) will approach the theoretical expected value of 0.5. Use the slider to set the number of trials and click **Execute** to start.",
        'slider_label': 'Number of trials?',
        'execute_button': 'Execute',
        'running_message': '🚀 Running Experiment with {n} trials...',
        'success_message': '✅ Experiment #{n} finished. Heads Proportion: {mean:.4f}',
        'history_header': '📊 Accumulated Results History',
        'download_button': 'Download Results (CSV)',
        'clear_button': 'Clear History',
        'caption': 'This is not yet a functional application. Under construction.',
        # ÊNFASE NOS GRÁFICOS E EIXOS PARA 'PROPORTION OF HEADS'
        'graph_title_1': 'Convergence of Heads Proportion to the Expected Value',
        'graph_title_2': '(Law of Large Numbers)',
        'x_axis': 'Number of Tosses',
        'y_axis': 'Proportion of Heads (Mean)',
        'sim_legend': 'Simulation (Heads)',
        'exp_legend': 'Expected (Theoretical)',
        'result_counts_header': 'Absolute Counts of Last Experiment',
        'heads_label': 'Heads',
        'tails_label': 'Tails',
        'no_col': 'No.',
        'iterations_col': 'Trials',
        'mean_col': 'Proportion (Heads)',
        'heads_col': 'Heads',
        'tails_col': 'Tails',
        'clear_toast': 'Experiment history cleared!',
        'language_button': 'Mudar para Português 🇧🇷',
        'mean_type_label': 'Proportion Type'
    }
}

# --- Helper Functions for i18n ---
def get_current_language():
    """Returns the current language code ('pt' or 'en')."""
    return st.session_state.get('language', 'pt') # Default: Portuguese

def get_text(key):
    """Returns the text corresponding to the key in the current language."""
    lang = get_current_language()
    return TEXTS[lang].get(key, TEXTS['pt'].get(key, f'MISSING TEXT: {key}'))

def toggle_language():
    """Toggles between Portuguese and English and forces Streamlit to rerun."""
    current_lang = get_current_language()
    new_lang = 'en' if current_lang == 'pt' else 'pt'
    st.session_state['language'] = new_lang

# --- CSS Injection to Remove Top Space and Adjust Button ---
# This reduces the default padding Streamlit puts at the top of the page.
st.markdown("""
<style>
    /* Target: Streamlit main page container */
    .block-container {
        padding-top: 3rem; /* Reduces top padding to a smaller value (1rem = ~16px) */
        padding-bottom: 0rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    /* Target: the element containing the H1/H2 title, adjusting its top margin */
    h1 {
        margin-top: 0rem; 
        padding-top: 0rem;
    }
    /* Reduces button height to make them less tall */
    .stButton > button {
        padding-top: 4px !important;
        padding-bottom: 4px !important;
        line-height: 1; /* Helps center text after reducing padding */
    }
    
    /* === NEW: Custom Styles for Metric Highlighting === */
    /* Style for Heads (Success/Green, similar to st.success) */
    .heads-container {
        border-left: 5px solid #388E3C; /* Dark Green Border */
        background-color: #E8F5E9; /* Light Green Background */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px; /* Added space below the container */
    }
    /* Style for Tails (Info/Blue, similar to st.info) */
    .tails-container {
        border-left: 5px solid #1976D2; /* Dark Blue Border */
        background-color: #E3F2FD; /* Light Blue Background */
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px; /* Added space below the container */
    }
    
    /* Custom styles for the metric content */
    /* Ensures H2/H3 for value is clean and aligned */
    .metric-value-in-container {
        font-size: 3rem !important; /* FIX: Increased size and added !important */
        font-weight: 600;
        margin-top: 0;
        margin-bottom: 0;
        line-height: 1.1 !important; /* FIX: Added !important */
        color: #000000; /* FIX: Set value text color to black */
    }
    /* Custom style for the metric label within the container */
    .metric-label-in-container {
        font-size: 14px;
        font-weight: bold;
        color: #333333;
        margin-bottom: 5px;
        margin-top: 0;
    }
    /* NEW: Style for Percentage text (smaller, gray) */
    .metric-percentage {
        font-size: 0.9rem;
        color: #666666;
        margin-top: 0px;
        margin-bottom: 0px;
    }
</style>
""", unsafe_allow_html=True)

# --- Persistent Variables (Session State) ---
# Initialize language state if it doesn't exist
if 'language' not in st.session_state:
    st.session_state['language'] = 'pt' 
    
# These variables are preserved as Streamlit reruns this script
if 'experiment_no' not in st.session_state:
    # Initializes the experiment counter
    st.session_state['experiment_no'] = 0 

if 'df_experiment_results' not in st.session_state:
    # Adds columns for absolute counts of Heads and Tails
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean', 'heads', 'tails'])

# --- Callback Function to Clear Results ---
def clear_results():
    """Clears the counter and the results DataFrame in the Session State."""
    st.session_state['experiment_no'] = 0
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean', 'heads', 'tails'])
    st.toast(get_text('clear_toast'), icon='🗑️')

# --- Altair Chart Creation Function ---
def create_altair_chart(data_points):
    """Creates the Altair chart with a dotted line for the theoretical value."""
    
    # 1. Prepare DataFrame for Altair
    # Transforms the list of dictionaries into a DataFrame and adds the index column (Iteration)
    df_chart = pd.DataFrame(data_points).reset_index().rename(columns={'index': 'Iteração'})
    
    # Map chart legends according to the language
    # CORREÇÃO: Mapeia as legendas internas para as chaves de tradução
    df_chart = df_chart.rename(columns={
        get_text('sim_legend'): get_text('sim_legend'), # Mantém a string traduzida
        get_text('exp_legend'): get_text('exp_legend')  # Mantém a string traduzida
    })

    # NEW: Get the translated mean type column name
    mean_type_column_name = get_text('mean_type_label')

    # Melt the DataFrame to have the columns in the same 'Mean Type' column
    df_melted = df_chart.melt(
        id_vars=['Iteração'], 
        value_vars=[get_text('sim_legend'), get_text('exp_legend')],
        var_name=mean_type_column_name, # CORRECTED: Uses the translated column name
        value_name='Valor'
    )

    # 2. Base Chart Configuration
    base = alt.Chart(df_melted).encode(
        # CORRECTION HERE: Added format='d' to force the X-axis to use integer format
        x=alt.X('Iteração:Q', axis=alt.Axis(title=get_text('x_axis'), format='d')),
        y=alt.Y('Valor:Q', scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(title=get_text('y_axis'))),
        color=f'{mean_type_column_name}:N' # CORRECTED: Uses the translated column in color encoding
    ).properties(
        # Title is now dynamic
        title=[
            get_text('graph_title_1'), 
            get_text('graph_title_2')
        ],
        height=450 # NEW: Sets a fixed height of 450 pixels
    )

    # 3. Line Styling (here comes the dotted line)
    line = base.mark_line().encode(
        # Condition that applies the dashed/dotted style to the 'Expected (Theoretical)' line (using dynamic text)
        strokeDash=alt.condition(
            alt.datum[mean_type_column_name] == get_text('exp_legend'), # Uses the translated column here
            alt.value([5, 5]), # [dash size, space size]
            alt.value([0])     # Solid line for Simulation
        )
    ).interactive()
    
    # 4. Legend Configuration (Moves the legend to the bottom)
    line = line.configure_legend(
        orient='bottom'        # Sets the orientation to the bottom
    )
    
    return line


# --- Main Simulation Function (now collects data AND renders) ---
def toss_coin(n, chart_placeholder):
    """Simulates the coin toss, collects the mean, and renders the graph progressively."""
    
    # 1. Simulation: 1 = Heads, 0 = Tails
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    
    # CHANGE HERE: Start the list of points with the initial state (0 iterations)
    # CORREÇÃO: As chaves internas do dict (Simulação e Esperado (Teórico)) DEVEM ser as chaves traduzidas,
    # caso contrário, elas não são encontradas no df_chart.rename logo abaixo.
    data_points = [{get_text('sim_legend'): 0.5, get_text('exp_legend'): 0.5}]
    
    outcome_no = 0
    outcome_1_count = 0 # Heads count
    
    # Define the rendering frequency to simulate the animation (maximum 50 updates)
    RENDER_FREQUENCY = max(1, n // 50) 

    # Iterate over the results
    for i, r in enumerate(trial_outcomes):
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
            
        mean = outcome_1_count / outcome_no 
        
        # Store the point
        # CORREÇÃO: As chaves devem ser traduzidas para serem consistentes com o renomeamento do DataFrame.
        data_points.append({get_text('sim_legend'): mean, get_text('exp_legend'): 0.5})

        # NEW: Renders the chart periodically
        if i == n - 1 or (i + 1) % RENDER_FREQUENCY == 0:
            chart_placeholder.altair_chart(
                create_altair_chart(data_points), 
                use_container_width=True
            )
            time.sleep(0.1) # Pause increased to 0.1s to slow down the animation

    # NEW: Calculates the final Tails count
    outcome_0_count = n - outcome_1_count
    
    # CORRECTED: Returns the final mean, the plot data list AND the absolute counts
    return mean, data_points, outcome_1_count, outcome_0_count 


# --- User Interface ---

# 1. Title (kept outside columns)
st.header(get_text('title'))

# 2. Language Button (Less tall, wider, left-aligned)
# Use columns to control width, maintaining left alignment
col_btn_lang, _ = st.columns([2, 5]) # Column 2/7 for the button, 5/7 empty to make it wider than default

with col_btn_lang:
    st.button(
        get_text('language_button'), 
        on_click=toggle_language, 
        use_container_width=True, # Ensures it fills the width of column [2]
        key="lang_button" # Added key for greater stability
    )

# 3. Experiment Description is now dynamic
st.markdown(get_text('description'))

# === NEW LOCATION FOR SLIDER, BUTTON, AND EXECUTION LOGIC ===

# --- User Interface (Slider and Button Side-by-Side) ---

# 1. Create two columns for the slider and the button
col_slider, col_button = st.columns([4, 1])

with col_slider:
    # Slider to select the number of trials (dynamic label)
    number_of_trials = st.slider(get_text('slider_label'), 1, 1000, 10)

with col_button:
    # Button to start the experiment, aligned with the slider (dynamic label)
    st.write(" ") # Adds a small space for vertical alignment
    start_button = st.button(get_text('execute_button'), use_container_width=True)


# --- CHART DEFINITION LOGIC (MOVED UP) ---

# NEW LOCATION: Create a placeholder for the Altair chart.
chart_placeholder = st.empty()

# Initialize the placeholder with a simple chart for display
# CORREÇÃO: Usa as chaves traduzidas para inicializar o gráfico
chart_placeholder.altair_chart(
    create_altair_chart([{get_text('sim_legend'): 0.5, get_text('exp_legend'): 0.5}]),
    use_container_width=True
)

# --- Execution and Storage Logic ---
if start_button:
    # 1. Initial message (dynamic)
    st.info(get_text('running_message').format(n=number_of_trials))
    
    # 2. Increment experiment counter (persistent)
    st.session_state['experiment_no'] += 1

    # 3. Add progress bar before simulation
    progress_bar = st.progress(0, text="Simulating Tosses...")
    
    # Quick progress bar simulation (immediate visual)
    for i in range(10):
        time.sleep(0.02)
        progress_bar.progress(min(100, (i + 1) * 10))
    
    # 4. Run the simulation and get the final mean, plot data, and counts
    mean, data_points, heads_count, tails_count = toss_coin(number_of_trials, chart_placeholder) 

    # 5. Clear the progress bar
    progress_bar.empty()

    # 6. Create the single experiment record
    new_result = pd.DataFrame(
        # NEW: Includes heads_count and tails_count
        [[st.session_state['experiment_no'], number_of_trials, mean, heads_count, tails_count]],
        # Internal columns (fixed)
        columns=['no', 'iterations', 'mean', 'heads', 'tails'] 
    )
    
    # 7. Concatenate the new result with the persistent DataFrame
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_result],
        ignore_index=True 
    )
    
    # Success message (dynamic)
    st.success(get_text('success_message').format(n=st.session_state["experiment_no"], mean=mean))


# === END OF NEW LOCATION ===

# NEW: Heads and Tails Counters (Visual)
st.markdown("---")

# Título fora do contêiner
st.subheader(get_text('result_counts_header'))

col_heads, col_tails, col_filler = st.columns([1, 1, 3])

# Variáveis para garantir que o resultado mais recente seja usado
last_heads = 0
last_tails = 0
last_mean = 0.0 # NEW: Get the mean value
total_tosses = 0

if not st.session_state['df_experiment_results'].empty:
    last_heads = st.session_state['df_experiment_results']['heads'].iloc[-1]
    last_tails = st.session_state['df_experiment_results']['tails'].iloc[-1]
    last_mean = st.session_state['df_experiment_results']['mean'].iloc[-1] # NEW: Get the mean
    total_tosses = st.session_state['df_experiment_results']['iterations'].iloc[-1]
    
# Calculate percentages using the mean (which is the Heads proportion)
heads_percent = last_mean * 100 
tails_percent = (1 - last_mean) * 100

with col_heads:
    # Start HTML wrapper for success style (Green) and inject content
    st.markdown(f"""
        <div class="heads-container">
            <p class="metric-label-in-container">{get_text("heads_label")}</p>
            <p class="metric-value-in-container">{last_heads}</p>
            <p class="metric-percentage">({heads_percent:.1f}%)</p>
        </div>
    """, unsafe_allow_html=True) 
    
with col_tails:
    # Start HTML wrapper for info style (Blue) and inject content
    st.markdown(f"""
        <div class="tails-container">
            <p class="metric-label-in-container">{get_text("tails_label")}</p>
            <p class="metric-value-in-container">{last_tails}</p>
            <p class="metric-percentage">({tails_percent:.1f}%)</p>
        </div>
    """, unsafe_allow_html=True)
    
st.markdown("---") 


# --- Display Results and Options ---
st.write('---')
# Dynamic subheader
st.subheader(get_text('history_header'))

# NEW: Create a temporary DataFrame for display with translated names
df_display = st.session_state['df_experiment_results'].copy()
# Rename columns to the current language before displaying
df_display.rename(columns={
    'no': get_text('no_col'),
    'iterations': get_text('iterations_col'),
    'mean': get_text('mean_col'),
    'heads': get_text('heads_col'),
    'tails': get_text('tails_col'),
}, inplace=True)

# Display the saved DataFrame in the session
st.dataframe(df_display, hide_index=True)

# Container for Download and Clear buttons
col_download, col_clear, _ = st.columns([1, 1, 3])

# 8. Add the download button (dynamic label)
with col_download:
    csv_data = st.session_state['df_experiment_results'].to_csv(index=False).encode('utf-8')
    st.download_button(
        label=get_text('download_button'),
        data=csv_data,
        file_name='resultados_moeda.csv',
        mime='text/csv',
        disabled=st.session_state['experiment_no'] == 0
    )

# 9. Add the button to clear the history (dynamic label)
with col_clear:
    st.button(
        get_text('clear_button'), 
        on_click=clear_results,
        disabled=st.session_state['experiment_no'] == 0
    )

st.write('\n')
st.caption(get_text('caption'))
