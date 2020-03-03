#Exploratory Data Analysis: Graphical Summaries

##Plotting/Constructing Histograms:

Given a data set consisting of n data points: x_1, x_2, ..., x_n

1st) Divide the range of my data set into intervals intervals B_1, B_2, ..., B_m. These intervals are 
called "bins".

The length of an i^th interval, B_i, is called the "bin width" of the i^th bin and is denoted by abs(B_i).

2) The area of a an i^th bin is equal to the number of data points with values which fall within this i^th bins interval divide by the total
number of data points in my data set which is n.

3) The height of a an i_th bin is then equal to the area of the i^th bin, A_i, divided by this i^th bins width, abs(B_i). So H_i = A_i/abs(B_i)

##Plotting/Constructing an Empirical Cumulative Distribution Function, F_n(x):

The Empirical Cumulative Distribution Function, ECDF, is denoted by F_n and is defined @ a certain (data)
point x as the proportion of data points in my dataset which have a value equal to or less than the value
of x (so the ECDF of a dataset containing n # of data points for a specific data point x 
is denoted by F_x(x)).


#Exploratory Data Analysis: Numerical Summaries

##The centre of a dataset:

The best known method for identifying the centre of a dataset is via the calculation of the sample mean 
my dataset:

x^bar_n = (x_1 + x_2 + ... + x_n ) / n

A 2nd method for identifying the centre of a dataset is by determining the sample median of my dataset. The 
sample median of a dataset is denoted by Med(x_1, x_2, ..., x_n) or simply by Med_n.

In order to determine the Med_n of a dataset I must first arrange all my data points in an ascending order
of values. The Med_n of my dataset is then the data point in the middle of this ascending order of data point
values.
















































