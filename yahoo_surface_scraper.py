# Connor Sanders
# 10/16/2017

# Yahoo Finance Web Scraper
# Tested on python 2.7 and 3.5
# Returns a JSON File containing financial statement data for a given company or list of companies

# How to use this script:
#   Make sure you have the PhantomJS Driver set up. If you need the manually add the path, go to line 150
#   python yahoo_surface_scraper.py StockTicker StatementType JSONFilename Frequency
#   If running multiple stock tickers at once, separate them each by commas with no spaces in between
# Examples:
#   python yahoo_surface_scraper.py AAPL Income test.json Annual
#     or
#   python3 yahoo_surface_scraper.py WFC Balance testfile Quarterly
#     or
#   python3 yahoo_surface_scraper.py WFC,AAPL Balance extracts.json Quarterly
# Feel free to email connor@exceleri.com with any questions, concerns, or improvement ideas!

import os
import sys
import re
import pip
from json import load, dump
import signal
import time
import datetime


# Package installer function to handle missing packages
def install(package):
    print(package + ' package for Python not found, pip installing now....')
    pip.main(['install', package])
    print(package + ' package has been successfully installed for Python\n Continuing Process...')

# Ensure beautifulsoup4 is installed
try:
    from bs4 import BeautifulSoup
except:
    install('beautifulsoup4')
    from bs4 import BeautifulSoup

# Ensure selenium is installed
try:
    from selenium import webdriver
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
except:
    install('selenium')
    from selenium import webdriver
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By


# Declare datetime time stamp, and current working directory and file variables
dt = datetime.datetime.today()
c_dir = os.getcwd()

# OS Specific Code for Cross Platform Purposes
os_system = os.name
if os_system == 'nt':
    json_local_dir = c_dir + '\\json_extracts\\'
    fields_dir = c_dir + '\\data_fields\\'
else:
    json_local_dir = c_dir + '/json_extracts/'
    fields_dir = c_dir + '/data_fields/'


class YahooFinanceFundamentals:

    def __init__(self, ticker):
        self.ticker = ticker

    # Yahoo Finance Base URL
    BASE_YAHOO_URL = 'https://finance.yahoo.com/quote/'
    FIELD_PARAM_FILE = 'yahoo_finance_fields.json'

    # Script Data Dictionary to map statement type to yahoo finance naming conventions
    _YAHOO_FINANCIAL_TYPES = {
        'income': 'financials',
        'balance': 'balance-sheet',
        'cash': 'cash-flow',
    }

    # Private Static Method to determine if variable is an int or not
    @staticmethod
    def _determine_if_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    # Private Static Method to determine if variable is an int or not
    @staticmethod
    def _determine_quarterly_button(soup):
        for buttons in soup.find_all('button'):
            if 'Quarterly' in str(buttons):
                return buttons

    # Private Static Method to convert tem[ 0 placeholders back to '-'
    @staticmethod
    def _convert_null_data_to_str(data_value):
        re_value = data_value
        if str(data_value) == '0':
            re_value = '-'
        return re_value

    # Private Static Method to determine if data has 3 or 4 periods
    @staticmethod
    def _frequency_count(frequency):
        if frequency == 'annual':
            period_count = 3
        elif frequency == 'quarterly':
            period_count = 4
        else:
            print('Please enter a frequency value of either annual or quarterly')
            sys.exit(1)
        return period_count

    # Private Static Method to reformat json data fields to camel case
    @staticmethod
    def _reformat_field_json(field_string):
        if ' ' in field_string:
            split_field_str_list = list(field_string.replace('/', ' ').split(' '))
            form_field = ''
            i = 0
            for split_field in split_field_str_list:
                if i == 0:
                    form_field += split_field.lower()
                    i += 1
                else:
                    form_field += split_field.capitalize()
        else:
            form_field = field_string.lower()
        return form_field

    # Private Static Method to open and load field data from field json file
    def _get_json_file_fields(self, statement_type):
        with open(fields_dir + self.FIELD_PARAM_FILE) as json_data:
            json_field_file_data = load(json_data)
        return json_field_file_data[statement_type]

    # Private Method to scrap data from yahoo finance web page
    def _scrap_yahoo_data(self, ticker, statement_type, frequency):
        raw_data_list = []
        YAHOO_URL = self.BASE_YAHOO_URL + ticker + '/' + self._YAHOO_FINANCIAL_TYPES[statement_type] + '?p=' + ticker
        driver = webdriver.PhantomJS()
        driver.implicitly_wait(5)
        driver.get(YAHOO_URL)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        if frequency == 'quarterly':
            q_button = self._determine_quarterly_button(soup)
            button_class = str(q_button.find_all('div')[0]).split('"')[1]
            button_xpath = '//*[@class="' + button_class + '"]/span'
            button = driver.find_element_by_xpath(button_xpath)
            i = 0
            while i < 10:
                try:
                    button.click()
                    WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.XPATH, button_xpath)))
                    break
                except:
                    i += 1
                    continue
            if i == 10:
                print('Please check your internet connection!\nUnable to connect to ' + YAHOO_URL + '! Exiting...')
                sys.exit(1)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
        for table_data in soup.find_all('td'):
            raw_data_list.append(table_data)
        driver.service.process.send_signal(signal.SIGTERM)
        driver.quit()
        return raw_data_list

    # Private method to organized returned raw data from scrap into a semi organized state
    def _raw_data_organization(self, ticker, statement_type, frequency):
        num_of_periods = self._frequency_count(frequency)
        dates = []
        financials_dict = {}
        raw_data_list = self._scrap_yahoo_data(ticker, statement_type, frequency)
        prev_val = ''
        cur_field = ''
        cur_values = []
        i = 0
        for raw_data in raw_data_list:
            if 'span' in str(raw_data):
                cleaned_value = str(raw_data.find_all('span')[0]).split('>')[1].split('<')[0]\
                    .replace("'", "").replace(',', '').replace('-', '0')
            else:
                cleaned_value = str(raw_data).split('>')[1].split('<')[0].replace("'", "").replace(',', '')\
                    .replace('-', '0')
            if len(cleaned_value.split('/')) == 3:
                dates.append(cleaned_value)
            else:
                if self._determine_if_int(cleaned_value) and self._determine_if_int(prev_val) is not True:
                    cur_field = prev_val
                    check_data = self._convert_null_data_to_str(cleaned_value)
                    cur_values.append(check_data)
                    i += 1
                elif self._determine_if_int(cleaned_value) and self._determine_if_int(prev_val):
                    check_data = self._convert_null_data_to_str(cleaned_value)
                    cur_values.append(check_data)
                    i += 1
                    if i == num_of_periods:
                        dict_ent = {cur_field: cur_values}
                        financials_dict.update(dict_ent)
                        cur_field = ''
                        cur_values = []
                        i = 0
                prev_val = cleaned_value
        return [dates, financials_dict]

    # Private Method to build the data dict entries
    def _get_financial_data_dict_ent(self, ticker, statement_type, frequency):
        output_list = []
        org_data = self._raw_data_organization(ticker, statement_type, frequency)
        date_list = org_data[0]
        finance_dict = org_data[1]
        data_fields = self._get_json_file_fields(statement_type)
        i = 0
        for date in date_list:
            date_fin_dict = {}
            sub_list = []
            for objs in data_fields:
                cat_data_dict = {}
                temp_data_dict = {}
                for r_column in list(objs.values())[0]:
                    column = self._reformat_field_json(r_column)
                    try:
                        dict_ent = {column: int(finance_dict[r_column][i])}
                    except:
                        dict_ent = {column: finance_dict[r_column][i]}
                    temp_data_dict.update(dict_ent)
                r_section_label = list(objs.keys())[0].split(',')[0]
                section_label = self._reformat_field_json(r_section_label)
                dict_ent = {section_label: temp_data_dict}
                cat_data_dict.update(dict_ent)
                sub_list.append(cat_data_dict)
            dict_ent = {date: sub_list}
            date_fin_dict.update(dict_ent)
            output_list.append(date_fin_dict)
            i += 1
        dict_ent = {ticker + '-' + statement_type + '-' + frequency: output_list}
        return dict_ent

    # Public method for the user to call for financial data
    def pull_financial_fundamentals(self, statement_type, frequency):
        output_obj = {}
        if isinstance(self.ticker, str):
            dict_ent = self._get_financial_data_dict_ent(self.ticker.upper(), statement_type.lower(), frequency.lower())
            output_obj.update(dict_ent)
        else:
            for tick in self.ticker:
                dict_ent = self._get_financial_data_dict_ent(tick.upper(), statement_type.lower(), frequency.lower())
                output_obj.update(dict_ent)
        return output_obj


