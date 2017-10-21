# yahoo_finance_stock_scraper

## Overview

A python script that scrapes the financial statement data of a list of stocks and stores the data to a JSON file. The script uses Selenium with PhantomJS and BeautifulSoup4 to achieve this.

## Features
Runs on Linux, Mac and Windows machines.
The script is set up to automatically install all unmet prerequisite packages using pip
This script will generated a json file in the json_extracts directory filled with request stock financial data
You can run one company at a time, or a whole list of them.
Tested on Python 2.7 and 3.5

## How to Use
1. Make sure you have python 2 or 3 installed with pip on your machine
2. Install the PhantomJS Web-driver if you haven't already. You can also download the executable and set a path to it on line 150.
  * [Download-PhantomJS](http://phantomjs.org/download.html) - Official driver download page with Windows and Mac executables ready to go.
  * [PhantomJS-Debian](https://www.vultr.com/docs/how-to-install-phantomjs-on-ubuntu-16-04) - In-depth setup guide for Debian/Ubuntu users due to extra steps
  * [PhantomJS-CentOS](http://teition.com/installing-phantomjs-on-amazon-linux-fedora-redhat-centos-over-ssh/) - Setup guide for RHEL, Amazon Linux, CentOS, and Fedora.
3. git copy the repository
```R
git clone https://github.com/JECSand/yahoo_finance_stock_scraper.git
```
4. cd into the yahoo_finance_stock_scraper directory
5. Enter the command in the following format to convert a single excel file:
```R
python yahoo_surface_scraper.py "StockTicker(s)" "StatementType" "JSONFilename" "Frequency"(Optional)
```
6. Use these guidelines for your Script Parameters
* StockTicker:
    * Either a single stock symbol, or a group of them separated by commas with no spaces unless wrapped in double quotes
* StatementType:
    * Determines which of the three financial statements will be pulled for each stock. Options are:
        * income - which will grab the stock's income statements
        * balance - which will extract the companies' balance sheets
        * cash - which will get the cash flow statements for the companies
* JSONFilename:
    * Desired naming convention for the extract file. An identifying meta-data stamp will also be added.
* Frequency:
    * Optional parameter for specifying the time period frequency of the returned data. Options are:
        * Annual (Default Value) - will return the last 3 years of data at annual intervals of time
        * Quarterly - will return the last 4 quarters of data at intervals of ~3 months each
7. Your newly extracted data will be located in the json_extracts directory!
## Examples
1. The following command will return Annual Income Statement data for Apple and store it in test_income-annual_YYYY-MM-DD_HH-mm-ss.json:
```R
python yahoo_surface_scraper.py "AAPL" "Income" "test.json" "Annual"
```
2. The next command will return Quarterly Balance Sheet data for both Wells Fargo and Ford Motor Co. The data will be saved to testfile_balance-quarterly_YYYY-MM-DD_HH-mm-ss.json:
```R
python3 yahoo_surface_scraper.py "WFC, F" "Balance" "testfile" "Quarterly"
```
3. The final example will return Annual Cash Flow data for Wells Fargo, Apple, and Ford Motor Co. The data will be saved to testdemo_cash-annual_YYYY-MM-DD_HH-mm-ss.json:
```R
python yahoo_surface_scraper.py "WFC, AAPL, F" "cash" "testdemo.json"
```
## Examples of Output
1. test_income-annual_YYYY-MM-DD_HH-mm-ss.json:
```javascript
{
    "AAPL-income-annual": [
        {
            "9/24/2016": [
                {
                    "revenue": {
                        "grossProfit": 84263000,
                        "totalRevenue": 215639000,
                        "costOfRevenue": 131376000
                    }
                },
                {
                    "operatingExpenses": {
                        "nonRecurring": "-",
                        "others": "-",
                        "sellingGeneralAndAdministrative": 14194000,
                        "operatingIncomeOrLoss": 60024000,
                        "totalOperatingExpenses": "-",
                        "researchDevelopment": 10045000
                    }
                },
                {
                    "incomeFromContinuingOperations": {
                        "totalOtherIncomeExpensesNet": 1348000,
                        "minorityInterest": "-",
                        "netIncomeFromContinuingOps": 45687000,
                        "incomeTaxExpense": 15685000,
                        "interestExpense": "-",
                        "incomeBeforeTax": 61372000,
                        "earningsBeforeInterestAndTaxes": 61372000
                    }
                },
                {
                    "non-recurringEvents": {
                        "otherItems": "-",
                        "extraordinaryItems": "-",
                        "discontinuedOperations": "-",
                        "effectOfAccountingChanges": "-"
                    }
                },
                {
                    "netIncome": {
                        "netIncome": 45687000,
                        "netIncomeApplicableToCommonShares": 45687000,
                        "preferredStockAndOtherAdjustments": "-"
                    }
                }
            ]
        }
    ]    
}
```
2. testfile_balance-quarterly_YYYY-MM-DD_HH-mm-ss.json
```javascript
{
    "F-balance-quarterly": [
        {
            "6/30/2017": [
                {
                    "currentAssets": {
                        "netReceivables": 60047000,
                        "cashAndCashEquivalents": 16223000,
                        "otherCurrentAssets": 3291000,
                        "shortTermInvestments": 22886000,
                        "inventory": 11092000
                    }
                },
                {
                    "fixedAssets": {
                        "longTermInvestments": 54792000,
                        "propertyPlantAndEquipment": 62391000,
                        "accumulatedAmortization": "-",
                        "otherAssets": 6602000,
                        "goodwill": "-",
                        "deferredLongTermAssetCharges": 10145000,
                        "intangibleAssets": "-"
                    }
                },
                {
                    "currentLiabilities": {
                        "otherCurrentLiabilities": 19958000,
                        "accountsPayable": 23568000,
                        "shortCurrentLongTermDebt": 50773000
                    }
                },
                {
                    "long-termLiabilities": {
                        "minorityInterest": 18000,
                        "negativeGoodwill": "-",
                        "otherLiabilities": 24840000,
                        "deferredLongTermLiabilityCharges": 735000,
                        "longTermDebt": 95236000
                    }
                },
                {
                    "stockholdersEquity": {
                        "commonStock": 41000,
                        "treasuryStock": 1253000,
                        "redeemablePreferredStock": "-",
                        "retainedEarnings": 18437000,
                        "preferredStock": "-",
                        "otherStockholderEquity": 6716000,
                        "capitalSurplus": 21735000,
                        "misc.StocksOptionsWarrants": 97000
                    }
                },
                {
                    "balanceSheetTotals": {
                        "totalCurrentLiabilities": 94299000,
                        "totalLiabilities": 215128000,
                        "totalAssets": 247469000,
                        "totalStockholderEquity": 32244000,
                        "netTangibleAssets": 32244000,
                        "totalCurrentAssets": 113539000
                    }
                }
            ]
        }
    ]
}
```
3. testdemo_cash-annual_YYYY-MM-DD_HH-mm-ss.json
```javascript
{
    "F-cash-annual": [
        {
            "12/31/2016": [
                {
                    "operatingActivities": {
                        "adjustmentsToNetIncome": 3544000,
                        "changesInOtherOperatingActivities": 1000,
                        "changesInAccountsReceivables": 2855000,
                        "depreciation": 8717000,
                        "changesInInventories": 815000,
                        "changesInLiabilities": 6595000
                    }
                },
                {
                    "investingActivities": {
                        "otherCashFlowsFromInvestingActivities": 55945000,
                        "capitalExpenditures": 6992000,
                        "investments": 37585000
                    }
                },
                {
                    "financingActivities": {
                        "netBorrowings": 11028000,
                        "otherCashFlowsFromFinancingActivities": 49000,
                        "salePurchaseOfStock": 145000,
                        "dividendsPaid": 3376000
                    }
                },
                {
                    "cashFlowTotals": {
                        "netIncome": 4596000,
                        "changeInCashAndCashEquivalents": 1633000,
                        "totalCashFlowsFromInvestingActivities": 25352000,
                        "totalCashFlowsFromFinancingActivities": 7458000,
                        "totalCashFlowFromOperatingActivities": 19792000
                    }
                }
            ]
        }
    ]
}
```
