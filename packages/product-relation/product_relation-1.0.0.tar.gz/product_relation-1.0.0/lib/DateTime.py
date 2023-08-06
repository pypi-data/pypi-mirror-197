from dateutil.relativedelta import relativedelta;
from datetime import datetime, timedelta, timezone, date;
import locale;
import dateutil.parser as dateparser;
from dateutil.parser import parse;
import pytz;
import math;
import calendar;
import time;
from . import fn;
from . import Logger;
import pandas as pd
def now(tzinfo=None, timestamp=False):
  if timestamp:
    return time.time();
  if tzinfo:
    return datetime.now(tzinfo);
  return datetime.utcnow();

def isSameDay(date):
  if not type(date) == datetime:
    date = getDateTime(date);
  return date.date() == datetime.today().date();

def getDateRange(duration):
  timestamp_from = getDateDayRange(duration[0]);
  timestamp_to = getDateDayRange(duration[1]);
  return [timestamp_from[0], timestamp_to[1]];
def getDateDayRange(datefrom):
  day_timestamp = math.floor(datefrom.timestamp()/86400);
  day_start_timestamp = getDateTime(day_timestamp*86400);
  day_end_timestamp = getDateTime((day_timestamp+1)*86400) - timedelta(microseconds=1);
  return [day_start_timestamp, day_end_timestamp];
def getDateTime(timestamp, tzinfo=timezone.utc):
  return datetime.fromtimestamp(timestamp, tzinfo);

def getMinutesAgo(minutes_to_check, dateFrom=datetime.utcnow()):#get datetime hours ago
  # Logger.v(hours_to_check, dateFrom);
  return dateFrom - timedelta(minutes=int(minutes_to_check));
def getHoursAgo(hours_to_check, dateFrom=datetime.utcnow()):#get datetime hours ago
  # Logger.v(hours_to_check, dateFrom);
  return dateFrom - timedelta(hours=int(hours_to_check));
def getDaysAgo(days_to_crawl, datefrom=None): # get datetime days ago
  if type(datefrom) == str:
    datefrom = convertDateTimeFromString(datefrom);
  if datefrom == None:
    datefrom = datetime.utcnow();
  elif not type(datefrom) == datetime:
    datefrom = convertDateTimeFromString(datefrom);
  return datefrom - timedelta(days=days_to_crawl);

def getMonthsAgo(months_to_crawl=0, datefrom=None): # get datetime months ago
  if type(datefrom) == str:
    datefrom = convertDateTimeFromString(datefrom);
  if datefrom == None:
    datefrom = now();
    datefrom = datefrom.replace(day=1);
  if months_to_crawl > 0:
    new_month = datefrom.month - months_to_crawl;
    new_year = math.ceil(abs(new_month)/12);
    if new_month <= 0:
      if new_month == 0:
        new_year += 1;
        new_month = 12;
      datefrom = datefrom.replace(year=datefrom.year-new_year, month=(new_month%13));
    else:
      datefrom = datefrom.replace(month=new_month);
    datefrom = datefrom + relativedelta(months=-months_to_crawl);

  return datefrom;

def getMonthsAgoNew(months_to_crawl=0, datefrom=None): # get datetime months ago
  if type(datefrom) == str:
    datefrom = convertDateTimeFromString(datefrom);
  if datefrom == None:
    datefrom = now();
    datefrom = datefrom.replace(day=1);
  if months_to_crawl > 0:
    datefrom = datefrom + relativedelta(months=-months_to_crawl);

  return datefrom;

def getNextMonth(today):
  if type(today) == str:
    today = convertDateTimeFromString(today);
  first_day = today.replace(day=1);
  if first_day.month == 12:
    return first_day.replace(year=first_day.year+1, month=1);
  else:
    return first_day.replace(month=first_day.month+1);

def getNextMonthV2(months_to_crawl=0, datefrom=None):
  if datefrom == None:
    datefrom = now();
  if type(datefrom) == str:
    datefrom = convertDateTimeFromString(datefrom);
  datefrom = datefrom.replace(day=1);
  if months_to_crawl > 0:
    datefrom = datefrom + relativedelta(months=months_to_crawl);
  return datefrom;

def getEndOfTheDay(datefrom):
  return datefrom + timedelta(days=1) - timedelta(seconds=1);
def getDifferenceBetweenDuration(durations, element='day'):
  if element == 'minute':
    result = getDifferenceInMinutes(durations[0], durations[1]);
  else:
    result = getDifferenceInNearestDays(durations[0], durations[1]);
  return result;