# Function to check user inputs
def check_inputs(script_args):
    if len(script_args) > 5:
        print('Please check your script parameters and try again!\n Make sure you if enter multiple '
              'tickers to have them in the following format without any spaces in between:\n')
        print('python yahoo_surface_scraper.py AAPL,WFC Income examplefile.json Quarterly')
        sys.exit(1)
    elif len(script_args) < 4:
        print('Please check your script parameters to ensure you are not missing any.\n'
              'To run this script you will need to enter atleast a ticker symbol and a desired statement type!')
        print('python yahoo_surface_scraper.py AAPL,WFC Cash examplefile.json')


# Function to create JSON Extract File Name
def get_json_filename(json_filename_input, statement_type, frequency):
    clean_filename_input = json_filename_input.replace(' ', '-').replace('_', '-')
    dt_str = str(dt).replace(':', '-').replace(' ', '_').split('.')[0]
    if '.' in clean_filename_input:
        filename_list = list(clean_filename_input.split('.'))
        if len(filename_list) > 2:
            print("Incorrect JSON Extract File naming Convention, Please don't add any extra periods! Exiting...")
            sys.exit(1)
        json_file_pre = filename_list[0]
    else:
        json_file_pre = clean_filename_input
    json_filename = str(json_file_pre + '_' + statement_type + '-' + frequency + '_' + dt_str + '.json').lower()
    return json_filename


# Function to write JSON Data to Timestamped JSON Output File
def create_json_extract_file(json_filename, json_data):
    with open(json_local_dir + json_filename, 'w') as json_outfile:
        dump(json_data, json_outfile, indent=4)
    print(json_filename + ' has been successfully created and can be found in ' + json_local_dir)


# Main Function
def main(ticker, statement_type, json_filename_input, frequency="annual"):
    if ',' in ticker:
        ticker = list(ticker.replace(' ', '').split(','))
    yahoo_fundamentals = YahooFinanceFundamentals(ticker)
    financial_data_extract = yahoo_fundamentals.pull_financial_fundamentals(statement_type, frequency)
    json_filename = get_json_filename(json_filename_input, statement_type, frequency)
    create_json_extract_file(json_filename, financial_data_extract)
    print(frequency.capitalize() + ' ' + statement_type.capitalize() +
          ' Data has been extracted and stored in for the following stocks: ')
    print(str(ticker).replace("['", "").replace("']", "").replace("', '", ", "))
    print('Process Completed Successfully!')


# Main Process Handler for Script
if __name__ == '__main__':
    check_inputs(sys.argv)
    if len(sys.argv) == 5:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 4:
        main(sys.argv[1], sys.argv[2], sys.argv[3])