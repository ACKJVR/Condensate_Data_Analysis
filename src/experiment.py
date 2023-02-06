import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import natsort
from src import exp_segment
from scipy import stats
import copy

class experiment():
    def __init__(self,dir): 
        seg_files = [file for file in dir.iterdir()]
        seg_files = natsort.natsorted(seg_files)
        self.seg_num = len(seg_files)

        self.data_dict = {"pos":[],"neg":[]}

        for file in seg_files:
            seg = exp_segment.experimental_segment(file)
            self.data_dict[seg.sign].append(seg)
        
        if self.data_dict["pos"]:
            self.parameters = copy.deepcopy(self.data_dict["pos"][0].parameter_dict)
        else:
             self.parameters = copy.deepcopy(self.data_dict["neg"][0].parameter_dict)

        self.parameters.pop("pressure")
        self.parameters.pop("delta pressure")

        self.model_dict = {}
        self.color_dict = {}

    
    def fit_model(self,Model):
        self.model = Model
        for key,value in self.data_dict.items():
            self.model_dict[key] = [self.model(data) for data in value]
        for key,value in self.model_dict.items():
            for seg_model in value:
                seg_model.fit()
    
    def plot_experiment(self,include_model=True,exp_direction="pos"):
        _,ax = plt.subplots()
        if not self.color_dict:
            self.define_colors()
        if exp_direction == "pos" or exp_direction == "all":
            self.__scatter_plot__("pos",ax,self.data_dict["pos"])
            if include_model:
                self.__model_plot__("pos",ax)

        if exp_direction == "neg" or exp_direction == "all":
            self.__scatter_plot__("neg",ax,self.data_dict["neg"])
            if include_model:
                self.__model_plot__("neg",ax)
        plt.show()

    def define_colors(self):
        for key in self.data_dict.keys():
            self.color_dict[key] = mpl.cm.plasma(np.linspace(0, 1, len(self.data_dict[key])))
    
    def __scatter_plot__(self,key,ax,data):
        colors = self.color_dict[key]
        for (segment,color) in zip(data,colors):
            ax.scatter(segment.time_data-segment.t0,segment.x_data-segment.L0,facecolors='none',edgecolor=color)
    
    def __model_plot__(self,key,ax):
        colors = self.color_dict[key]
        if not self.model_dict:
            return 0
        for seg_model,color in zip(self.model_dict[key],colors):
            ax.plot(seg_model.seg.time_data-seg_model.t0,seg_model.model(seg_model.seg.time_data,*seg_model.params)-seg_model.L0,c=color)

    def fit_pressures(self,plot=False):
        pressures = []
        fit_parameter = []
        for set in self.model_dict.values():
            for mod in set:
                fit_vals = mod.return_values()
                fit_parameter.append(fit_vals["A"])
                pressures.append(mod.pressure)
        
        pressures = np.array(pressures)
        fit_parameter = np.array(fit_parameter).flatten()

        self.pressure_result = stats.linregress(pressures,fit_parameter)

        if plot:
            _,ax = plt.subplots()
            ax.scatter(pressures,fit_parameter,facecolors='none',edgecolor='k')
            ax.plot(pressures,self.pressure_result.slope*pressures + self.pressure_result.intercept)
            plt.show()

    def rescale_data(self,plot=False):
        self.rescaled_segs = {}
        for key,value in self.model_dict.items():
            self.rescaled_segs[key] = [mod.rescale_data() for mod in value]

        if plot:
            if not self.color_dict:
                self.define_colors()
            
            _,ax = plt.subplots()
            for key in self.rescaled_segs.keys():
                self.__scatter_plot__(key,ax,self.rescaled_segs[key])

            plt.show()
