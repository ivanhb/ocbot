
my_commands = {
    "/howToContactYou" : {"notes":" Check how you can contact me"},
    "/askCOCI" : {"notes":"Params: [[DOI]]. Check the COCI info for a specific DOI"},
    "/whoCiteMeInCOCI" : {"notes":"Params: [[DOI]]. Check the COCI citations for this DOI"}
}

def get_my_commands():
    return my_commands

def exec_my_commands(command,param):
    if command == "/howToContactYou":
        return how_to_contact_you(param)
    if command == "/askCOCI":
        return ask_coci(param)
    if command == "/whoCiteMeInCOCI":
        return who_cite_me_in_coci(param)





#ADD all the methods you want to use
####################################

import csv
import urllib.request
import json
import re

contact = {
    'Website':'http://opencitations.net/',
    'Email':'contact@opencitations.net',
    'Twitter':'https://twitter.com/opencitations',
    'Github': 'https://github.com/essepuntato/opencitations',
    'Wordpress': 'https://opencitations.wordpress.com/'
}

def how_to_contact_you(a_text):
    str_to_return = ""
    for c in contact:
        str_to_return = str_to_return + "\n"+c+": "+contact[c]
    return str_to_return


#'http://opencitations.net/index/coci/api/v1/metadata/10.1108/jd-12-2013-0166'
def ask_coci(a_text):
    str_to_return = ""

    try:
        a_text = a_text[0]
    except:
        return "You must text me a DOI !"

    find_list = re.findall(r"(10.\d{4,9}\/[-._;()/:A-Za-z0-9][^\\s]+)",a_text)
    if len(find_list) == 0:
        return "Please, text me a correct DOI format"

    res = find_list[0]

    api_call = 'http://opencitations.net/index/coci/api/v1/metadata/'
    input = res
    api_call = api_call+input
    #call API
    try:

        contents = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_output = json.loads(contents)
        if len(json_output) == 0:
            return "No data found in COCI for: "+ input
        else:
            rc_data = json_output[0]
            str_to_return = str_to_return + "\n\n Title: "+rc_data['title']
            str_to_return = str_to_return + "\n\n Author/s: "+rc_data['author']
            str_to_return = str_to_return + "\n\n Year: "+rc_data['year']
            str_to_return = str_to_return + "\n\n #Citations: "+rc_data['citation_count']
    except:
        return "Sorry, the connection with COCI went wrong!"

    return str_to_return


def who_cite_me_in_coci(a_text):
    str_to_return = ""

    try:
        a_text = a_text[0]
    except:
        return "You must text me a DOI !"

    find_list = re.findall(r"(10.\d{4,9}\/[-._;()/:A-Za-z0-9][^\\s]+)",a_text)
    if len(find_list) == 0:
        return "Please, text me a correct DOI format"

    res = find_list[0]
    api_call = 'http://opencitations.net/index/coci/api/v1/citations/'
    input = res
    api_call = api_call+input
    #call API
    try:
        contents = urllib.request.urlopen(api_call).read().decode('utf-8')
        json_output = json.loads(contents)
        if len(json_output) == 0:
            return "No citations found in COCI for: "+ input
        else:
            str_to_return = str_to_return + "\n #Citations: "+str(len(json_output))+ "\n\n"
            for c_elem in json_output:
                str_to_return = str_to_return + "\n Citing: "+c_elem['citing']
                str_to_return = str_to_return + "\n Timespan: "+c_elem['timespan']
                str_to_return = str_to_return + "\n COCI Resource: "+"http://opencitations.net/index/coci/browser/ci/"+c_elem['oci']
                str_to_return = str_to_return + "\n\n"
    except:
        return "Sorry, the connection with COCI went wrong!"

    return str_to_return



def check_input_doi(a_text):
    try:
        a_text = a_text[0]
    except:
        return "You must text me a DOI !"

    find_list = re.findall(r"(10.\d{4,9}\/[-._;()/:A-Za-z0-9][^\\s]+)",a_text)
    if len(find_list) == 0:
        return "Please, text me a correct DOI format"

    return "[[doi]]"+find_list[0]
