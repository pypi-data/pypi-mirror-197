import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import requests

def InfoAcaoHistorico(ticker, start_date, end_date):
    """
    Função para obter o histórico de preços de uma ação dentro de um determinado intervalo de tempo.

    :param :
    -----------
    ticker : str
        Símbolo da ação a ser consultada.
    start_date : str
        Data de início do intervalo de tempo no formato "YYYY-MM-DD".
    end_date : str
        Data de fim do intervalo de tempo no formato "YYYY-MM-DD".

    :return :
    --------
    data : pandas.DataFrame
        DataFrame contendo os dados do histórico de preços da ação.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data

def InfoAcaoMultiplas(tickers):
    """
    Função para obter informações de várias ações ao mesmo tempo.

    :param :
    -----------
    tickers : list
        Lista de símbolos das ações a serem consultadas.

    :return :
    --------
    data : pandas.DataFrame
        DataFrame contendo as informações das ações, indexado pelos símbolos das ações.
    """
    stocks = yf.Tickers(tickers)
    info = [stock.info for stock in stocks.tickers]
    return pd.DataFrame(info, index=tickers)


def DadosInflacao(ticker, start_date, end_date):
    """
    Função para obter os dados históricos de inflação de um determinado período.

    :param :
    -----------
    ticker : str
        Ticker representando a inflação.
    start_date : str
        Data de início no formato 'YYYY-MM-DD'.
    end_date : str
        Data de fim no formato 'YYYY-MM-DD'.

    :return :
    --------
    inflation_data : pandas.Series
        Série temporal contendo as informações de inflação.
    """    
    inflation_data = yf.download(ticker, start=start_date, end=end_date, interval='1mo')['Adj Close']
    return inflation_data
    

def DadosFinanceiros(ticker, start_date, end_date):
    """
    Baixa dados financeiros de uma determinada ação dentro 
    de um período específico, utilizando a API do Yahoo Finance.

    :param :
    -----------
    ticker: 
        Uma variável string que representa o ticker da ação da empresa 
        cujos dados financeiros devem ser baixados.
    start_date: 
        Uma variável string que representa a data de início do período para o 
        qual os dados financeiros devem ser baixados.
    end_date: 
        Uma variável string que representa a data de fim do período para o 
        qual os dados financeiros devem ser baixados.

    :return :
    -----------
    data : 
        Atribui os dados baixados a uma variável chamada data em que é retornada na função.
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def ObterPrecoAcao(symbol):
    """
    Função para obter o preço atual de uma ação.

    :param :
    -----------
    symbol : str
        Símbolo da ação a ser consultada.

    :return :
    --------
    price : float
        Preço atual da ação.
    """
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=SUA_CHAVE_API'
    response = requests.get(url)
    data = response.json()
    price = float(data['Global Quote']['05. price'])
    return price

def CalcularRetornoAcao(symbol, data_inicio, data_fim):
    """
    Função para calcular o retorno percentual de uma ação em um período de análise.

    :param :
    -----------
    symbol : str
        Símbolo da ação a ser analisada.
    data_inicio : str
        Data de início do período de análise no formato 'YYYY-MM-DD'.
    data_fim : str
        Data de fim do período de análise no formato 'YYYY-MM-DD'.

    :return :
    --------
    retorno : float
        Retorno percentual da ação no período de análise.
    """
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize=full&apikey=SUA_CHAVE_API'
    response = requests.get(url)
    data = response.json()['Time Series (Daily)']
    preços = [float(data[d]['4. close']) for d in data if d >= data_inicio and d <= data_fim]
    retorno = (preços[-1] / preços[0]) - 1
    return retorno * 100

def ObterTaxaCambio(moeda_origem, moeda_destino):
    """
    Função para obter a taxa de câmbio entre duas moedas.

    :param :
    -----------
    moeda_origem : str
        Sigla da moeda de origem.
    moeda_destino : str
        Sigla da moeda de destino.

    :return :
    --------
    taxa : float
        Taxa de câmbio entre as duas moedas.
    """
    url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={moeda_origem}&to_currency={moeda_destino}&apikey=SUA_CHAVE_API'
    response = requests.get(url)
    data = response.json()
    taxa = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
    return taxa

