import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt # data visualization
import seaborn as sns # statistical data visualization
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.model_selection import train_test_split
import math
from scipy.spatial.distance import jensenshannon


def set_image_size(fig_size = (20,15), font_scale = 3):
  sns.set(font_scale = font_scale)
  plt.rcParams["figure.figsize"] = (20,15)
  plt.rcParams['legend.fontsize'] = 'x-large'

def max_print_out(pattern=True):
    '''It will maximize print out line and set float format with .2f'''
    set_image_size()
    number = None if pattern else 10
    # Set options to avoid truncation when displaying a dataframe
    pd.set_option("display.max_rows", number)
    pd.set_option("display.max_columns", 150)
    # Set floating point numbers to be displayed with 2 decimal places
    pd.set_option('display.float_format', '{:.2f}'.format)
    # for showing all entities 

def histogram_plot_summary(entropy_report):
    sns.histplot(data=entropy_report, x = 'entropy', kde=True, hue='dataset', alpha=0.7, bins=20)
    plt.title("Entropy histogram of all three datasets", fontsize = 40)
    plt.savefig("histogram_plot_summary.png")

def boxplot_summary(entropy_report):
    sns.boxplot(data=entropy_report, y="entropy", x='dataset')
    plt.title("Boxplot of all three datasets",  fontsize = 40)
    plt.xlabel('Dataset', fontsize = 40)
    plt.ylabel('Entropy', fontsize = 40)
    plt.savefig("boxplot_summary.png")

def violin_plot_summary(entropy_report):
    sns.violinplot(data=entropy_report, y="entropy", x='dataset')
    plt.title("Violin plot of all three datasets",  fontsize = 40)
    plt.xlabel('Dataset', fontsize = 40)
    plt.ylabel('Entropy', fontsize = 40)
    plt.savefig("violin_plot_summary.png")

def historgram_plot_facetgrid(entropy_report):
    g = sns.FacetGrid(entropy_report, col="Diagnosis", col_wrap=5, sharey=False ,  sharex=False, hue = 'dataset')
    # Map histogram plot to "total_bill" column
    g.map(sns.histplot, "entropy", kde = True)
    g.set_titles(col_template="{col_name}")
    g.set_ylabels("Entropy")
    g.fig.set_size_inches(60, 60)
    g.tight_layout()
    g.add_legend()
    # Set title and legends
    plt.savefig("historgram_plot_facetgrid.png")

def boxplot_facetgrid(entropy_report):
    g = sns.FacetGrid(entropy_report,  col="Diagnosis", col_wrap=4, sharey=False ,  sharex=False)
    # Map histogram plot to "total_bill" column
    g.map(sns.boxplot, "dataset", "entropy",  palette="Set1")
    g.fig.set_size_inches(60, 60)
    g.set_titles(col_template="{col_name}")
    g.set_ylabels("Entropy")
    g.fig.set_size_inches(60, 60)
    g.tight_layout()
    g.add_legend()
    plt.savefig("boxplot_facetgrid.png")

def violinplot_facetgrid(entropy_report):
    g = sns.FacetGrid(entropy_report,  col="Diagnosis", col_wrap=4, sharey=False ,  sharex=False)
    # Map histogram plot to "total_bill" column
    g.map(sns.violinplot, "dataset", "entropy",  palette="Set1")
    g.fig.set_size_inches(60, 60)
    g.set_titles(col_template="{col_name}")
    g.set_ylabels("Entropy")
    g.fig.set_size_inches(60, 60)
    g.tight_layout()
    g.add_legend()
    plt.savefig("violinplot_facetgrid.png")


def entropy_plot(entropy_report, type_report = 'summary', type_plot = 'histogram'):
  if type_report == 'summary':
    if type_plot == 'histogram':
      histogram_plot_summary(entropy_report)
    elif type_plot == 'boxplot':
       boxplot_summary(entropy_report)
    elif type_plot == 'violinplopt':
      violin_plot_summary(entropy_report)
    else:
      print("Wrong input type")
  elif type_report == 'facetgrid':
    if type_plot == 'histogram':
      historgram_plot_facetgrid(entropy_report)
    elif type_plot == 'boxplot':
       boxplot_facetgrid(entropy_report)
    elif type_plot == 'violinplot':
      violinplot_facetgrid(entropy_report)
    else:
      print("Wrong input")    

