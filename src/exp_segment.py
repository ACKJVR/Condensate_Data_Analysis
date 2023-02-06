import numpy as np

class experimental_segment():
    def __init__(self,file):
        self.parameter_dict = {}
        self.__import_header__(file)

        self.pressure = self.parameter_dict["pressure"]
        self.time_data, self.x_data = np.hsplit(np.genfromtxt(file,delimiter=','),2)
        self.time_data = self.time_data.flatten()
        self.x_data = self.x_data.flatten()
        self.t0 = self.time_data[0]
        self.L0 = self.x_data[0]

        if self.parameter_dict["delta pressure"] > 0:
            self.sign = "pos"
        else:
            self.sign = "neg"

    def __import_header__(self,file):
        with open(file) as f:
            while True: 
                key = f.readline()
                item = f.readline()

                if key[0] == '#':
                    key = key.strip('#').strip()
                    item = item.strip('#').strip()
                    if 'pressure' in key:
                        item = float(item)
                    self.parameter_dict[key]=item
                else:
                    break

class rescaled_segment():
    def __init__(self,data,params):
        self.time_data = data[0]
        self.x_data = data[1]
        self.parameter_dict = params
        self.t0 = self.time_data[0]
        self.L0 = self.x_data[0]
        self.max_extent = max(self.time_data)
        self.pressure = self.parameter_dict["pressure"]
        if self.parameter_dict["delta pressure"] > 0:
            self.sign = "pos"
        else:
            self.sign = "neg"