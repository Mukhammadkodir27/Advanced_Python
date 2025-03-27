# -*- coding: utf-8 -*-
"""
# Advanced Econometrics
# Spring semester
# Lab 05: Count data Models
# Rafal Wozniak
# The code partially uses codes from the textbook by
# Florian Heiss, Daniel Brunner,
# Using Python for Introductory Econometrics
"""

# packages
import math as math
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm


# working directory
import os as os
os.getcwd()
os.chdir('C:\\Users\\Hp\\WNE\\Advanced_Econometrics\\AE_Lab_06')
os.getcwd()

# read the data
dt = pd.read_csv("DebTrivedi.csv")

# dependent variable:
#   ofp - the number of physician office visits as the dependent variable 
# 
# independent vars:
#   hosp - number of hospital stays, 
#   health - self-perceived health status, 
#   numchron - number of chronic conditions, 
#   gender, 
#   school - number of years of education 
#   privins - private insurance indicator


# Poisson regression
reg_poisson = smf.poisson(formula='ofp ~ hosp + health + numchron +'
                          'gender + school + privins',
                          data = dt)
results_poisson = reg_poisson.fit(disp=0)
print(results_poisson.summary())

# Negative Binomial regression
# NB1 for overdispersion and underdispersion
# Variance equal to E[Y]+alpha*E[Y]
from statsmodels.discrete.discrete_model import NegativeBinomial

endog = dt["ofp"]
exog_vars = ["hosp", "numchron"]
exog = sm.add_constant(dt[exog_vars])

reg_nb1 = NegativeBinomial(endog, exog, loglike_method='nb1')
results_nb1 = reg_nb1.fit()
print(results_nb1.summary())

# Negative Binomial regression
# NB2 for overdispersion only
# Variance equal to E[Y]+alpha*E[Y]^2

endog = dt["ofp"]
exog_vars = ["hosp", "numchron"]
exog = sm.add_constant(dt[exog_vars])

reg_nb1 = NegativeBinomial(endog, exog, loglike_method='nb2')
results_nb1 = reg_nb1.fit()
print(results_nb1.summary())

# Zero Inflated Poisson regression model
from statsmodels.discrete.count_model import ZeroInflatedPoisson

endog = dt["ofp"].astype(float)
exog_vars = ["hosp", "numchron"]
exog = sm.add_constant(dt[exog_vars])
exog_infl = exog

reg_zip = ZeroInflatedPoisson(endog, exog, exog_infl)
results_zip = reg_zip.fit()
print(results_zip.summary())

# Hurdle Poisson for zero-inflation
from statsmodels.discrete.truncated_model import HurdleCountModel

endog = dt["ofp"].astype(float)
exog_vars = ["hosp", "numchron"]
exog = sm.add_constant(dt[exog_vars])

reg_hurdle = HurdleCountModel(endog, exog, dist='poisson', zerodist='poisson')
results_hurdle = reg_hurdle.fit()
print(results_hurdle.summary())


