import os
import xml.etree.ElementTree as ET
import csv
from collections import defaultdict

def parse_xml_files(folder_path):
    class_times = defaultdict(float)

    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            tree = ET.parse(os.path.join(folder_path, filename))
            root = tree.getroot()

            for testcase in root.findall('.//testcase'):
                classname = testcase.attrib['classname']
                time = float(testcase.attrib['time'])

                class_times[classname] += time

    return class_times

def distribute_into_groups(class_times):
    sorted_classes = sorted(class_times.items(), key=lambda x: x[1], reverse=True)

    total_time = sum(time for _, time in sorted_classes)
    time_per_group = total_time / 5

    groups = [[] for _ in range(5)]
    curr_group = 0
    group_time = 0

    for classname, time in sorted_classes:
        if group_time + time <= time_per_group:
            groups[curr_group].append((classname, time))
            group_time += time
        else:
            curr_group += 1
            if curr_group >= len(groups):
                curr_group = len(groups) - 1  # Ensure it doesn't go beyond the last group
            group_time = time
            groups[curr_group].append((classname, time))

    return groups

def write_to_csv(output_file, result_groups):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['classname', 'time', 'groupNo'])

        for i, group in enumerate(result_groups, 1):
            group_time = sum(time for _, time in group)
            for classname, time in group:
                writer.writerow([classname, round(time, 3), i])

if __name__ == "__main__":
    folder_path = r'C:\Users\SHREE\OneDrive\Documents\Ridecell_Programming_Assignment\data'
    output_file = r'C:\Users\SHREE\OneDrive\Documents\Ridecell_Programming_Assignment\data\output.csv'

    class_times = parse_xml_files(folder_path)
    result_groups = distribute_into_groups(class_times)
    write_to_csv(output_file, result_groups)
    print("Your task is succefully completed...")
