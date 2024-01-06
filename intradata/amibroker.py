import os
from helper import Helper
import win32com.client


class AmiBroker():
    app_folder = os.path.dirname(os.path.realpath(__file__))
    database_folder = os.path.join(app_folder, 'database')
    # format_file_path = os.path.join(app_folder, 'vnami.format')
    format_file_path = os.path.join(app_folder, 'intradata.format')
    merged_data_file_name = "All.csv"
    merged_data_file_path = os.path.join(database_folder, merged_data_file_name)
    amibroker = None

    # Get Amibroker instance
    @classmethod
    def get_amibroker_instance(cls):
        if cls.amibroker is None and Helper.is_amibroker_opened():
            # app_patch = r'D:\trading\AmiBroker 6.30x64 Portable\Broker.exe'
            cls.amibroker = win32com.client.Dispatch("Broker.Application")
            # cls.amibroker = win32com.client.Dispatch(app_patch)
        return cls.amibroker
    
    # Merge all csv files into one then import data into Amibroker
    @classmethod
    def import_data(cls):
        amibroker = cls.get_amibroker_instance()
        if amibroker is not None:
            Helper.delete_file(cls.merged_data_file_path) # Make sure the merged data file is empty
            try:
                Helper.merge_csv_files(cls.database_folder, cls.merged_data_file_name)
                amibroker.Import(0, cls.merged_data_file_path, cls.format_file_path)
                amibroker.RefreshAll()
                print(f"Success: Import data into Amibroker")
            except Exception as e:
                print(f"Error: Cannot import data into Amibroker. Detail: {e}")
            Helper.delete_file(cls.merged_data_file_path) # Delete the merged data file after done
        else:
            print("Error: Amibroker is not opened")


# For testing purposes only
if __name__ == "__main__":
    Helper.measure_time(AmiBroker.import_data)
    