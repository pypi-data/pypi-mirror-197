import  numpy  as np  
import pandas  as  pd 
import  matplotlib.pyplot as plt 
from  scipy  import  stats
import  pylab

def log_transformation(feature:pd.Series)->pd.Series:
    '''
    this  function is used to transform the data into logarthimic data
    Args:[feature(pd.Series)]
    '''
    return np.log(feature)


def recip_transformation(feature:pd.Series)->pd.Series:
    '''
    this  function is used to transform the data into Reciprocal data
    Args:[feature(pd.Series)]
    '''
    return 1/feature

def sqrt_transformation(feature:pd.Series)->pd.Series:
    '''
    this  function is used to transform the data into square rooted data
    Args:[feature(pd.Series)]
    '''
    return np.sqrt(feature)

def expo_transformation(feature:pd.Series)->pd.Series:
    '''
    this  function is used to transform the data into exponential data
    Args:[feature(pd.Series)]
    '''
    return feature**(1/1.2)


def plot_data(feature:pd.Series):
    '''
    This function plots the histogram and  probplot(best fit line) for the given data
    Args:[feature(pd.Series)]
    '''
    plt.figure(figsize=(10,6))
    plt.subplot(2,2,1)
    feature.hist()
    plt.subplot(2,2,2)
    stats.probplot(feature,dist='norm',plot=pylab)
    plt.show()


def probplot_transform(feature:pd.Series,trans_method:str='default'):
    '''
    This function used to interpret whether the given data follows normal distribution by using histogram and probplot. if the data not follows normal distribution then with the help of the trans_method param it can transform the data using Box-Cox,Logarithmic,Reciprocal,Square Root,Exponential Transformation.

    Args:[feature(pd.Series),trans_method('default','log','box_cox','recip','sqrt','expo')]
    '''
    try:
        if trans_method=="default":

            plot_data(feature)
            return feature
        
        elif trans_method=="log":
            feature=log_transformation(feature)
            plot_data(feature)
            return feature
        
        elif trans_method=="box_cox":
            feature1,param=stats.boxcox(feature)
            feature1=pd.Series(feature1)
            plot_data(feature1)
            return feature1
        
        elif trans_method=="recip":
            feature=recip_transformation(feature)
            plot_data(feature)
            return feature
        
        elif trans_method=="sqrt":
            feature=sqrt_transformation(feature)
            plot_data(feature)
            return feature
        
        elif trans_method=="expo":
            feature=expo_transformation(feature)
            plot_data(feature)
            return feature
        else:
            print("provide correct trans_method values['default','log','box_cox','recip','sqrt','expo'] ")
    except Exception as e:
        print(e)



