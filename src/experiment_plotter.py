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
        plt.subplots_adjust(wspace=.4)
        plt.show=()

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
            for (seg, mod) in zip(self.experiment.data_dict[key],self.experiment.model_dict[key]):


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

newPlot = experiment_plotter(fig3b)
newPlot.full_plot()
        
    


