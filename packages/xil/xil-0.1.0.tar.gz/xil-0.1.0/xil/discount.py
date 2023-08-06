"""
Discount bank

https://www.discountbank.co.il/DB/private/general-information/foreign-currency-transfers/exchange-rates
"""
from typing import Callable

import pandas as pd

from xil._df_normalizer import BaseDataFrameNormalizer

_DISCOUNT_URL = "\
https://www.discountbank.co.il/DB/private/general-information/foreign-currency-transfers/exchange-rates"
_IDX0 = pd.MultiIndex.from_product([["currency"], ["amount", "code", "official rate"]])
_IDX1 = pd.MultiIndex.from_product([["transfer", "cash"], ["buy", "sell"]])
_DISCOUNT_IDX = _IDX0.append(_IDX1)


def get_discount_df(url: str = _DISCOUNT_URL) -> pd.DataFrame:
    """Get Discount Bank exchange rates"""
    df = pd.read_html(url, header=[0, 1])[0]
    df.columns = _DISCOUNT_IDX
    amount_key = ("currency", "amount")
    amount_fixer: Callable[[str], str] = lambda x: x.split(" ")[0]
    df[amount_key] = df[amount_key].apply(amount_fixer)
    df = BaseDataFrameNormalizer(df).norm()
    return df


if __name__ == "__main__":
    print(get_discount_df())
