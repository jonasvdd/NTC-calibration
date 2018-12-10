# -*- coding: utf-8 -*-
"""
    *********
    TSP01.py
    *********
    
    Wrapper of a `TSP01 <https://www.thorlabs.de/newgrouppage9.cfm?objectgroup_id=5884&pn=TSP01/>`_ sensor.
"""
__author__ = 'Jonas Van Der Donckt'

import visa 


class TSP01:
    """
    Is a wrapper for the THORLABS TSP01. 
    Makes use of SCPI (Standard Commands for Programmable Intstruments) 
    to retrieve the temperature/humidity. 
    """

    def __init__(self):
        """
        Creates an instance of the TSP01 temperature logger
        """
        rm = visa.ResourceManager('@py')
        resources = rm.list_resources()      # USB0::4883::33016::M00495749::0::INSTR
        print("available resources")
        for i, resource in enumerate(resources, 1):
            print("\t%s: %s" % (i, resource))
        res_id = 0
        while res_id not in range(1, len(resources) + 1):
            print("Choose the tsp01 resource: ")
            res_id = int(input())

        self.sensor = rm.open_resource(resources[res_id - 1])

        print(self.sensor.query('*IDN?'))

    def USB_temperature(self):
        """
        Reads the built-in temperature of the TSP01 logger
        
        :return: the temperature in °C
        :rtype: float
        """
        return self.sensor.query_ascii_values(':READ?')[0]

    def USB_humidity(self):
        """
        Retrieves the built-in relative humidity
        """
        return self.sensor.query_ascii_values(":SENSe2:HUMidity:DATA?")[0]

    def probe_1_temperature(self):
        """
        Reads the temperature of external probe 1
        
        :return: the temperature °C
        :rtype: float
        """
        return self.sensor.query_ascii_values(':SENSe3:TEMPerature:DATA?')[0]

    def probe_2_temperature(self):
        """
        Reads the temperature of external probe 1
        
        :return: the temperature °C
        :rtype: float
        """
        return self.sensor.query_ascii_values(':SENSe4:TEMPerature:DATA?')[0]


##############################
# for testing purposes:
##############################
if __name__ == "__main__":
    text = "testing functionality"
    print('-'*(8 + len(text)) + '\n    ' + text + '\n' + '-'*(8 + len(text) ))
    
    tsp01 = TSP01()
    print("internal temperature:         {} °C".format(tsp01.USB_temperature()))
    print("internal humidity:            {} %r.h".format(tsp01.USB_humidity()))
    print("external temperature probe 1: {} °C".format(tsp01.probe_1_temperature()))
    print("external temperature probe 2: {} °C".format(tsp01.probe_2_temperature()))
