# 近くの相手を見つけるプログラム
from random import randint, uniform
import queue
import os

class NodeSettings:
    pass

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Node:
    def __init__(self, id, settings):
        self.evaluation_mode = settings.evaluation_mode
        self.settings = settings
        self.max_speed = settings.max_speed
        self.max_connect = settings.max_connect   
        self.max_area = settings.max_area
        self.max_cache = 100

        # evaluate
        self.max_step = settings.max_step
        self.save_fine_name = settings.save_fine_name
        self.step = 0
        self.step2 = 0
        self.score = 0
        self.score_all = 0

        self.id = id
        self.all_node = []
        self.pos = Vector(
            randint(0, self.max_area.x), 
            randint(0, self.max_area.y)
        )
        self.vec = Vector(
            uniform(-self.max_speed, self.max_speed), 
            uniform(-self.max_speed, self.max_speed)
        )        
        self.nodes = Vector([], [])        
        self.nodes_ex = []
        self.nodes_d = Vector(queue.LifoQueue(), queue.Queue())
        self.cache = set()
        time = settings.time
        self.time1 = [time[0][0], time[0][1]]
        self.time2 = [time[1][0], time[1][1]]


    def update(self):
        if self.check_count(self.time1):
            self.update_pos()

        if self.check_count(self.time2):
            self.evaluate()
            self.calc_distance()
            self.next_connect() 


    def connect(self, node):
        self.add_step_early_stop()

        if len(self.nodes.x) >= self.max_connect.x: return False
        if len(node.nodes.y) >= node.max_connect.y: 
            # 受け入れ可能数を超えている
            self.nodes_ex.append(node) # オーバーしたものを記録しておく            
            return False

        self.nodes.x.append(node)        
        node.nodes.y.append(self)        
        return True        


    def disconnect(self, node):
        # self.add_step_early_stop()

        self.nodes.x.remove(node)
        node.nodes.y.remove(self)
        
        # if node in self.cache:
        #     self.cache.remove(node)
        # el
        if len(self.cache) >= self.max_cache: 
            self.cache.pop()
        self.cache.add(node)


    # 次の接続
    def next_connect(self):
        while not self.nodes_d.y.empty():         # 次、接続候補nodeなし
                        
            if ( len(self.nodes.x) + len(self.nodes_ex) ) < self.max_connect.x:
                # 接続に余裕がある       
                self.connect(self.nodes_d.y.get())
            elif not self.nodes_d.x.empty():
                # これ以上接続できない        
                self.disconnect(self.nodes_d.x.get())
                self.connect(self.nodes_d.y.get())    
            else: return                 


    # 距離を計算する
    def calc_distance(self):      
        self.nodes_d.x = queue.LifoQueue()
        self.nodes_d.y = queue.Queue()
        
        l1 = self.nodes.x + self.nodes.y # 接続先
        l2 = set()                       # 接続先の接続先

        # 接続先の接続先を取得
        temps = {}        
        for l in l1:           
            if l in self.nodes.x: 
                temps[l] = self.distance(l)                
                
            for t in l.nodes.x:
                l2.add(t) # 接続先の接続先を追加
            for t in l.nodes.y:
                l2.add(t) # 接続先の接続先を追加

        # 過剰分
        for l in self.nodes_ex:
            for t in l.nodes.x:
                l2.add(t) # 接続先の接続先を追加
                
            for t in l.nodes.y:
                l2.add(t) # 接続先の接続先を追加

        # 距離順でソート
        if len(temps) != 0:  # nodes.x 0件の場合
            temps = sorted(temps.items(), key=lambda x:x[1])
            self.max_d = temps[len(temps)-1][1]  # 最大距離
            
            for n,_ in temps:
                if not n in self.nodes_ex:
                    self.nodes_d.x.put(n) # オーバー分は含めない
        else: self.max_d = 0

        # 最大値より小さい接続先の接続先を見つける
        temps = {}
        for l in l2:
            d = self.distance(l)
            
            if d >= self.max_d and self.max_d != 0: continue
            
            if (l in self.nodes.x or
                l in self.nodes.y or
                l in self.nodes_ex or
                l == self 
            ): continue # 重複防止            
            
            temps[l] = d

        # 距離順でソート
        temps = sorted(temps.items(), key=lambda x:x[1])
        for n,_ in temps:
            self.nodes_d.y.put(n)
        
        if len(temps) != 0:
            # 接続候補があるため終了
            self.nodes_ex.clear()   
            return

        # -----------------------------------------
        # 接続候補がないため、
        # キャッシュにアクセスして、ランダムに接続する
        if len(self.cache) == 0: 
            # 0件　終了
            self.nodes_ex.clear()   
            return
        
        cache_list = list(self.cache)
        
        node = cache_list[randint(0, len(self.cache)-1)] # ランダムに抽出する
        self.add_step_early_stop() # キャッシュにアクセスするので+1

        l = node.nodes.x + node.nodes.y     
        if len(l) == 0:
            # 0件　終了
            self.nodes_ex.clear()
            return

        n = l[randint(0, len(l)-1)]
        if not (n in self.nodes.x or
            n in self.nodes.y or
            n in self.nodes_ex or
            n == self 
        ):
            self.nodes_d.y.put(n)
        self.nodes_ex.clear()   
                

    # 評価
    def evaluate(self):    
        if self.id != 0: return
        self.score = 0
                
        self.add_step_early_stop(False)        
        self.step2 += 1

        temps = {}
        for other in self.all_node:
            if other.id == 0: continue
            temps[other] = self.distance(other)

        temps = sorted(temps.items(), key=lambda x:x[1])
        
        for i,(min_n,_) in enumerate(temps):
            if i > (self.max_connect.x + self.max_connect.y):
                break
            if min_n in self.nodes.x or min_n in self.nodes.y:
                self.score += 1

        self.score /= (self.max_connect.x + self.max_connect.y)
        self.score_all += self.score
        # print(f"[{self.step}]:{self.score}")


        if self.evaluation_mode == 0:
            if self.score > 0:
                self.save_record()


    def add_step_early_stop(self, addStep=True):
        if self.id != 0: return
        if addStep:
            self.step += 2

        # if self.step2 >= self.max_step:

        if self.evaluation_mode == 0:
            if self.step < self.max_step: return
            self.save_record()
        else:
            if self.step2 < self.max_step: return
            self.save_record2()


    # 最短node探索
    def save_record(self):        
        txt = ""
        if not os.path.isfile(self.save_fine_name):
            
            txt += "step,step2,num,connect_x,connect_y,area_x,area_y,speed,time1,time2\n"

        txt += f"{self.step},{self.step2},{len(self.all_node) + 1},{self.max_connect.x},{self.max_connect.y},{self.max_area.x},{self.max_area.y},{self.max_speed},{self.time1[1]},{self.time2[1]}"
        
        with open(self.save_fine_name, 'a', encoding="utf-8") as f:
            print(txt, file=f)

        exit()

    
    # 移動シミュレーション
    def save_record2(self):
        txt = ""
        if not os.path.isfile(self.save_fine_name):
            
            txt += "step,step2,score_mean,num,connect_x,connect_y,area_x,area_y,speed,time1,time2\n"

        txt += f"{self.step},{self.step2},{self.score_all/self.max_step},{len(self.all_node) + 1},{self.max_connect.x},{self.max_connect.y},{self.max_area.x},{self.max_area.y},{self.max_speed},{self.time1[1]},{self.time2[1]}"
        
        with open(self.save_fine_name, 'a', encoding="utf-8") as f:
            print(txt, file=f)

        if self.step2 >= self.max_step:
            exit()



    # 座標の更新
    def update_pos(self):
        self.pos.x += self.vec.x
        self.pos.y += self.vec.y

        if self.pos.x < 0 or self.max_area.x < self.pos.x:
            self.vec.x = -self.vec.x
        
        if self.pos.y < 0 or self.max_area.y < self.pos.y:
            self.vec.y = -self.vec.y


    # 間隔をあける
    def check_count(self, count):
        count[0] += 1
        if count[0] < count[1]: return False
        
        count[0] = 0
        return True
    

    # 距離の計算
    def distance(self, node):
        return self._distance(self.pos.x, self.pos.y, node.pos.x, node.pos.y)    
    def distance2(self, node1, node2):
        return self._distance(node2.pos.x, node2.pos.y, node1.pos.x, node1.pos.y)    
    def _distance(self, x1,y1,x2,y2):
        return int(pow(pow(x2-x1,2)+pow(y2-y1,2),0.5))