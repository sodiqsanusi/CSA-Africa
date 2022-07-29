import os, skimage.io
import matplotlib.pyplot as plt
import numpy as np
import random    


sheets = {}

def load_sheet(path, sheet):
    fname = os.path.join("DawnLike", path, sheet)+".png"
    if fname not in sheets:        
        sheets[fname] = skimage.io.imread(fname)/255.0
    return sheets[fname]

def get_sprite(path, sheet, x, y):
    sheet =  load_sheet(path, sheet)
    return sheet[x*16:(x+1)*16, y*16:(y+1)*16, :]
    
def assign(codes, region, path, sheet):
    k = 0
    d = {}
    for i in range(region[0][0], region[0][1]):
        for j in range(region[1][0], region[1][1]):
            d[codes[k]]  =    get_sprite(path, sheet, i, j)
            k += 1
    return d

ds = assign('ghijklmnopqrstuvwxyz', [[3,6], [7,10]], "Objects", "Floor")
ws = assign('ABCDEFGHIJKLMN', [[33,36], [0,3]], "Objects", "Wall")
ds.update(ws)
ws = assign('0123456789abcdef', [[3,5], [0,8]], "Objects", "Ground0")
ds.update(ws)

ds['#'] = get_sprite("Objects", "Ground0", 5, 7)
ds['*'] = get_sprite("Items", "Tool", 1, 1)

ds['@'] = get_sprite("Characters", "Player0", 1, 7)
ds['@-'] = get_sprite("Characters", "Player1", 1, 7)

def render_map(rmap, tiles, out_img, items, w=16):
    for y, line in enumerate(rmap.splitlines()):
        for x, ch in enumerate(line):   
            if ch in tiles:
                out_img[y*w:(y+1)*w, x*w:(x+1)*w, :] = tiles[ch][:,:,:3]
                
    for item in items:
        x,y,ch = item
        if ch in tiles:
            
            alpha = tiles[ch][:,:,3:4]
            
            out_img[y*w:(y+1)*w, x*w:(x+1)*w, :3] = (alpha * tiles[ch][:,:,:3] + (1-alpha)*out_img[y*w:(y+1)*w, x*w:(x+1)*w, :])
    

walkable_table = set('j')

class Map(object):
    def __init__(self, map_str):        
        self.lines = map_str.splitlines()
        self.h = len(self.lines)
        self.w = max([len(l) for l in self.lines])
        self.out_img = np.zeros((16*(self.h+1),16*(self.w+1),3))
        
        self.items = {}
        
    def set_map(self, x, y, ch):
        if x>=0 and y>=0 and x<self.w and y<self.h:
            self.lines[y] = self.lines[y][0:x] + ch + self.lines[y][x+1:]
            
    def add_item(self, x, y, ch):
        self.items[(x,y)] = ch
    
    def walkable(self, x, y):
        if x>=0 and y>=0 and x<self.w and y<self.h:
            ch = self.lines[y][x]            
            if not ch in walkable_table:
                return False            
            return True
        return False
    
            
    def render(self, extra_items=[]):
        item_list = [(k[0],k[1],v) for k,v in self.items.items()]
        render_map("\n".join(self.lines), ds, self.out_img, item_list+extra_items)
        return self.out_img
        

class Player(object):
    def __init__(self, x, y):
        self.x, self.y = x,y
        self.ch = "@"

    def go(self, rmap, dx, dy):
        if rmap.walkable(self.x+dx, self.y+dy):
            self.x += dx
            self.y += dy
            return True        
            
        return False
        
    def tick(self):
        if self.ch=='@':
            self.ch = '@-'
        else:
            self.ch = '@'

    def left(self, rmap):
        return self.go(rmap, -1, 0)
            
    def right(self, rmap):
        return self.go(rmap, 1, 0)
    
    
    

class Plant(object):
    def __init__(self):        
        self.water_level = random.randint(2,28)
        self.alive = True
        self.height = random.randint(3,18)
        self.life = random.uniform(10, 30)
        
    def tick(self):
        self.water_level -= random.uniform(0.1, 0.2)
        if self.water_level>0.5 and self.alive:
            self.height += random.uniform(0.05, 0.2) * self.life            
        self.life -= random.uniform(0.02, 0.05)
        
        if self.water_level<=0:
            self.water_level =0            
            self.life -= random.uniform(0.5, 2)
            
        if self.life<0:
            self.alive = False
            self.height = 0
            
    def sample(self):
        if self.alive:            
            self.height *= 0.5
            if self.height<5:
                self.life = 0
                self.alive = False            
            return self.height
        else:
            return 0
        
    def water(self):
        self.water_level += random.uniform(0.5, 2.0)
        
    def is_dry(self):
        return self.water_level < 10
        
    def measure(self):
        return self.height
        
        
        

        
from IPython import display
import time

def tick(game):
    plt.clf()
    game.render()
    
    plt.axis("off")
    plt.tight_layout()
    plt.gcf().canvas.draw()    
    
    time.sleep(0.01)
    
    
play_map = """
  ABBBBBBBBBBBBC              
  DjjjjjjjjjjjjD
  GBBBBBBBBBBBBI"""

class JungleGame(object):
    def __init__(self, play_map=play_map):
        self.play_map = play_map
        
        
        
        self.reset()
        
    def reset(self):    
        self.rmap = Map(self.play_map)        
        self.samples = 0
        self.plants = [Plant() for i in range(12)]
        self.current_plant = self.plants[0]
        for i in range(12):
            self.rmap.add_item(3+i, 2, random.choice('0123456789abcdef'))
        self.player = Player(3,2)        
        tick(self)
        
    def wait(self):
        self.tick()
        
    def left(self):
        r = self.player.left(self.rmap)
        self.tick()
        return r
    
    def right(self):
        r = self.player.right(self.rmap)
        self.tick()
        return r
        
    def water(self):        
        self.current_plant.water()
        self.tick()
        
    def measure(self):
        self.tick()
        return self.current_plant.measure()
        
    def sample(self):
        h = self.current_plant.sample()
        if h>3:
            self.add_sample()
            
    def add_sample(self):
        if self.samples<30:
            self.rmap.add_item(self.samples, 0, '*')
        self.samples += 1
        
    def all_dead(self):
        return all([not p.alive for p in self.plants])
            
    def is_dry(self):
        self.tick()
        return self.current_plant.is_dry()
        
    def is_alive(self):
        return self.current_plant.alive
        
    def samples_collected(self):
        return self.samples
                       
    def tick(self):
    
        self.player.tick()
        for i,plant in enumerate(self.plants):
            # kill dead plants
            plant.tick()
            if not plant.alive:
                self.rmap.items[(3+i,2)] = '#'
                
        ix = self.player.x - 3
        self.current_plant = self.plants[ix]
        tick(self)
        
    def render(self):
        p = self.player        
        plt.imshow(self.rmap.render(extra_items=[(p.x, p.y, p.ch)]), interpolation="nearest")         
        
        
    