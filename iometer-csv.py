import os
from os.path import join
import configparser
import csv

CONF = 'iometer_csv_parser.ini'
folders = []
result_dict = []

# If exists the configuration file, scan those folders in the config file. Otherwise, scan local. 
if os.path.isfile(CONF):
    cfg = configparser.ConfigParser()
    cfg.read(CONF, 'utf8')
    folders = cfg.get('Scan', 'ScanFolder').split(';')
else:
    folders.append(".")

for folder in folders:
    # test_name = os.path.basename(folder)  # extract Test Name from the folder name
    for (dirname, dirs, files) in os.walk(folder):
        for filename in files:
            if filename.endswith('csv'):
                print("Parsing file: %s" % os.path.join(dirname, filename))
                vmname = filename.split(".")[0]  # extract VM name from the file name
                test_name = dirname  # use dirname as test name
                csv_content = []
                for row in csv.reader(open(os.path.join(dirname, filename)), delimiter=",",
                                      skipinitialspace=True):  # put CSV content in a big list
                    csv_content.append(row)
                for i, element in enumerate(csv_content):  # start parsing the content one by one
                    try:
                        if not element:  # if the element is empty, skip it.
                            continue
                        elif element[
                            0] == "'Time Stamp":  # if the element starts with 'Time Stamp, the next element is the test time
                            test_result_position = i + 1
                            time_stamp = csv_content[test_result_position][0]
                        elif element[
                            0] == "'size":  # if the element starts with 'size, the next element will be test configurations
                            test_result_position = i + 1
                            block_size = csv_content[test_result_position][0]
                            percent_reads = csv_content[test_result_position][2]
                            percent_random = csv_content[test_result_position][3]
                        elif element[
                            0] == "ALL":  # if the element starts with 'Target Type, the next element will be test result
                            test_result_position = i
                            IOps = float(csv_content[test_result_position][6])
                            MBps = float(csv_content[test_result_position][9])
                            AvgRespTime = float(csv_content[test_result_position][17])
                            MaxRespTime = float(csv_content[test_result_position][22])
                            IOs = int(csv_content[test_result_position][32]) + int(
                                csv_content[test_result_position][33])
                            percent_CPU = csv_content[test_result_position][48]
                            latency_0_50us = int(csv_content[test_result_position][59]) / IOs * 100
                            latency_50_100us = int(csv_content[test_result_position][60]) / IOs * 100
                            latency_100_200us = int(csv_content[test_result_position][61]) / IOs * 100
                            latency_200_500us = int(csv_content[test_result_position][62]) / IOs * 100
                            latency_05_1ms = int(csv_content[test_result_position][63]) / IOs * 100
                            latency_1_2ms = int(csv_content[test_result_position][64]) / IOs * 100
                            latency_2_5ms = int(csv_content[test_result_position][65]) / IOs * 100
                            latency_5_10ms = int(csv_content[test_result_position][66]) / IOs * 100
                            latency_10_15ms = int(csv_content[test_result_position][67]) / IOs * 100
                            latency_15_20ms = int(csv_content[test_result_position][68]) / IOs * 100
                            latency_20_30ms = int(csv_content[test_result_position][69]) / IOs * 100
                            latency_30_50ms = int(csv_content[test_result_position][70]) / IOs * 100
                            latency_50_100ms = int(csv_content[test_result_position][71]) / IOs * 100
                            latency_100_200ms = int(csv_content[test_result_position][72]) / IOs * 100
                            latency_200_500ms = int(csv_content[test_result_position][73]) / IOs * 100
                            latency_05_1s = int(csv_content[test_result_position][74]) / IOs * 100
                            latency_1_2s = int(csv_content[test_result_position][75]) / IOs * 100
                            latency_2_47s = int(csv_content[test_result_position][76]) / IOs * 100
                            latency_47_5s = int(csv_content[test_result_position][77]) / IOs * 100
                            latency_5_10s = int(csv_content[test_result_position][78]) / IOs * 100
                            latency_10plus = int(csv_content[test_result_position][79]) / IOs * 100
                            result = [test_name, vmname, time_stamp, block_size, percent_reads, percent_random,
                                      "{0:.0f}".format(IOps),
                                      "{0:.1f}".format(MBps),
                                      "{0:.1f}".format(AvgRespTime),
                                      "{0:.1f}".format(MaxRespTime),
                                      percent_CPU,
                                      "{0:.1f}".format(latency_0_50us),
                                      "{0:.1f}".format(latency_50_100us),
                                      "{0:.1f}".format(latency_100_200us),
                                      "{0:.1f}".format(latency_200_500us),
                                      "{0:.1f}".format(latency_05_1ms),
                                      "{0:.1f}".format(latency_1_2ms),
                                      "{0:.1f}".format(latency_2_5ms),
                                      "{0:.1f}".format(latency_5_10ms),
                                      "{0:.1f}".format(latency_10_15ms),
                                      "{0:.1f}".format(latency_15_20ms),
                                      "{0:.1f}".format(latency_20_30ms),
                                      "{0:.1f}".format(latency_30_50ms),
                                      "{0:.1f}".format(latency_50_100ms),
                                      "{0:.1f}".format(latency_100_200ms),
                                      "{0:.1f}".format(latency_200_500ms),
                                      "{0:.1f}".format(latency_05_1s),
                                      "{0:.1f}".format(latency_1_2s),
                                      "{0:.1f}".format(latency_2_47s),
                                      "{0:.1f}".format(latency_47_5s),
                                      "{0:.1f}".format(latency_5_10s),
                                      "{0:.1f}".format(latency_10plus)]
                            result_dict.append(result)

                    except:
                        print("not able to parse:")
                        print(element)
                        continue

# print(result_dict)
print('{} lines written'.format(len(result_dict)))

ofile = open('iometer_csv_parser.csv', "w", newline='')
writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
writer.writerow(["Test Name", "Guest VM Name", "Time Stamp", "Transfer Request Size", "Percent Read/Write Distribution",
                 "Percent Random/Sequential Distribution",
                 "Total I/O per Second", "Total MBs per Second", "Average I/O Response Time (ms)",
                 "Maximum I/O Response Time (ms)", "CPU Utilization (total)",
                 "%lat 0 to 50 uS", "%lat 50 to 100 uS", "%lat 100 to 200 uS", "%lat 200 to 500 uS", "%lat 0.5 to 1 mS",
                 "%lat 1 to 2 mS", "%lat 2 to 5 mS", "%lat 5 to 10 mS",
                 "%lat 10 to 15 mS", "%lat 15 to 20 mS", "%lat 20 to 30 mS", "%lat 30 to 50 mS", "lat 50 to 100 mS",
                 "%lat 100 to 200 mS", "lat 200 to 500 mS", "%lat 0.5 to 1 S",
                 "%lat 1 to 2 s", "%lat 2 to 4.7 s", "%lat 4.7 to 5 s", "%lat 5 to 10 s", "%lat >= 10 s"])
writer.writerows(result_dict)
ofile.close()
