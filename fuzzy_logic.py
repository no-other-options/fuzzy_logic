from fuzzy_variable import FuzzyVariable
from fuzzy_rules import Rule
import numpy as np 
import utils

class FuzzyLogic:
    def __init__(self, variables, output):
        self.input_variables = variables
        self.output_variable = output

    def calculate_suitability(self, values):
        mds = self.fuzzification(values)
        return self.defuzzification(mds)
        
    def fuzzification(self, values):
        result = dict()
        for i in range(len(self.input_variables)):
            result[self.input_variables[i].var_name] = self.input_variables[i].get_membership_values(values[i])
        return result 

    def defuzzification(self, values):
        rules = Rule()
        
        # 1. Getting degrees of membership for each category
        values = rules.calculate(values)

        # 2. Making new functions that define shapes of each category 
        #    membership degree being the max value of y
        print(values)
        new_funcs = self.new_values(self.output_variable, values)
        self.som_mom(self.output_variable, values)
        new_funcs.modify_categories_md(values, self.output_variable)
        new_funcs.plot_categories(save=True)
        # 3. Calculating overlapping points
        _, intersect_points = self.find_intersections(new_funcs)

        # 4. Joining all xs and calculating max y values at each point
        points = self.calculate_joint_points(self.get_x_points(new_funcs, intersect_points), new_funcs)
        #new_funcs.plot_categories(save=True, points=points)
        
        # 5. Filtering all points to keep the  
        filtered_points = self.filter_points(new_funcs, points, values)
        print(f'Points after filtering: {filtered_points}')

        plots, centroids = self.calculate_plots_centroids(new_funcs, filtered_points)
        print(plots)
        print(centroids)
        
        return self.cog(plots, centroids)

    def find_max_values(self, fvar, values, eps = 1e-2):
        fvar_cats = fvar.get_categories()
        keys = list(fvar_cats.keys())
        rez = dict()
        for key in keys:
            ind = [i for i in range(len(fvar_cats[key])) if abs(fvar_cats[key][i]-values[key]) <= eps]
            xlist = np.array(fvar.x_bounds)
            xlist = xlist[ind]
            if np.abs(values[key] - 1) <= eps:
                rez[key] = list(xlist)
                pass
            else:
                b = np.min(xlist)
                c = np.max(xlist)
                rez[key] = [b,c]
        return rez

    def new_values(self, fvar, values):
        x_md = self.find_max_values(fvar, values) # finds x points where membership function reaches the degree of membership
        cbounds_org = fvar.cat_bounds
        cbounds_new = []
        for i in range(fvar.cat_num):
            bound = cbounds_org[i]
            x0 = bound[0]
            x1 = bound[len(bound)-1]
            new_points = x_md[fvar.cat_names[i]]
            if len(new_points) == 1:
                x_mid = x_md[fvar.cat_names[i]][0]
                cbounds_new.append([x0, x_mid, x1])
            else:
                cbounds_new.append([x0, new_points[0], new_points[1], x1])
            
        modified_suit = FuzzyVariable('New Fuzzy Functions', fvar.x_bounds, fvar.cat_num, list(fvar.get_categories().keys()), cbounds_new)

        return modified_suit
    
    def find_intersections(self, fvar):

        intersection_points = dict()
        categories = fvar.get_categories()
        cnames = fvar.cat_names
        all_points = []
        
        for i in range(fvar.cat_num):
            temp = []
            for j in range(fvar.cat_num):
                if cnames[i] == cnames[j]:
                    continue
                calc = dict()
                match = self.find_matching_points(fvar.x_bounds, fvar.categories[cnames[i]], fvar.x_bounds, fvar.categories[cnames[j]])
                calc['cat'] = cnames[j]
                #calc['y values'] = xy
                calc['(x y)'] = match
                temp.append(calc)
                if len(match) > 0:
                    all_points.append(match)
            intersection_points[cnames[i]] = temp
        #print('Matching points', intersection_points.values)        
        return intersection_points, sum(all_points,[])

    def find_matching_points(self, x1_list, y1_list, x2_list, y2_list):
        matching_points = []
        
        for x1, y1, x2, y2 in zip(x1_list, y1_list, x2_list, y2_list):
            if abs(x1-x2) <= 0.01 and abs(y1-y2) <= 0.01 and y1 > 0 and y2 > 0:
                matching_points.append((x1, y1))
        #print(f'matching points: {matching_points}')
        return matching_points

    def calculate_plots_centroids(self, fvar, points):
        categories = fvar.get_categories()
        names_cat = list(categories.keys())
        plots = []
        centroids = []
        
        for i in range(len(points)-1):
            
            p1 = points[i] # current point
            p2 = points[i+1] # next point
        
            if p1[1] == 0 and p2[1] == 0:
                continue
            
            elif p1[1] == 0 or p2[1] == 0: 
                plot, centroid = utils.triangle_plot_centre(p1, p2)
                print(f'Trikampis  = Taškai {p1}, {p2}')
                print(f'Plotas: {plot}, Centroidas: {centroid}')
                
            elif p1[1] == p2[1]:
                plot, centroid = utils.rect_plot_centre(p1, p2)
                print(f'Stačiakampis  = Taškai {p1}, {p2}')
                print(f'Plotas: {plot}, Centroidas: {centroid}')
            
            else:
                plot, centroid = utils.trap_plot_centre(p1, p2)
                print(f'Trapecija  = Taškai {p1}, {p2}')
                print(f'Plotas: {plot}, Centroidas: {centroid}')

            if plot > 0:
                plots.append(plot)
                centroids.append(centroid)
            
        return plots, centroids

    def cog(self, plots, centroids):
        product = 0
        sum = 0
        for i in range(len(plots)):
            sum += plots[i] 
            product += (plots[i] * centroids[i])
        print(sum)
        print(product)
        return product/sum

    def som_mom(self, fvar, values):
        max_key = max(values, key=lambda k: values[k])
        max_value = values[max_key]
        rez = self.find_max_values(fvar, values)
        print('SOM', min(rez[max_key]))
        print('MOM', np.mean(rez[max_key]))



    
    '''
    Joins all x's where fuzzy variables start, intersect, reach their max/membership degree.
        <param> fvar - FuzzyVariable object
        <param> matches - list of tuples holding intersection points
    Returns single list
    '''
    def get_x_points(self, fvar, matches):
        x_bounds = []
        #print(matches)
        
        for i in range(fvar.cat_num):
            #if isinstance(fvar.cat_bounds[i], str):
                #print(fvar.cat_bounds[i])
            x_bounds += fvar.cat_bounds[i]
            #print(f'step {i}: bounds: {x_bounds}')
        
        for j in matches:
            #if isinstance(j[0], str):
                #print(j[0])
            x_bounds += [j[0]]
        
        x_bounds = set(x_bounds)
        x_bounds = sorted(x_bounds)
        
        return x_bounds

    def calculate_joint_points(self, xs, fvar):
        '''
        Calculates max y values at each significant x

        Params:
        --------
        xs - list of significant x values
        fvar - FuzzyVariable object

        Returns:
        --------
        A list of points, that contain significant x's and max y values(every function is compared the highest y is chosen)
       '''
        list_of_points = [] # holds (x,y) of significant points
        categories = fvar.get_categories()
        
        for x in xs:
            ys = []
            for cat in fvar.cat_names:
                if x != 0.0:
                    y = categories[cat][int(x/0.01)-1]
                else:
                    y = categories[cat][0]
                ys.append(y)
                #if y == 0.75:
                    #print(ys)
            pair = (x, np.max(ys))
            list_of_points.append(pair)
        return list_of_points

    def filter_points(self, fvar, points, values):
        #print(f'Points before filtering: {points}')
        bounds = fvar.cat_bounds
        mds = list(values.values())
        categories = list(fvar.get_categories().values())
        new_points = []

        current_sequence = [points[0]]

        for i in range(1, len(points)):
            x0, y0 = points[i]
            '''
            if self.is_valid == False:
                if len(current_sequence) > 1:
                    new_points.extend([current_sequence[0],  current_sequence[-1]])
                current_sequence = []
                continue
            '''
            x1, y1 = points[i-1]
            
            if abs(round(y0, 2) - round(y1, 2)) <= 0.011 and abs(x0-x1) >= 0:  
                current_sequence.append(points[i])
            else:
                if len(current_sequence) > 1:
                    new_points.extend([current_sequence[0],  current_sequence[-1]])
                current_sequence = [points[i]]
            #print(f'Point: ({x0},{y0})     =   Sequence: {current_sequence}')
        if len(current_sequence) > 1:
            new_points.extend([current_sequence[0], current_sequence[-1]])
        #print('Filtered points in filtering process', new_points)
        new_points = self.remove_duplicates(new_points)
        return new_points

    def remove_duplicates(self, lst):
        new_lst = []
        
        for i in range(len(lst)):
            is_unique = True
            for j in range(i+1, len(lst)):
                if lst[i] == lst[j]:
                    #print(lst[j])
                    is_unique = False
            if is_unique:
                new_lst.append(lst[i])
        return new_lst

    # USES SKFUZZY OFFICIAL METHOD 'centroid'
    # CODE TAKEN FROM: https://github.com/scikit-fuzzy/scikit-fuzzy/blob/master/skfuzzy/defuzzify/defuzz.py
    # 
    # 
    #                             DO NOT FORGET TO CITE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 
    '''
    def centroid(x, mfx):
    
    Defuzzification using centroid (`center of gravity`) method.

    Parameters
    ----------
    x : 1d array, length M
        Independent variable
    mfx : 1d array, length M
        Fuzzy membership function

    Returns
    -------
    u : 1d array, length M
        Defuzzified result

    See also
    --------
    skfuzzy.defuzzify.defuzz, skfuzzy.defuzzify.dcentroid
    """

    '''
    #As we suppose linearity between each pair of points of x, we can calculate
    #the exact area of the figure (a triangle or a rectangle).
    '''

    sum_moment_area = 0.0
    sum_area = 0.0

    # If the membership function is a singleton fuzzy set:
    if len(x) == 1:
        return (x[0] * mfx[0]
                / np.fmax(mfx[0], np.finfo(float).eps).astype(float))

    # else return the sum of moment*area/sum of area
    for i in range(1, len(x)):
        x1 = x[i - 1]
        x2 = x[i]
        y1 = mfx[i - 1]
        y2 = mfx[i]

        # if y1 == y2 == 0.0 or x1==x2: --> rectangle of zero height or width
        if not (y1 == y2 == 0.0 or x1 == x2):
            if y1 == y2:  # rectangle
                moment = 0.5 * (x1 + x2)
                area = (x2 - x1) * y1
            elif y1 == 0.0 and y2 != 0.0:  # triangle, height y2
                moment = 2.0 / 3.0 * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y2
            elif y2 == 0.0 and y1 != 0.0:  # triangle, height y1
                moment = 1.0 / 3.0 * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y1
            else:
                moment = ((2.0 / 3.0 * (x2 - x1) * (y2 + 0.5 * y1))
                          / (y1 + y2) + x1)
                area = 0.5 * (x2 - x1) * (y1 + y2)

            sum_moment_area += moment * area
            sum_area += area

    return (sum_moment_area
            / np.fmax(sum_area, np.finfo(float).eps).astype(float))
        
        
    # TO DO:
    # - Write a function that checks if entered values fit within the boundaries of each variable
    # - Calculates a value for dependency to each output class
    '''