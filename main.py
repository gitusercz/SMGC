# To start it requests, BeautifulSoup4 has to be installed
# An example line is:
# {"power":0.00,"overpower":0.00,"is_valid":true,"timestamp":1676545932,"counters":[0.000, 0.000, 0.000],"total":429559}
#
# An example of a logged row:
# 2023-02-15 21:12:54	1676495575	1.00	3.533	2.308	2.282	429558

from time import sleep, strftime
from functions import extract_value
from functions import create_scaled_timediff
from functions import generate_graph
from functions import is_it_midnight
from functions import is_the_day_over_yet
import datetime
import requests
import re
from bs4 import BeautifulSoup
from configobj import ConfigObj

# ===========Loading settings from config file
config = ConfigObj("config.ini")
shelly_IP = (config['Shelly_IP'])
graph_path = (config['graph_path'])
measuring_freq = int(config['measuring_freq'])
measuring_freq_when_idle = int(config['measuring_freq_when_idle'])
workmode = config['workmode']
graphname_prefix_for_streak = config['graphname_prefix_for_streak']
graphname_prefix_for_24h = config['graphname_prefix_for_24h']
# ===========Loading settings from config file

logfreq = measuring_freq
separator_already_there = True
waiting_for_midnight_to_start = True
streak_pwr_values = []
is_24h_setup_done = False

print("SMGC started...")
while 1:
    page = requests.get("http://" + shelly_IP + "/meter/0")
    soup = BeautifulSoup(page.content, 'html.parser')
    current_msg = soup.prettify()

    # # Lines for development
    # current_msg = input("Enter a line: ")
    # # Adding a newline only required for development.
    # current_msg += "\n"
    u1, u2, u3 = extract_value("counters", current_msg)
    if workmode == 'streak':
        if extract_value("power", current_msg) != '0.00':
            # Start of a new streak:
            if separator_already_there:
                streak_pwr_startvalue = float(extract_value("total", current_msg))  # Record the total power value as starting point
                streak_start = datetime.datetime.now()                              # Record when the streak started
                streak_pwr_values = []                                              # Init an empty list of power values
            streak_pwr_values.append(float(extract_value("power", current_msg)))
            separator_already_there = False
            logfreq = measuring_freq
            with open(r'log.log', 'a') as log:
                log.write(
                    strftime("%Y-%m-%d %H:%M:%S") + "\t" + extract_value("tstamp", current_msg) + "\t" + extract_value(
                        "power", current_msg) + "\t" + u1 + "\t" + u2 + "\t" + u3 + "\t" + extract_value("total",
                                                                                                         current_msg))
        else:
            # Doing statistics, as this is when the power use dropped to 0
            if not separator_already_there:
                streak_total_pwr = (float(extract_value("total", current_msg)) - streak_pwr_startvalue) / 60
                time_diff = datetime.datetime.now() - streak_start
                time_diff_secs = time_diff.total_seconds()
                # generating the graph in a function
                generate_graph(streak_total_pwr, time_diff, streak_pwr_values, graph_path, graphname_prefix_for_streak, workmode)
                with open(r'log.log', 'a') as log:
                    log.write("=== Measurement finished at: " + strftime(
                        "%Y-%m-%d %H:%M:%S") + " Streak duration was " + create_scaled_timediff(time_diff_secs) + " with power use: " + "{:.2f}".format(streak_total_pwr) + " Wh ===\n")
                    logfreq = measuring_freq_when_idle
                    separator_already_there = True
    if workmode == '24h':
        while not is_it_midnight() and waiting_for_midnight_to_start == True:
            sleep(1)
            waiting_for_midnight_to_start = False
    #     collecting the lines
        if not is_24h_setup_done:
            streak_pwr_startvalue = float(
                extract_value("total", current_msg))    # Record the total power value as starting point
            streak_start = datetime.datetime.now()      # Record when the streak started
            streak_pwr_values = []                      # Init an empty list of power values
            with open(r'log.log', 'a') as log:
                log.write("=== A new 24 hour measurement started at: " + strftime("%Y-%m-%d %H:%M:%S") + "===\n")
            is_24h_setup_done = True

        streak_pwr_values.append(float(extract_value("power", current_msg)))
    #     Close to midnight, create statistics, draw graph and set up for another 24h measurement
        if is_the_day_over_yet():
            streak_total_pwr = (float(extract_value("total", current_msg)) - streak_pwr_startvalue) / 60
            time_diff = datetime.datetime.now() - streak_start
            time_diff_secs = time_diff.total_seconds()
            generate_graph(streak_total_pwr, time_diff, streak_pwr_values, graph_path, graphname_prefix_for_24h, workmode)
            with open(r'log.log', 'a') as log:
                log.write("=== 24h Measurement finished at: " + strftime(
                    "%Y-%m-%d %H:%M:%S") + " with power use: " + "{:.2f}".format(streak_total_pwr) + " Wh ===\n")
            waiting_for_midnight_to_start = True
            is_24h_setup_done = False
    sleep(logfreq)
