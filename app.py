# Importando pacotes

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import locale
from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder
from IPython.display import HTML

st.set_page_config(layout="wide")
# Funções

locale.setlocale(locale.LC_NUMERIC, 'de_DE.utf8')

# Função para formatar os números com pontos como separadores de milhares
def style_table(df, columns, title):
    def format_with_dots(value):
        if isinstance(value, (int, float)):
            return '{:,.0f}'.format(value).replace(',', '.')
        return value

    styler = df.style.format(format_with_dots, subset=columns)\
        .set_table_styles([
            {'selector': 'thead th',
             'props': [('background-color', 'yellow'), ('color', 'black'), ('font-weight', 'bold')]},
            {'selector': 'td',
             'props': [('text-align', 'center')]}
        ])\
        .map(lambda v: 'color: red' if isinstance(v, int) and v < 0 else 'color: black', subset=columns)\
        .background_gradient(subset=columns, cmap='RdYlGn', axis=1, low=0, high=1)\
        .set_caption(title)

    # Aplica estilos específicos para a última linha
    styler = styler.set_properties(**{'background-color': 'white'}, subset=pd.IndexSlice[df.index[-1], :])

    return styler

def style_table_pct_allcol(df, title):
    def format_as_percent(value):
        if isinstance(value, (int, float)):
            return '{:,.0f}%'.format(value * 100).replace(',', '.')
        return value

    # Apply styles to the DataFrame
    styler_pct = df.style.format(format_as_percent) \
        .set_table_styles([
            {'selector': 'thead th',
             'props': [('background-color', 'yellow'), ('color', 'black'), ('font-weight', 'bold')]},
            {'selector': 'td',
             'props': [('text-align', 'center')]}
        ], overwrite=False) \
        .applymap(lambda v: 'color: red' if isinstance(v, float) and v < 0 else 'color: black') \
        .background_gradient(cmap='RdYlGn', axis=None, low=0.3, high=0.7) \
        .set_caption(title) \
        .set_table_styles([
            {'selector': 'caption',
             'props': [('caption-side', 'top'), ('font-weight', 'bold'), ('font-size', '1.5em')]}
        ], overwrite=False)

    return styler_pct

def style_table_pct(df, columns, title):
    def format_as_percent(value):
        if isinstance(value, (int, float)):
            return '{:,.0f}%'.format(value * 100).replace(',', '.')
        return value

    # Encontra o valor máximo nas colunas especificadas para a normalização
    max_val = df[columns].max().max()

    # Define uma função que normaliza os valores para o gradiente
    def normalize(value):
        if isinstance(value, (int, float)):
            return value / max_val
        return value

    # Normaliza os valores das colunas para o gradiente
    df_normalized = df.copy()
    for col in columns:
        df_normalized[col] = df_normalized[col].apply(normalize)

    # Aplica estilos ao DataFrame normalizado
    styler_pct = df_normalized.style.format(format_as_percent, subset=columns) \
        .set_table_styles([
            {'selector': 'thead th',
             'props': [('background-color', 'yellow'), ('color', 'black'), ('font-weight', 'bold')]},
            {'selector': 'td',
             'props': [('text-align', 'center')]}
        ]) \
        .map(lambda v: 'color: red' if isinstance(v, float) and v < 0 else 'color: black', subset=columns)\
        .background_gradient(subset=columns, cmap='RdYlGn', axis=None, low=0, high=1) \
        .set_caption(title) \
        .set_table_styles([
            {'selector': 'caption',
             'props': [('caption-side', 'top'), ('font-weight', 'bold'), ('font-size', '1.5em')]}
        ], overwrite=False)

    return styler_pct


def style_table_pct_semcol1(df, columns, title):
    def format_as_percent(value):
        if isinstance(value, (int, float)):
            return '{:,.0f}%'.format(value * 100).replace(',', '.')
        return value

    # Aplica estilos ao DataFrame
    # Excluding the first column for styling
    styler_pct = df.style.format(format_as_percent, subset=columns[1:]) \
        .set_table_styles([
            {'selector': 'thead th',
             'props': [('background-color', 'yellow'), ('color', 'black'), ('font-weight', 'bold')]},
            {'selector': 'td',
             'props': [('text-align', 'center')]}
        ], overwrite=False) \
        .applymap(lambda v: 'color: red' if isinstance(v, float) and v < 0 else 'color: black', subset=columns[1:]) \
        .background_gradient(subset=columns[1:], cmap='RdYlGn', axis=None, low=0, high=1) \
        .set_caption(title) \
        .set_table_styles([
            {'selector': 'caption',
             'props': [('caption-side', 'top'), ('font-weight', 'bold'), ('font-size', '1.5em')]}
        ], overwrite=False)

    return styler_pct


