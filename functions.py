from datetime import datetime
import time
import numpy as np
import matplotlib.pyplot as plt


def extract_value(field, message):
    if field == 'power':
        c = message.split('power')
        d = c[1].replace("\":", "")
        e = d.split(',')
        return e[0]
    elif field == 'tstamp':
        c = message.split("timestamp\":")
        d = c[1].split(",")
        return d[0]
    elif field == 'counters':
        c = message.split("counters\":[")
        d = c[1].split(",")
        u1 = d[0]
        u2 = d[1].replace(" ", "")
        u3 = d[2].replace("]", "")
        u3 = u3.replace(" ", "")
        return u1, u2, u3
    elif field == 'total':
        c = message.split("total\":")
        d = c[1].replace("}", "")
        return d

# Well, a more sophisticated version of field extraction would be recognising, it is json format. I paste a working
# solution below, but it is not yet implemented.
# import json
#
# def extract_fields(message):
#     try:
#         data = json.loads(message)
#         power = data["power"]
#         timestamp = data["timestamp"]
#         return power, timestamp
#     except (KeyError, json.JSONDecodeError) as e:
#         print("Error extracting fields:", str(e))
#         return None, None
#
# # Example usage:
# message = '{"power":0.00,"overpower":0.00,"is_valid":true,"timestamp":1676545932,"counters":[0.000, 0.000, 0.000],"total":429559}'
# power, timestamp = extract_fields(message)
# if power is not None and timestamp is not None:
#     print("Power:", power)
#     print("Timestamp:", timestamp)

def create_scaled_timediff(tdiff_in_secs):
    if tdiff_in_secs < 100:
        return "{:.0f}".format(tdiff_in_secs) + ' seconds'
    if 100 <= tdiff_in_secs < 3600:
        return time.strftime("%M:%S", time.gmtime(tdiff_in_secs))
    else:
        return time.strftime("%H:%M:%S", time.gmtime(tdiff_in_secs))


def generate_graph(streak_total_pwr, time_diff, streak_pwr_values, graph_path, plotname_prefix, workmode):
    time_diff_secs = time_diff.total_seconds()
    time_diff_in_mins = time_diff_secs / 60
    time_diff_in_hours = time_diff_secs / 3600
    max_streak_pwr_value = max(streak_pwr_values)
    # Generating the graph for the streak
    if workmode == 'streak':
        if time_diff_secs < 100:
            x = np.linspace(0, time_diff_secs, len(streak_pwr_values))
            plt.xlabel("Time [seconds]",  fontsize=6)
        elif time_diff_in_hours < 4:
            x = np.linspace(0, time_diff_in_mins, len(streak_pwr_values))
            plt.xlabel("Time [minutes]",  fontsize=6)
        else:
            x = np.linspace(0, time_diff_in_hours, len(streak_pwr_values))
            plt.xlabel("Time [hours]",  fontsize=6)
        plt.title("Length: " + create_scaled_timediff(time_diff_secs) + ", Pwr use: " + "{:.1f}".format(
            streak_total_pwr) + " Wh" + ", Max: " + "{:.1f}".format(max_streak_pwr_value) + " W", fontsize=14)

    if workmode == '24h':
        x = np.linspace(0, 24, len(streak_pwr_values))
        plt.xlabel("Time [hours]",  fontsize=6)
        plt.title(time.strftime("%Y-%m-%d") + ", Pwr use: " + "{:.1f}".format(
            streak_total_pwr) + " Wh" + ", Max: " + "{:.1f}".format(max_streak_pwr_value) + " W",  fontsize=14)
        plt.xlim([0, 24])
        plt.xticks([0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24], [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
    plt.grid(axis="x", color="black", alpha=.3, linewidth=.5, linestyle=':')
    plt.grid(axis="y", color="black", alpha=.3, linewidth=.5, linestyle=':')

    plt.ylabel("Power [W]",  fontsize=6)
    plt.plot(x, streak_pwr_values)
    # plt.figure(figsize=(30,20))
    plt.savefig(graph_path + "/" + plotname_prefix + time.strftime("%Y-%m-%d %H-%M-%S") + "_with_powerUse_" + "{:.2f}".format(
        streak_total_pwr) + "_Wh.png", dpi=350)
    # plt.savefig('PowerUseLog_' + strftime("%Y-%m-%d %H%M%S") + '.png')
    plt.clf()


def is_it_midnight():
    t = datetime.now()
    if t.hour == 0 and t.minute == 0 and t.second == 0:
        return True
    else:
        return False

def is_the_day_over_yet():
    t = datetime.now()
    if t.hour == 23 and t.minute == 59 and t.second == 55:
        return True
    else:
        return False
