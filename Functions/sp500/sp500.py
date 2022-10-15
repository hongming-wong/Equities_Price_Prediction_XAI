def get_sp500_tickers(split=False):
    """
    Return all the s&p 500 tickers
    """
    tickers = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 'GOOG', 'BRK.B', 'UNH', 'JNJ', 'XOM', 'META', 'JPM', 'NVDA',
               'PG', 'V', 'HD', 'CVX', 'LLY', 'PFE', 'MA', 'ABBV', 'PEP', 'MRK', 'KO', 'BAC', 'COST', 'TMO', 'WMT',
               'AVGO', 'DIS', 'MCD', 'ABT', 'DHR', 'CSCO', 'ACN', 'VZ', 'NEE', 'WFC', 'BMY', 'CRM', 'TXN', 'LIN', 'COP',
               'CMCSA', 'ADBE', 'PM', 'QCOM', 'CVS', 'UNP', 'RTX', 'AMGN', 'LOW', 'UPS', 'HON', 'SCHW', 'T', 'ELV',
               'INTU', 'IBM', 'MDT', 'INTC', 'MS', 'NKE', 'NFLX', 'SPGI', 'AMD', 'GS', 'AMT', 'PYPL', 'SBUX', 'ADP',
               'DE', 'ORCL', 'LMT', 'CAT', 'CI', 'BLK', 'AXP', 'TMUS', 'C', 'GILD', 'NOW', 'CB', 'PLD', 'MDLZ', 'MMC',
               'VRTX', 'REGN', 'ADI', 'TJX', 'MO', 'SO', 'DUK', 'AMAT', 'ZTS', 'TGT', 'NOC', 'SYK', 'PGR', 'GE', 'BA',
               'ISRG', 'EOG', 'BKNG', 'BDX', 'CME', 'CCI', 'PNC', 'HUM', 'MMM', 'WM', 'FISV', 'CL', 'TFC', 'D', 'CSX',
               'AON', 'MU', 'BSX', 'DG', 'USB', 'ETN', 'ATVI', 'PXD', 'EQIX', 'APD', 'EW', 'ITW', 'SLB', 'ICE', 'LRCX',
               'EL', 'MPC', 'NSC', 'MCK', 'SHW', 'GD', 'SRE', 'GM', 'SNPS', 'PSA', 'FIS', 'GIS', 'OXY', 'ADM', 'ORLY',
               'CDNS', 'CNC', 'AEP', 'F', 'EMR', 'KLAC', 'VLO', 'AZO', 'CMG', 'CTVA', 'MET', 'ADSK', 'LHX', 'MRNA',
               'APH', 'HCA', 'DVN', 'FCX', 'NXPI', 'BIIB', 'PSX', 'MAR', 'MCO', 'KMB', 'ROP', 'ENPH', 'MSI', 'EXC',
               'TRV', 'STZ', 'A', 'AIG', 'SYY', 'AJG', 'O', 'ECL', 'PAYX', 'COF', 'TEL', 'FDX', 'WMB', 'XEL', 'MSCI',
               'JCI', 'IQV', 'ALL', 'CHTR', 'TT', 'MCHP', 'MNST', 'CTAS', 'HLT', 'NEM', 'KMI', 'HSY', 'AFL', 'PRU',
               'FTNT', 'RMD', 'DOW', 'DXCM', 'MTB', 'PH', 'SBAC', 'ALB', 'EA', 'YUM', 'KDP', 'CARR', 'ED', 'HES', 'GPN',
               'CTSH', 'WELL', 'ROST', 'ILMN', 'TWTR', 'SPG', 'CMI', 'PCAR', 'DLTR', 'VICI', 'KR', 'DLR', 'NUE', 'BK',
               'KEYS', 'RSG', 'PEG', 'WEC', 'ANET', 'CSGP', 'IDXX', 'AMP', 'TDG', 'BAX', 'ES', 'ON', 'OTIS', 'CEG',
               'VRSK', 'KHC', 'FAST', 'PPG', 'AME', 'AVB', 'DD', 'WBD', 'DFS', 'ROK', 'MTD', 'TROW', 'FRC', 'AWK',
               'ODFL', 'IFF', 'EXR', 'EQR', 'HPQ', 'OKE', 'CPRT', 'WBA', 'WTW', 'GWW', 'DTE', 'STT', 'HAL', 'GLW',
               'CBRE', 'IT', 'FITB', 'ZBH', 'FANG', 'DHI', 'EIX', 'WY', 'BKR', 'GPC', 'ABC', 'CDW', 'CTRA', 'APTV',
               'ULTA', 'EPAM', 'ARE', 'VMC', 'FTV', 'EFX', 'TSCO', 'AEE', 'EBAY', 'ETR', 'FE', 'HIG', 'MLM', 'PCG',
               'INVH', 'NDAQ', 'SIVB', 'LEN', 'TSN', 'MOH', 'CF', 'LYB', 'RJF', 'ANSS', 'HBAN', 'PPL', 'URI', 'RF',
               'CAH', 'LH', 'LUV', 'PWR', 'WST', 'DRE', 'DAL', 'MAA', 'NTRS', 'CNP', 'MKC', 'K', 'IR', 'CHD', 'TTWO',
               'CFG', 'PFG', 'CMS', 'MOS', 'DOV', 'BR', 'STE', 'WAT', 'VRSN', 'HOLX', 'MPWR', 'AMCR', 'VTR', 'PAYC',
               'TDY', 'CLX', 'ESS', 'XYL', 'CAG', 'HPE', 'DRI', 'MRO', 'BALL', 'PKI', 'ALGN', 'IEX', 'FDS', 'AES',
               'EQT', 'WAB', 'KEY', 'SJM', 'DGX', 'EXPD', 'CINF', 'ATO', 'TYL', 'BRO', 'EXPE', 'J', 'SWKS', 'ZBRA',
               'NTAP', 'SYF', 'TRMB', 'EVRG', 'WRB', 'MTCH', 'AVY', 'JKHY', 'FMC', 'FLT', 'HRL', 'LNT', 'OMC', 'JBHT',
               'AKAM', 'CTLT', 'COO', 'BBY', 'SEDG', 'CPT', 'IRM', 'POOL', 'CTXS', 'ETSY', 'INCY', 'UDR', 'CBOE',
               'GRMN', 'LVS', 'TXT', 'NVR', 'LKQ', 'PEAK', 'LDOS', 'TER', 'BF.B', 'CHRW', 'IP', 'HWM', 'NLOK', 'NDSN',
               'DPZ', 'SWK', 'KIM', 'HST', 'APA', 'GNRC', 'LW', 'ABMD', 'PTC', 'TECH', 'LYV', 'SNA', 'KMX', 'STX',
               'PKG', 'BXP', 'MAS', 'RE', 'UAL', 'VTRS', 'NI', 'WDC', 'IPG', 'NLSN', 'CRL', 'FOXA', 'L', 'MGM', 'AAP',
               'PARA', 'VFC', 'CPB', 'SBNY', 'CMA', 'NRG', 'TFX', 'GL', 'HSIC', 'TAP', 'CE', 'BIO', 'PHM', 'HII', 'EMN',
               'FFIV', 'HAS', 'CDAY', 'QRVO', 'RCL', 'RHI', 'JNPR', 'MKTX', 'REG', 'WRK', 'ALLE', 'BBWI', 'AIZ', 'AAL',
               'ROL', 'ZION', 'WHR', 'BWA', 'TPR', 'PNW', 'FBHS', 'CZR', 'CCL', 'LNC', 'PNR', 'LUMN', 'WYNN', 'SEE',
               'AOS', 'FRT', 'IVZ', 'XRAY', 'OGN', 'UHS', 'NWSA', 'BEN', 'DXC', 'NWL', 'ALK', 'NCLH', 'MHK', 'DVA',
               'FOX', 'RL', 'VNO', 'DISH', 'NWS']



    for i, ticker in enumerate(tickers):
        tickers[i] = ticker + ".US"

    if split:
        return tickers[0:400], tickers[400:450], tickers[450:]

    return tickers
