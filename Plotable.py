class Plotable:
    def __init__(self):
        self.__x_vals = []
        self.__y_vals = []
    
    def get_x_vals(self):
        return self.__x_vals
    
    def get_y_vals(self):
        return self.__y_vals
    
    def append_x_vals(self,x):
        self.get_x_vals().append(x)
        
    def append_y_vals(self,y):
        self.get_y_vals().append(y)