def style_table_pct_html(df, columns, title):
    def format_as_percent(value):
        if isinstance(value, (int, float)):
            return '{:,.0f}%'.format(value * 100).replace(',', '.')
        return value

    # Encontra o valor máximo nas colunas especificadas para a normalização, excluindo a primeira coluna
    max_val = df[columns[1:]].max().max()

    # Define uma função que normaliza os valores para o gradiente, excluindo a primeira coluna
    def normalize(value):
        if isinstance(value, (int, float)):
            return value / max_val
        return value

    # Normaliza os valores das colunas para o gradiente, excluindo a primeira coluna
    df_normalized = df.copy()
    for col in columns[1:]:
        df_normalized[col] = df_normalized[col].apply(normalize)

    # Aplica estilos ao DataFrame normalizado, excluindo a primeira coluna
    styler_pct = df_normalized.style.format(format_as_percent, subset=columns[1:]) \
        .set_table_styles([
            {'selector': 'thead th',
             'props': [('background-color', 'yellow'), ('color', 'black'), ('font-weight', 'bold')]},
            {'selector': 'td',
             'props': [('text-align', 'center')]}
        ], overwrite=False) \
        .map(lambda v: 'color: red' if isinstance(v, float) and v < 0 else 'color: black', subset=columns[1:]) \
        .background_gradient(subset=columns[1:], cmap='RdYlGn', axis=None, low=0, high=1) \
        .set_caption(title) \
        .set_table_styles([
            {'selector': 'caption',
             'props': [('caption-side', 'top'), ('font-weight', 'bold'), ('font-size', '1.5em')]}
        ], overwrite=False) \

    # Retorna a string HTML do DataFrame estilizado
    return styler_pct.render()


######### Formatação agrupando colunas

def style_table_agrupamento(df, columns, title, group_headers):
    def format_as_percent(value):
        if isinstance(value, (int, float)):
            return '{:,.0f}%'.format(value * 100).replace(',', '.')
        return value

    max_val = df[columns[1:]].max().max()

    def normalize(value):
        if isinstance(value, (int, float)):
            return value / max_val
        return value

    df_normalized = df.copy()
    for col in columns[1:]:
        df_normalized[col] = df_normalized[col].apply(normalize)

    def render_custom_header(group_headers):
        header_html = "<tr>"
        for header, span in group_headers:
            header_html += f'<th colspan="{span}">{header}</th>'
        header_html += "</tr>"
        return header_html

    styler_pct = df_normalized.style.format(format_as_percent, subset=columns[1:]) \
        .set_table_styles([
            {'selector': 'thead th',
             'props': [('background-color', 'yellow'), ('color', 'black'), ('font-weight', 'bold')]},
            {'selector': 'td',
             'props': [('text-align', 'center')]}
        ], overwrite=False) \
        .applymap(lambda v: 'color: red' if isinstance(v, float) and v < 0 else 'color: black', subset=columns[1:]) \
        .background_gradient(subset=columns[1:], cmap='RdYlGn', axis=None, low=0, high=1) \
        .set_caption(title) \
        .set_table_styles([
            {'selector': 'caption',
             'props': [('caption-side', 'top'), ('font-weight', 'bold'), ('font-size', '1.5em')]}
        ], overwrite=False) \
        .set_table_attributes('class="dataframe"') \
        .render().replace('<thead>', f'<thead>{render_custom_header(group_headers)}')
    
    styler_html = styler_pct.to_html().replace('<thead>', f'<thead>{render_custom_header(group_headers)}')

    return styler_html



# ____________________________________________________________________________________________________________________________________________________________________


def penetracao_bees(df, id, total_bees, total_nom_bees):
    ids_bees = df[df[total_bees]>0][id].nunique()
    receita_total = df[total_bees] + df[total_nom_bees]
    intermed = receita_total > 0
    total_ids = df[intermed][id].nunique()

    return ids_bees / total_ids


def cont_bees(df):
    ids_bees = df[df['TOTAL_BEES'] != 0]['bees_account_id'].nunique()
    return ids_bees
    

def formata_numero(valor, prefixo=''):
    if valor < 1000:
        return f'{prefixo}{valor:.2f}'
    elif valor < 1000000:
        return f'{prefixo}{valor / 1000:.2f} k'
    elif valor < 1000000000:
        return f'{prefixo}{valor / 1000000:.2f} mi'
    else:
        return f'{prefixo}{valor / 1000000000:.2f} bi'
    
def formata_percentual(valor, sufixo='%'):
    return f'{valor*100:.1f}{sufixo}'


# Importando dados

export_df = pd.read_csv('export.csv')
export_oc_df = pd.read_csv('export_oc.csv')
export_month = pd.read_csv('export_month.csv')
export_month_oc = pd.read_csv('export_month_oc.csv')


