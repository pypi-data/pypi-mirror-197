"""
Mercantile bank

https://www.mercantile.co.il/MB/private/foregin-currency/exchange-rate

The structure is identical Discount's, but the data is different.
"""
import pandas as pd

from xil.discount import get_discount_df

_MERCANTILE_URL = "\
https://www.mercantile.co.il/MB/private/foregin-currency/exchange-rate"


def get_mercantile_df(url: str = _MERCANTILE_URL) -> pd.DataFrame:
    """Get Mercantile Bank exchange rates"""
    # The structure is identical Discount's, but the data is different - use Discount's
    # function
    return get_discount_df(url)


if __name__ == "__main__":
    print(get_mercantile_df())
