
import pandas as pd
import numpy as np
from scipy.stats import levene, shapiro
from statsmodels.multivariate.manova import MANOVA

data = pd.read_excel('C:\data\saengjunsil_data.xlsx', sheet_name = 'CHH', engine = 'openpyxl')

# 독립변인과 종속변인을 나눕니다.
independent_vars = data[['growth', 'ecotype']]
dependent_vars = data[['CHH', 'CG', 'CHG']]

# 등분산성 검증
levene_test = levene(dependent_vars['줄넘기 횟수'], dependent_vars['악력'], dependent_vars['오래달리기 횟수'])
print('Levene test: ', levene_test)

# 정규성 검증
shapiro_test1 = shapiro(dependent_vars['줄넘기 횟수'])
shapiro_test2 = shapiro(dependent_vars['악력'])
shapiro_test3 = shapiro(dependent_vars['오래달리기 횟수'])
print('Shapiro test (줄넘기): ', shapiro_test1)
print('Shapiro test (악력): ', shapiro_test2)
print('Shapiro test (오래달리기): ', shapiro_test3)

# MANOVA 분석
maov = MANOVA(dependent_vars, independent_vars)
print(maov.mv_test())
