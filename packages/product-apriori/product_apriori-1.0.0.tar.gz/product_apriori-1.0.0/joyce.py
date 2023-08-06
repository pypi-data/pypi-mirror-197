
from logging import root
# import Router;
import os;
from pip import main
from lib import DateTime;
from lib import fn;
from datetime import date
import nltk;

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown')

try:
    nltk.data.find('corpus/reader/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpus/reader/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')
    
root_path = fn.getRootPath();


# #------------------------------------------------------------------------------------------- import library testing
# pip install wheel
# pip install setuptools
# pip install twine
# pip install pytest==4.4.1
# pip install pytest-runner==4.4

from product_apriori import main
import datetime
from datetime import datetime, timedelta

 

start_date = "2022-10-01"     
end_date = "2022-10-01"     


main.run({
    'root_path':root_path,
    'include_plucode': [],          # empty list will include all the plucode
    'include_department': [],       # empty list will include all the department
    'exclude_department': ['101', '-', '', '990', '989'],
    'include_m_category': [],       # empty list will include all the m category
    'store_code': ['B081'],
    'date_time_list': start_date,
    'end_date': end_date,
    'country_list': ['my'],
    'level': 'M_PLUCODE',   # M_DEPARTMENT, M_PLUCODE, M_CATEGORY
    'minsup': 0.002,
    'refresh': True,
    # 'share_drive': "Y:\\",
    # 'process': ['merge_all_raw', 'filter_raw', 'transform', 'apriori'], # 'merge_all_raw', 'filter_raw', 'transform', 'apriori'
    'process': ['merge_filter_raw', 'transform', 'apriori'], # 'merge_filter_raw', 'transform', 'apriori'
})
