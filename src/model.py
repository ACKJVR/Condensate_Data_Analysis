import numpy as np
from matplotlib import pyplot as plt
import scipy.optimize as spo
from abc import ABC
from src import exp_segment

# Define abstract base class for all models
class Model(ABC):
    # Pass the model class the pressure, initial time, and initial length upon construction
    def __init__(self,seg):
        self.pressure = seg.pressure
        self.t0 = seg.t0
        self.L0 = seg.L0
        self.seg = seg
        self.params = False

    def fit(self):
        self.define_bounds()
        (self.params, self.covar) = spo.curve_fit(self.model,self.seg.time_data,self.seg.x_data,bounds=self.bound)
        
    def error(self,k,time,data):
        return np.sum((data-self.model(time,k))**2)
        
    def model(self):
        pass

    def plot(self):
        if not self.params:
            self.fit()
        
        _,ax = plt.subplots()
        ax.scatter(self.seg.time_data,self.seg.x_data)
        ax.plot(self.seg.time_data,self.model(self.seg.time_data,*self.params),'r')
        plt.show()
    
    def define_bounds(self):
        self.bound = (-np.inf,np.inf)

    def return_values(self):
        pass

    def rescale_data(self):
        if not self.params:
            self.fit()

class wetting_model(Model):
    def model(self,t,A):
        return np.sqrt(A*(t-self.t0) + np.power(self.L0,2))
        
    def define_bounds(self):
        if self.seg.sign=="pos":
            self.bound = (0,np.inf)
        elif self.seg.sign=="neg":
            self.bound = (-np.inf,0)

    def return_values(self):
        if not self.params:
            self.fit()
        return {"A":self.params}
    
    def rescale_data(self):
        super().rescale_data()
        length_data = self.seg.x_data
        time_data = self.seg.x_data
        length_data = length_data**2 - self.L0**2
        time_data = self.params*(time_data-self.t0)
        return exp_segment.rescaled_segment((time_data,length_data),self.seg.parameter_dict)



class wetting_model_modified(Model):
    def model(self,t,A,C):
        return np.sqrt(A*(t-self.t0) + np.power(self.L0,2)) + C