def CalcularCDI(data_inicio, data_fim):
    """
    Função para calcular a taxa CDI média ponderada entre as datas informadas.

    :param :
    -----------
    data_inicio : str
        Data de início no formato 'YYYY-MM-DD'.
    data_fim : str
        Data de fim no formato 'YYYY-MM-DD'.

    :return :
    --------
    cdi : float
        Taxa CDI média ponderada no período entre as datas informadas.
    """
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial={}&dataFinal={}'
    data_inicio = pd.to_datetime(data_inicio).strftime('%d/%m/%Y')
    data_fim = pd.to_datetime(data_fim).strftime('%d/%m/%Y')
    response = requests.get(url.format(data_inicio, data_fim))
    if response.status_code == 200:
        dados = pd.read_json(response.text)
        num_dias_uteis = pd.date_range(start=data_inicio, end=data_fim, freq='B').shape[0]
        cdi = ((1 + dados['valor'].mean() / 100) ** (1 / num_dias_uteis) - 1) * 100
        cdi = round(cdi, 2)
        return cdi
    else:
        raise Exception('Erro ao obter as taxas SELIC diárias')
    
def CustoReal(custos_diretos, custos_indiretos):
    """
    Esta função calcula o custo real de um projeto, somando seus custos diretos e indiretos.

    :param :
    -------
    custos_diretos :
        uma lista ou tupla contendo os custos diretos do projeto.
    custos_indiretos : 
        uma lista ou tupla contendo os custos indiretos do projeto.

    :return :
    --------
        O custo real do projeto, obtido pela soma dos custos diretos e indiretos.
    """
    custo_real = custos_diretos + custos_indiretos
    return custo_real

def CustoTotalEmprestimo(valor_emprestado, taxa_juros, periodo_pagamento):
    """
    Calcula o custo total de um empréstimo a partir do valor emprestado, da taxa de juros e do período de pagamento.

    :param :
    --------
        valor_emprestado (float): 
            valor do empréstimo.
        taxa_juros (float): 
            taxa de juros aplicada.
        periodo_pagamento (int): 
            período de pagamento em meses.

    :return :
    --------
        custo_total (float) : 
            custo total do empréstimo.
    """
    num_pagamentos = periodo_pagamento * 12
    valor_parcela = (valor_emprestado * taxa_juros / 12) / (1 - (1 + taxa_juros / 12) ** (-num_pagamentos))
    custo_total = valor_parcela * num_pagamentos - valor_emprestado
    return custo_total

def CustoEfetivoTotal(valor_emprestado, taxa_juros, periodo_pagamento, tarifas):
    """
    Calcula o Custo Efetivo Total (CET) de um empréstimo a partir do valor emprestado, da taxa de juros, do período de pagamento e das tarifas.

    :param :
    --------
        valor_emprestado (float): 
            valor do empréstimo.
        taxa_juros (float): 
            taxa de juros aplicada.
        periodo_pagamento (int): 
            período de pagamento em meses.
        tarifas (float): 
            valor das tarifas cobradas.

    Returns:
    --------
        CET (float) : 
            Custo Efetivo Total (CET) do empréstimo.
    """
    num_pagamentos = periodo_pagamento * 12
    valor_parcela = (valor_emprestado * taxa_juros / 12) / (1 - (1 + taxa_juros / 12) ** (-num_pagamentos))
    juros = valor_parcela * num_pagamentos - valor_emprestado
    custo_total = juros + tarifas
    CET = (custo_total / valor_emprestado) * 100
    return CET

def CustoOportunidade(valor_presente, tempo, taxa_retorno_alternativa):
    """
    Calcula o custo de oportunidade de um investimento.

    :param :
    --------
    valor_presente (float): 
        Valor presente do investimento.
    tempo (float): 
        Tempo de investimento em anos.
    taxa_retorno_alternativa (float): 
        Taxa de retorno esperada em um investimento alternativo.

    : return:
        custo_oportunidade(float) : O custo de oportunidade do investimento.
    """
    valor_futuro = valor_presente * (1 + taxa_retorno_alternativa) ** tempo
    custo_oportunidade = valor_futuro - valor_presente

    return custo_oportunidade

