import matplotlib.pyplot as plt
import os
import pickle

class Polyomino:
    def __init__(self, content):
        self.content = tuple(content)
    
    def normalize(self):
        min_x = min(x for x, y in self.content)
        min_y = min(y for x, y in self.content)
        normalized = sorted([(x - min_x, y - min_y) for x, y in self.content])
        return Polyomino(normalized)
    
    def rotate(self):
        return Polyomino([(y, -x) for x, y in self.content])
    
    def reflect(self):
        return Polyomino([(-x, y) for x, y in self.content])
    
    def canonical_hash(self):
        hashes = []
        
        # 考虑原始和反射后的所有旋转
        for reflect in [False, True]:
            variant = self.reflect() if reflect else self
            for _ in range(4):
                normalized = variant.normalize()
                hashes.append(normalized.oriented_hash())
                variant = variant.rotate()
        
        return min(hashes)
    
    def oriented_hash(self):
        n = len(self.content)
        hash = 0
        for x, y in self.content:
            bit = x * n + y
            hash += 1 << bit
        return hash
    
    def __eq__(self, other):
        return self.canonical_hash() == other.canonical_hash()
    
    def __hash__(self):
        return self.canonical_hash()
    
    def append(self, pos):
        tmp = list(self.content)
        tmp.append(pos)
        return Polyomino(tmp)
    
    def extend(self):
        new_polyominoes = set()

        for cell in self.content:
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_cell = (cell[0] + dx, cell[1] + dy)
                if new_cell not in self.content:
                    new_poly = self.append(new_cell)
                    new_polyominoes.add(new_poly.normalize())

        return new_polyominoes
    

class PolyominoUtils:
    def __init__(self):
        self.generated = dict()

    def generate_polyominoes(self, n):
        if n == 0:
            return set()
        if n == 1:
            return {Polyomino([(0, 0)])}
        
        if self.generated.get(n):
            return self.generated[n]

        smaller_polyominoes = self.generate_polyominoes(n - 1)
        polyominoes = set()
        
        for poly in smaller_polyominoes:
            extensions = poly.extend()
            polyominoes.update(extensions)
        
        self.generated[n] = polyominoes
        return polyominoes
    
    def draw_polynomino(self, poly, save_path):
        fig, ax = plt.subplots(figsize=(4, 4))
        
        # 设置坐标轴
        max_x = max(x for x, y in poly.content)
        max_y = max(y for x, y in poly.content)
        
        # 绘制方块
        for x, y in poly.content:
            rect = plt.Rectangle((x, y), 1, 1, 
                               facecolor='lightblue', 
                               edgecolor='black', 
                               linewidth=2)
            ax.add_patch(rect)
        
        ax.set_xlim(-1, max_x + 2)
        ax.set_ylim(-1, max_y + 2)
        ax.set_aspect('equal')
        ax.axis('off')
    
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        # plt.show()

        plt.close()

    def draw_all_polynominoes(self, n, save_path):
        polynominoes = self.generate_polyominoes(n)
        counter = 0
        for poly in polynominoes:
            os.makedirs(f"{save_path}/{counter}", exist_ok=True)
            self.draw_polynomino(poly, f"{save_path}/{counter}/board.png")
            counter = counter + 1

    def generate_move_info(self, poly):
        L = []
        U = []
        cells = list(poly.content)

        from collections import defaultdict

        # up move
        points_by_y = defaultdict(list)
        for idx, (x, y) in enumerate(cells):
            points_by_y[y].append((x, idx))
        
        for y, point_data in points_by_y.items():
            point_data.sort(key=lambda item: item[0])
            
            current_chain = []
            prev_x = None
            
            for x, idx in point_data:
                if prev_x is None or x != prev_x + 1:
                    if current_chain:
                        L.append(current_chain)
                    current_chain = [idx]
                else:
                    current_chain.append(idx)
                prev_x = x

            if current_chain:
                L.append(current_chain)
        
        # up move
        points_by_x = defaultdict(list)
        for idx, (x, y) in enumerate(cells):
            points_by_x[x].append((y, idx))
        
        for x, point_data in points_by_x.items():
            point_data.sort(key=lambda item: item[0])
            
            current_chain = []
            prev_y = None
            
            for y, idx in point_data:
                if prev_y is None or y != prev_y + 1:
                    if current_chain:
                        U.append(current_chain)
                    current_chain = [idx]
                else:
                    current_chain.append(idx)
                prev_y = y

            if current_chain:
                U.append(current_chain)
        
        R = [i[::-1] for i in L]
        D = [i[::-1] for i in U]

        return [L, R, U, D]

    def generate_all_move_info(self, n, save_path):
        polynominoes = self.generate_polyominoes(n) 
        counter = 0
        for poly in polynominoes:
            os.makedirs(f"{save_path}/{counter}", exist_ok=True)
            info = self.generate_move_info(poly)
            with open(f"{save_path}/{counter}/move.pkl", 'wb') as f:
                pickle.dump(info, f)
            counter = counter + 1

def main():
    generator = PolyominoUtils()
    generator.generate_polyominoes(8)
    # breakpoint()
    # generator.draw_all_polynominoes(8,"polynominoes")

    generator.generate_all_move_info(8, "polynominoes")

def find(n, content):
    generator = PolyominoUtils()
    polynominoes = generator.generate_polyominoes(n)
    target_poly = Polyomino(content).normalize()
    for idx, poly in enumerate(polynominoes):
        if poly == target_poly:
            return idx
    return -1
    
if __name__ == "__main__":
    print(find(8, [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(1,0),(1,1)]))