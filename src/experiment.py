import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
import natsort
from src import exp_segment


class experiment():
    def __init__(self,dir): 
        seg_files = [file for file in dir.iterdir()]
        seg_files = natsort.natsorted(seg_files)

        self.data_dict = {"pos":[],"neg":[]}

        for file in seg_files:
            seg = exp_segment.experimental_segment(file)
            self.data_dict[seg.sign].append(seg)
        
        if self.data_dict["pos"]:
            self.parameters = self.data_dict["pos"][0].parameter_dict
        else:
             self.parameters = self.data_dict["neg"][0].parameter_dict

        self.parameters.pop("pressure")
        self.parameters.pop("delta pressure")

        self.model_dict = {}

    
    def fit_model(self,Model):
        self.model = Model
        for key,value in self.data_dict.items():
            self.model_dict[key] = [self.model(data) for data in value]
        for key,value in self.model_dict.items():
            for seg_model in value:
                seg_model.fit()
    
    def plot_experiment(self,include_model=True,exp_direction="pos"):
        fig,ax = plt.subplots()
        self.color_dict = {}
        for key in self.data_dict.keys():
            self.color_dict[key] = mpl.cm.plasma(np.linspace(0, 1, len(self.data_dict[key])))

        if exp_direction == "pos" or exp_direction == "all":
            self.__scatter_plot__("pos",ax)
            if include_model:
                self.__model_plot__("pos",ax,)

        if exp_direction == "neg" or exp_direction == "all":
            self.__scatter_plot__("neg",ax)
            if include_model:
                self.__model_plot__("neg",ax,)
        plt.show()
    
    def __scatter_plot__(self,key,ax):
        colors = self.color_dict[key]
        for (segment,color) in zip(self.data_dict[key],colors):
            ax.scatter(segment.time_data-segment.t0,segment.x_data-segment.L0,facecolors='none',edgecolor=color)
            # ax.scatter(segment.time_data,segment.x_data)

    
    def __model_plot__(self,key,ax):
        colors = self.color_dict[key]
        if not self.model_dict:
            return 0
        for seg_model,color in zip(self.model_dict[key],colors):
            ax.plot(seg_model.seg.time_data-seg_model.t0,seg_model.model(seg_model.seg.time_data,*seg_model.params)-seg_model.L0,c=color)