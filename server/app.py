#!/usr/bin/env python
#Author: Febry Yadi Zainal

#import library
import re
from flask import Flask, request
from flask_restful import Resource, Api
import json
import os
import sys
import logging
import json
import random
import string


#Constans
version = 0.1
name = "app"
title = name + ' v' + str(version)


#Flask object initiation
app = Flask(__name__)

#flask restful object initiation
api = Api(app)


"""
    Default Configuration Value
"""
config = {
    name:{
        'host':'0.0.0.0',
        'port':'8080'
    },
    'logging':{
        'format':'%(asctime)s %(msecs)d -> %(module)s %(levelname)s : %(message)s',
        'dateformat':'%Y%m%d_%H%M%S',
        'path':'var/log/' + name + '.log',
        'level':'INFO'
    }
}



class Writer(object):
    def __init__(self, directory='', filename='randomData', max_files=sys.maxsize,
                 max_file_size=2000000):
        self.ii = 1
        self.directory, self.filename = directory, filename
        self.max_file_size, self.max_files = max_file_size, max_files
        self.finished, self.fh = False, None
        self.open()

    def rotate(self):
        if os.stat(self.filename_template).st_size > self.max_file_size:
            self.close()
            self.ii += 1
            if self.ii <= self.max_files:
                self.open()
            else:
                self.close()
                self.finished = True

    def open(self):
        self.fh = open(self.filename_template, 'w')

    def write(self, text=""):
        self.fh.write(text)
        self.fh.flush()
        self.rotate()

    def close(self):
        self.fh.close()

    @property
    def filename_template(self):
        return self.directory + self.filename + ".txt"
    
class generateFile:
    def generate_alphabet(size=random.randint(1, 27), chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for i in range(size))


    def generate_alphabet(size=random.randint(1, 27), chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for i in range(size))


    def generate_integer():
        return random.randint(000000000, 999999999)


    def generate_real():
        return random.uniform(000000000, 99999999)


    def generate_alphanumerics():
        return " " * random.randint(0, 10) + ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=random.randint(0, 36))) + " " * random.randint(0, 10)

    def generateRandom():
        logging.info('generate file starting...')
        randomfile = Writer(max_files=1)
        fileDir = os.getcwd() + '/' +randomfile.filename_template
        logging.info('file was generated = ' + fileDir)
        buffer = ""
        while not randomfile.finished:
            try:
                buffer += generateFile.generate_alphabet() + ", " + str(generateFile.generate_integer()) + ", " + str(generateFile.generate_real()) + ", " + str(
                    generateFile.generate_alphanumerics()) + ", "

                if len(buffer) >= 100000:
                    randomfile.write(buffer)
                    buffer = ""
            except ValueError as e:
                randomfile.close()
        return fileDir

class readFile:
    def regex(word):
        pattern = 'alphabet'
        pattern_alphabet = re.compile("[a-z]+")
        pattern_integer = re.compile("[0-9]+")
        pattern_float = re.compile("[0-9]*.[0-9]+")
        pattern_alphanumeric = re.compile("[0-9a-z]+")

        if pattern_alphabet.fullmatch(word) is not None:
            pattern = 'alphabet'

        elif pattern_integer.fullmatch(word) is not None:
            pattern = 'integer'

        elif pattern_float.fullmatch(word) is not None:
            pattern = 'float'

        elif pattern_alphanumeric.fullmatch(word) is not None:
            pattern = 'alphanumeric'
        
        return pattern


    def read(filein):
        logging.info('read file starting...')
        with open(filein) as file:
            a = file.read()
            mem = [i.strip() for i in a.split(',')]
            sum_alphabet = 0
            sum_integer = 0
            sum_float = 0
            sum_alphanumeric = 0
            for i in mem:
                pattern = readFile.regex(i)
                if pattern == 'alphabet':
                    sum_alphabet+=1
                if pattern == 'integer':
                    sum_integer+=1
                if pattern == 'float':
                    sum_float+=1
                if pattern == 'alphanumeric':
                    sum_alphanumeric+=1
                    
            sum_pattern = {
                'sum_alphabet': sum_alphabet,
                'sum_integer': sum_integer,
                'sum_float': sum_float,
                'sum_alphanumeric': sum_alphanumeric
            }
            
            return sum_pattern

#create resources class
class myResource(Resource):
    def get(self):
        '''
            this method to handle get request
        '''
        try:
            jsonData = json.loads(request.data)
            logging.info('[>>>] ' + str(json.dumps(jsonData)))
            if jsonData['type'] == 'report':
                sum_pattern = readFile.read(jsonData['param']['link'])
                logging.info('read file done')
                response = jsonData
                response['requestUuid'] = jsonData['uuid']
                response['param']['alphabetical strings'] = sum_pattern['sum_alphabet']
                response['param']['integers'] = sum_pattern['sum_integer']
                response['param']['real numbers'] = sum_pattern['sum_float']
                response['param']['alphanumerics'] = sum_pattern['sum_alphanumeric']
                del response['uuid']
        except Exception as e:
            response = jsonData
            response['requestUuid'] = jsonData['uuid']
            del response['uuid']
            response['param']['messages'] = str(e)

        logging.info('[<<<] ' + str(json.dumps(response)))
        return response
    
    def post(self):
        '''
            this method to handle post request
        '''
        try:
            jsonData = json.loads(request.data)
            logging.info('[>>>] ' + str(json.dumps(jsonData)))
            link = generateFile.generateRandom()
            response = jsonData
            response['requestUuid'] = jsonData['uuid']
            response['param']['link'] = link
            del response['uuid']
        except Exception as e:
            response = jsonData
            response['requestUuid'] = jsonData['uuid']
            del response['uuid']
            response['param']['messages'] = str(e)
        
        logging.info('[<<<] ' + str(json.dumps(response)))
        return response

api.add_resource(myResource, "/api", methods=["GET", "POST"])

if __name__ == '__main__':
    """
        log configuration
    """
    try:
        logging.basicConfig(
            format = config['logging']['format'],
            datefmt = config['logging']['dateformat'],
            filename = config['logging']['path'],
            level = getattr(logging, config['logging']['level'].upper(), None)
        )
    except Exception as e:
        print(e)
        sys.exit(0)
        
    print(title)
    app.run(debug=True, host=config[name]['host'], port=config[name]['port'])
    