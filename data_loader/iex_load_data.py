import pandas_datareader.data as web
from datetime import datetime
import os

os.environ["IEX_API_KEY"] = "pk_960e75eef25a40eb960a43626ac4487a"
# os.environ["IEX_API_KEY"] = "sk_bc11cd2d4a30446e9471b640d7cb47a9"

start = datetime(2016, 9, 1)

end = datetime(2018, 9, 1)

# api_key=os.getenv('TIINGO_API_KEY')

f = web.DataReader('F', 'iex', start, end, access_key=os.getenv("IEX_API_KEY"))

print(f.loc['2018-08-31'])