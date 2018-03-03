import pygame
import sys
import random
import time
#from obstacle import *

pygame.init()
pygame.font.init()

x_max=800
y_max=600
screen=pygame.display.set_mode((x_max,y_max))
FPS=30

myfont = pygame.font.SysFont("monospace", 15)
clock=pygame.time.Clock()

keys=pygame.key.get_pressed()#this is a list of all the states of all the keys

stand=100
ground=y_max-120
gravity=15
max_height=ground+10




keys=pygame.key.get_pressed()#this is a list of all the states of all the keys
#ground=y_max-100
start=x_max
speed=10


class obstacle:


    def __init__(self,x=start,y=ground,h=50,b=30):
        self.x=x
        self.y=random.randrange(10,y)
        self.h=random.randrange(h,h*3)#height
        self.w=b#width

        self.draw(x,y)




    def draw(self,x,y):
        self.shape=pygame.draw.rect(screen,(255,255,0),(x,y,self.w,self.h),0)
        self.shape
    def move(self,speed):

        self.x-=speed
        self.draw(self.x,self.y)

    def chk_edge(self):
        if self.x<=0:
            return 1
        else: return 0




#o=obstacle()
obs_list=[]



class Player:

    def __init__(self):
#add required paths here
"""
        img_run='/home/arjun/My_stuff/Python/Project_run_man/run_small.png'
        img_jump='/home/arjun/My_stuff/Python/Project_run_man/jump_small.png'
        img_die='/home/arjun/My_stuff/Python/Project_run_man/die_small.png'
        img_glide='/home/arjun/My_stuff/Python/Project_run_man/glide_small.png'
"""
        self.life=1
        self.x=stand
        self.y=ground#place of standing is stand place
        self.img_no=0#the  frame
        self.cell_list={}

        self.cell_list['run']=self.ret_frames(img_run,2,5)
        self.cell_list['jump']=self.ret_frames(img_jump,2,5)
        self.cell_list['die']=self.ret_frames(img_die,3,4)
        self.cell_list['glide']=self.ret_frames(img_glide,3,4)
        self.run()



    def chk_collide(self,r2):
        #check for each of the four corners
        size=self.cell_list['run'][0].get_size()#obtain size using one of our random surfaces

        if r2.x<self.x<r2.x+r2.w and r2.y<self.y<r2.y+r2.h:
            self.life-=1
            self.die()
        if r2.x<self.x+size[0]<r2.x+r2.w and r2.y<self.y<r2.y+r2.h:
            self.life-=1
            self.die()
        if r2.x<self.x<r2.x+r2.w and r2.y<self.y+size[1]<r2.y+r2.h:
            self.life-=1
            self.die()
        if r2.x<self.x+size[0]<r2.x+r2.w and r2.y<self.y+size[1]<r2.y+r2.h:
            self.life-=1
            self.die()



    def ret_frames(self,img,no_row=1,no_col=1):#cuts the sprite sheet into small pices
        image=pygame.image.load(img)
        size=image.get_size()
        width=int(size[0]/no_col)
        height=int(size[1]/no_row)
        cell_list=[]

        #print(width,height)
        for x in range(0,size[0],width):
            for y in range(0,size[1],height):
                #creates a small area to work
                s=pygame.Surface((width,height))
                #blit keeps overwriting on the canvas
                s.blit(image,(0,0),(x,y,width,height))
                cell_list.append(s)

        return cell_list

    def jump(self,chk):

        self.img_no=0#image number

        if self.img_no<=len(self.cell_list['jump'])-4:
            self.img_no+=1
        else:
            self.img_no=0

        if chk==0:
            player.y-=gravity

        """else :
            player.y-=gravity
        """
        screen.blit(self.cell_list['jump'][self.img_no],(self.x,self.y))# x and y coordinates on screen


    def run(self):
        if self.img_no<=len(self.cell_list['run'])-4:
            self.img_no+=2
        else:
            self.img_no=0

        if self.y<=ground:
            self.y+=gravity
            screen.blit(self.cell_list['glide'][self.img_no],(self.x,self.y))# and y coordinates on screen

        else:
            screen.blit(self.cell_list['run'][self.img_no],(self.x,self.y))# and y coordinates on screen



    def die(self):
        screen.fill((255,255,255))
        largeText = pygame.font.SysFont("monospace",30)
        TextSurf, TextRect = text_objects("Game Over"+'                        Score:'+str(int(Score.score)), largeText)
        TextRect.center = ((x_max/2),(y_max/2))
        screen.blit(TextSurf, TextRect)
        smallText= pygame.font.SysFont("monospace",20)
        TextSurf, TextRect = text_objects(("High Score:"), smallText)
        TextRect.center = ((x_max/4),(y_max/4))
        screen.blit(TextSurf, TextRect)
        Score.store_score(Score)
        k=Score.high_score(Score)
        for i in range(4):
                TextSurf, TextRect = text_objects((str(i+1)+'. '+str(k[i])),smallText)
                TextRect.center = ((x_max/4),(y_max/4)+(i+1)*20)
                screen.blit(TextSurf, TextRect)

        pygame.display.update()
        clock.tick(FPS)
        while 1:

            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN:
                    return





