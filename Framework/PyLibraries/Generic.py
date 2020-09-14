import pandas as pd
import configparser
from dateutil.relativedelta import relativedelta
import dateutil
import subprocess
import os
import datetime
import time
from robot.api import logger
import shutil
import collections

def marge_dictionaries(to_dict, *args):
    '''
    Author : Niket Shinde
    Description : Marge multiple dictionary  to to_dict
    :param to_dict: all dictionaries will marge to this dictionary
    :param args: all dictionaries
    :return: Marged dictionary
    '''
    for dictionary in args:
        to_dict.update(dictionary)

    logger.debug('<B>Marged dictionary : </B>'+str(to_dict), html=True)
    return to_dict


def concatenate_string(*args):
    """
    Author : Niket Shinde
    Description : Marge multiple strings  to to_dict
    :param args: string sequences
    :return: Marged string
    """

    # string = ""
    # for temp_str in args:
    #     string += temp_str

    return ''.join([x for x in args])


def csv_to_dictionary(file_path, csv_file_delimiter):
    """
    Author : Niket Shinde
    Description : csv to dictionary
    :param file_path: path of csv file
    :param csv_file_delimiter:
    :return: dictionary
    """
    df = pd.read_csv(file_path, delimiter=csv_file_delimiter, keep_default_na=False, encoding='utf_8')
    column_list = df["KEYS"].tolist()
    df.index = column_list
    return df.to_dict()


def pop_csv(file_path, column_name, csv_file_delimiter):
    """
    Author : Niket Shinde
    Description : pop value from bottom of column from csv
    :param file_path: path of csv
    :param column_name: column name from which you want to pop value
    :param csv_file_delimiter:
    :return: poped value
    """
    df = pd.read_csv(file_path, csv_file_delimiter)
    df_read = df[df[column_name].notnull()]
    value = df_read.loc[df_read.shape[0] - 1, column_name]
    df.loc[df_read.shape[0] - 1, column_name] = ''
    # write to test data csv
    df.to_csv(file_path, index=False, encoding='utf8', sep=csv_file_delimiter)
    return value


def add_date(day, num, interval):
    '''
    Author : Niket Shinde
    Description : add date
    :param day: date
    :param num: number
    :param interval: interval
    :return: date after addition
    '''
    added_date = day
    if interval == 'd' or interval == 'days':
        added_date = day + relativedelta(days=+num)
    elif interval == 'm' or interval == 'months':
        added_date = day + relativedelta(months=+num)
    elif interval == 'y' or interval == 'years':
        added_date = day + relativedelta(years=+num)
    elif interval == 'hh' or interval == 'hours':
        added_date = day + relativedelta(days=+num)
    elif interval == 'mm' or interval == 'minutes':
        added_date = day + relativedelta(days=+num)
    elif interval == 'ss' or interval == 'seconds':
        added_date = day + relativedelta(seconds=+num)
    else:
        added_date = "invalid interval"
    return added_date


def ini_to_dictionary(int_file_path, section, dictionary_properties={}):
    """
    Author : Niket Shinde
    Description : get data from INI file to dictionary
    :param int_file_path: path of INI file
    :param section:
    :return: dictionary
    """
    config = configparser.RawConfigParser()
    config.read(int_file_path)
    config.sections()
    options = config.options(section)
    for option in options:
        try:
            dictionary_properties[option.upper()] = config.get(section, option)
            if dictionary_properties[option.upper()] == -1:
                print("skip: %s" % option.upper())
        except:
            print("exception on %s!" % option.upper())
            dictionary_properties[option.upper()] = None
    logger.debug("Value From section ' "+section+"' : "+str(dictionary_properties))
    return dictionary_properties


def get_file_data(path):
    """
    Author : Niket Shinde
    :param path:  path of file
    :return:
    """
    try:
        file_data = open(path, 'r')
        try:
            text = None
            text = file_data.read()
        finally:
            file_data.close()
            return text
    except IOError as e:
            print("Error: can\'t find file or read data")
            print("Exception : " + e)