def getDifferenceInMonths(datefrom, dateto):
  months = 0;
  if type(datefrom) == str:
    datefrom = parse(datefrom);
  if type(dateto) == str:
    datefrom = parse(dateto);
  months = relativedelta(dateto, datefrom).months;
  return months;
def getDifferenceInNearestDays(datefrom, dateto):
  if type(datefrom) == str:
    datefrom = convertDateTimeFromString(datefrom);
  if type(dateto) == str:
    dateto = convertDateTimeFromString(dateto);
  different = dateto - datefrom;
  return math.ceil(different.total_seconds()/float(86400)+1);
def getDifferenceInMinutes(datefrom, dateto):
  if type(datefrom) == str:
    datefrom = convertDateTimeFromString(datefrom);
  if type(dateto) == str:
    dateto = convertDateTimeFromString(dateto);
  different = dateto - datefrom;
  return math.ceil(different.total_seconds()/float(60));
def convertDateTimeFromString(date, offset=0, negative=False, include_timezone=True, is_string=False):
  #return dateparser.parse(date);
  if isTimestamp(date) and is_string == False:
    date = convertDateTimeFromTimestamp(date);
  
  if type(date) == datetime:
    return date;
  if type(date) == str:
    if date and '+' in date:
      date_parts = date.split('+');
      date = '{0}+{1}'.format(date_parts[0], date_parts[-1].replace(':', ''));

    dataset = ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S','%Y-%m-%d', '%Y-%m-%d %H-%M-%S', '%Y-%m-%d %H-%M-%S.%f', '%Y-%m-%d %H:%M:%S%z', '%Y-%m-%d %H:%M:%S%z', '%Y-%m', '%d-%m-%Y', '%d/%m/%Y', '%d.%m.%y', '%d.%m.%y %H:%M', '%d/%m/%Y %H:%M', '%d/%m/%y %H:%M', '%d/%m/%Y', '%y%m%d', '%Y%m%d', '%Y %m', '%M-%y', '%d%m%Y'];

    for dset in dataset:
      try:
        new_date = datetime.strptime(date, dset);
        if new_date.tzinfo == None:
          new_date = new_date.replace(tzinfo=pytz.UTC);
        if offset != 0:
          if negative == False:
            new_date = new_date - timedelta(hours=offset);
          else:
             new_date = new_date + timedelta(hours=offset);
        
        if include_timezone == True:
          result = new_date;
        else:
          result = new_date.replace(tzinfo=None);
        return result;
      except Exception as ex:
        continue;
        # Logger.e('convertDateTimeFromString.error', ex);
      
def getReadableDate(date, detail=False, date_format='%d %b %Y'):
  if type(date) == str:
    date = convertDateTimeFromString(date);
  
  #if not detail:
  return date.strftime(date_format);
  #else:
  #  return date.strftime('%d %b %Y \t %I:%M %p');
def toString(date, withDetail=True, withTimezone=False, date_format='%Y-%m-%d'):
  if type(date) == str:
    date = convertDateTimeFromString(date);
  if withTimezone:
    return date.strftime('%Y-%m-%dT%H:%M:%S%z');
  if not withDetail:
    return date.strftime('%Y-%m-%d %H:%M:%S');
  return date.strftime(date_format);
def getNextMonthStartDate(month=0):
  today = now();
  new_month = today.month+month+1;
  if new_month > 12:
    today = today.replace(year=today.year+1, month=new_month-12);
  else:
    today = today.replace(day=1, month=new_month);
  return today.replace(day=1);
def getLastMonthEndDate(month=0):
  today = now();
  today = today.replace(day=1);
  if month > 0:
    new_month = today.month - month;
    new_year = math.ceil(abs(new_month)/12);
    if new_month <= 0:
      if new_month == 0:
        new_year += 1;
        new_month = 12;
      today = today.replace(year=today.year-new_year, month=(new_month%13));
    else:
      today = today.replace(month=new_month);

  return today - timedelta(days=1);
def getYesterdayEndDate():
  return now() - timedelta(days=1);
