from pybrain.optimization import *
import numpy as np
import math
from xlrd import open_workbook

def m1(weights) :
    return p_mean(weights)

def m2(weights) :
    return p_variance(weights) + m1(weights)**2

def m3(weights):
    summ = 0.
    for i in range(0, len(weights)) :
        for j in range(0, len(weights)) :
            for k in range(0, len(weights)) :
                summ += weights[i] * weights[j] * weights[k] * skewness(i, j, k)
    return summ

def m4(weights):
    summ = 0.
    for i in range(0, len(weights)) :
        for j in range(0, len(weights)) :
            for k in range(0, len(weights)) :
                for l in range(0, len(weights)) :
                    summ += weights[i] * weights[j] * weights[k] * weights[l] * kurtosis(i, j, k, l)
    return summ

def mean(data) :
    n    = 0
    summ = 0.
    for x in data:
        n    = n + 1
        summ = summ + x
    mean = summ / n
    return mean

def p_mean(weights) :
    res = 0.
    for i in range(0, len(datas)) :
        res += mean(datas[i]) * weights[i]

    return res

def variance(data, mean):
    sum1 = 0.
    sum2 = 0.
    n = len(data) - 1
    for x in data:
        sum1 = sum1 + (x - mean)**2
        sum2 = sum2 + (x - mean)
    variance = (sum2 - sum3**2 / n) / n
    return variance

def covvar(data1, data2):
    return np.cov(data1, data2)

def p_variance(weights) :
    summ = 0.
    for i in range(0, len(datas)) :
        for j in range(0, len(datas)) :
            summ += weights[i] * weights[j] * covvar(datas[i], datas[j])[0][1]
    return summ

def skewness(i, j, k) :
    summ = 0.
    for t in range(0, len(datas[i]) - 1) :
        summ += datas[i][t] * datas[j][t] * datas[k][t]
    summ = summ / (len(datas[i]) - 1)
    return summ

def p_skewness(weights) :
    return m3(weights) - 3. * m2(weights) * m1(weights) + 2. * m1(weights)**3

def kurtosis(i, j, k, l) :
    summ = 0.
    for t in range(0, len(datas[i]) - 1) :
        summ += datas[i][t] * datas[j][t] * datas[k][t] * datas[l][t]
    summ = summ / (len(datas[i]) - 1)
    return summ

def p_kurtosis(weights) :
    res = m4(weights) - 4. * m3(weights) * m1(weights) + 6. * m2(weights) * (m1(weights))**2 - 3. * (m1(weights))**4
    return res

def log_one_plus_mean(weights) :
    return math.log10(1. + p_mean(weights))

def one_plus_mean_inPow(pow, weights) :
    return (1. + p_mean(weights))**pow;

def EU(weights) :
    summ = 0.
    for weight in weights :
        if weight < 0 or weight > 1 :
            return -1
        summ += weight

    if summ <= 1. and summ > 0. :
        return log_one_plus_mean(weights) - p_variance(weights) / (2 * one_plus_mean_inPow(2, weights)) + p_skewness(weights) / (3 * one_plus_mean_inPow(3, weights)) - p_kurtosis(weights) / 4 * one_plus_mean_inPow(4, weights)
        #return log_one_plus_mean(w) - p_variance(w) / (2 * one_plus_mean_inPow(2, w)) + p_skewness(w) / (3 * one_plus_mean_inPow(3, w)) - p_kurtosis(w) / 4 * one_plus_mean_inPow(4, w)
    else :
        return -1


datas = []
book = open_workbook('/home/mmaxy/odd.xls')
sheet = book.sheet_by_index(0)
for col_index in range(1, 4):
    data = []
    for row_index in range(2, sheet.nrows):
        data.append(sheet.cell(row_index,2*(col_index)).value)
    datas.append(data)

w1 = 0.
w2 = 0.
w3 = 1. - w1 - w2
weights = [w1, w2, w3]
bestEU = EU(weights)
print "bestEU = " + str(bestEU)
print "weights" + str(weights)
for weight1 in range(101) :
    for weight2 in range(101 - weight1) :
        w1 = weight1 / 100.
        #print "w1 = " + str(w1)
        w2 = weight2 / 100.
        #print "w2 = " + str(w2)
        w3 = 1. - w1 - w2
        #print "w3 = " + str(w3)
        w = [w1, w2, w3]
        res = EU(w)
        if res > bestEU :
            bestEU = res
            weights[0] = w1
            weights[1] = w2
            weights[2] = w3
            print "bestEU = " + str(bestEU)
            print "weights" + str(weights)
print "---Solution---"
print "EU"
print bestEU
print "weights"
print weights
