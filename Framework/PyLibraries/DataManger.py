import Generic
import datetime
import dateutil
import re
import pandas as pd
from robot.api import logger
# from faker import Faker
import random


functions_list = ["$SSN$", '$date$', '$datetime$', '$GS1$']


def get_global_test_data_to_dictionary(file_path, colname, csv_file_delimiter, file_names):
    '''
    Author : Niket Shinde
    Description : to get data from global data csv
    :param file_path: path of CSV file
    :param colname: name of column
    :param csv_file_delimiter: delimiter used in CSV file
    :return: dictionary
    '''
    datadict = {}
    for file in file_names.split(','):
        all_dictionary = Generic.csv_to_dictionary(file_path+'\\'+file, csv_file_delimiter)
        # datadict = update_value(all_dictionary[colname], file_path, csv_file_delimiter)
        datadict.update(all_dictionary[colname])
        #print("Before RUN Global dictionary : ", datadict)
        logger.debug('<B>Before RUN Global Data dictionary :  </B>'+str(datadict))
    return datadict


def get_test_data_to_dictionary(file_path, csv_file_delimiter):
    """
    Author : Niket Shinde
    Description : to get data from test data csv
    :param file_path: path of file without file extension
    :param csv_file_delimiter: delimiter for csv file
    :return: dictionary
    """
    datadict = {}
    datadict = Generic.csv_to_dictionary(file_path + ".csv", csv_file_delimiter)
    logger.debug('<B>Before RUN Test Data dictionary :  </B>' + str(datadict))
    return datadict


def update_dictionary(global_dictionary, data_dictionary , file_path, csv_file_delimiter, stritr=''):
    """
    Author : Niket Shinde
    Description : update values in global dictionary
    :param global_dictionary:
    :param data_dictionary:
    :param file_path:
    :param csv_file_delimiter:
    :param stritr:
    :return: dictionary object
    """
    datadict = global_dictionary

    for key in datadict:
        text = datadict[key]
        cell_value = text
        text = str(text)
        logger.debug(key+' : '+text)
        #logger.debug(text[0:3].upper())
        if text[0:3].upper() == "ITR":
            cell_value = data_dictionary[cell_value][key]
            logger.debug("Updated Test Dictionary Node : " + "[" + key + "] : " + str(cell_value))
        if text.startswith(r'[') and text.endswith(r']'):
            text = text[1:-1]
            values = text.split(sep=',')
            print(values)
            for i, item in enumerate(values):
                # values[i] = item.strip()
                if '%' in values[i]:
                    #values[i] = item[1:-1]
                    #values[i] = datadict[values[i]]
                    key_name = re.findall(r'%.*%', values[i])[0][1:-1]
                    if key_name in datadict.keys():
                        values[i] = re.sub(r'%'+key_name+'%', str(datadict[key_name]), values[i])
                    else:
                        pass
                    #values[i] = updated_value
                elif values[i][0:3].upper() == "ITR":
                        values[i] = data_dictionary[values[i]][key]
                else:
                    pass
            if len(values) > 1:
                if values[1].lower() == '+':
                    cell_value = int(values[0]) + int(values[2])
                elif values[1].lower() == '-':
                    cell_value = int(values[0]) - int(values[2])
                elif values[0].lower() == 'concat':
                    #cell_value = values[0] + ' ' + values[2]
                    cell_value = str(values[1]).join(values[2:])
                    print("cell_value : ", cell_value)
                elif values[0].lower() == 'date':
                    cell_value = datetime.datetime.today() if values[1].lower() == 'today' else dateutil.parse(values[1])
                    cell_value = Generic.add_date(cell_value, int(values[2]), values[3])
                    cell_value = cell_value.date().strftime('%Y-%m-%d')
                elif values[0].lower() == 'datetime':
                    cell_value = datetime.datetime.today() if values[1].lower() == 'today' else dateutil.parse(values[1])
                    cell_value = Generic.add_date(cell_value, int(values[2]), values[3])
                    cell_value = cell_value.strftime('%Y-%m-%d %H:%M:%S')
                elif values[0].lower() == 'timestamp':
                    cell_value = datetime.datetime.today() if values[2].lower() == 'today' else dateutil.parse(values[2])
                    cell_value = Generic.add_date(cell_value, int(values[3]), values[4])
                    cell_value = cell_value.strftime('%Y-%m-%d %H:%M:%S')
                    cell_value = Generic.get_timestamp(cell_value, int(values[1]))
                else:
                    pass
                print(cell_value)
            else:
                cell_value = values[0]
        elif text.startswith(r'$') and text.endswith(r'$'):
            if text in functions_list:
                if text == "$SSN$":
                    #cell_value = Generic.pop_csv(file_path+"SSN.csv", datadict["DATASET"], csv_file_delimiter)
                    cell_value = Generic.get_SSN('Sweden')
                    cell_value = re.sub(r'\..*', "", str(cell_value), re.I)
                    print("SSN : " + cell_value)
                if text == "$GS1$":
                    cell_value = Generic.get_GS1_number('735999', '18')
                    cell_value = re.sub(r'\..*', "", str(cell_value), re.I)
                    print("GS1 : " + cell_value)
                if text == "$date$":
                    cell_value = datetime.datetime.today()
                    cell_value = cell_value.strftime('%Y-%m-%d')
                if text == "$datetime$":
                    cell_value = datetime.datetime.today()
                    cell_value = cell_value.strftime('%Y-%m-%d %H:%M:%S')

        elif text == '':
            if key in data_dictionary[stritr].keys():
                if data_dictionary[stritr][key] != '':
                    cell_value = data_dictionary[stritr][key]
        else:
            pass
        datadict[key] = cell_value
    logger.debug('<B>After update value in Global Data dictionary :  </B>' + str(datadict), html=True)
    return datadict


