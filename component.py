import numpy as np
import pandas as pd

class component():
    def __init__(self, mat, min_idx, max_idx):
        self.mat = np.array(mat)
        self.shape = self.mat.shape
        self.scope = {'min':min_idx, 'max':max_idx}
        self.contained_by = None
        self.containing = []
        self.neighbor = []
        self.size = (self.mat != 0).sum()
        self.colors = np.unique(self.mat)
        if self.colors[0]:
            self.is_square = True
        else:
            self.is_square = False
        self.vertical = []
        self.horizonal = []
        self.hsymmetric = True
        self.vsymmetric = True
        for i in range(0, (self.mat.shape[0]) // 2):
            if np.any((self.mat[i,:] == self.mat[self.shape[0] - i - 1,:]) == False):
                self.hsymmetric = False
                break
        for j in range(0, (self.mat.shape[1]) // 2):
            if np.any((self.mat[:,j] == self.mat[:,self.shape[1] - j - 1]) == False):
                self.vsymmetric = False
                break
        if len(self.colors) > 2 or self.is_square and len(self.colors) > 1:
            self.sub_comps = find_components(self.mat)
        else:
            self.sub_comps = [self]
        self.sub_comp_num = len(self.sub_comps)
    
    def get_features(self):
        features = pd.DataFrame({'{}'.format(i):[(self.mat == i).sum()] for i in range(10)})
        features['hsym'] = [self.hsymmetric]
        features['vsym'] = [self.vsymmetric]
        features['filled'] = [self.is_square]
        features['contained'] = [self.contained_by != False]
        features['sub_comp_num'] = [self.sub_comp_num]
        for i in range(10):
                features['{} exist'.format(i)] = features['{}'.format(i)] != 0
        return features
    
    def __str__(self) -> str:
        return self.mat.__str__()

    def __eq__(self, other) -> bool:
        if np.unique(self.mat == other.mat)[-1]:
            return True
        else:
            return False
    
    def is_contained(self, other):
        if self.contained_by == other:
            return True
        else:
            return other.is_containing(self)
    
    def is_containing(self, other):
        if self == other:
            return False
        if other in self.containing:
            return True
        elif (
            self.scope['min_idx'][0] <= other.scope['min_idx'][0]
        ) and (
            self.scope['min_idx'][1] <= other.scope['min_idx'][1]
        ) and (
            self.scope['max_idx'][0] >= other.scope['max_idx'][0]
        ) and (
            self.scope['max_idx'][1] >= other.scope['max_idx'][1]
        ):
            self.containing.append(other)
            if other.contained_by and self.containing(other.contained_by):
                return True
            other.contained_by = self
            return True
        else:
            return False
    
    def is_neighbor(self, other):
        if self == other:
            return False
        if other in self.neighbor:
            return True
        elif {i for i in range(
                self.scope['min_idx'][0] - 1, self.scope['max_idx'][0] + 1
            )} & {i for i in range(other.scope['min_idx'][0] - 1, other.scope['max_idx'][0] + 1)} and {i for i in range(
                self.scope['min_idx'][1] - 1, self.scope['max_idx'][1] + 1
            )} & {i for i in range(other.scope['min_idx'][1] - 1, other.scope['max_idx'][1] + 1)}:
            self.neighbor.append(other)
            other.neighbor.append(self)
            return True
        else:
            return False
    
    def find_neighbors(self, others):
        result = []
        for other in others:
            if self.is_neighbor(other):
                result.append(other)
        return result
    
    def find_inner(self, others):
        result = []
        for other in others:
            if self.is_containing(other):
                result.append(other)
        return result

def find_component(matrix, diagonal=False, multi_color=False, reversed=False, background=0):
    def visit(i_,j_):
        if (i_ < 0) or (i_ == shape[0]) or (j_ < 0) or (j_ == shape[1]):
            return None
        cur_color = mat[i_,j_]
        if (cur_color == background) or (cur_color != color and not multi_color):
            return None
        visited.add((i_,j_))
        mat[i_,j_] = background
        component_mat[i_,j_] = cur_color
        if i_ < min_idx[0]:
            min_idx[0] = i_
        if i_ > max_idx[0]:
            max_idx[0] = i_
        if j_ < min_idx[1]:
            min_idx[1] = j_
        if j_ > max_idx[1]:
            max_idx[1] = j_

        if diagonal:
            i_neighbor = {i_-1,i_,i_+1}
            j_neighbor = {j_-1,j_,j_+1}
            neighbors = {(a,b) for a in i_neighbor for b in j_neighbor}
        else:
            neighbors = {(i_-1,j_), (i_+1,j_), (i_,j_-1), (i_,j_+1)}
        for neighbor in neighbors - visited:
            visit(neighbor[0],neighbor[1])

    mat = np.array(matrix)
    if reversed:
        mat = (mat != background).astype(int)
    shape = mat.shape
    i, j = shape
    i -= 1
    j -= 1
    component_mat = np.zeros(shape, dtype=int)
    while mat[i,j] == background:
        if j:
            j -= 1
        else:
            j = shape[1] - 1
            i -= 1
    color = mat[i,j]
    visited = set()
    min_idx = [i,j]
    max_idx = [i,j]
    visit(i,j)
    component_mat = component_mat[min_idx[0]:max_idx[0]+1,min_idx[1]:max_idx[1]+1]
    comp = component(component_mat, min_idx, max_idx)
    print(comp)
    return mat, comp

def find_components(matrix, diagonal=False, multi_color=False, reversed=False, background=0):
    mat = np.array(matrix)
    components = []
    while len(np.unique(mat)) != 1:
        mat, comp = find_component(mat, diagonal, multi_color, reversed, background)
        components.append(comp)
    return components