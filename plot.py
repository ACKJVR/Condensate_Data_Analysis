from pathlib import Path
from src import model
from src import experiment
from src import experiment_plotter

data_path = Path("data_files")
uncoated_files = ["fig_3b","fig_2c","oil_1","oil_2"]
uncoated_experiments = []
for file in uncoated_files:
    new_experiment = experiment.experiment(data_path/file)
    new_experiment.fit_model(model.wetting_model)
    uncoated_experiments.append(new_experiment)

export_dir = Path("figures")
Path.mkdir(export_dir,exist_ok=True)
for exp in uncoated_experiments:
    plotter = experiment_plotter.experiment_plotter(exp)
    plotter.full_plot(export=True,path=export_dir,display=False)