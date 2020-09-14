import Generic
from robot.api import logger
import xml.etree.ElementTree as ET
import http.client
import json
import requests
import xml.dom.minidom as minidom
import cx_Oracle

class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()

        return {description[0]: str(row[col]) for col, description in enumerate(self._cursor.description)}

def get_web_service_environment_variables(global_env, path):
    """
    Author : Niket Shinde
    Description :
    :param global_env:
    :param path:
    :return:
    """
    tree = ET.parse(path)
    root = tree.getroot()
    wdls_dictionary = {}
    for item in root.findall(r'./' + global_env + '/'):
        # print ("Node Name : "+ item.tag)
        # print("Node Attributes : ",item.attrib)
        wdls_dictionary[item.tag] = {}
        wdls_dictionary[item.tag]['attributes'] = item.attrib
        for child in item:
            # print( "child child Node Name : ", child.tag)
            # print( child.attrib)
            wdls_dictionary[item.tag][child.tag] = {}
            wdls_dictionary[item.tag][child.tag]['attributes'] = child.attrib
            wdls_dictionary[item.tag][child.tag]['headers'] = {}
            for sub_child in child:
                # print( "sub child Node Name: ", sub_child.tag+" : "+sub_child.text)
                wdls_dictionary[item.tag][child.tag]['headers'][sub_child.tag] = sub_child.text
    return wdls_dictionary

"""
def send_request(wdls_dictionary, project_dir, node_dictionary, service_name, function_name):
    url = wdls_dictionary[service_name]['attributes']['URL']
    method = wdls_dictionary[service_name][function_name]['attributes']['Method']
    subfunction = wdls_dictionary[service_name][function_name]['attributes']['URL']
    template_path = project_dir+'RequestTemplates\\'+wdls_dictionary[service_name][function_name]['attributes']['TemplateName']
    logger.debug('<B>Template path :  </b>'+template_path, html=True)
    headers_dictionary = wdls_dictionary[service_name][function_name]['headers']
    for key, value in headers_dictionary.items():
        if value.startswith(r'$') and value.endswith(r'$'):
            headers_dictionary[key] = node_dictionary[value[1:-1]]
    print('*HTML*<b>URl : </b>'+url)
    print('*HTML*<b>Method : </b>' + method)
    print('*HTML*<b>Request Headers : </b>')
    for keys, values in headers_dictionary.items():
        print(keys+' : '+values)
    # requests.get(url=url, params=headers_dictionary))
    conn = http.client.HTTPConnection(url)
    # get and update template data
    all_body = Generic.get_file_data(template_path)
    logger.debug('<b>Request Template before update values : </b>'+all_body, html=True)
    logger.debug('<b>values dictionary : </b>'+str(node_dictionary), html=True)

    # Enter value in request template
    for keys, values in node_dictionary.items():
        logger.debug('<b>Before '+keys+' :  </b>' + str(values), html=True)
        all_body = all_body.replace('$'+keys.upper()+'$', str(values))
    print('*HTML*<b>Request : </b>'+all_body)
    conn.request(method, subfunction, all_body, headers_dictionary)
    res = conn.getresponse()
    status_code = res.getcode()
    print('*HTML*<b>Status : </b>' +str(status_code))
    data = res.read()
    print('*HTML*<b>Response : </b>'+data.decode("utf-8"))
    dictionary_temp = {'response': data.decode("utf-8"), 'status': status_code}
    return dictionary_temp
"""