def getPastDate(count=1, end=None, duration=3):
  current = now();
  if end == None:
    end = getDaysAgo(0);
  year = end.year;
  months = [];
  for m in range(0, min(36, count+1)): #limit max to 3 year
    #print(int((today.month-month))%12, (today.month-month));
    different = (end.month-m-1);
    if different < 0 and different>= -24:
      year = end.year + math.ceil((different+1)/12)-1;
    elif different >=0:
      year = end.year
    else:
      continue;

    month = different%12+1;
    #print(count, different, math.ceil(different/12)-1);
    #print(today.year-int(today.month-month));
    if m == 0:
      last_day = end.day;
    else:
      first_weekday, last_day = calendar.monthrange(year, month);
    
    first_date = end.replace(year=year, month=month, day=1) - timedelta(days=1); 
    last_date = end.replace(year=year, month=month, day=last_day) + timedelta(days=1);

    if year < (current.year - 2):
      Logger.v('break');
      break;
    months.append((first_date, last_date));
  total_days = (months[0][1] - months[-1][0]).days;
  result = [];
  for m in fn.chunks(months, duration):
    result.append([toString(m[-1][0]), toString(m[0][1])]);
  return (result, total_days);
def adjustPastDate(pastDate, start_date, exact=True):
  readable_start_date = toString(start_date);
  pastDate = list(pastDate);
  for index in range(0, len(pastDate)):
    p = pastDate[index];
    s = convertDateTimeFromString(p[0]);
    e = convertDateTimeFromString(p[1]) - timedelta(days=1);
    if isAfter(readable_start_date, s):
      if isBefore(readable_start_date, e):
        if exact:
          pastDate[index][0] = readable_start_date;
        return pastDate[:index+1];
      else:
        if not exact:
          return pastDate[:index+1];
        return None;
  return pastDate;
def inrange(created_time, timerange):
  if type(created_time) == str:
    created_time= convertDateTimeFromString(created_time);
  if isAfter(created_time, timerange[0])  and isBefore(created_time, timerange[1]):
    return True;
  return False;

def filterDataByRange(data, date_range, keyname='created_time'): #date_range is tupple
    start_date = convertDateTimeFromString(date_range[0]);
    end_date = convertDateTimeFromString(date_range[1]) + timedelta(days=1);
    return (list(filter(lambda x: (isBefore(x[keyname], end_date) and isAfter(x[keyname], start_date)), data)) , (end_date-start_date).days);

def filterDatasByRange(datas, date_range, keyname='created_time'): #date_range is tupple
  result = {};
  days = 0;
  for name in datas.keys():
    result[name], days = filterDataByRange(datas[name], date_range, keyname);
  return result, days;
def isAfter(a, b, include_ref=True): #check if a is after date b
  if not type(a) == datetime:
    a = convertDateTimeFromString(a);
  if not type(b) == datetime:
    b = convertDateTimeFromString(b);

  if include_ref == True:
    result = a.utctimetuple() >= b.utctimetuple();
  else:
    result = a.utctimetuple() > b.utctimetuple();
  return result;

def isBefore(a, b): #check if a is before date b
  if not type(a) == datetime:
    a = convertDateTimeFromString(a);
  if not type(b) == datetime:
    b = convertDateTimeFromString(b);
  return a.utctimetuple() < b.utctimetuple();
day_of_week = ['Mond'];
def getDateCategoryName(date, element, offset=0):
  if type(date) == str:
    date = convertDateTimeFromString(date, offset=offset);
  else:
    date = getHoursAgo(-offset, dateFrom=date); 
  if element == 'day':
    return date.strftime('%d');
  elif element == 'week':
    return "Week %s of %s"%(math.ceil(date.day/7), date.strftime('%B'));
  elif element == 'year':
    return date.strftime('%Y');
  elif element == 'day_of_week':
    return date.strftime('%A');
  elif element == 'shortform_day_of_week':
    return date.strftime('%a');
  elif element == 'month':
    return date.strftime('%B');
  elif element == 'monthb_year':
    return date.strftime('%B_%Y');
  elif element == 'hour':
    return date.strftime('%H00');
  elif element == 'yearmonthdate':
    return date.strftime('%Y-%m-%d');
  elif element == 'monthBUnderscoreyear':
    return date.strftime('%B_%Y');
  elif element == 'year_month_digit':
    return date.strftime('%Y-%m');
  elif element == 'date_string':
    return date.strftime('%d %b %Y');
  elif element == 'short_year_month_string':
    y = date.strftime('%Y')[2:4];
    m = date.strftime('%b')[:3];
    return '{0}-{1}'.format(m, y);
  elif element == 'date':
    return toString(date);
  elif element == 'quarter':
    quarter_mapping = {};
    for m in range(1, 13):
      quarter_mapping[m] = (m-1)//3 + 1;
    return 'Q{0}'.format(quarter_mapping[date.month]);

