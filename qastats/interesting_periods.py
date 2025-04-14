####
# QUANTARMY 2022 - PRIVATE CODE - ALL RIGTHS RESERVED
# QUANTARMY 2023 - PRIVATE CODE - ALL RIGTHS RESERVED
# QUANTARMY 2024 - GNU PUBLIC LICENSE (ALL SOURCE RELEASED)
# QUANTARMY 2025 - GNU PUBLIC LICENSE - OPEN SOURCE
# by jcx - jcx@quantarmy.com | https://quantarmy.com
####
# Noviembre 2022
# Enero 2023 - 
# Feb 2024 - Update 2.0
# Abril 2025 - Update 2.1
##### armystats v2
#
#### 
#To-Do
# -> Tests


"""Generates a list of historical event dates that may have had
significant impact on markets.  See extract_interesting_date_ranges."""

import datetime as dt
from collections import OrderedDict

import pandas as pd

PERIODS = OrderedDict()
# Dotcom bubble
PERIODS["Dotcom"] = (
    pd.Timestamp("20000310", tzinfo=dt.timezone.utc),
    pd.Timestamp("20000910", tzinfo=dt.timezone.utc),
)

# Lehmann Brothers
PERIODS["Lehman"] = (
    pd.Timestamp("20080801", tzinfo=dt.timezone.utc),
    pd.Timestamp("20081001", tzinfo=dt.timezone.utc),
)

# 9/11
PERIODS["9/11"] = (
    pd.Timestamp("20010911", tzinfo=dt.timezone.utc),
    pd.Timestamp("20011011", tzinfo=dt.timezone.utc),
)

# 05/08/11  US down grade and European Debt Crisis 2011
PERIODS["US downgrade/European Debt Crisis"] = (
    pd.Timestamp("20110805", tzinfo=dt.timezone.utc),
    pd.Timestamp("20110905", tzinfo=dt.timezone.utc),
)

# 16/03/11  Fukushima melt down 2011
PERIODS["Fukushima"] = (
    pd.Timestamp("20110316", tzinfo=dt.timezone.utc),
    pd.Timestamp("20110416", tzinfo=dt.timezone.utc),
)

# 01/08/03  US Housing Bubble 2003
PERIODS["US Housing"] = (
    pd.Timestamp("20030108", tzinfo=dt.timezone.utc),
    pd.Timestamp("20030208", tzinfo=dt.timezone.utc),
)

# 06/09/12  EZB IR Event 2012
PERIODS["EZB IR Event"] = (
    pd.Timestamp("20120910", tzinfo=dt.timezone.utc),
    pd.Timestamp("20121010", tzinfo=dt.timezone.utc),
)

# August 2007, March and September of 2008, Q1 & Q2 2009,
PERIODS["Aug07"] = (
    pd.Timestamp("20070801", tzinfo=dt.timezone.utc),
    pd.Timestamp("20070901", tzinfo=dt.timezone.utc),
)
PERIODS["Mar08"] = (
    pd.Timestamp("20080301", tzinfo=dt.timezone.utc),
    pd.Timestamp("20080401", tzinfo=dt.timezone.utc),
)
PERIODS["Sept08"] = (
    pd.Timestamp("20080901", tzinfo=dt.timezone.utc),
    pd.Timestamp("20081001", tzinfo=dt.timezone.utc),
)
PERIODS["2009Q1"] = (
    pd.Timestamp("20090101", tzinfo=dt.timezone.utc),
    pd.Timestamp("20090301", tzinfo=dt.timezone.utc),
)
PERIODS["2009Q2"] = (
    pd.Timestamp("20090301", tzinfo=dt.timezone.utc),
    pd.Timestamp("20090601", tzinfo=dt.timezone.utc),
)

# Flash Crash (May 6, 2010 + 1 week post),
PERIODS["Flash Crash"] = (
    pd.Timestamp("20100505", tzinfo=dt.timezone.utc),
    pd.Timestamp("20100510", tzinfo=dt.timezone.utc),
)

# April and October 2014).
PERIODS["Apr14"] = (
    pd.Timestamp("20140401", tzinfo=dt.timezone.utc),
    pd.Timestamp("20140501", tzinfo=dt.timezone.utc),
)
PERIODS["Oct14"] = (
    pd.Timestamp("20141001", tzinfo=dt.timezone.utc),
    pd.Timestamp("20141101", tzinfo=dt.timezone.utc),
)

# Market down-turn in August/Sept 2015
PERIODS["Fall2015"] = (
    pd.Timestamp("20150815", tzinfo=dt.timezone.utc),
    pd.Timestamp("20150930", tzinfo=dt.timezone.utc),
)

# Market regimes
PERIODS["Low Volatility Bull Market"] = (
    pd.Timestamp("20050101", tzinfo=dt.timezone.utc),
    pd.Timestamp("20070801", tzinfo=dt.timezone.utc),
)

PERIODS["GFC Crash"] = (
    pd.Timestamp("20070801", tzinfo=dt.timezone.utc),
    pd.Timestamp("20090401", tzinfo=dt.timezone.utc),
)