# Tabelas

## Pen_bees por segmento
### Setando filtros de vendors

export_df_filtro1 = export_df[export_df['vendor_display_name'] == "OCSI Cavite"]
export_df_filtro2 = export_df[export_df['vendor_display_name'] == "Actiserve"]

export_month_filtro1 = export_month[export_month['vendor_display_name'] == "OCSI Cavite"]
export_month_filtro2 = export_month[export_month['vendor_display_name'] == "Actiserve"]

############### Consolidado
### Preparando as tabelas de cada caso para segmentos

agg_segmento = export_df.groupby('segment')
pens_base_segmento_bees_all = agg_segmento.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_ALLD', 'TOTAL_NONBEES_ALLD'))
pens_base_segmento_bees_90d = agg_segmento.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D'))
pens_base_segmento_bees_30d = agg_segmento.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D'))
pens_base_segmento_bees_15d = agg_segmento.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_15D', 'TOTAL_NONBEES_15D'))
pens_base_segmento_bees_7d = agg_segmento.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D'))

pens_segmento = pd.DataFrame({
    'BEES 90D': pens_base_segmento_bees_90d.round(2),
    'BEES 30D': pens_base_segmento_bees_30d.round(2),
    'BEES 7D': pens_base_segmento_bees_7d.round(2)
})

#---------------------------------------------------------------------------------------------------------------------------------------------------

agg_segmento_filtro1 = export_df_filtro1.groupby('segment')
pens_base_segmento_bees_all1 = agg_segmento_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_ALLD', 'TOTAL_NONBEES_ALLD'))
pens_base_segmento_bees_90d1 = agg_segmento_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D'))
pens_base_segmento_bees_30d1 = agg_segmento_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D'))
pens_base_segmento_bees_15d1 = agg_segmento_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_15D', 'TOTAL_NONBEES_15D'))
pens_base_segmento_bees_7d1 = agg_segmento_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D'))

pens_segmento1 = pd.DataFrame({
    'BEES 90D': pens_base_segmento_bees_90d1.round(2),
    'BEES 30D': pens_base_segmento_bees_30d1.round(2),
    'BEES 7D': pens_base_segmento_bees_7d1.round(2)
})

#---------------------------------------------------------------------------------------------------------------------------------------------------
agg_segmento_filtro2 = export_df_filtro2.groupby('segment')
pens_base_segmento_bees_all2 = agg_segmento_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_ALLD', 'TOTAL_NONBEES_ALLD'))
pens_base_segmento_bees_90d2 = agg_segmento_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D'))
pens_base_segmento_bees_30d2 = agg_segmento_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D'))
pens_base_segmento_bees_15d2 = agg_segmento_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_15D', 'TOTAL_NONBEES_15D'))
pens_base_segmento_bees_7d2 = agg_segmento_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D'))


pens_segmento2 = pd.DataFrame({
    'BEES 90D': pens_base_segmento_bees_90d2.round(2),
    'BEES 30D': pens_base_segmento_bees_30d2.round(2),
    'BEES 7D': pens_base_segmento_bees_7d2.round(2)
})

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Por segmento pelos 3 ultimos meses

export_month['month_year'] = pd.to_datetime(export_month['month_year'])
ultimos_meses = export_month[export_month['month_year'].dt.month.isin([10,11,12])]
ultimos_meses_v2 = ultimos_meses[ultimos_meses['TOTAL_BEES'] > 0]

pivot_1g = ultimos_meses.pivot_table(index='segment', 
                                     columns='month_year', 
                                     values='bees_account_id', 
                                     aggfunc='nunique')


pivot_2g = ultimos_meses_v2.groupby(['segment', 'month_year']).apply(cont_bees).unstack()


pivot_3g = pivot_2g / pivot_1g
#---------------------------------------------------------------------------------------------------------------------------------------------------

### Preparando as tabelas de cada caso para tamanho

agg_tamanho = export_df.groupby('ch_size')
pens_base_tamanho_bees_all = agg_tamanho.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_ALLD', 'TOTAL_NONBEES_ALLD'))
pens_base_tamanho_bees_90d = agg_tamanho.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D'))
pens_base_tamanho_bees_30d = agg_tamanho.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D'))
pens_base_tamanho_bees_15d = agg_tamanho.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_15D', 'TOTAL_NONBEES_15D'))
pens_base_tamanho_bees_7d = agg_tamanho.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D'))

pens_tamanho = pd.DataFrame({
    'BEES 90D': pens_base_tamanho_bees_90d.round(2),
    'BEES 30D': pens_base_tamanho_bees_30d.round(2),
    'BEES 7D': pens_base_tamanho_bees_7d.round(2)
})

