import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np

class experiment_plotter():
    def __init__(self,exp):
        self.experiment = exp
        self.trajectory = np.genfromtxt(self.experiment.dir/"trajectory.dat",delimiter=',')
        self.pressure_data = np.genfromtxt(self.experiment.dir/"pressure.dat",delimiter=',')
        if not self.experiment.pressure_result:
            self.experiment.fit_pressures()

    def full_plot(self):
        fig,axs = plt.subplots(2,2,figsize=(10,7))
        self.full_experiment_plot(axs[0,0])
        self.data_with_model_plot(axs[0,1])
        self.pressure_fit_plot(axs[1,0])
        self.rescaled_plot(axs[1,1])
        plt.subplots_adjust(wspace=.4)
        plt.show=()

    def rescaled_plot(self,ax=False):
        ax, display = self.set_display(ax)
        max_extent = []
        for key in self.rescaled_segs.keys():
            for segment in self.rescaled_segs[key]:
                color = self.pressure_to_color(segment.pressure)
                color2 = list(color)
                color2[3] = .2
                color2 = tuple(color2)
                ax.scatter(segment.time_data-segment.t0,segment.x_data,facecolors=color2,marker='o',edgecolor='none',s=15)
                max_extent.append(segment.max_extent)
        
        max_extent = max(max_extent)
        ax.set_xscale('log')
        ax.set_yscale('log')

        ax.plot(np.linspace(0,max_extent,100),np.linspace(0,max_extent,100)+1,'k')
        if display:
            plt.show()

    def pressure_fit_plot(self,ax=False):
        ax, display = self.set_display(ax)
        ax.scatter(self.experiment.pressures,self.experiment.fit_parameter,facecolors=self.pressure_to_color(self.experiment.pressures),edgecolor='none')
        ax.plot(self.experiment.pressures,self.experiment.pressure_result.slope*self.experiment.pressures + self.experiment.pressure_result.intercept,color='black')
        if display:
            plt.show()

    def full_experiment_plot(self,ax=False):
        ax, display = self.set_display(ax)
        
        ax2 = ax.twinx()
        ax2.plot(*self.pressure_data.T,color='0.8',linestyle='dashed',zorder=1)
        ax.plot(*self.trajectory.T,color='0.5',zorder=2)
        for key in self.experiment.data_dict.keys():
            for seg in self.experiment.data_dict[key]:
                ax.plot(seg.time_data,seg.x_data,color=self.pressure_to_color(seg.pressure),zorder=3)
        
        if display:
            plt.show()

    def data_with_model_plot(self,ax=False):
        ax, display = self.set_display(ax)
        for key in self.experiment.data_dict.keys():
            for (segment, seg_model) in zip(self.experiment.data_dict[key],self.experiment.model_dict[key]):
                color = self.pressure_to_color(segment.pressure)
                color2 = list(color)
                color2[3] = .2
                color2 = tuple(color2)
                ax.scatter(segment.time_data-segment.t0,segment.x_data-segment.L0,facecolors=color2,marker='o',edgecolor='face',s=15)
                ax.plot(seg_model.seg.time_data-seg_model.t0,seg_model.model(seg_model.seg.time_data,*seg_model.params)-seg_model.L0,c=color)

        if display:
            plt.show()

    def set_display(self,ax):
        if not ax:
            display = True
            _,ax = plt.subplots(figsize=(7,5))
        else: 
            display = False

        return ax, display 

    def pressure_to_color(self,pressure):
        interp_pressure = np.interp(pressure,(self.experiment.pressures.min(),self.experiment.pressures.max()),(0,1))
        return mpl.cm.plasma(interp_pressure)
        
    


