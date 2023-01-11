import time
import json
import cPickle as pickle
import os
import sys


def get_current_time_in_ms():
    return int(round(time.time() * 1000))


def json_load(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(full_path) as data_file:
            data = json.load(data_file)
            return data
    except IOError as ex:
        print "Error loading json file '{}': {}".format(full_path, ex.message)
        sys.exit(1)


def pickle_list_to_file(filename, list_of_objects):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(full_path, "w+") as data_file:
            pickle.dump(list_of_objects, data_file, pickle.HIGHEST_PROTOCOL)
    except IOError as ex:
        print "Error saving to pickle file '{}': {}".format(full_path, ex.message)
        sys.exit(1)


def unpickle_list_from_file(filename):
    full_path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(full_path, "r+") as data_file:
            return pickle.load(data_file)
    except IOError as ex:
        print "Error loading list from pickle file '{}': {}".format(full_path, ex.message)
        sys.exit(1)