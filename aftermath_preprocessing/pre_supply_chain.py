import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
pd.set_option('display.max_colwidth', -1)  # or 199
pd.set_option('display.max_columns', None)  # or 1000
# pd.set_option('display.max_rows', None)  # or 1000


df = pd.read_csv('data/global_supplychain.csv')
df = df[['supplier_ticker', 'customer_ticker', 'revenue_dependency']]
G = nx.from_pandas_edgelist(df, 'supplier_ticker', 'customer_ticker', ['revenue_dependency'])
nx.draw(G,node_size=0.5)
plt.show()
# df2 = df[['supplier_ticker', 'customer_ticker']].copy()