def reorder(order_list, element):
  if element == 'hour' or element == 'day':
    return sorted(order_list);
  elif element == 'month':
    _MONTH_MAP = {m.lower(): i for i, m in enumerate(calendar.month_name[1:])}
    return sorted(order_list, key=lambda x: _MONTH_MAP[x.lower()]);
  elif element == 'day_of_week':
    _WEEKDAY_MAP = {d.lower(): i for i, d in enumerate(calendar.day_name)};
    return sorted(order_list, key=lambda x: _WEEKDAY_MAP[x.lower()]);
  return order_list;

def monthlyGetBetween(duration):
  # result = [];
  # duration = [convertDateTimeFromString(d) for d in duration];
  # current = duration[0];
  # result.append(toString(current));
  # while current < duration[1]:
  #   current = getNextMonth(current);
  #   result.append(toString(current));
  # # print(result)
  # return result;
  result = [];
  date_list = getBetween(duration, element='date', offset=0, data=None, default=None, date=False)['order'];
  for date in date_list:
    date_str = toString(date);
    monthly_date = '{0}-{1}-01'.format(date_str[0:4], date_str[5:7]);
    if monthly_date not in result:
      result.append(monthly_date);
  return result;
  
def getBetween(duration, element='day', offset=0, data=None, default=None, date=False):
  result = {
    'order': [],
    'data': {}, 
  };
  duration = [convertDateTimeFromString(d) for d in duration];
  if element == 'hour':
    for x in range(0, 24):
      current = now().replace(hour=x);
      name = getDateCategoryName(current, element, offset); 
      if not name in result['data']:
        result['data'][name] = [];
        result['order'].append(name);
  elif element == 'month':
    current = duration[0];
    while current < duration[1]:
      name = getDateCategoryName(current, element, offset); 
      current = getNextMonth(current);
      if not name in result['data']:
        result['data'][name] = [];
        result['order'].append(name);
  else: #support day and date
    different = getDifferenceInNearestDays(duration[0], duration[1]);
    for d in range(0, different):
      datefrom = getDaysAgo(-d, duration[0]);
      if date == True:
        name = getDateCategoryName(datefrom, 'yearmonthdate', offset);
      else:
        name = getDateCategoryName(datefrom, element, offset); 
      if not name in result['data']:
        if data and name in data:
          result['data'][name] = data[name];
        elif default:
          result['data'][name] = default;
        else:
          result['data'][name] = [];
        result['order'].append(name);


  result['order'] = reorder(result['order'], element);
  return result;
def convertDuration(duration, offset=0):
  duration[0] = convertDateTimeFromString(duration[0], offset);
  duration[1] = getEndOfTheDay(convertDateTimeFromString(duration[1], offset));
  return duration;

def getNextDay(days_to_crawl, datefrom=None): # get datetime days ago
  if datefrom == None:
    datefrom = datetime.utcnow();
  elif not type(datefrom) == datetime:
    datefrom = convertDateTimeFromString(datefrom);
  return datefrom + timedelta(days=days_to_crawl);

def getOffsetDate(date, offset=0, negative=False):
  if offset != 0:
    if negative == False:
      date = date - timedelta(hours=offset);
    else:
       date = date + timedelta(hours=offset);
    Logger.v('after offset date', date);     
  return date; 

def twitter_to_datetime(datestring):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(datestring,'%a %b %d %H:%M:%S +0000 %Y')) ;
    return ts;

