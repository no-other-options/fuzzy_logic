import numpy as np

def trapezoid_mf(x_array, arg_list):
    type = len(arg_list)
    if len(arg_list) == 4:
        a, m1, m2, b = arg_list
    elif len(arg_list) == 3:
        a, m, b = arg_list
        
    if not isinstance(x_array, (int, float)):
        p = []
        for x in x_array:
            if type == 4:
                p.append(trapezoid(x, a, m1, m2, b))
            elif type == 3:
                p.append(triangular(x, a, m, b))
        return np.array(p)
    else:
        if type == 4:
            return trapezoid(x_array, a, m1, m2, b)
        elif type == 3:
            return triangular(x_array, a, m, b)

def trapezoid(x, a, m1, m2, b):
    if x >= m1 and x <= m2:
        return 1
    elif x > a and x < m1:
        return ((x - a)/(m1 - a))
    elif x < b and x > m2:
        return ((b - x)/(b - m2))
    else:
        return 0

def triangular(x, a, m, b):
    if x == m:
        return 1
    elif x > a and x < m:
        return (x - a) / (m - a)
    elif m < x and x < b:
        return (b - x) / (b - m) 
    else:
        return 0

#            ------- TRIANGLE ----------
def triangle_plot_centre(p1, p2):
    hpoint = None
    lpoint = None

    if p1[1] == 0:
        hpoint = p2
        lpoint = p1
        centroid = tria_centr(hpoint, lpoint)
        if centroid < lpoint[0]:
            centroid += lpoint[0]
    else:
        hpoint = p1
        lpoint = p2
        centroid = tria_centr(hpoint, lpoint)
        if centroid < hpoint[0]:
            centroid += hpoint[0]
            
    plot = triangular_plot(hpoint, lpoint)

    return plot, centroid
    
def triangular_plot(hpoint, lpoint):
    
    b = hpoint[1]
    a = hpoint[0] - lpoint[0]

    return a*b/2

def tria_centr(hpoint, lpoint):
    return (hpoint[0] + hpoint[0] + lpoint[0])/3
#           -----------------------------

#          -------- RECTANGLE -----------
def rect_plot_centre(p1, p2):
    plot = rect_plot(p1, p2)
    centroid = rect_centr(p1, p2)

    return plot, centroid

def rect_plot(p1, p2):
    return abs(p1[0]-p2[0])*p1[1]

def rect_centr(p1, p2):
    return (p1[0] + p2[0])/2
#          --------------------------------

#          -------- TRAPEZOID ------------
def trap_plot_centre(p1, p2):
    h = abs(p1[0] - p2[0])
    plot = trap_plot(p1, p2, h) 

    if p1[1] > p2[1]:
        a = p2[1]
        b = p1[1]
        centroid = trap_centr(a, b, h)
        if centroid < p2[0]:
            centroid += p2[0]  
    else:
        a = p1[1]
        b = p2[1]
        centroid = trap_centr(a, b, h)
        if centroid < p1[0]:
            centroid += p1[0] 

    return plot, centroid

def trap_plot(p1, p2, h):
    return ((p1[1] + p2[1])*h)/2

def trap_centr(a, b, h):
    top = h*(2*a+b)
    bottom = 3 * (a+b)
    return top/bottom
#           -----------------------------

def get_values_dict(dictionary, str_list):
    keyword, value = str_list
    return dictionary[keyword][value]

    # TO DO
    # - Write a function for a triangular membership function