def send_request(wdls_dictionary, project_dir, node_dictionary, service_name, function_name):
    """
    Author : Niket Shinde
    :param wdls_dictionary:
    :param project_dir:
    :param node_dictionary:
    :param service_name:
    :param function_name:
    :return:
    """
    url = wdls_dictionary[service_name]['attributes']['URL']
    method = wdls_dictionary[service_name][function_name]['attributes']['Method']
    subfunction = wdls_dictionary[service_name][function_name]['attributes']['URL']
    url = url + subfunction
    template_path = project_dir+'\\RequestTemplates\\'+wdls_dictionary[service_name][function_name]['attributes']['TemplateName']
    logger.debug('<B>Template path :  </b>'+template_path, html=True)
    headers_dictionary = wdls_dictionary[service_name][function_name]['headers']
    for key, value in headers_dictionary.items():
        if value.startswith(r'$') and value.endswith(r'$'):
            headers_dictionary[key] = node_dictionary[value[1:-1]]
    print('*HTML*<b>URl : </b>'+url)
    print('*HTML*<b>Method : </b>' + method)
    print('*HTML*<b>Request Headers : </b>')
    for keys, values in headers_dictionary.items():
        print(keys+' : '+values)
    # requests.get(url=url, params=headers_dictionary))

    # get and update template data
    all_body = Generic.get_file_data(template_path)
    logger.debug('<b>Request Template before update values : </b>'+all_body, html=True)
    logger.debug('<b>values dictionary : </b>'+str(node_dictionary), html=True)

    # Enter value in request template
    for keys, values in node_dictionary.items():
        logger.debug('<b>Before '+keys+' :  </b>' + str(values), html=True)
        if str(values).lower() == "null":
            all_body = all_body.replace('"$' + keys.upper() + '$"', str(values))
        else:
            all_body = all_body.replace('$'+keys.upper()+'$', str(values))
    print('<b>Request : </b>'+all_body)

    response = requests.request(method, url, data=all_body, headers=headers_dictionary)
    print(response)
    status_code = response.status_code
    print('*HTML*<b> <font size="4"> Response Status code: </b>' + str(status_code) + '</Font>')
    print('<b>Response : </b> ' + response.text)
    # print('*HTML*<b>Response : </b> <textarea rows="10" cols="90"> '+response.text+'</textarea>')
    dictionary_temp = {'response': response.text, 'status': status_code}
    return dictionary_temp


def get_value_from_json(json_text, key):
    """
    Author : Niket Shinde
    Description :
    :param json_text:
    :param key:
    :return:
    """
    data = json.loads(json_text)
    logger.debug("<B>JSON Key : </B>"+key, html=True)
    logger.debug("<B>"+key+" value in JSON : </B>" + data[key], html=True)
    return data[key]


def get_value_from_xml(xml, node_name):
    """
    Author : Niket Shinde
    :param xml:
    :param node_name:
    :return:
    """
    my_document = minidom.parse(xml)
    items = my_document.getElementsByTagName(node_name)
    node_value = items[0].childNodes[0].data if items[0].childNodes.length > 0 else None
    logger.debug("xml node value " + node_name + " : ", node_value)
    return node_value


def get_value_from_xml_string(xml_text, node_name):
    """
    Author : Snehal Rakshe
    :param xml:
    :param node_name:
    :return:
    """
    #print("Inside function get value from xml" + xml_text)
    start_node_name = "<" + node_name + ">"
    str_position = xml_text.find(start_node_name) + len(start_node_name)
    end_node_name = "</" + node_name + ">"
    end_position = xml_text.find(end_node_name)
    customer_id = xml_text[str_position:end_position]
    return customer_id

def get_value_from_cabdb(strSQL):
    """
    Author : Snehal Rakshe
    :param sql query:
    :return database row as dictionary having column name as key and value :
    """

    dsn_tns = cx_Oracle.makedsn('ORADB', '1521',service_name='RTLTEST')  # if needed, place an 'r' before any parameter in order to address any special character such as '\'.
    conn = cx_Oracle.connect(user='CAB', password='CAB', dsn=dsn_tns)  # if needed, place an 'r' before any parameter in order to address any special character such as '\'. For example, if your user name contains '\', you'll need to place 'r' before the user name: user=r'User Name'

    c = conn.cursor()
    c.execute(strSQL)
    for row in CursorByName(c):
        return row
        print(row)
        # return (c.fetchall()[0][0])
    conn.close()