def set_value(variable, value_from, key=None):
    """
    Author : Niket Shinde
    :param variable:
    :param value_from:
    :param key:
    :return:
    """
    temp = variable
    if type(value_from) is dict:
        if key in value_from.keys() and value_from[key] != '':
            temp = value_from[key]
    else:
        temp = value_from

    logger.debug("Set value of variable : "+str(temp))
    return temp


def create_profile(path):
    """
    Author : Niket Shinde
    :param path:
    :return:
    """
    from selenium import webdriver
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", path)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk",'application/csv')
    fp.update_preferences()
    return fp.path


def run_soapUI_test():
    """
    Author : Niket Shinde
    :return:
    """
    output = subprocess.Popen((r"C:\Users\shindnik\MyProject\python\MyNotes\my_text_file1.bat", "an_argument", "another_argument"), stdout=subprocess.PIPE).stdout
    result = ""
    for line in output:
        result += str (line) + '\n'
    output.close()
    return result


def is_chrome(browser):
    """
    Author : Niket Shinde
    :param browser:
    :return:
    """
    return browser in ['chrome', 'Chrome', 'gc', 'googlechrome']


def create_edi_file(template_path, value_dictionary, project_path, edifile_path):
    """
    Author : Niket Shinde
    :param template_path:
    :param value_dictionary:
    :param project_path:
    :param edifile_path:
    :return:
    """
    template_data = get_file_data(template_path)
    logger.debug('<b>EDI Template before update values : </b> <BR>'+template_data, html=True)
    logger.debug('<b>values dictionary : </b> <BR>'+str(value_dictionary), html=True)
    # Enter value in EDI template
    for keys, values in value_dictionary.items():
        logger.debug('<b>Before '+keys+' :  </b> <BR>' + str(values), html=True)
        template_data = template_data.replace('$'+keys.upper()+'$', str(values))
    print('*HTML*<b>EDI Template with update values : </b> <BR>'+template_data)

    template_name = template_path[template_path.rfind('/')+1:template_path.rfind('.')]
    edi_file_name = "AT_" + template_name + get_timestamp(str(datetime.datetime.today()), 1) + ".edi"
    file_name = project_path + "results\\" + edi_file_name
    file = open(file_name, "w")
    file.write(template_data)
    logger.debug('<b>EDI file create at local location : </b> <BR>' + str(file_name), html=True)
    file.close()
    source = file_name
    destination = edifile_path+edi_file_name
    # os.rename(source, destination)
    shutil.move(source, destination)
    logger.debug('<b>EDI file  moved from local to server location : </b> <BR>' + str(destination), html=True)
    return destination


def get_timestamp(from_datetime=None, format_num=1):
    """
    Author : Niket Shinde
    :param from_datetime:
    :param format_num:
    :return:
    """
    format_dictionary = {
        1: "%d%m%y%H%M%S",  # 110919130142
        2: "%Y%m%d",    # 20190911
        3: "%H%M%S",    # 130237
        4: "%Y%m%d%H%M",    # 201909111302
        5: "%#m/%d/%y",     # 9/11/19
        6: "%#m/%d/%Y",     # 9/11/2019
        7: "%#m/%d/%Y %H:%M",   # 9/11/2019 11:55
        8: "%d%m%y%H%M%S%f",  #160819122257349053
        9: "%H%M%S%f",  #122551300096
        10: "",
        11: "",
        12: ""
    }
    datetime_value = dateutil.parser.parse(from_datetime).timestamp()
    #print(datetime_value)
    formatted_datetime = datetime.datetime.fromtimestamp(datetime_value).strftime(format_dictionary[format_num])
    print('get_timestamp : ', formatted_datetime)
    return formatted_datetime


def get_GS1_number(initial_number, number_len):
    """
    :Author:  Niket Shinde
    :param initial_number:
    :param number_len:
    :return:
    :RFkeyword_code:        ${GS1}=  Get GS1 Number  75999  17

    """
    time.sleep(.01)
    now = datetime.datetime.now()
    timestamp = datetime.datetime.timestamp(now)
    timestamp = str(timestamp)[::-1]
    GSIN = (initial_number + str(timestamp)).replace('.', '')
    number_size = int(number_len)-1
    logger.debug("random number : " + GSIN[:number_size], html=True)
    sum = 0
    j = 1
    for i in GSIN[0:number_size]:
        number = int(i)
        sum += number * 3 if j % 2 == 0 else number * 1
        j += 1
    #print("sum : ", sum)
    #print("Last digit : ", 10 - (sum % 10))
    GS1_number = GSIN[:number_size] + str(10 - (sum % 10)) if sum % 10 != 0 else GSIN[:number_size] + '0'
    print("Valid GS1 Number : ", GS1_number)
    return GS1_number


