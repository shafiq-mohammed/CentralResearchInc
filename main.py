# Author: Shafiq Mohammed

import requests
import json
import logging
import os
import pprint

# Implementing logging, setting log level to error
LOG = os.getcwd() + "/_trial_temp/test.log"
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)


class Connection:
    """
    A class to represent our connection to our endpoint

    ...

    Attributes
    ----------
    url : str
        url of our endpoint
    success : int
        number of times endpoint returned true for health status
    failure : int
        number of times endpoint returned false for health status
    min_response_time: int
        fastest response time returned by endpoint
    max_response_time: int
        slowest response time returned by endpoint
    aggregated_response_time: int
        aggregate of response times by endpoint - using it in the end to compute mean response time.

    Methods
    -------
    check_health():
        Checks the health of the endpoint
    """

    def __init__(self, url):
        """
        Constructs all the necessary attributes for the Connection, including assigning the url to a variable
        :param url: the url of our endpoint
        """
        self.url = url
        self.success = 0
        self.failure = 0
        self.min_response_time = 0
        self.max_response_time = 0
        self.aggregated_response_time = 0

    def check_health(self):
        """
        Checks the health of the endpoint
        :return: returns status of server in boolean format
        """
        try:
            response = requests.get(self.url + '/health')
        except requests.ConnectionError:
            logging.fatal(self.url + " is an invalid endpoint - please enter a working url.")
            exit()  # Implemented a hard exit because if the endpoint is invalid then we should not proceed.
        self.set_times(response.elapsed.microseconds)
        status = response.json()['status']
        return status

    def set_times(self, resp_time):
        """
        Set's the min and max response times as well as aggregates it up for the mean response time
        :param resp_time: response time of the endpoint in microseconds
        """
        if self.min_response_time == 0:  # This means that the value has not been set yet
            self.min_response_time = resp_time
        if self.max_response_time == 0:
            self.max_response_time = resp_time

        if resp_time < self.min_response_time:
            self.min_response_time = resp_time
        if resp_time > self.max_response_time:
            self.max_response_time = resp_time

        self.aggregated_response_time += resp_time


def main():
    """
    Holds the core logic.
    :return: results of all services in a json/dict formatted string
    """
    # The following block holds and executes our core logic
    if __name__ == "__main__":
        connections = []  # This will hold our connection objects
        output_json = {}

        # We have a config file that has endpoints as a list within a json object. But we need to test for edge cases first
        with open('config.json', 'r') as config_file:
            try:
                config_data = json.load(config_file)
            except json.JSONDecodeError:
                logging.fatal("config.json does not contain a properly formatted json file. Please fix config file.")
                exit()  # Cannot continue with program execution so implementing a hard exit

            if 'services' not in config_data:
                logging.fatal("config.json does not contain services. Please fix config file.")
                return
            for service in config_data['services']:
                my_connection = Connection(url=service)
                connections.append(my_connection)

            #  Here we are iterating through each Connection object. We used enumerate so we have an index so we can write "server#" in output
            for index, connection in enumerate(connections):
                for i in range(0, 10000):
                    health = connection.check_health()
                    if health:
                        connection.success += 1
                    else:
                        connection.failure += 1

                service_num = "service" + str(index + 1)  # so we can create the key for the output json/dict.
                mean_response_time = connection.aggregated_response_time / (connection.success + connection.failure)  # Instead of making another counter, I just added success+failure to get total calls
                output_json[service_num] = {"success": connection.success, "failure": connection.failure, "min_response_time": connection.min_response_time, "max_response_time": connection.max_response_time, "mean_response_time": mean_response_time}

            logging.info(pprint.pformat(output_json))
            return output_json


if __name__ == "__main__":
    pprint.pprint(main())