pens_tamanho_format = style_table_pct(pens_tamanho, pens_tamanho.columns, 'Geral')

#---------------------------------------------------------------------------------------------------------------------------------------------------

agg_tamanho_filtro1 = export_df_filtro1.groupby('ch_size')
pens_base_tamanho_bees_all1 = agg_tamanho_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_ALLD', 'TOTAL_NONBEES_ALLD'))
pens_base_tamanho_bees_90d1 = agg_tamanho_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D'))
pens_base_tamanho_bees_30d1 = agg_tamanho_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D'))
pens_base_tamanho_bees_15d1 = agg_tamanho_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_15D', 'TOTAL_NONBEES_15D'))
pens_base_tamanho_bees_7d1 = agg_tamanho_filtro1.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D'))

pens_tamanho1 = pd.DataFrame({
    'BEES 90D': pens_base_tamanho_bees_90d1.round(2),
    'BEES 30D': pens_base_tamanho_bees_30d1.round(2),
    'BEES 7D': pens_base_tamanho_bees_7d1.round(2)
})


pens_tamanho1_colcerta = pens_tamanho1
pens_tamanho1_format = style_table_pct(pens_tamanho1_colcerta,pens_tamanho1.columns ,"OCSI Cavite")
teste = style_table_pct(pens_tamanho1_colcerta,pens_tamanho1.columns ,"Actiserve")

#---------------------------------------------------------------------------------------------------------------------------------------------------
agg_tamanho_filtro2 = export_df_filtro2.groupby('ch_size')
pens_base_tamanho_bees_all2 = agg_tamanho_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_ALLD', 'TOTAL_NONBEES_ALLD'))
pens_base_tamanho_bees_90d2 = agg_tamanho_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D'))
pens_base_tamanho_bees_30d2 = agg_tamanho_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D'))
pens_base_tamanho_bees_15d2 = agg_tamanho_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_15D', 'TOTAL_NONBEES_15D'))
pens_base_tamanho_bees_7d2 = agg_tamanho_filtro2.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D'))


pens_tamanho2 = pd.DataFrame({
    'BEES 90D': pens_base_tamanho_bees_90d2.round(2),
    'BEES 30D': pens_base_tamanho_bees_30d2.round(2),
    'BEES 7D': pens_base_tamanho_bees_7d2.round(2)
})

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Por tamanho pelos 3 ultimos meses

export_month['month_year'] = pd.to_datetime(export_month['month_year'], format='%Y-%m-%d')
agg_data_tam_geral = export_month.groupby('ch_size')
pens_data_tam_geal = agg_data_tam_geral.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES', 'TOTAL_NONBEES'))

penetracao_out_tam = agg_data_tam_geral.apply(lambda x: penetracao_bees(x[x['month_year'].dt.month == 10], 'bees_account_id', 'TOTAL_BEES', 'TOTAL_NONBEES'))
penetracao_nov_tam = agg_data_tam_geral.apply(lambda x: penetracao_bees(x[x['month_year'].dt.month == 11], 'bees_account_id', 'TOTAL_BEES', 'TOTAL_NONBEES'))
penetracao_dez_tam = agg_data_tam_geral.apply(lambda x: penetracao_bees(x[x['month_year'].dt.month == 12], 'bees_account_id', 'TOTAL_BEES', 'TOTAL_NONBEES'))


data_df_tam_geral = pd.DataFrame({
    'OUT': penetracao_out_tam,
    'NOV':penetracao_nov_tam,
    'DEZ': penetracao_dez_tam
})
#---------------------------------------------------------------------------------------------------------------------------------------------------

# Por segmento pelos 3 ultimos meses OCSI

export_month_filtro1['month_year'] = pd.to_datetime(export_month_filtro1['month_year'], format='%Y-%m-%d')
agg_data_seg_geraloc = export_month_filtro1.groupby('segment')
pens_data_seg_geraloc = agg_data_seg_geraloc.apply(lambda x: penetracao_bees(x, 'bees_account_id', 'TOTAL_BEES', 'TOTAL_NONBEES'))

penetracao_out_oc = agg_data_seg_geraloc.apply(lambda x: penetracao_bees(x[x['month_year'].dt.month == 10], 'bees_account_id', 'TOTAL_BEES', 'TOTAL_NONBEES'))
penetracao_nov_oc = agg_data_seg_geraloc.apply(lambda x: penetracao_bees(x[x['month_year'].dt.month == 11], 'bees_account_id', 'TOTAL_BEES', 'TOTAL_NONBEES'))
penetracao_dez_oc = agg_data_seg_geraloc.apply(lambda x: penetracao_bees(x[x['month_year'].dt.month == 12], 'bees_account_id', 'TOTAL_BEES', 'TOTAL_NONBEES'))