def ValorPresenteLiquido(c0, fluxos_caixa, taxa_desconto):
    """
    calcula o valor presente líquido (VPL) de uma série de fluxos de caixa

    :param :
    -------
    c0: 
        o fluxo de caixa inicial ou investimento.
    fluxos_caixa: 
        uma lista ou array de fluxos de caixa, onde valores 
        positivos representam entradas e valores negativos representam saídas.
    taxa_desconto:  
        a taxa de desconto usada para calcular o valor presente dos fluxos de caixa futuros.

    :retur :
    --------
        vpl :
            valor presente liquido.
    """
    vpl = c0
    plt.plot(fluxos_caixa)
    plt.ylabel('Fluxos de caixa')
    plt.xlabel('Périodo do fluxos de caixa')
    plt.show()
    for i, cf in enumerate(fluxos_caixa):
        vpl += cf / (1 + taxa_desconto) ** (i + 1)
    return vpl

def RendaPerpetua(valor_pagamento, taxa_desconto):
    """
    calcula o valor presente de uma renda perpétua, ou seja, 
    uma série de pagamentos iguais que serão recebidos para sempre.
    :param :
    -------
    valor_pagamento: 
        o valor do pagamento que será recebido a cada período
    taxa_desconto: 
        a taxa de desconto usada para calcular o valor presente dos pagamentos futuros

    :return :
    --------
    valor_presente : 
        retorna o valor presente da renda
    """
    valor_presente = valor_pagamento / taxa_desconto
    return valor_presente

def Prestacao(PV, r, n):
    """
    calcula o valor de uma prestação constante a ser paga 
    periodicamente para quitar um empréstimo ou financiamento com juros compostos.

    :param :
    -------
    PV: 
        o valor presente ou o montante principal do empréstimo ou financiamento
    r: 
        a taxa de juros periódica
    n: 
        o número total de períodos de pagamento

    :return :
    --------
    round:
        retorna a prestação. 
    """
    prestacao = PV * r * (1 + r)**n / ((1 + r)**n - 1)
    return round(prestacao, 2)

def VariacaoPercentual(valor_inicial, valor_final):
    """
    Calcula a variação percentual entre dois valores.

    :param : float
        valor_inicial : Valor inicial.
        valor_final : Valor final.

    :return :
        float: A variação percentual entre os valores, em porcentagem.
    """
    variacao_percentual = (valor_final - valor_inicial) / valor_inicial * 100
    return variacao_percentual

def TabelaAmortizacao(valor_presente, taxa_juros, prazo_meses):
    """
    Retorna uma tabela de amortização de um empréstimo com juros compostos.
    
    :param :
    valor_presente (float): 
        valor presente do empréstimo
    taxa_juros (float):
        taxa de juros mensal do empréstimo (ex: 0.01 para 1% ao mês)
    prazo_meses (int): 
        prazo do empréstimo em meses
    
    :return :
        pandas.DataFrame: tabela de amortização com as seguintes colunas:
            - Mês: mês da amortização
            - Parcela: valor da parcela mensal (amortização + juros)
            - Juros: valor dos juros da parcela
            - Amortização: valor da amortização da parcela
            - Saldo Devedor: saldo devedor após a amortização
    """
    parcela = np.pmt(taxa_juros, prazo_meses, valor_presente)
    saldos_devedores = [valor_presente]
    for i in range(prazo_meses):
        saldo_devedor = saldos_devedores[i] + parcela
        saldos_devedores.append(saldo_devedor)
    amortizacoes = [valor_presente - saldos_devedores[0]]
    for i in range(prazo_meses-1):
        amortizacao = parcela - (saldos_devedores[i] * taxa_juros)
        amortizacoes.append(amortizacao)
    amortizacoes.append(saldo_devedor)
    tabela = pd.DataFrame({
        "Mês": range(1, prazo_meses+1),
        "Parcela": parcela,
        "Juros": [saldo_devedor * taxa_juros for saldo_devedor in saldos_devedores[:-1]],
        "Amortização": amortizacoes,
        "Saldo Devedor": saldos_devedores[:-1]
    })
    tabela["Mês"] = tabela["Mês"].astype(int)
    tabela["Parcela"] = tabela["Parcela"].round(2)
    tabela["Juros"] = tabela["Juros"].round(2)
    tabela["Amortização"] = tabela["Amortização"].round(2)
    tabela["Saldo Devedor"] = tabela["Saldo Devedor"].round(2)
    return tabela

