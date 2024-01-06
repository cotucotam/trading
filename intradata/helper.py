import os
import csv
import time
import psutil
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor


class Helper():
    # Execute thread pool
    @staticmethod
    def execute_thread_pool(tasks, max_workers=10):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(f, *args) for f, args in tasks]
            results = [future.result() for future in futures]
            return results
    
    # Get the last working day, which is not Saturday or Sunday
    @staticmethod
    def get_last_working_day():
        today = datetime.today()
        if today.weekday() == 5: # Today is Sat then minus 1 day
            today -= timedelta(days=1)
        elif today.weekday() == 6: # Today is Sun then minus 2 days
            today -= timedelta(days=2)
        elif today.weekday() == 0 and today.hour < 15: # Today is Mon morning so minus 3 days
            today -= timedelta(days=3)
        else:
            if today.hour < 15: # Before 3 p.m
                today -= timedelta(days=1)
        return today.strftime('%Y/%m/%d')

    # Check if Amibroker is opened
    @staticmethod
    def is_amibroker_opened():
        for process in psutil.process_iter():
            if process.name() == "Broker.exe":
                return True
        return False
    
    # Calculate running time of a function
    @staticmethod
    def measure_time(func, *args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        time_delta = int(end-start)
        hours, remainder = divmod(time_delta, 3600)
        minutes, seconds = divmod(remainder, 60)
        print("Elapsed time: {:02} hours {:02} minutes {:02} seconds.".format(int(hours), int(minutes), int(seconds)))
        return result
    
    # Merge all csv files located in a specific folder into one csv file
    @staticmethod
    def merge_csv_files(source_folder, output_file_name):
        csv_files = [f for f in os.listdir(source_folder) if f.endswith('.csv')] # Get a list of all csv files in the specified directory
        output_file_path = os.path.join(source_folder, output_file_name) # Specify the file to write the merged data
        # Open the output file in write mode
        with open(output_file_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            # Loop through each csv files
            for file in csv_files:
                file_path = os.path.join(source_folder, file)
                with open(file_path, 'r') as infile:
                    reader = csv.reader(infile)
                    for row in reader:
                        writer.writerow(row) # Write the data from the input file to the output file
    
    # Delete file by path
    @staticmethod
    def delete_file(file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)

    
# For testing purposes only
if __name__ == "__main__":
    print(Helper.is_amibroker_opened())
