from projects.analytics.product_relation import main
import datetime
from datetime import datetime, timedelta
from lib import fn;
 
root_path = fn.getRootPath();
start_date = "2022-10-01"     
end_date = "2022-10-01"     

print(root_path)
exit()
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