def get_SSN(country_name):
    now = datetime.datetime.now()
    time.sleep(.01)
    timestamp = datetime.datetime.timestamp(now)
    GSIN = (str(timestamp)).replace('.', '')
    SSN = GSIN[0:4] + ('0' + str((int(GSIN[4:6]) % 11) + 1))[-2:] + ('0' + str((int(GSIN[6:8]) % 27) + 1))[-2:] + GSIN[
                                                                                                                  -3:]
    check_sum = 0
    j = 1
    for i in SSN[2:]:
        number = int(i)
        if j % 2 == 0:
            check_sum += number * 1
        else:
            check_sum += number * 2 if len(str(number * 2)) <= 1 else int(str(number * 2)[0]) + int(str(number * 2)[1])
        j += 1
    SSN = SSN + str(10 - (check_sum % 10)) if check_sum % 10 != 0 else SSN + '0'
    SSN = '19' + SSN[2:-4] + SSN[-4:]
    print("Valid SSN Number for ", country_name, ": ", SSN)
    return SSN


def add_record(data_dictionary, path, Order_Portal_fields, num=1 ,delimiter_char=',', first_record='N'):
    #OrderPortal_fields = 'OrderGroup,CampaignCode,CustomerCode,FirstName,LastName,Type,PersonOrOrganizationNumber,BusinessPhone,MobilePhone,HomePhone,Language,EmailAddress,MainAddressStreetName,MainAddressStreetNumber,MainAddressFloor,MainAddressApartment,MainAddressPostalCode,MainAddressCity,MainAddressCountry,MainAddressAttention,MainAddressCareOf,DeliverySiteType,DeliverySiteStreetName,DeliverySiteStreetNumber,DeliverySiteFloor,DeliverySiteApartment,DeliverySitePostalCode,DeliverySiteCity,DeliverySiteCountry,DeliverySiteAttention,GridAuthor,GridArea,BalanceResponsible,MeteringMethod,SettlementMethod,MeterPointNumber,Eldependency,ConsumptionCode,SelectedStandardcontract,ProductID1,ProductID2,ProductID3,ProductID4,ProductID5,ProductID6,ProductID7,ProductID8,ProductID9,ProductID10,StartDate,SalesChannel,ResponseChannel,ResponseDate,PriceDate,VersionDate,AddtionalInfo,InvoiceGroupName,ClerkName,ReasonCode,InvoiceType,InvoiceCode,IsNegativeResponse,InvoiceAddressStreetName,InvoiceAddressStreetNumber,InvoiceAddressFloor,InvoiceAddressApartment,InvoiceAddressPostalCode,InvoiceAddressCity,InvoiceAddressCountry,InvoiceDistribution,ManualInvEmailAddress,ManualInvPhoneNumber,InvoiceAddressAttention,InvoiceAddressCareOf,InvoiceOutputType,PayTerm,InvGroup,ConfirmationType,RestrictionId1,RestrictionValue1,RestrictionId2,RestrictionValue2,RestrictionId3,RestrictionValue3,RestrictionId4,RestrictionValue4,RestrictionId5,RestrictionValue5,RestrictionId6,RestrictionValue6,RestrictionId7,RestrictionValue7,RestrictionId8,RestrictionValue8,RestrictionId9,RestrictionValue9,RestrictionId10,RestrictionValue10,ProxyFlag,PropertyAuthor,EstimatedConsumption,PreviousOccupants,OrderId'
    record = ''
    if first_record.upper() == 'N':
        if num == 1:
            for x in Order_Portal_fields.split(delimiter_char):
                if ('OP_'+x) in data_dictionary.keys():
                        record = record + data_dictionary['OP_'+x] + delimiter_char
                else:
                    record = record + delimiter_char
        else:
            for n in range(int(num)):

                for x in Order_Portal_fields.split(delimiter_char):
                    if ('OP_' + x) in data_dictionary.keys():
                        if ('OP_' + x) in ['OP_FirstName', 'OP_LastName']:
                            record = record + data_dictionary['OP_' + x]+str(n) + delimiter_char
                        elif ('OP_' + x) in ['OP_OrderId']:
                            record = record + create_string('orderid') + delimiter_char
                        elif ('OP_' + x) in ['OP_OrderGroup']:
                            record = record + create_string('OrderGroup') + delimiter_char
                        elif('OP_' + x) in ['OP_PersonOrOrganizationNumber']:
                            record = record + get_SSN('Sweden') + delimiter_char
                        elif ('OP_' + x) in ['OP_MeterPointNumber']:
                            record = record + get_GS1_number('735999', '18') + delimiter_char
                        elif ('OP_' + x) in ['OP_EmailAddress','OP_ManualInvEmailAddress']:
                            email_array = (data_dictionary['OP_EmailAddress']).split('@')
                            record = record + email_array[0]+str(n)+'@'+email_array[1] + delimiter_char
                        else:
                            record = record + data_dictionary['OP_' + x] + delimiter_char
                    else:
                        record = record + delimiter_char
                record = record[:len(record) - 1] + '\n'
        create_file(path, record[:len(record) - 1] + '\n')
    else:
        record = Order_Portal_fields
        create_file(path, record+'\n', 'w+')
    # print('*HTML* <B> Record Added : </B> <textarea rows="4" cols="50"> ',record,' </textarea>')
    return record


