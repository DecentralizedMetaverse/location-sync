import sys
import pygame
from node import Node, Vector, NodeSettings
from random import randint, uniform
from os import makedirs

class Main:
    def __init__(self, gui_mode = False, evaluation_mode = 0, screenshot=False):
        self.screenshot = screenshot
        self.gui_mode = gui_mode
        # 評価モード 0:最短ノード探索の評価 1:移動の評価
        self.evaluation_mode = evaluation_mode 
        self.node_settings = NodeSettings() # Node設定値
        self.node_settings.evaluation_mode = evaluation_mode

        self.set_value()
        self.set_window()
        self.set_node()
        self.connect_in_distance_order()

        self.count = 0
    
    def set_value(self):
        # 設定値
        args = sys.argv
        if len(args) > 1:
            self.node_num = int(args[1])
            self.node_settings.max_connect = Vector(int(args[2]),int(args[3]))
            self.node_settings.max_area = Vector(int(args[4]),int(args[5]))
            self.node_settings.max_speed = float(args[6])
            time1=[0,int(args[7])]
            time2=[0,int(args[8])]
            self.node_settings.max_step=int(args[9])
        else:
            self.node_num = 1000
            self.node_settings.max_connect = Vector(5,5)   
            self.node_settings.max_area = Vector(1000,1000)
            self.node_settings.max_speed = 0.1
            time1=[0,0]
            time2=[0,0]
            self.node_settings.max_step = 1000

        if self.evaluation_mode == 0:
            save_fine_path = "save1"
            self.node_settings.save_fine_name = f"{save_fine_path}/save{self.node_settings.max_connect.x}.csv"
        else:
            save_fine_path = "save2"
            self.node_settings.save_fine_name = f"{save_fine_path}/save{self.node_settings.max_connect.x}.csv"

        makedirs(save_fine_path, exist_ok=True)

        self.node_settings.time = [time1, time2]
        self.nodes = [Node(i, self.node_settings) for i in range(self.node_num)]


    def set_window(self):
        # -----------------------------------
        # window設定
        if self.gui_mode:
            pygame.init()                                       # pygame初期化
            self.screen = pygame.display.set_mode((1000, 1000))      # メイン画面初期化
            pygame.display.set_caption("P2P")                   # タイトル
            self.clock = pygame.time.Clock()                         # Clockオブジェクトの生成
            self.fps = 60

        self.running = True                                          # ループを続けるかのフラグ
        
    def set_node(self):
        # nodeの設定
        for n in self.nodes:              
            if not n.id == 0:
                self.nodes[0].all_node.append(n)

    def connect_in_distance_order(self):
        # 距離順で接続する 最初のnodeのみランダム
        once = True
        for n in self.nodes:       
            if self.evaluation_mode == 0 and n.id == 0: continue                 

            temps = {}
            for other in self.nodes:
                if other.id == 0: continue
                temps[other] = n.distance(other)

            temps = sorted(temps.items(), key=lambda x:x[1])
            for i,(min_n,_) in enumerate(temps):
                if i > n.max_connect.x:
                    break
                n.connect(min_n)
        
        if self.evaluation_mode == 0 :
            random_num = self.rand_int(1, self.node_num-1, self.nodes[0].max_connect.x)
            for n in random_num:
                self.nodes[0].connect(self.nodes[n])

    def update(self):
        while self.running:
            if self.gui_mode:
                self.update_gui()
            else:
                self.update_cui()

    def finalize(self):
        # 終了処理
        if self.gui_mode:
            pygame.quit()
            sys.exit()

    def update_cui(self):
        # CUI処理
        for n in self.nodes:
            n.update()

    def update_gui(self):
        # GUI処理
        for n in self.nodes:
            n.update()

        # 接続を表す線を表示
        color = (200,200,200)
        once = True
        for n in self.nodes:
            if once:
                once = False
                continue
            self.draw_line(self.screen,color,n)
        
        color = (0,255,0)
        self.draw_line(self.screen,color,self.nodes[0],True,3)

        # 自身を表す円を表示
        once = True
        color = (200,200,200)
        for n in self.nodes:
            if once:
                once = False
                continue
            pygame.draw.ellipse(self.screen,color,(n.pos.x,n.pos.y,5,5))

        color = (0,255,0)
        pygame.draw.ellipse(self.screen,color,(self.nodes[0].pos.x,self.nodes[0].pos.y,5,5))


        # -----------------------------------------
        pygame.display.update() # メイン画面の更新
        
        if self.screenshot:
            pygame.image.save(self.screen, f"screenshot/{self.count}.jpg")
            self.count +=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False # 終了
                break                               

        self.clock.tick(self.fps)         # フレームレートの設定
        self.screen.fill((0,0,0))    #画面を黒で塗りつぶす
    


    # 線を引く
    def draw_line(self, screen, color, node, both=False, size=1, color2=(255,0,0)):        
        for n in node.nodes.x:
            pygame.draw.line(screen,color,(node.pos.x+2,node.pos.y+2),(n.pos.x+2,n.pos.y+2),size)
        
        if not both: return
        color = (0,100,0)
        for n in node.nodes_ex:
            pygame.draw.line(screen,color,(node.pos.x+2,node.pos.y+2),(n.pos.x+2,n.pos.y+2),size)

        for n in node.nodes.y:
            pygame.draw.line(screen,color2,(node.pos.x+2,node.pos.y+2),(n.pos.x+2,n.pos.y+2),size)


    # 重複なしランダム生成
    def rand_int(self, n1, n2, size):    
        n = []
        while len(n) < size:
            r = randint(n1, n2)
            if r in n: continue
            n.append(r)

        return n


if __name__ == '__main__':
    main = Main(gui_mode=True, evaluation_mode=1)
    main.update()