PERIODS["Recovery"] = (
    pd.Timestamp("20090401", tzinfo=dt.timezone.utc),
    pd.Timestamp("20130101", tzinfo=dt.timezone.utc),
)

PERIODS["New Normal"] = (
    pd.Timestamp("20130101", tzinfo=dt.timezone.utc),
    pd.Timestamp("20180921", tzinfo=dt.timezone.utc),
)

PERIODS["Taper Tantrum"] = (
    pd.Timestamp("20130522", tzinfo=dt.timezone.utc),  # Anuncio de Bernanke
    pd.Timestamp("20130930", tzinfo=dt.timezone.utc),
)

PERIODS["Brexit Referendum"] = (
    pd.Timestamp("20160623", tzinfo=dt.timezone.utc),  # Fecha del referéndum
    pd.Timestamp("20161231", tzinfo=dt.timezone.utc),  # Impacto inicial en mercados
)

PERIODS["Brexit Process"] = (
    pd.Timestamp("20170329", tzinfo=dt.timezone.utc),  # Activación del Artículo 50
    pd.Timestamp("20201231", tzinfo=dt.timezone.utc),  # Fin del período de transición
)

PERIODS["US-China Trade War"] = (
    pd.Timestamp("20180706", tzinfo=dt.timezone.utc),  # Primeros aranceles importantes de EE.UU. a China
    pd.Timestamp("20200115", tzinfo=dt.timezone.utc),  # Firma del acuerdo comercial "Fase Uno"
)

PERIODS["Covid"] = (
    pd.Timestamp("20200211", tzinfo=dt.timezone.utc),
    pd.Timestamp("20230505", tzinfo=dt.timezone.utc),  # La OMS declaró el fin de la emergencia sanitaria el 5 de mayo de 2023
)

PERIODS["GameStop Short Squeeze"] = (
    pd.Timestamp("20210112", tzinfo=dt.timezone.utc),  # Inicio del movimiento
    pd.Timestamp("20210208", tzinfo=dt.timezone.utc),  # Fin del pico principal
)

# Eventos económicos recientes
PERIODS["Post-Covid Recovery"] = (
    pd.Timestamp("20220301", tzinfo=dt.timezone.utc), 
    pd.Timestamp("20221231", tzinfo=dt.timezone.utc),
)

PERIODS["Fed Rate Hikes"] = (
    pd.Timestamp("20220316", tzinfo=dt.timezone.utc),  # Primera subida de tasas post-COVID
    pd.Timestamp("20230726", tzinfo=dt.timezone.utc),  # Última subida del ciclo agresivo
)

PERIODS["Russia-Ukraine War"] = (
    pd.Timestamp("20220224", tzinfo=dt.timezone.utc),
    pd.Timestamp("today", tzinfo=dt.timezone.utc),
)

PERIODS["Inflation Crisis"] = (
    pd.Timestamp("20220101", tzinfo=dt.timezone.utc),
    pd.Timestamp("20230630", tzinfo=dt.timezone.utc),
)
PERIODS["Crypto Crash 2022"] = (
    pd.Timestamp("20220501", tzinfo=dt.timezone.utc),  # Colapso de Terra Luna
    pd.Timestamp("20221130", tzinfo=dt.timezone.utc),  # Quiebra de FTX
)

PERIODS["Banking Crisis 2023"] = (
    pd.Timestamp("20230310", tzinfo=dt.timezone.utc),  # Colapso de SVB
    pd.Timestamp("20230515", tzinfo=dt.timezone.utc),
)

PERIODS["US Debt Ceiling Crisis 2023"] = (
    pd.Timestamp("20230501", tzinfo=dt.timezone.utc),  # Intensificación de la crisis
    pd.Timestamp("20230602", tzinfo=dt.timezone.utc),  # Firma de la ley de suspensión
)

PERIODS["Russia-Ukraine War"] = (
    pd.Timestamp("20220224", tzinfo=dt.timezone.utc),
    pd.Timestamp("today", tzinfo=dt.timezone.utc),
)

PERIODS["Israel-Hamas War"] = (
    pd.Timestamp("20231007", tzinfo=dt.timezone.utc),
    pd.Timestamp("today", tzinfo=dt.timezone.utc),
)

PERIODS["AI Boom"] = (
    pd.Timestamp("20221130", tzinfo=dt.timezone.utc),  # Lanzamiento de ChatGPT
    pd.Timestamp("today", tzinfo=dt.timezone.utc),
)

PERIODS["Trump Victory 2024"] = (
    pd.Timestamp("20241105", tzinfo=dt.timezone.utc),
    pd.Timestamp("today", tzinfo=dt.timezone.utc),
)

PERIODS["Trump Tariffs Liberation Day"] = (
    pd.Timestamp("20250402", tzinfo=dt.timezone.utc),  # Announcement of Liberation Day tariffs
    pd.Timestamp("today", tzinfo=dt.timezone.utc), 
)