def create_file(path, data="", mode='a+'):
    file = open(path, mode)
    if mode in ['w+', 'a+', 'w', 'a']:
        file.write(data)
    if mode in ['r', 'r+']:
        line = file.readline()
        return line
    file.close()


def get_data_from_file(path):
    return open(path, "r").read()


def create_string(key, value=None):
    key = key.lower().strip()
    if key == 'orderid':
        value = 'AT_' + str(get_timestamp(str(datetime.datetime.now()), 9))
    elif key == 'ordergroup':
        value = 'OG_' + str(get_timestamp(str(datetime.datetime.now()), 9))
    else:
        print(key, 'Not Defined')
    return value



def validate_order_status(class_name, expected='success'):
    if expected.lower() == 'invalid' : expected = 'danger'
    if expected.lower() == 'ready to submit': expected = 'warning'
    if class_name.find('success') != -1:
        if expected.lower().strip() == 'success':
            print('status is "Succeeded')
            return {'status': True, 'msg': 'status is "Succeeded'}
        else:
            print('*ERROR* status is not "Succeeded"')
            return {'status': False, 'msg': 'status is not "Succeeded'}
    if class_name.find('warning') != -1:
        if expected.lower().strip() == 'warning':
            print('status is "Ready To Submit')
            return {'status': True, 'msg': 'status is "Ready To Submit'}
        else:
            print('*ERROR* status is not "Ready To Submit"')
            return {'status': False, 'msg': 'status is not "Ready To Submit'}
    elif class_name.find('failed') != -1 and expected.lower().strip() == 'failed':
        if expected.lower().strip() == 'failed':
            print('status is "Failed"')
            return{'status': True, 'msg': 'status is "Failed"'}
        else:
            print('*ERROR* status is not "Failed')
            return{'status': False, 'msg': 'status is not "Failed"'}
    elif class_name.find('danger') != -1:
        if expected.lower().strip() == 'danger':
            print('status is "Invalid"')
            return{'status': True, 'msg': 'status is "Invalid"'}
        else:
            print('*ERROR* status is not "Invalid" ')
            return{'status': False, 'msg': 'status is not "Invalid" '}
    else:
        print('*ERROR* invalid class name : ', class_name)
        return{'status': False, 'msg': '*ERROR* invalid class name : '+class_name}


def checkDictKeyExists(dict, key):
    if key in dict.keys():
        dicKeyExists =  True
    else:
        dicKeyExists = False

    return  dicKeyExists