data_df_seg_oc = pd.DataFrame({
    'OUT': penetracao_out_oc,
    'NOV':penetracao_nov_oc,
    'DEZ': penetracao_dez_oc
})



#---------------------------------------------------------------------------------------------------------------------------------------------------

# Visualizações

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Tabela de grandezas

actiserve_sku_sum = export_df[export_df['vendor_display_name'] == 'Actiserve']['DISTINCT_SKUS_ALLD'].sum()
actiserve_poc_unique = export_df[export_df['vendor_display_name'] == 'Actiserve']['bees_account_id'].nunique()

ocsi_cavite_sku_sum = export_df[export_df['vendor_display_name'] == 'OCSI Cavite']['DISTINCT_SKUS_ALLD'].sum()
ocsi_cavite_poc_unique = export_df[export_df['vendor_display_name'] == 'OCSI Cavite']['bees_account_id'].nunique()

total_sku_sum = export_df['DISTINCT_SKUS_ALLD'].sum()
total_poc_unique = export_df['bees_account_id'].nunique()

tabela_grandezas = pd.DataFrame({
    'sku': [actiserve_sku_sum, ocsi_cavite_sku_sum, total_sku_sum],
    'poc': [actiserve_poc_unique, ocsi_cavite_poc_unique, total_poc_unique]
}, index=['Actiserve', 'OCSI Cavite', 'Total'])

tabela_grandezas = tabela_grandezas.round(0)
headerColor = 'grey'
rowEvenColor = 'lightgrey'
rowOddColor = 'white'

headers = ['<b>Fornecedor</b>', '<b>SKU</b>', '<b>POC</b>']
values = [tabela_grandezas.index, tabela_grandezas['sku'], tabela_grandezas['poc']]

tabela_formatada = go.Table(
    header=dict(
        values=headers,
        line_color='darkslategray',
        fill_color=headerColor,
        align=['left', 'center'],
        font=dict(color='white', size=14)
    ),
    cells=dict(
        values=values,
        line_color='darkslategray',
        fill_color=[[rowOddColor, rowEvenColor, rowOddColor] * len(tabela_grandezas)],
        align=['left', 'center'],
        font=dict(color='darkslategray', size=12)
    )
)



tabela_teste = style_table(tabela_grandezas, tabela_grandezas.columns, 'Geral')

#---------------------------------------------------------------------------------------------------------------------------------------------------

## Mapa de calor por segmento
colunas_seg_heatmap = pens_segmento
colunas_tam_heatmap = pens_tamanho

# Criar heatmap para segmento consolidado
heatmap_segmento =  px.imshow(colunas_seg_heatmap,
                labels=dict(x="Rolling Cuts", y="Segment", color="Intensidade"),
                x=colunas_seg_heatmap.columns,
                y=pens_segmento.index,
                title="% Bees Buyers Rolling Cuts [Segment] - All",
                text_auto=".0%",
                aspect="auto",
                color_continuous_scale='Magma')

heatmap_segmento.update_layout(autosize=True, showlegend=False, width=550, height=400, margin=dict(t=50, l=10, r=10, b=10))
heatmap_segmento.update_coloraxes(showscale=False)

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Criar heatmap para tamanho consolidado
heatmap_tamanho =  px.imshow(colunas_tam_heatmap,
                labels=dict(x="Rolling Cuts", y="Size", color="Intensidade"),
                x=colunas_tam_heatmap.columns,
                y=pens_tamanho.index,
                title="% Bees Buyers Rolling Cuts [Size] - All",
                text_auto=".0%",
                aspect="auto",
                color_continuous_scale='Magma')

heatmap_tamanho.update_layout(autosize=True, showlegend=False, width=450, height=400, margin=dict(t=50, l=10, r=10, b=10))
heatmap_tamanho.update_coloraxes(showscale=False)
#---------------------------------------------------------------------------------------------------------------------------------------------------
# Heatmap dos 3 ultimos meses por segmento sem discriminar vendedor

heatmap_data_geral =  px.imshow(pivot_3g,
                labels=dict(x="Month", y="Segment", color="Intensidade"),
                x=pivot_3g.columns,
                y=pivot_3g.index,
                title="% Bees Buyers Month [Segment] - All",
                text_auto=".0%",
                aspect="auto",
                color_continuous_scale='Magma')

heatmap_data_geral.update_layout(autosize=True, showlegend=False, width=450, height=400, margin=dict(t=50, l=10, r=10, b=10))
heatmap_data_geral.update_coloraxes(showscale=False)

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Heatmap dos 3 ultimos meses por tamanho sem discriminar vendedor

