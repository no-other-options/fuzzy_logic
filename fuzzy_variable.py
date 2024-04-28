from utils import trapezoid_mf, trapezoid, triangular
import matplotlib.pyplot as plt
import numpy as np

# Defines a linguistic variable. 
# Each object has:
# - range of x values
# - fuzzy values - categories,
# - number of said categories
# - bounds of every category - coefficients for a membership function
class FuzzyVariable:

    def __init__(self, name, x_bounds, nr_categories, cats, cat_bounds):
        self.var_name = name
        self.x_bounds = x_bounds
        self.cat_num = nr_categories
        self.cat_bounds = cat_bounds
        self.cat_names = cats
        self.categories = self.pair_cats_bounds(cats, cat_bounds)

    def pair_cats_bounds(self, categories, bounds):
        cat = dict()
        for i in range(self.cat_num):
            if len(bounds[i]) == 4 or len(bounds[i]) == 3:
                cat[categories[i]] = trapezoid_mf(self.x_bounds, bounds[i]) 
            else:
                raise NotImplementedError("More points are not supported.")
        return cat

    def get_categories(self):
        return self.categories

    def plot_categories(self, xlabel=None, title=None, save=False, y_vals=None, points = None):
        if xlabel == None:
            xlabel=self.var_name
            
        if title == None:
            title = self.var_name
            
        keys = list(self.categories.keys())
        
        for i in range(self.cat_num):
            plt.plot(self.x_bounds, self.categories[keys[i]], label=f"{title}: {keys[i]}")

        if points != None:
            x_values = [point[0] for point in points]
            y_values = [point[1] for point in points]

            # Plot the points
            plt.scatter(x_values, y_values)
            for i, point in enumerate(points):
                plt.text(point[0], point[1], f'({round(point[0],2)}, {round(point[1],2)})', fontsize=6, ha='right')
        
        plt.xlabel(xlabel)
        plt.ylabel('Membership value')
        plt.title(title) 
        plt.legend()
        plt.grid(True)
        if save:
            plt.savefig(f'{title.replace(" ","")}.png')
        plt.show()
        

    def get_membership_values(self, x):
        if len(self.cat_bounds[0]) == 4:
            membership = dict()
            keys = list(self.categories.keys())
            
            for i in range(self.cat_num):
                membership[keys[i]] = trapezoid_mf(x, self.cat_bounds[i])
                
            return membership
            
        else:
            raise NotImplementedError("More points are not supported.")
            
            return None

    def modify_categories_md(self, values, fvar):
        for i in range(self.cat_num):
            val = values[self.cat_names[i]]
            lst = fvar.categories[self.cat_names[i]]
            self.categories[self.cat_names[i]] = [x if x <= val else val for x in lst]

    
    
