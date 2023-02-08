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
        if not self.experiment.rescaled_segs:
            self.experiment.rescale_data()
        
        self.pressure_extremes = (self.experiment.pressures.min(),self.experiment.pressures.max())
        self.color_map = mpl.cm.plasma
        self.label_coords = [0.07,0.92]
        self.legend_font_size = 12

    def full_plot(self,export=False,display=True,path=''):
        fig,axs = plt.subplots(2,2,figsize=(11,7))
        self.full_experiment_plot(axs[0,0])
        self.data_with_model_plot(axs[0,1])
        self.pressure_fit_plot(axs[1,0])
        self.rescaled_plot(axs[1,1])
        fig.subplots_adjust(wspace=.7,hspace=.3)
        self.pressure_colorbar(fig)
        if export:
            if path:
                file_name = self.experiment.dir.stem+'_full_plot.png'
                plt.savefig(path/file_name,bbox_inches='tight')
            else:
                print('No path given')
        if display:
            plt.show=() 
        else:
            plt.close()

    def pressure_colorbar(self,fig):
        fig.subplots_adjust(right=0.9)
        cbar_ax = fig.add_axes([0.95, 0.15, 0.02, 0.7])
        norm = mpl.colors.Normalize(vmin=self.pressure_extremes[0], vmax=self.pressure_extremes[1])
        fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=self.color_map),cax=cbar_ax, orientation='vertical', label='$\displaystyle \Delta$ Pressure (Pa)',aspect=40)

    def rescaled_plot(self,ax=False):
        fig, ax, display = self.set_display(ax)
        max_extent = []
        for key in self.experiment.rescaled_segs.keys():
            for segment in self.experiment.rescaled_segs[key]:
                color = self.pressure_to_color(segment.pressure)
                color2 = list(color)
                color2[3] = .8
                color2 = tuple(color2)
                ax.scatter(segment.time_data-segment.t0,segment.x_data-segment.L0,facecolors=color2,marker='o',edgecolor='none',s=15)
                max_extent.append(segment.max_extent)
        
        max_extent = max(max_extent)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('$\displaystyle \\left| \\frac{\Delta P-P_\\gamma}{8 \mu} (t-t_0) \\right|$')
        ax.set_ylabel('$\displaystyle \\left| \\left(\\frac{L_p(t)}{L_0}\\right)^2 - 1 \\right|$')

        ax.plot(np.linspace(0,max_extent,100),np.linspace(0,max_extent,100),'k')
        legend_elements = [mpl.lines.Line2D([0], [0], color='k', lw=2, label='$\displaystyle y=x$'),
                   mpl.lines.Line2D([0], [0], marker='o', lw=0, label='Data',
                          markerfacecolor='grey', markersize=7,markeredgecolor='none')]
        ax.legend(handles=legend_elements, prop={'size': self.legend_font_size},loc=4,frameon=False)
        if display:
            self.pressure_colorbar(fig)
            plt.show()
        else:
            plt.text(*self.label_coords, '(d)', horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,bbox=dict(boxstyle="square",facecolor='white'))


    def pressure_fit_plot(self,ax=False):
        fig, ax, display = self.set_display(ax)
        ax.scatter(self.experiment.pressures,self.experiment.fit_parameter,facecolors=self.pressure_to_color(self.experiment.pressures),edgecolor='none')
        ax.plot(self.experiment.pressures,self.experiment.pressure_result.slope*self.experiment.pressures + self.experiment.pressure_result.intercept,color='black')
        ax.set_xlabel('$\Delta P$')
        ax.set_ylabel('$\\frac{1}{8\\mu}(\Delta P - P_\\gamma) $')
        legend_elements = [mpl.lines.Line2D([0], [0], color='k', lw=2, label='Best Fit'),
                   mpl.lines.Line2D([0], [0], marker='o', lw=0, label='Model Coefficient',
                          markerfacecolor='grey', markersize=7,markeredgecolor='none')]
        ax.legend(handles=legend_elements, prop={'size': self.legend_font_size},loc=4,frameon=False)
        if display:
            self.pressure_colorbar(fig)
            plt.show()
        else:
            plt.text(*self.label_coords, '(c)', horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)


    def full_experiment_plot(self,ax=False):
        fig, ax, display = self.set_display(ax)
        
        ax2 = ax.twinx()
        line2, = ax2.plot(*self.pressure_data.T,color='0.7',linestyle='dashed',zorder=1)
        line1, = ax.plot(*self.trajectory.T,color='0.5',zorder=2)
        for key in self.experiment.data_dict.keys():
            for seg in self.experiment.data_dict[key]:
                ax.plot(seg.time_data,seg.x_data,color=self.pressure_to_color(seg.pressure),zorder=3)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('$\displaystyle L_p(t)/R_p$')
        ax2.set_ylabel('Pressure (Pa)')
        ax.legend([line1,line2],['$\\displaystyle L_p(t)$','Pressure'],prop={'size': self.legend_font_size},loc=3,frameon=True)
        
        if display:
            self.pressure_colorbar(fig)
            plt.show()
        else:
            plt.text(*self.label_coords, '(a)', horizontalalignment='center',verticalalignment='center', transform=ax.transAxes,bbox=dict(boxstyle="square",facecolor='white',edgecolor='none'))


    def data_with_model_plot(self,ax=False):
        fig,ax,display = self.set_display(ax)
        for key in self.experiment.data_dict.keys():
            for (segment, seg_model) in zip(self.experiment.data_dict[key],self.experiment.model_dict[key]):
                color = self.pressure_to_color(segment.pressure)
                color2 = list(color)
                color2[3] = .2
                color2 = tuple(color2)
                ax.scatter(segment.time_data-segment.t0,segment.x_data-segment.L0,facecolors=color2,marker='o',edgecolor='none',s=15)
                ax.plot(seg_model.seg.time_data-seg_model.t0,seg_model.model(seg_model.seg.time_data,*seg_model.params)-seg_model.L0,c=color)
        
        ax.set_xlabel('$\\displaystyle t-t_0$')
        ax.set_ylabel('$\\displaystyle \\frac{L_p(t)-L_0}{R_p}$')
        legend_elements = [mpl.lines.Line2D([0], [0], color='k', lw=2, label='Fitted Model'),
                   mpl.lines.Line2D([0], [0], marker='o', lw=0, label='Data',
                          markerfacecolor='grey', markersize=7,markeredgecolor='none')]
        ax.legend(handles=legend_elements, prop={'size': self.legend_font_size},loc=7,frameon=False)
        if display:
            self.pressure_colorbar(fig)
            plt.show()
        else:
            plt.text(*self.label_coords, '(b)', horizontalalignment='center',verticalalignment='center', transform=ax.transAxes)

    def set_display(self,ax):
        if not ax:
            display = True
            fig,ax = plt.subplots(figsize=(7,5))
        else: 
            display = False
            fig = False

        return fig, ax, display 

    def pressure_to_color(self,pressure):
        interp_pressure = np.interp(pressure,(self.pressure_extremes[0],self.pressure_extremes[1]),(0,1))
        return mpl.cm.plasma(interp_pressure)