player=Player()



chk_pause=0

def pause():#flaw, you have to keep pressing p to keep it paused

    #for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_p]!=0:
            return 1#while event.type==pygame.KEYUP:
        else:
            return 0


def reset():
    global player
    global obs_list
    player=Player()
    obs_list=[]
    Score.score=0


def msg_(msg, color):
	text=myfont.render(msg,True,color)
	screen.blit(text,[x_max/2,y_max/2])



class Score:
    score=0
    def __init__(self):
        score=0


    def score_update(self,x=30,y=50):

        label = myfont.render(str(int(self.score)), 1, (255,255,0),(0,0,0))#parameters are the text, aliasing(something to do with rendering of font and alpha),the bgcolour
        screen.blit(label, (x, y))


    def store_score(self):

        l=self.high_score(self)
        l.append(int(self.score))
        l.sort(reverse=True)
        for i in l:
            l[l.index(i)]=int(i)#need to make all numbers int before sort
        l.sort(reverse=True)
        for i in l:
            l[l.index(i)]=str(i)#need to make all numbers int before sort
        f=open('high_score.txt','w')
        for i in l:
            f.write(i+',')


        f.close()

    def high_score(self):
        f=open('high_score.txt','r')
        l=f.readline()
        l=l.split(',')
        k=[]
        for i in l:
            if i.isdigit():
                k.append(int(i))#need to make all numbers int before sort
        k.sort(reverse=True)
        f.close()
        return k
def play():
    global chk_pause
    player.run()

    while player.life==1:

        chk_pause=pause()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()


        if chk_pause==0:
            screen.fill((0,0,0))
            #chk_pause=pause()


            if pygame.key.get_pressed()[pygame.K_UP]!=0:

                    if player.y>=10:
                        player.jump(0)
                    else: player.jump(1)
            else:
                player.run()
                for i in obs_list:
                    if player.chk_collide(i):
                        player.die()



            #if event.type==pygame.KEYUP:
            #    player.run()


            #print(player.x,player.y,player.cell_list['run'][0].get_size()[0],player.cell_list['run'][0].get_size()[1])
            #print(r2.x,r2.y,r2.h+x,r2.h+y)



            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if random.randint(1,50)==1:
                obs_list.append(obstacle())

            for j in range(len(obs_list)):
                obs_list[j].move(speed+int(Score.score*0.1))

            for i in obs_list:
                if i.x<=-50:
                    obs_list.remove(i)

            Score.score+=0.1
            Score.score_update(Score)



            clock.tick(FPS)

            pygame.display.update()
        """else:
            while chk_pause==1:
                chk_pause=pause()
"""
    #    play()

black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
        smallText = pygame.font.SysFont("monospace",20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        screen.blit(textSurf, textRect)

def quitgame():
    pygame.quit()



def game_menu():

    menu = True
    reset()
    player.life=1
    while menu:
        for event in pygame.event.get():#print(event)
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill(white)
        largeText = pygame.font.SysFont("monospace",115)
        TextSurf, TextRect = text_objects("2D NINJA-GO", largeText)
        TextRect.center = ((x_max/2),(y_max/2))
        screen.blit(TextSurf, TextRect)
        button("GO!",150,450,100,50,green,bright_green,play)
        button("Quit",550,450,100,50,red,bright_red,quitgame)
        menu=False
        pygame.display.update()
        clock.tick(FPS)


while 1:
    game_menu()
    reset()
    #player.die()

    #pygame.quit()
