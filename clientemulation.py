import glob
from sourcefile import SourceFile


class ClientEmulation:
    def __init__(self, raw):
        list_of_files = glob.glob('../emulator/*')
        for file_name in sorted(list_of_files):
            if file_name.endswith(".eeg"):
                print "Processing " + file_name
                sourcefile = SourceFile(file_name)
                float_array = sourcefile.read_all()
                print "Processing " + file_name + " " + str(len(float_array))
                for data in float_array:
                    raw.add_float(data)
        print "List of file"
        print list_of_files
        print "List of file end"

