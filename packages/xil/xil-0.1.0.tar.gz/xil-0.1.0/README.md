[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Tests](https://github.com/jond01/xil/actions/workflows/tests.yml/badge.svg)](https://github.com/jond01/xil/actions/workflows/tests.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

# XIL

Gather and compare foreign currency exchange buy and sell rates offered by Israeli
banks.


## Banks data

The XIL project supports the following banks:

| Bank and data source                                                                                                                                       | XIL module        | Tests | Bank name (Hebrew)           |
|------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|-------|------------------------------|
| [Bank Leumi Le-Israel](https://www.leumi.co.il/Lobby/currency_rates/40806/)                                                                                | `leumi`           | :x:   | בנק לאומי לישראל             |
| [Bank Hapoalim](https://www.bankhapoalim.co.il/he/foreign-currency/exchange-rates)                                                                         | `poalim`          | :x:   | בנק הפועלים                  |
| [Mizrahi Tefahot Bank](https://www.mizrahi-tefahot.co.il/brokerage/currancyexchange/)                                                                      | `mizrahi_tefahot` | :x:   | בנק מזרחי טפחות              |
| [Israel Discount Bank](https://www.discountbank.co.il/DB/private/general-information/foreign-currency-transfers/exchange-rates)                            | `discount`        | :x:   | בנק דיסקונט לישראל           |
| [First International Bank of Israel](https://www.fibi.co.il/wps/portal/FibiMenu/Marketing/Private/ForeignCurrency/Trade/Rates)                             | `fibi`            | :x:   | הבנק הבינלאומי הראשון לישראל |
| [Bank of Jerusalem](https://www.bankjerusalem.co.il/capital-market/rates)                                                                                  | `jerusalem`       | :x:   | בנק ירושלים                  |
| [Mercantile Discount Bank](https://www.mercantile.co.il/MB/private/foregin-currency/exchange-rate)                                                         | `mercantile`      | :x:   | בנק מרכנתיל דיסקונט          |
| [Bank Massad](https://www.bankmassad.co.il/wps/portal/FibiMenu/Marketing/Private/ForeignCurrency/ForexOnline/Rates)                                        | `massad`          | :x:   | בנק מסד                      |
| [Bank of Israel](https://www.boi.org.il/roles/markets/%D7%A9%D7%A2%D7%A8%D7%99-%D7%97%D7%9C%D7%99%D7%A4%D7%99%D7%9F-%D7%99%D7%A6%D7%99%D7%92%D7%99%D7%9D/) | `boi`             | :x:   | בנק ישראל                    |

For the data sources (websites and URLs) for each bank, see the docstring of the
corresponding XIL module.

Banks that are not supported yet:

- Bank Yahav (בנק יהב): no public information available.
  https://www.bank-yahav.co.il/investments/foreing-currency/
- One Zero Digital Bank (וואן זירו הבנק הדיגיטלי): no public information available.
  https://www.onezerobank.com/

## Installation
The project requires Python 3.10 or above. To install the project, run:
```shell
pip install git+https://github.com/jond01/xil.git
```

## Contributing to the XIL project
Please read the [Contribution Guide](CONTRIBUTING.md).