def isDate(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    # print('type', type(string))
    if fn.isFloat(string) or fn.isInteger(string):
      return False;

    if type(string) == datetime:
      return True;

    if string is None or type(string) != str:
      return False;
    try: 
        # print(string)
        parse(string, fuzzy=fuzzy)
        return True;

    except ValueError:
        return False;

def monthMapping(mode='digit_name', name_length=None):
  result = {};
  for m in range(1, 13):
    month_name = getDateCategoryName(date='2020-{0}-01'.format(str(m).zfill(2)), element='month');
    month_name = month_name[:name_length].lower();
    if mode == 'name_digit':
      result[month_name] = m;
    else:
      result[m] = month_name;
  # Logger.v('result', result);
  return result;

def isTimestamp(string):
  dt_object = convertDateTimeFromTimestamp(string);
  if type(dt_object) == datetime:
    return True;
  else:
    return False;

def convertDateTimeFromTimestamp(string):
  dt_object = None;
  if fn.isInteger(string):
    # print(string)
    timestamp = fn.convertToInt(string);
    dt_object = datetime.fromtimestamp(timestamp);
    # print(dt_object)
  return dt_object;

def allDateOfWeek(year, weekday='sunday'):
  offset_mapping = {
    'monday': 'W-MON',
    'tuesday': 'W-TUE',
    'wednesday': 'W-WED',
    'thursday': 'W-THU',
    'friday': 'W-FRI',
    'saturday': 'W-SAT',
    'sunday': 'W-SUN',
  };
  year = int(year);
  offset_freq = offset_mapping[weekday];
  date_list = pd.date_range(start=str(year-1), end=str(year+2), freq=offset_freq).strftime('%Y-%m-%d').tolist();
  # print(date_list);
  return date_list;

def getCutOffByWeekday(check_date, weekday='sunday'):
  year = toString(convertDateTimeFromString(check_date), date_format='%Y');
  date_list = allDateOfWeek(year, weekday);
  # print('date_list', date_list, year, weekday, check_date)
  cutoff = None;
  for idx, date in enumerate(date_list):
    next_week_date = date_list[idx + 1];
    # print('date', check_date, 'next_week_date', next_week_date, date_list[idx], isAfter(check_date, date_list[idx]), isBefore(check_date, next_week_date))
    if isAfter(check_date, date_list[idx]) and isBefore(check_date, next_week_date):
      cutoff = next_week_date;
      break;
  # print('cutoff', cutoff)
  return cutoff;

def floatHourToTime(fh):
  hours, hourSeconds = divmod(fh, 1)
  minutes, seconds = divmod(hourSeconds * 60, 1)
  return (
      int(hours),
      int(minutes),
      int(seconds * 60),
  )

def convertExcelDate(excel_date):
  # print('excel_date', excel_date)
  if fn.isFloat(excel_date) and math.isnan(excel_date) == False:
    # excel_date = 42139.23213
    if type(excel_date) == str:
      excel_date = float(excel_date);
    dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + int(excel_date) - 2)
    hour, minute, second = floatHourToTime(excel_date % 1)
    dt = dt.replace(hour=hour, minute=minute, second=second)

    # print(dt)
    # assert str(dt) == "2015-05-15 00:13:55"
    return toString(dt);
  elif fn.isFloat(excel_date) and math.isnan(excel_date) == True:
    return None;
  else:
    return toString(excel_date);

def getDifferenceInMonths(start_date, end_date):
  
  # print(type(start_date) is None)
  # print(type(end_date) is None)
  if start_date is None or end_date is None:
    return None;
  else:
    if type(start_date) == str:
      start_date = convertDateTimeFromString(start_date);
    if type(end_date) == str:
      end_date = convertDateTimeFromString(end_date);
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month);

def getWeekNumber(date_string):
  if pd.isna(date_string) == False:
    dt = convertDateTimeFromString(date_string);
    week_num = toString(dt, date_format='%V');
  else:
    week_num = '';
  return week_num;

def getDateByWeekday(date_string, weekday='monday', nearest_date=False):
  weekday_mapping = {
    'monday': 1,
    'tuesday': 2,
    'wednesday': 3,
    'thursday': 4,
    'friday': 5,
    'saturday': 6,
    'sunday': 7,
  };
  day = fn.getNestedElement(weekday_mapping, weekday, None);
  week_num = getWeekNumber(date_string);
  result = None;
  if week_num != '' and day is not None:
    dt = convertDateTimeFromString(date_string);
    year = toString(dt, date_format='%Y');
    result = datetime.strptime(f'{year}-{week_num}-{day}', "%Y-%W-%w");
    result = toString(result);

  # if nearest_date == False:
  #   if isBefore(date_string, result) == True:
  #     result = toString(getDaysAgo(days_to_crawl=7, datefrom=result));
  #   else:
  #     result = result;
  return result;

def getQuarterByDate(date):
  if not type(date) == datetime:
    date = convertDateTimeFromString(date);

  quarter = None;
  if date is not None:
    month = toString(date, date_format='%m');

    # quarter_mapping = {};
    # for m in range(1, 13):
    #   quarter_mapping[str(m).zfill(2)] = m//4 + 1;
    #   print('q', m//4 + 1, m//4);

    quarter_mapping = {'01': 1, '02': 1, '03': 1, '04': 2, '05': 2, '06': 2, '07': 3, '08': 3, '09': 3, '10': 4, '11': 4, '12': 4} ;

    quarter = quarter_mapping[month];
    # print('month', month, quarter_mapping, quarter)


  return quarter;