def marge_test_dictionaries(itr, test_dictionary, gobal_dictionary):
    """
    Author : Niket Shinde
    Description : Marge updated value from global dictionary to test dictionary with respective iteration
    :param itr: iteration
    :param test_dictionary: test data dictionary
    :param gobal_dictionary: global data dictionary
    :return: dictionary object
    """

    for iteration in list(test_dictionary.keys()):
        for key in list(gobal_dictionary.keys()):
            if key in list(test_dictionary[iteration].keys()):
                pass
                #test_dictionary[iteration][key] = gobal_dictionary[key]
            else:
                if iteration == 'KEYS':
                    test_dictionary[iteration][key] = key
                else:
                    test_dictionary[iteration][key] = ''

    test_dictionary[itr].update(gobal_dictionary)
    logger.debug('<B>After Marging Globale dictionary to Test data dictionary :  </B>' + str(test_dictionary), html=True)
    return test_dictionary


def test_dictionary_to_csv(dictdata, file_path, csv_file_delimiter):
    """
    Author : Niket Shinde
    Description : import test data dictionary to test data csv
    :param dictdata: test data dictionary
    :param file_path: imported to path
    :param csv_file_delimiter:
    :return:
    """
    column_list = dictdata['KEYS'].keys()
    df = pd.DataFrame.from_dict(dictdata)
    df.index = column_list
    df.drop(columns=['KEYS'])
    print(df)
    columns_header = list(dictdata.keys())
    #columns_header.remove('KEYS')
    df.to_csv(path_or_buf=file_path+'.csv', sep=csv_file_delimiter, index=False, columns=columns_header, index_label=True)


def generate_test_data(region, number, file_path, csv_file_delimiter="|"):
    """
    Author : Niket Shinde
    :param region:
    :param x:
    :param file_path:
    :param csv_file_delimiter:
    :return:
    """
    print(region)
    fake = Faker(str(region))
    cust_data = {}
    for i in range(0, int(number)):
        cust_data[i] = {}
        cust_data[i]['id'] = random.randrange(999, 10000)
        cust_data[i]['first_name'] = fake.first_name()
        cust_data[i]['last_name'] = fake.last_name()
        cust_data[i]['name'] = cust_data[i]['first_name'] + ' ' + cust_data[i]['last_name']
        cust_data[i]['ssn'] = fake.ssn()
        cust_data[i]['dob'] = fake.date_of_birth(tzinfo=None, minimum_age=10, maximum_age=115).strftime("%x")
        cust_data[i]['email'] = fake.email()
        cust_data[i]['phone'] = fake.phone_number()
        cust_data[i]['street_name'] = fake.street_name()
        cust_data[i]['street_number'] = random.randrange(1, 99)
        cust_data[i]['flat_number'] = random.randrange(1, 999)
        cust_data[i]['floor_number'] = random.randrange(1, 20)
        cust_data[i]['postcode'] = fake.postcode()
        cust_data[i]['city'] = fake.city_name()
        cust_data[i]['address'] = fake.address()
        cust_data[i]['comment'] = fake.text()
        cust_data[i]['latitude'] = str(fake.latitude())
        cust_data[i]['longitude'] = str(fake.longitude())
    logger.debug(cust_data)

    df = pd.DataFrame.from_dict(cust_data, orient='index')
    df.to_csv(path_or_buf=file_path + '.csv', sep=csv_file_delimiter)
    return cust_data