heatmap_data_geral_tam =  px.imshow(data_df_tam_geral,
                labels=dict(x="Month", y="Segment", color="Intensidade"),
                x=data_df_tam_geral.columns,
                y=data_df_tam_geral.index,
                title="% Bees Buyers Month [Size] - All",
                text_auto=".0%",
                aspect="auto",
                color_continuous_scale='Magma')

heatmap_data_geral_tam.update_layout(autosize=True, showlegend=False, width=450, height=400, margin=dict(t=50, l=10, r=10, b=10))
heatmap_data_geral_tam.update_coloraxes(showscale=False)
#---------------------------------------------------------------------------------------------------------------------------------------------------
# Heatmap OCSI Cavite segmento

heatmap_seg_ocsi_rc =  px.imshow(pens_segmento1,
                labels=dict(x="Rolling Cuts", y="Segment", color="Intensidade"),
                x=pens_segmento1.columns,
                y=pens_segmento1.index,
                title="% Bees Buyers Rolling Cuts [Segment] - OCSI Cavite",
                text_auto=".0%",
                aspect="auto",
                color_continuous_scale='Magma')

heatmap_seg_ocsi_rc.update_layout(autosize=True, showlegend=False, width=450, height=400, margin=dict(t=50, l=10, r=10, b=10))
heatmap_seg_ocsi_rc.update_coloraxes(showscale=False)

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Heatmap OCSI tamanho

heatmap_tam_ocsi_rc =  px.imshow(pens_tamanho1,
                labels=dict(x="Rolling Cuts", y="Segment", color="Intensidade"),
                x=pens_tamanho1.columns,
                y=pens_tamanho1.index,
                title="% Bees Buyers Rolling Cuts [Size] - OCSI Cavite",
                text_auto=".0%",
                aspect="auto",
                color_continuous_scale='Magma')

heatmap_tam_ocsi_rc.update_layout(autosize=True, showlegend=False, width=450, height=400, margin=dict(t=50, l=10, r=10, b=10))
heatmap_tam_ocsi_rc.update_coloraxes(showscale=False)

#---------------------------------------------------------------------------------------------------------------------------------------------------
# Heatmap OCSI segmento por data

heatmap_seg_ocsi_data =  px.imshow(data_df_seg_oc,
                labels=dict(x="Rolling Cuts", y="Segment", color="Intensidade"),
                x=data_df_seg_oc.columns,
                y=data_df_seg_oc.index,
                title="% Bees Buyers Months [Segment] - OCSI Cavite",
                text_auto=".0%",
                aspect="auto",
                color_continuous_scale='Magma')

heatmap_seg_ocsi_data.update_layout(autosize=True, showlegend=False, width=450, height=400, margin=dict(t=50, l=10, r=10, b=10))
heatmap_seg_ocsi_data.update_coloraxes(showscale=False)

#---------------------------------------------------------------------------------------------------------------------------------------------------

### Outros indicadores

###### Orders por ponto de venda

export_month_actiserve = export_month[export_month['vendor_display_name'] == 'Actiserve']
export_month_ocsi = export_month[export_month['vendor_display_name'] == 'OCSI Cavite']


graf_act= export_month_actiserve.groupby('month_year').agg(
    SKU_sum=('DISTINCT_ORDERS', 'sum'),
    ID_distinct_count=('bees_account_id', pd.Series.nunique)
)

graf_act['metric1'] = graf_act['SKU_sum'] / graf_act['ID_distinct_count']

barras_act_orderspoc = px.bar(
    graf_act,
    x=graf_act.index,
    y='metric1',
    title='Métrica ao longo do tempo',
    color_discrete_sequence=['#5F9EA0']
)

barras_act_orderspoc.update_traces(
    texttemplate='%{y:.1f}',
    textposition='outside'  )

