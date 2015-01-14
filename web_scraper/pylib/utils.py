import json
import time, datetime
import io
import string
import csv, codecs, cStringIO
import random
import sys
import traceback
import decimal
import unicodecsv #need installation

''' 
10:48 AM 9/23/2014 dump_csv can now append.
11:42 PM 9/22/2014 parse_decimal now return float values.
10:56 PM 9/13/14 modified dump_csv, now can handle unicode.
11:13 PM 9/13/14 added seralizer for dump_json to handle datetime and decimal values.
10:43 PM 9/1/14 added print_json
'''    


''' 
    =====================
    date/time functions
    =====================
'''    
def utc_to_mysql_time(utc): 
    ''' conver twitter style utc time stamp (Tue Aug 26 01:41:57 +0000 2014) to mysql time stamp (2014-08-26 03-55-32) '''
    return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(utc,'%a %b %d %H:%M:%S +0000 %Y'))
    
def mysql_time(t=datetime.datetime.now()): 
    ''' return a datetime string of a date time object according to the mysql format
    the argument t is date time object. if not provided, returns the current time'''
    return t.strftime('%Y-%m-%d %H:%M:%S')

def current_time():
    ''' return a datetime object of current time '''
    return datetime.datetime.now()    

''' 
    =====================
    I/O related functions
    =====================
'''   
def serializer(obj):
    '''
        convert datetime objects into serializable formats
        also handle decimal objects
        http://goo.gl/qnqOfa
    '''
    if hasattr(obj, 'isoformat'): # datetime to isoformat.
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    else:
        return obj
    
def dump_json(data, filename):
    ''' dump python object to a serialized JSON formatted string. see http://stackoverflow.com/questions/12309269/write-json-data-to-file-in-python '''
    with io.open(filename, 'w',encoding='utf8') as outfile:
        outfile.write(unicode(json.dumps(data, outfile, indent=4, ensure_ascii=False, default=serializer)))
        print 'json data written to %s'%filename
            
def to_unicode(data):
    '''
    convert data from other types (int, str etc) into unicode strings. We assume the data is either a dict, tuple, or a list.
    '''
    if isinstance(data,dict):
        return {key:unicode(value) for key, value in data.iteritems()}
    elif isinstance(data, tuple):
        return (unicode(value) for value in data)
    elif isinstance(data, list):
        return [unicode(value) for value in data]
    else:
        raise
    
def dump_csv(data, filename, dialect="excel", open_mode="w", *args, **kwargs):
    ''' dump python data into a csv file. 
        expect data to be a list, a tuple, etc.
        it can deal with unicode, unlike csv writer.
        Python is full of annoying bugs - you must specify line 
        terminator to be '\n' otherwise you get extra blank rows!!
    '''
    with open(filename, open_mode) as outfile:
        # dialect,lineterminator='\n',*args, **kwargs
        csvwriter = unicodecsv.writer(outfile, lineterminator='\n')
        for row in data:
            if isinstance(row, dict):
                csvwriter.writerow(row.values())
            else:
                csvwriter.writerow(row)
        print 'csv data written to %s'%filename
        
    # return nrows
    
# def write_csv(data, csvwriter):
    # ''' append rows to csv file
    # '''
    # nrows = 0
    # for row in data:
        # # print row.values()
        # nrows += 1
        # csvwriter.writerow(row.values())
    # return nrows

def dump_str(s, filename, encoding="utf-8"):
    ''' write str to file 
    '''
    import codecs
    with codecs.open(filename, 'w', encoding) as strwriter:
        strwriter.write(s)
        print 'string data written to %s'%filename
    return len(s)    
    
def write_str(s, strwriter):
    ''' 
        append str to a file object
    '''    
    strwriter.write(s)
    return len(s)
    # if is_debug():
        # print '%s bytes appended'%(len(s))
    
def read_file(filename):
    ''' read a text file into a string object. http://stackoverflow.com/questions/8369219/how-do-i-read-a-text-file-into-a-string-variable-in-python '''
    with open(filename, 'r') as infile:
        return infile.read()
        
def printable(s):
    '''return only printable characters of a string so that is print-safe'''
    return filter(lambda x: x in string.printable, s)
    
def enable_utf_print():
    '''enable console to print UTF characters. Otherwise, Python will throw an error. Another annoying habit of Python'''
    sys.stdout = codecs.getwriter("utf-8")(sys.__stdout__) 
    
def print_json(o):
    print json.dumps(o,indent=2)
    
''' 
    =====================
    parse related functions
    =====================
'''    

def substr_after(orginal, marker):
    '''
    get the part of a string after the marker.
    if the marker is not found, returns ''
    '''
    if orginal.find(marker) >= 0:    
        return orginal[orginal.find(marker)+len(marker):]
    else:
        return ''

def substr_before(orginal, marker):
    '''
    get the part of a string before the marker.
    if unfound, returns the original string
    '''
    if orginal.find(marker) >= 0:
        return orginal[:orginal.find(marker)]
    else:
        return original

def parse_decimal(s):    
    '''
    remove non-digit characters and convert to decimal (but return in string format).
    e.g. $6,150,593.22 --> 6150593.22
    cannot deal with negative values.
    '''    
    from re import sub
    from decimal import Decimal
    try:
        return float(Decimal(sub(r'[^\d.]', '', s)))
    except Exception as e:
        return None
    
def parse_datetime(s):
    '''
    recognize most time formats such as
    Fri Sep 25 18:09:49 -0500 2009
    2008-06-29T00:42:18.000Z
    2011-07-16T21:46:39Z
    return datetime object
    '''    
    from dateutil.parser import parse
    return parse(s)
    
def parse_unixtime(u):
    '''
    recognize unix time stamp e.g. 1294989360
    to a datetime object.
    '''
    from datetime import datetime
    return datetime.utcfromtimestamp(u)
    
''' 
    =====================
    job control functions
    =====================
'''    
    
def my_sleep(low=2, high=5):
    '''
    provide a standard behavior between two http requests. It randomizes between two values. 
    '''
    if low <= high:
        wait = random.randint(low,high)
        print "%s sleeping for %s seconds"%(mysql_time(),wait)
        time.sleep(wait)
    else:
        print "my_sleep: low must be less than high"
        raise
        
def is_writedb():
    global _writedb_
    if "_writedb_" in globals():
        return _writedb_
    else:
        return False 
def is_debug():
    global _debug_
    if "_debug_" in globals():
        return _debug_
    else:
        return False
def is_online():
    global _online_
    if "_online_" in globals():
        return _online_
    else:
        return False   

 