def JurosSimples(principal, taxa, tempo):
    """
    calcula o valor total (incluindo juros) resultante de um empréstimo com juros simples.  

    :param :
    -------
    principal: 
        o valor inicial emprestado ou investido
    taxa: 
        a taxa de juros (expressa como um número decimal)
    tempo: 
        o período de tempo (em anos) em que o dinheiro é emprestado ou investido

    :return :
    --------
        Retorna o total a pagar
    """
    juros = principal * taxa * tempo
    total = principal + juros
    return total
    
def JurosCompostos(capital, taxa, tempo):
    """
    Calcula o montante total, incluindo juros compostos, ganho a partir de um capital inicial
    durante um determinado período de tempo a uma taxa de juros fixa.

    :param :
    capital :
        o valor inicial do investimento
    taxa : 
        a taxa de juros, expressa como uma fração decimal (por exemplo, 0,05 para 5%)
    tempo : 
        o período de tempo, em anos

    :return :
        O montante total, incluindo juros compostos, ganho durante o período de tempo especificado.
    """
    juros = capital * ((1 + taxa) ** tempo - 1)
    return capital + juros

def TaxaJuros(capital, futuro, tempo):
    """
    calcular a taxa de juros

    :param :
    -------
    capital: 
        representa a quantia inicial de dinheiro investido ou emprestado
    futuro:
        representa o valor futuro do investimento ou empréstimo
    tempo: 
        representa o período de tempo (em anos) para o qual o investimento ou empréstimo é feito

    :return :
    --------
    retorna o a taxa de juros.
    """
    return (futuro / capital) ** (1 / tempo) - 1
    
def TaxaEquivalente(taxa, periodo_taxa, periodo_equivalente):
    """
    Calcula a taxa de juros equivalente.
    
    :param :
    -------
    taxa (float): 
        A taxa de juros em um período.
    periodo_taxa (int): 
        O número de períodos que a taxa é aplicada.
    periodo_equivalente (int): 
        O número de períodos em que se quer obter a taxa equivalente.
    
    :return :
    --------
    taxa_equivalente(float): 
        A taxa de juros equivalente.
    """
    taxa_equivalente = ((1 + taxa) ** (periodo_taxa / periodo_equivalente)) - 1
    return taxa_equivalente

def TaxaNominal(taxa_efetiva, periodo):
    """
    Essa função calcula a taxa nominal correspondente a uma taxa efetiva e período dados.
    
    Argumentos:
    taxa_efetiva (float): a taxa efetiva a ser convertida em taxa nominal.
    periodo (int): o período da taxa efetiva, em unidades de tempo.
    
    Retorno:
    taxa_nominal (float): a taxa nominal correspondente, em porcentagem.
    """
    taxa_nominal = ((1 + taxa_efetiva) ** periodo - 1) * 100
    return taxa_nominal

def TaxaReal(taxa_nominal, taxa_inflacao):
    """
    Essa função calcula a taxa real correspondente a uma taxa nominal e taxa de inflação dados.
    
    :param :
    -------
    taxa_nominal (float): 
        a taxa nominal a ser ajustada para a taxa real.
    taxa_inflacao (float): 
        a taxa de inflação a ser levada em conta no cálculo da taxa real.
    
    :return :
    --------
    taxa_real (float): 
        a taxa real correspondente, em porcentagem.
    """
    taxa_real = ((1 + taxa_nominal / 100) / (1 + taxa_inflacao / 100) - 1) * 100
    return taxa_real

def TaxaEfetiva(taxa_nominal, periodo):
    """
    Calcula a taxa efetiva a partir de uma taxa nominal e um período especificados.

    :param :
    -------
    taxa_nominal (float): 
        A taxa nominal em porcentagem.
    periodo (float): 
        O período em que a taxa nominal será aplicada.

    :return :
    --------
        float: A taxa efetiva em porcentagem.
    """
    taxa_efetiva = ((1 + taxa_nominal / 100) ** (1 / periodo) - 1) * 100
    return taxa_efetiva