barras_act_orderspoc.update_layout(
    xaxis_tickangle=0,
    xaxis_title='Data',
    yaxis_title='Métrica',
    margin=dict(b=100),
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

#---------------------------------------------------------------------------------------------------------------------------------------------------

# Share of Revenue

def share_revenue(df, bees, nombees):
    if (df[bees].sum() + df[nombees].sum()) == 0:
        return 0
    else:
        share_of_revenue = df[bees].sum() / (df[bees].sum() + df[nombees].sum())
        return share_of_revenue


def verificar_coluna_para_float(df, coluna):
    for valor in df[coluna]:
        try:
            float(valor)  
        except ValueError:  
            return False    
    return True 


export_ocsi = export_df[export_df['vendor_display_name'] == 'OCSI Cavite']
export_actiserve = export_df[export_df['vendor_display_name'] == 'Actiserve']

export_month1 = export_month[export_month['vendor_display_name'] == "OCSI Cavite"]
export_month2 = export_month[export_month['vendor_display_name'] == "Actiserve"]

export_month1['month_year'] = pd.to_datetime(export_month_filtro1['month_year'], format='%Y-%m-%d')
export_month2['month_year'] = pd.to_datetime(export_month_filtro1['month_year'], format='%Y-%m-%d')


######## OUT

export_month_out = export_month[export_month['month_year'].dt.month == 10]
export_month_cavite_out = export_month1[export_month1['month_year'].dt.month == 10]
export_month_actverse_out = export_month2[export_month2['month_year'].dt.month == 10]

######## NOV

export_month_nov = export_month[export_month['month_year'].dt.month == 11]
export_month_cavite_nov = export_month1[export_month1['month_year'].dt.month == 11]
export_month_actverse_nov = export_month2[export_month2['month_year'].dt.month == 11]

######## DEZ

export_month_dez = export_month[export_month['month_year'].dt.month == 12]
export_month_cavite_dez = export_month1[export_month1['month_year'].dt.month == 12]
export_month_actverse_dez = export_month2[export_month2['month_year'].dt.month == 12]

#### Construindo as tabelas

vendedores = ['OCSI Cavite','Actiserve', 'PH']

table_share_revenue = pd.DataFrame({
    'Vendors': vendedores,
    '90D': [share_revenue(export_ocsi, 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D'), share_revenue(export_actiserve, 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D'), share_revenue(export_df, 'TOTAL_BEES_90D', 'TOTAL_NONBEES_90D')],
    '30D': [share_revenue(export_ocsi, 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D'), share_revenue(export_actiserve, 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D'), share_revenue(export_df, 'TOTAL_BEES_30D', 'TOTAL_NONBEES_30D')],
    '7D': [share_revenue(export_ocsi, 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D'), share_revenue(export_actiserve, 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D'), share_revenue(export_df, 'TOTAL_BEES_7D', 'TOTAL_NONBEES_7D')],
    'OUT': [share_revenue(export_month_cavite_out, 'TOTAL_BEES', 'TOTAL_NONBEES'), share_revenue(export_month_actverse_out, 'TOTAL_BEES', 'TOTAL_NONBEES'), share_revenue(export_month_out, 'TOTAL_BEES', 'TOTAL_NONBEES')],
    'NOV':[share_revenue(export_month_cavite_nov, 'TOTAL_BEES', 'TOTAL_NONBEES'), share_revenue(export_month_actverse_nov, 'TOTAL_BEES', 'TOTAL_NONBEES'), share_revenue(export_month_nov, 'TOTAL_BEES', 'TOTAL_NONBEES')],
    'DEZ': [share_revenue(export_month_cavite_dez, 'TOTAL_BEES', 'TOTAL_NONBEES'), share_revenue(export_month_actverse_dez, 'TOTAL_BEES', 'TOTAL_NONBEES'), share_revenue(export_month_dez, 'TOTAL_BEES', 'TOTAL_NONBEES')]
})

index_revenue = table_share_revenue.set_index('Vendors')
share_pvendor_vf = style_table_pct_allcol(index_revenue, 'Share of Revenue')


#---------------------------------------------------------------------------------------------------------------------------------------------------

# Share of orders


table_share_order = pd.DataFrame({
    'Vendors': vendedores,
    '90D': [share_revenue(export_ocsi, 'DISTINCT_ORDERS_BEES_90D', 'DISTINCT_ORDERS_NONBEES_90D'), share_revenue(export_actiserve, 'DISTINCT_ORDERS_BEES_90D', 'DISTINCT_ORDERS_NONBEES_90D'), share_revenue(export_df, 'DISTINCT_ORDERS_BEES_90D', 'DISTINCT_ORDERS_NONBEES_90D')],
    '30D': [share_revenue(export_ocsi, 'DISTINCT_ORDERS_BEES_30D', 'DISTINCT_ORDERS_NONBEES_30D'), share_revenue(export_actiserve, 'DISTINCT_ORDERS_BEES_30D', 'DISTINCT_ORDERS_NONBEES_30D'), share_revenue(export_df, 'DISTINCT_ORDERS_BEES_30D', 'DISTINCT_ORDERS_NONBEES_30D')],
    '7D': [share_revenue(export_ocsi, 'DISTINCT_ORDERS_BEES_7D', 'DISTINCT_ORDERS_NONBEES_7D'), share_revenue(export_actiserve, 'DISTINCT_ORDERS_BEES_7D', 'DISTINCT_ORDERS_NONBEES_7D'), share_revenue(export_df, 'DISTINCT_ORDERS_BEES_7D', 'DISTINCT_ORDERS_NONBEES_7D')],
    'OUT': [share_revenue(export_month_cavite_out, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES'), share_revenue(export_month_actverse_out, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES'), share_revenue(export_month_out, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES')],
    'NOV':[share_revenue(export_month_cavite_nov, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES'), share_revenue(export_month_actverse_nov, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES'), share_revenue(export_month_nov, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES')],
    'DEZ': [share_revenue(export_month_cavite_dez, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES'), share_revenue(export_month_actverse_dez, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES'), share_revenue(export_month_dez, 'DISTINCT_ORDERS_BEES', 'DISTINCT_ORDERS_NONBEES')]
})

index_order = table_share_order.set_index('Vendors')
shareorder_p = style_table_pct_allcol(index_order, 'Share of Orders')





#---------------------------------------------------------------------------------------------------------------------------------------------------

## Formatando imagens

# Logo
logo_resize = Image.open('logo.png')
logo_resize = logo_resize.resize((2000, 400))
logo_resize.save('resized_image.png')




#---------------------------------------------------------------------------------------------------------------------------------------------------

###### TESTE DE TABELAS AGRUPADAS COM AGGRID









#---------------------------------------------------------------------------------------------------------------------------------------------------





# Nomeando abas

abas = st.tabs(["Geral", "Sem Minimart"])
aba0 = abas[0]
aba1 = abas[1]

# Header
# Criando relatório

with aba0:
    colX= st.columns(2)
    col0 = st.columns(1)
    col1, col2 = st.columns(2)
    resumo = st.columns(1)
    tab1, tab2, tab3 = st.columns(3)
    col5 = st.columns(1)
    tabela_geral, tabela_geral1, tabela_geral2 = st.columns(3)
    vendor_geral = st.columns(1)
    colA = st.columns(1)
    col3, col4 = st.columns(2)
    col_data_seg, col_data_tam = st.columns(2)
    col_vendor_1 = st.columns(1)
    vendor_ocsi_esquerda, vendor_ocsi_direita = st.columns(2)
    vendor_ocsi_data_esquerda, vendor_ocsi_data_direita = st.columns(2)
    linha = st.columns(1)
    indicador_2 = st.columns(1)
    op1, op2 = st.columns(2)
    df_teste, df_teste2 = st.columns(2)

    with resumo[0]:
        st.subheader("Summary")
    
    with tab1:
        st.table(share_pvendor_vf)
    with tab2:
        st.table(shareorder_p)

    with colX[0]:
        st.image('resized_image.png')

    with col0[0]:
        st.subheader("KPI's management (dados não exaustivos)")

    with col1:
        st.metric('Revenue', formata_numero(export_df['TOTAL_ALLD'].sum(), 'PHP '))
    with col2:
        st.metric('% Bees Buyers', formata_percentual(penetracao_bees(export_df, 'bees_account_id','TOTAL_BEES_ALLD', 'TOTAL_NONBEES_ALLD')))
        
    with tabela_geral:
        st.table(pens_tamanho_format)
    with tabela_geral1:
        st.table(pens_tamanho1_format)
    with tabela_geral2:
        st.table(teste)

    with vendor_geral[0]:
        st.markdown("""
    <style>
    .fonte-personalizada1 {
        font-size: 20px;
        font-style: bold;
    }
    </style>
    <div class="fonte-personalizada1">
        All Vendors
    </div>
    """, unsafe_allow_html=True)


    with col5[0]:
        st.subheader("% Bees Buyers")

        st.markdown("""
    <style>
    .fonte-personalizada2 {
        font-size: 12px;
        font-style: italic;
    }
    </style>
    <div class="fonte-personalizada2">
        Metodológia: Contagem distinta de ID's que possuam receita BEES > 0 dividido pela contagem distinta de IDs
    </div>
    """, unsafe_allow_html=True)
        

    with col3:
        st.plotly_chart(heatmap_segmento, use_container_width = True)
    with col4:
        st.plotly_chart(heatmap_tamanho, use_container_width = True)
    with col_data_seg:
         st.plotly_chart(heatmap_data_geral, use_container_width = True)
    with col_data_tam:
        st.plotly_chart(heatmap_data_geral_tam, use_container_width = True)

    with col_vendor_1[0]:
        st.markdown("""
    <style>
    .fonte-personalizada1 {
        font-size: 20px;
        font-style: bold;
    }
    </style>
    <div class="fonte-personalizada1">
        OCSI Cavite
    </div>
    """, unsafe_allow_html=True)
        
    with vendor_ocsi_esquerda:
        st.plotly_chart(heatmap_seg_ocsi_rc, use_container_width = True)
    with vendor_ocsi_direita:
        st.plotly_chart(heatmap_tam_ocsi_rc, use_container_width = True)
    with linha[0]:
        st.markdown("<hr>", unsafe_allow_html=True)
    with indicador_2[0]:
        st.subheader("Order / POC")
    
    with op1:
        st.plotly_chart(barras_act_orderspoc, use_container_width = True)

