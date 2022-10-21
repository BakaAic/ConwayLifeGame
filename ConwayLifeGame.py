import math
from tkinter import *
from tkinter.ttk import * 
import threading
import random
import gc

class NaturalEnvironment:
    def __init__(self, NaturalSize=(600,600), NaturalName="Natural"):
        self.NaturalName=NaturalName
        self.EnvironmentWidth = NaturalSize[0]
        self.EnvironmentHeight = NaturalSize[1]
        self.Ecosphere=[]
        self.Inoculation_Area=[]
        
    def destroy(self):
        self.Ecosphere=[]
        self.Inoculation_Area=[]
        
Natural=[]
Natural.append(NaturalEnvironment((600,600),"Conway's Life Game"))

class NaturalRules:
    NaturalNo=0
    NaturalHandle=Natural[NaturalNo]
    CodeAuthor="Aikko"
    @classmethod
    def resetNatural(cls,Natural_handle=None):
        cls.NaturalHandle.destroy()
        if Natural_handle:
            cls.NaturalHandle=Natural_handle
        else:
            cls.NaturalHandle=Natural[cls.NaturalNo]
            
    @classmethod
    def setNaturalNo(cls,NaturalNo):
        cls.NaturalNo=NaturalNo
        cls.NaturalHandle=Natural[NaturalNo]
        
    @classmethod
    def register(cls, organism):
        cls.NaturalHandle.Ecosphere.append(organism)
        return organism
    
    @classmethod
    def unregister(cls, organism):
        cls.NaturalHandle.Ecosphere.remove(organism)
        return organism
    
    @classmethod
    def getLifePositon(cls):
        positions=[]
        for organism in cls.NaturalHandle.Ecosphere:
            positions.append(organism.position())
        return list(set(positions))
    
    @classmethod
    def getVaildBornArea(cls,vaildArea:list):
        vaildBornArea=vaildArea
        for organism in cls.NaturalHandle.Ecosphere:
            if (organism.pos_x,organism.pos_y) in vaildArea:
                vaildBornArea.remove((organism.pos_x,organism.pos_y))
        return vaildBornArea
    
    @classmethod
    def scanBorn(cls,BornArea:list,LifeArea:list):
        def _lifeCheck(vaildArea,lifeArea):
            count=0
            for pos in vaildArea:
                if pos in lifeArea:
                    count+=1
            if count==3:
                return True
            else:
                return False
        for _x,_y in BornArea:
            inoculation=Inoculation(_x,_y)
            inoculation.setInoculation(_lifeCheck(inoculation.getVaildPoint(),LifeArea))
            cls.NaturalHandle.Inoculation_Area.append(inoculation)
            
    @classmethod
    def getNumber(cls):
        return len(cls.NaturalHandle.Ecosphere)
    
    @classmethod
    def Born(cls):
        for inoculation in cls.NaturalHandle.Inoculation_Area:
            if inoculation():
                Organism(inoculation.pos_x,inoculation.pos_y)
                
    @classmethod
    def getNaturalSize(cls):
        return (cls.NaturalHandle.EnvironmentWidth,cls.NaturalHandle.EnvironmentHeight)
    
    @classmethod
    def isLife(cls, pos):
        for organism in cls.NaturalHandle.Ecosphere:
            if organism.position() == pos:
                return True
        return False
    
    
class PointAttributes():
    def __init__(self,x,y):
        self.pos_x = x
        self.pos_y = y
        self.maxW = NaturalRules.getNaturalSize()[0]
        self.maxH = NaturalRules.getNaturalSize()[1]
        self.wall_left= self._checkWall_left()
        self.wall_right= self._checkWall_right()
        self.wall_top= self._checkWall_top()
        self.wall_bottom= self._checkWall_bottom()
        
    def _checkWall_left(self):
        if self.pos_x == 0:
            return True
        else:
            return False
        
    def _checkWall_right(self):
        if self.pos_x == self.maxW-1:
            return True
        else:
            return False
        
    def _checkWall_top(self):
        if self.pos_y == 0:
            return True
        else:
            return False
        
    def _checkWall_bottom(self):
        if self.pos_y == self.maxH-1:
            return True
        else:
            return False
        
    def getVaildPoint(self):
        vaildPoint_pos=[]   #vaildPoint_pos = [(x1,y1),(x2,y2),...]
        if not self.wall_left and not self.wall_top:
            vaildPoint_pos.append((self.pos_x-1, self.pos_y-1))
        if not self.wall_top:
            vaildPoint_pos.append((self.pos_x, self.pos_y-1))
        if not self.wall_right and not self.wall_top:
            vaildPoint_pos.append((self.pos_x+1, self.pos_y-1))
        if not self.wall_right:
            vaildPoint_pos.append((self.pos_x+1, self.pos_y))
        if not self.wall_right and not self.wall_bottom:
            vaildPoint_pos.append((self.pos_x+1, self.pos_y+1))
        if not self.wall_bottom:
            vaildPoint_pos.append((self.pos_x, self.pos_y+1))
        if not self.wall_left and not self.wall_bottom:
            vaildPoint_pos.append((self.pos_x-1, self.pos_y+1))
        if not self.wall_left:
            vaildPoint_pos.append((self.pos_x-1, self.pos_y))
        if vaildPoint_pos==[]:
            return False
        else:
            return tuple(vaildPoint_pos)
        
        
class Organism(PointAttributes):
    def __init__(self,x,y):
        super().__init__(x,y)
        NaturalRules.register(self)
        self.life = True
        
    def setLife(self,state):
        self.life=state
        
    def position(self):
        return (self.pos_x,self.pos_y)
    
    def generation(self,lifeArea):
        def _lifeCheck(vaildArea,lifeArea):
            if vaildArea:
                count=0
                for pos in vaildArea:
                    if pos in lifeArea:
                        count+=1
                if count<2 or count>3:
                    return False
                else:
                    return True
            else:
                return False
        self.setLife(_lifeCheck(self.getVaildPoint(),lifeArea))
        
        
class Inoculation(PointAttributes):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.inoculation = False
        
    def __call__(self):
        return self.inoculation
    
    def setInoculation(self,state):
        self.inoculation = state
        
        
class Conway():
    def __init__(self,Natural,F_visionUpdate):
        self.Natural=Natural
        self.NaturalSize=NaturalRules.getNaturalSize()
        self.visionUpdate=F_visionUpdate
        self.Loop=False
        self.isStop=True
        
    def destroy(self):
        self.Loop=False
        self.Natural.destroy()
        self.Natural=None
        self.NaturalSize=None
        self.visionUpdate=None
        gc.collect()
        
    def stopLoop(self):
        self.Loop=False
        
    def startLoop(self):
        self.Loop=True
        self.isStop=False
        
    def drawOrganism(self,pos_x,pos_y):
        if not NaturalRules.isLife((pos_x,pos_y)):
            Organism(pos_x,pos_y)
            self.visionUpdate()
            
    def CreateOrganism(self,OrganismNumber,colonyRate=3,villageRate=None,villageDistance=10):
        assert OrganismNumber<=self.NaturalSize[0]*self.NaturalSize[1]
        _count=OrganismNumber
        _village_flag=False
        _viliage_on=False
        _x,_y=0,0
        __x,__y=0,0
        while True:
            _x=random.randint(0,self.NaturalSize[0]-1)
            _y=random.randint(0,self.NaturalSize[1]-1)
            if _village_flag and not _viliage_on:
                if random.randint(0,villageRate):
                    _village_flag=False
                else:
                    _viliage_on=True
            if _viliage_on:
                _ret1=self.calcDistance((_x,_y),(__x,__y))
                _ret2=NaturalRules.isLife((_x,_y))
                if self.calcDistance((_x,_y),(__x,__y))>villageDistance:
                    if not NaturalRules.isLife((_x,_y)):
                        continue
                    else:
                        _viliage_on=False
                        _village_flag=False
            if not NaturalRules.isLife((_x,_y)):
                Organism(_x,_y)
                _count-=1
                if _count==0:
                    return
                while random.randint(0,colonyRate):
                    next_pos=random.choice([(0,0),(0,1),(1,0),(1,1),(0,-1),(-1,0),(-1,-1),(-1,1),(1,-1)])
                    _x+=next_pos[0]
                    _y+=next_pos[1]
                    if not NaturalRules.isLife((_x,_y)):
                        Organism(_x,_y)
                        _count-=1
                        if _count==0:
                            return
                    else:
                        break
                else:
                    if villageRate!=None and villageRate!=0:
                        __x,__y=_x,_y
                        _village_flag=True
            else:
                continue
            
    def calcDistance(self,pos1,pos2):
        return int(round(math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)))
    
    def Generation(self):
        VaildArea=[]
        LifeArea=NaturalRules.getLifePositon()
        for organism in self.Natural.Ecosphere[:]:
            _ret=organism.getVaildPoint()
            if _ret:
                VaildArea.extend(_ret)
            organism.generation(LifeArea)
        VaildBornArea=NaturalRules.getVaildBornArea(list(set(VaildArea)))
        NaturalRules.scanBorn(VaildBornArea,LifeArea)
        NaturalRules.Born()
        self.clearGarbage()
        
    def clearGarbage(self):
        for organism in self.Natural.Ecosphere[:]:
            if not organism.life:
                NaturalRules.unregister(organism)
        self.Natural.Inoculation_Area.clear()
        gc.collect()
        
    def getOrganismNumber(self):
        return NaturalRules.getNumber()
    
    def mainloop(self):
        self.Loop=True
        while self.Loop:
            try:
                self.Generation()
                self.visionUpdate()
            except:
                pass
        self.isStop=True
        
        
class GUI:
    def __init__(self):
        self.GameThread=None
        self.LifeGame=None
        self.initOrganism=500
        self.initColonyRate=3
        self.initVillageRate=5
        self.initVillageDistance=10
        self.initSize_width=600
        self.initSize_height=600
        self.colonyRate=3
        self.villageRate=5
        self.villageDistance=10
        self.visionSize=1  #1-16
        self.visionFocusPos=[0,0]
        self._min_size=100
        #----
        self.visionMoveUp_Flag=False
        self.visionMoveDown_Flag=False
        self.visionMoveLeft_Flag=False
        self.visionMoveRight_Flag=False
        #----
        self.visionDrop_Flag=False
        self.visionDrop_x=0
        self.visionDrop_y=0
        #----
        self.visionFocusZoom_Flag=False
    def pixelSize(self):
        return int(24/(self.visionSize))
    
    def visionCalculate(self):
        def _isInclude(pos_x,pos_y):
            if pos_x<self.visionFocusPos[0] or pos_x>self.visionFocusPos[0]+self._min_size*self.pixelSize()-1:
                return False
            if pos_y<self.visionFocusPos[1] or pos_y>self.visionFocusPos[1]+self._min_size*self.pixelSize()-1:
                return False
            return True    
        
        NautralData=NaturalRules.getLifePositon()
        _showData=[]
        for pos in NautralData:
            if _isInclude(*pos):
                _showData.append(pos)
        correctPos=[]
        _size=(self.visionSize*2)
        for pos in _showData:
            correctPos.append((int((pos[0]-self.visionFocusPos[0])*_size) ,int((pos[1]-self.visionFocusPos[1])*_size)))
        return correctPos
    
    def main(self):
        self.root=Tk()
        self.root.geometry('1040x640')
        self.root.resizable(width=False, height=False)
        self.root.title('Conway Life Game')
        self.root.protocol('WM_DELETE_WINDOW',self.close)
        _Frame_vision=LabelFrame(self.root,width=620,height=620,text='Vision')
        _Frame_vision.place(anchor=CENTER,relx=0.5,rely=0.5,x=-210)
        _Frame_Frame_vision=Frame(_Frame_vision,width=600,height=600)
        _Frame_Frame_vision.pack()
        self._Canvas_vision=Canvas(_Frame_Frame_vision,width=600,height=600,bg='black')
        self._Canvas_vision.pack()
        self._Canvas_vision.bind_all('<MouseWheel>',self.visionWheelResize)
        self._Canvas_vision.bind('<Motion>',self.visionMove)
        self._Canvas_vision.bind('<Leave>',self.visionLostFocus)
        self._Canvas_vision.bind('<Button-1>',self.visionDraw)        
        self._Canvas_vision.bind('<B1-Motion>',self.visionDraw)
        self._Canvas_vision.bind('<B3-Motion>',self.visionDrop)
        self._Canvas_vision.bind('<ButtonPress-3>',self.visionDropPress)
        self._Canvas_vision.bind('<ButtonRelease-3>',self.visionDropRelease)
        _Frame_control=LabelFrame(self.root,width=400,height=620,text='Control')
        _Frame_control.place(anchor=CENTER,relx=0.5,rely=0.5,x=300)
        _Frame_setting=LabelFrame(_Frame_control,width=380,height=330,text='Setting')
        _Frame_setting.place(anchor=CENTER,relx=0.5,rely=0.5,y=-135)
        _Frame_Info=LabelFrame(_Frame_control,width=380,height=80,text='Info')
        _Frame_Info.place(anchor=CENTER,relx=0.5,rely=0.5,y=70)
        _Frame_Button=LabelFrame(_Frame_control,width=380,height=180,text='Button')
        _Frame_Button.place(anchor=CENTER,relx=0.5,rely=0.5,y=200)
        #----button----#
        self._Button_start=Button(_Frame_Button,text='Start',width=40,command=self.start)
        self._Button_start.place(anchor=CENTER,relx=0.5,rely=0.3)
        self._Button_stop=Button(_Frame_Button,text='Stop',width=40,command=self.stop)
        self._Button_stop.place(anchor=CENTER,relx=0.5,rely=0.55)
        self._Button_reset=Button(_Frame_Button,text='ResetGame',width=40,command=self.resetLifeGame)
        self._Button_reset.place(anchor=CENTER,relx=0.5,rely=0.8)
        self._Label_reset=Label(_Frame_Button,text='',foreground='red')
        self._Label_reset.place(anchor=CENTER,relx=0.5,rely=0.1)
        #----button----#
        #----Info----#
        self._Label_numberOrganism=Label(_Frame_Info,text='Organism Number:0')
        self._Label_numberOrganism.place(anchor=W,relx=0.1,rely=0.3,y=-2,x=65)
        self._Label_visionRate=Label(_Frame_Info,text='Vision SizeRate:1')
        self._Label_visionRate.place(anchor=W,relx=0.1,rely=0.6,y=2,x=66)
        #----Info----#
        #----Setting----#
        _Label_Size_W=Label(_Frame_setting,text='Natural Width:')
        _Label_Size_W.place(anchor=W,relx=0.13,rely=0.1,x=0,y=0)
        _Label_Size_H=Label(_Frame_setting,text='Natural Height:')
        _Label_Size_H.place(anchor=W,relx=0.13,rely=0.25,x=0,y=0)
        _Label_InitOrganism=Label(_Frame_setting,text='Init Organism:')
        _Label_InitOrganism.place(anchor=W,relx=0.13,rely=0.4,x=0,y=0)
        self._Label_colonyRate=Label(_Frame_setting,text='Colony Rate:3'+'  --Bigger get more probability')
        self._Label_colonyRate.place(anchor=W,relx=0.13,rely=0.65,x=0,y=0)
        self._Label_villageRate=Label(_Frame_setting,text='Village Rate:5'+'  --Smaller get more probability')
        self._Label_villageRate.place(anchor=W,relx=0.13,rely=0.8,x=0,y=0)
        self._Label_villageDistance=Label(_Frame_setting,text='Village Distance:10')
        self._Label_villageDistance.place(anchor=W,relx=0.13,rely=0.95,x=0,y=0)
        self._Spinbox_Size_width=Spinbox(_Frame_setting,width=20,from_=600,to=10000,increment=100)
        self._Spinbox_Size_width.insert(0,self.initSize_width)
        self._Spinbox_Size_width.place(anchor=W,relx=0.4,rely=0.1,x=0,y=0)
        self._Spinbox_Size_height=Spinbox(_Frame_setting,width=20,from_=600,to=10000,increment=100)
        self._Spinbox_Size_height.insert(0,self.initSize_height)
        self._Spinbox_Size_height.place(anchor=W,relx=0.4,rely=0.25,x=0,y=0)
        self._Spinbox_InitOrganism=Spinbox(_Frame_setting,width=20,from_=0,to=10000,increment=100)
        self._Spinbox_InitOrganism.insert(0,self.initOrganism)
        self._Spinbox_InitOrganism.place(anchor=W,relx=0.4,rely=0.4,x=0,y=0)
        self._Scale_colonyRate=Scale(_Frame_setting,from_=0,to=15,orient=HORIZONTAL,length=280,command=self.colonyRateChange)
        self._Scale_colonyRate.set(self.initColonyRate)
        self._Scale_colonyRate.place(anchor=CENTER,relx=0.5,rely=0.6,x=0,y=-5)
        self._Scale_villageRate=Scale(_Frame_setting,from_=0,to=15,orient=HORIZONTAL,length=280,command=self.villageRateChange)
        self._Scale_villageRate.set(self.initVillageRate)
        self._Scale_villageRate.place(anchor=CENTER,relx=0.5,rely=0.75,x=0,y=-5)
        self._Scale_villageDistance=Scale(_Frame_setting,from_=3,to=30,orient=HORIZONTAL,length=280,command=self.villageDistanceChange)
        self._Scale_villageDistance.set(self.initVillageDistance)
        self._Scale_villageDistance.place(anchor=CENTER,relx=0.5,rely=0.9,x=0,y=-5)
        self._Scale_visionSize=Scale(_Frame_setting,from_=1,to=16,orient=VERTICAL,length=300,command=self.visionSizeChange)
        self._Scale_visionSize.set(self.visionSize)
        self._Scale_visionSize.place(anchor=CENTER,relx=0.01,rely=0.5,x=10,y=-5)
        #----Setting----#
        _Label_Author=Label(_Frame_control,text='author:Aikko',foreground='#B0B0B0')
        _Label_Author.place(anchor=SE,relx=0.99,rely=0.99,x=5,y=5)
        self.visionUpdate()
        self.root.mainloop()
    
    def colonyRateChange(self,event):
        _tmp=int(round(float(event)))
        if _tmp!=self.colonyRate:
            self.colonyRate=_tmp
            self._Label_colonyRate['text']='Colony Rate:'+str(self.colonyRate)+'  --Bigger get more probability'
            self.visionUpdate()
    
    def villageRateChange(self,event):
        _tmp=int(round(float(event)))
        if _tmp!=self.villageRate:
            self.villageRate=_tmp
            self._Label_villageRate['text']='Village Rate:'+str(self.villageRate)+'  --Smaller get more probability'
            self.visionUpdate()
        
    def villageDistanceChange(self,event):
        _tmp=int(round(float(event)))
        if _tmp!=self.villageDistance:
            self.villageDistance=_tmp
            self._Label_villageDistance['text']='Village Distance:'+str(self.villageDistance)
            self.visionUpdate()
    
    def visionDraw(self,event):
        def _visionDrawPos(pos_x,pos_y):
            pos_x=int(pos_x/2/self.visionSize)
            pos_y=int(pos_y/2/self.visionSize)
            pos_x=pos_x+self.visionFocusPos[0]
            pos_y=pos_y+self.visionFocusPos[1]
            return pos_x, pos_y
        if self.LifeGame:
            _x,_y=_visionDrawPos(event.x,event.y)
            self.LifeGame.drawOrganism(_x,_y)
    
    def visionDropPress(self,event):
        self.visionDrop_x,self.visionDrop_y=event.x,event.y
        self.visionDrop_Flag=True
    
    def visionDropRelease(self,event):
        self.visionDrop_Flag=False
    
    def visionDrop(self,event):
        if self.visionDrop_Flag:
            _size_x,_size_y=self.LifeGame.NaturalSize
            self.visionFocusPos[0]=self.visionFocusPos[0]-(event.x-self.visionDrop_x)/2/self.visionSize
            if self.visionFocusPos[0]<0:
                self.visionFocusPos[0]=0            
            if self.visionFocusPos[0]+int(_size_x/self.visionSize)>_size_x+int((_size_x-300)/self.visionSize):
                self.visionFocusPos[0]=_size_x+int((_size_x-300)/self.visionSize)-int(_size_x/self.visionSize)
            self.visionFocusPos[1]=self.visionFocusPos[1]-(event.y-self.visionDrop_y)/2/self.visionSize
            if self.visionFocusPos[1]<0:
                self.visionFocusPos[1]=0
            if self.visionFocusPos[1]+int(_size_y/self.visionSize)>_size_y+int((_size_y-300)/self.visionSize):
                self.visionFocusPos[1]=_size_y+int((_size_y-300)/self.visionSize)-int(_size_y/self.visionSize)
            self.visionDrop_x,self.visionDrop_y=event.x,event.y
            self.visionUpdate()
        
    def visionMove(self,event):
        _length=30
        self.visionFocusZoom_Flag=True
        if not self.visionDrop_Flag:
            if event.x<_length:
                if not self.visionMoveLeft_Flag:
                    self.root.after(100,self.visionMoveLeft)
                    self.visionMoveLeft_Flag=True
            else:
                self.visionMoveLeft_Flag=False        
            if event.x>600-_length:
                if not self.visionMoveRight_Flag:
                    self.root.after(100,self.visionMoveRight)
                    self.visionMoveRight_Flag=True
            else:
                self.visionMoveRight_Flag=False
            if event.y<_length:
                if not self.visionMoveUp_Flag:
                    self.root.after(100,self.visionMoveUp)
                    self.visionMoveUp_Flag=True
            else:
                self.visionMoveUp_Flag=False
            if event.y>600-_length:
                if not self.visionMoveDown_Flag:
                    self.root.after(100,self.visionMoveDown)
                    self.visionMoveDown_Flag=True
            else:
                self.visionMoveDown_Flag=False
            
    def visionLostFocus(self,event):
        self.visionMoveUp_Flag=False
        self.visionMoveDown_Flag=False
        self.visionMoveLeft_Flag=False
        self.visionMoveRight_Flag=False
        self.visionDrop_Flag=False
        self.visionFocusZoom_Flag=False
    
    def visionMoveUp(self):
        _,_size_y=self.LifeGame.NaturalSize
        if self.visionFocusPos[1]>0:
            self.visionFocusPos[1]-=int(10/self.visionSize) if int(10/self.visionSize)>0 else 1
            if self.visionFocusPos[1]<0:
                self.visionFocusPos[1]=0
            self.visionUpdate()
        if self.visionMoveUp_Flag and not self.visionDrop_Flag:
            self.root.after(100,self.visionMoveUp)
            
    def visionMoveDown(self):
        _,_size_y=self.LifeGame.NaturalSize
        if self.visionFocusPos[1]+int(_size_y/self.visionSize)<_size_y+int((_size_y-300)/self.visionSize):
            self.visionFocusPos[1]+=int(10/self.visionSize) if int(10/self.visionSize)>0 else 1
            if self.visionFocusPos[1]+int(_size_y/self.visionSize)>_size_y+int((_size_y-300)/self.visionSize):
                self.visionFocusPos[1]=_size_y+int((_size_y-300)/self.visionSize)-int(_size_y/self.visionSize)
            self.visionUpdate()
        if self.visionMoveDown_Flag and not self.visionDrop_Flag:
            self.root.after(100,self.visionMoveDown)
            
    def visionMoveLeft(self):
        _size_x,_=self.LifeGame.NaturalSize
        if self.visionFocusPos[0]>0:
            self.visionFocusPos[0]-=int(10/self.visionSize) if int(10/self.visionSize)>0 else 1
            if self.visionFocusPos[0]<0:
                self.visionFocusPos[0]=0
            self.visionUpdate()
        if self.visionMoveLeft_Flag and not self.visionDrop_Flag:
            self.root.after(100,self.visionMoveLeft)
            
    def visionMoveRight(self):
        _size_x,_=self.LifeGame.NaturalSize
        if self.visionFocusPos[0]+int(_size_x/self.visionSize)<_size_x+int((_size_x-300)/self.visionSize):
            self.visionFocusPos[0]+=int(10/self.visionSize) if int(10/self.visionSize)>0 else 1
            if self.visionFocusPos[0]+int(_size_x/self.visionSize)>_size_x+int((_size_x-300)/self.visionSize):
                self.visionFocusPos[0]=_size_x+int((_size_x-300)/self.visionSize)-int(_size_x/self.visionSize)
            self.visionUpdate()
        if self.visionMoveRight_Flag and not self.visionDrop_Flag:
            self.root.after(100,self.visionMoveRight)

    def visionSizeChange(self,event):
        _size_x,_size_y=self.LifeGame.NaturalSize
        if int(float(event))!=self.visionSize:
            _before=self.visionSize
            self.visionSize=int(float(event))
            if self.visionSize>_before:
                self.visionFocusPos[0]+=int(abs(((_size_x-int((_size_x-300)/self.visionSize))/(_before)-_size_x/self.visionSize)/2))
                self.visionFocusPos[1]+=int(abs(((_size_y-int((_size_y-300)/self.visionSize))/(_before)-_size_y/self.visionSize)/2))
                if self.visionFocusPos[0]+int(_size_x/self.visionSize)>_size_x+int((_size_x-300)/self.visionSize):
                    self.visionFocusPos[0]=_size_x+int((_size_x-300)/self.visionSize)-int(_size_x/self.visionSize)
                if self.visionFocusPos[1]+int(_size_y/self.visionSize)>_size_y+int((_size_y-300)/self.visionSize):
                    self.visionFocusPos[1]=_size_y+int((_size_y-300)/self.visionSize)-int(_size_y/self.visionSize) 
            else:    
                self.visionFocusPos[0]-=int(abs(((_size_x+int((_size_x-300)/self.visionSize))/(_before)-_size_x/self.visionSize)/2))
                self.visionFocusPos[1]-=int(abs(((_size_y+int((_size_y-300)/self.visionSize))/(_before)-_size_y/self.visionSize)/2))
                if self.visionFocusPos[0]<0:
                    self.visionFocusPos[0]=0
                if self.visionFocusPos[1]<0:
                    self.visionFocusPos[1]=0
                if self.visionFocusPos[0]+int(_size_x/self.visionSize)>_size_x+int((_size_x-300)/self.visionSize):
                    self.visionFocusPos[0]=_size_x+int((_size_x-300)/self.visionSize)-int(_size_x/self.visionSize)
                if self.visionFocusPos[1]+int(_size_y/self.visionSize)>_size_y+int((_size_y-300)/self.visionSize):
                    self.visionFocusPos[1]=_size_y+int((_size_y-300)/self.visionSize)-int(_size_y/self.visionSize)
            self._Label_visionRate['text']='Vision Rate:'+str(self.visionSize)
            self.visionUpdate()

    def visionWheelResize(self,event):
        _size_x,_size_y=self.LifeGame.NaturalSize
        def _visionABSPos(pos_x,pos_y,state):
            pos_x=int(pos_x/2/(self.visionSize+1*state))
            pos_y=int(pos_y/2/(self.visionSize+1*state))
            pos_x=pos_x+self.visionFocusPos[0]
            pos_y=pos_y+self.visionFocusPos[1]
            return pos_x, pos_y
        
        if event.delta>0:
            if self.visionSize<16:
                self.visionSize+=1
                if self.visionSize>16:
                    self.visionSize=16
                if self.visionFocusZoom_Flag:
                    _x,_y=_visionABSPos(event.x,event.y,-1)
                    self.visionFocusPos[0]=_x-((event.x/600) * (_size_x/(self.visionSize))*0.5)
                    self.visionFocusPos[1]=_y-((event.y/600) * (_size_y/(self.visionSize))*0.5)
                else:
                    self.visionFocusPos[0]+=int(abs(((_size_x-int((_size_x-300)/self.visionSize))/(self.visionSize-1)-_size_x/self.visionSize)*0.5))
                    self.visionFocusPos[1]+=int(abs(((_size_y-int((_size_y-300)/self.visionSize))/(self.visionSize-1)-_size_y/self.visionSize)*0.5))
                if self.visionFocusPos[0]+int(_size_x/self.visionSize)>_size_x+int((_size_x-300)/self.visionSize):   
                    self.visionFocusPos[0]=_size_x+int((_size_x-300)/self.visionSize)-int(_size_x/self.visionSize)
                if self.visionFocusPos[1]+int(_size_y/self.visionSize)>_size_y+int((_size_y-300)/self.visionSize):
                    self.visionFocusPos[1]=_size_y+int((_size_y-300)/self.visionSize)-int(_size_y/self.visionSize)
                self._Label_visionRate['text']='Vision Rate:'+str(self.visionSize)
                self._Scale_visionSize.set(self.visionSize)
                self.visionUpdate()
        else:
            if self.visionSize>1:
                self.visionSize-=1
                if self.visionSize<1:
                    self.visionSize=1
                if self.visionFocusZoom_Flag:
                    _x,_y=_visionABSPos(event.x,event.y,1)
                    self.visionFocusPos[0]=_x-((event.x/600) * (_size_x/(self.visionSize))*0.5)
                    self.visionFocusPos[1]=_y-((event.y/600) * (_size_y/(self.visionSize))*0.5)
                else:
                    self.visionFocusPos[0]-=int(abs(((_size_x+int((_size_x-300)/self.visionSize))/(self.visionSize+1)-_size_x/self.visionSize)*0.5))
                    self.visionFocusPos[1]-=int(abs(((_size_y+int((_size_y-300)/self.visionSize))/(self.visionSize+1)-_size_y/self.visionSize)*0.5))
                if self.visionFocusPos[0]<0:
                    self.visionFocusPos[0]=0                        
                if self.visionFocusPos[1]<0:
                    self.visionFocusPos[1]=0
                if self.visionFocusPos[0]+int(_size_x/self.visionSize)>_size_x+int((_size_x-300)/self.visionSize):
                    self.visionFocusPos[0]=_size_x+int((_size_x-300)/self.visionSize)-int(_size_x/self.visionSize)            
                if self.visionFocusPos[1]+int(_size_y/self.visionSize)>_size_y+int((_size_y-300)/self.visionSize):
                    self.visionFocusPos[1]=_size_y+int((_size_y-300)/self.visionSize)-int(_size_y/self.visionSize)                   
                self._Label_visionRate['text']='Vision Rate:'+str(self.visionSize)
                self._Scale_visionSize.set(self.visionSize)
                self.visionUpdate()

    def close(self):
        self.GameThread=None
        self.LifeGame.Loop=False
        self.root.destroy()
        
    def createLoop(self):
        if self.GameThread is None and self.LifeGame is not None and self.LifeGame.Loop==False:
            self.GameThread=threading.Thread(target=self.LifeGame.mainloop)
            self.GameThread.start()
        
    def visionUpdate(self):
        self._Canvas_vision.delete('all')
        vision_Pos=self.visionCalculate()
        _pixelSize=int(self.visionSize*2)
        for pos_x,pos_y in vision_Pos:
            self._Canvas_vision.create_rectangle(pos_x,pos_y,pos_x+_pixelSize,pos_y+_pixelSize,fill='white')
        self._Canvas_vision.update()
        self._Label_numberOrganism['text']='Organism Number:'+str(self.LifeGame.getOrganismNumber())
        self._Label_numberOrganism.update()
        
    def start(self):
        if self.LifeGame is not None:
            if self.LifeGame.Loop==False:
                self.createLoop()
                
    def stop(self):
        if self.LifeGame is not None:
            if self.LifeGame.Loop==True:
                self.LifeGame.stopLoop()
                self.GameThread=None
                
    def setLifeGame(self,initOrganism,colonyRate=3,villageRate=5,villageDistance=5):
        self.LifeGame=Conway(Natural[0],self.visionUpdate)
        self.LifeGame.CreateOrganism(initOrganism,colonyRate,villageRate,villageDistance)
        
    def resetLifeGame(self,size=(600,600)):
        global Natural
        self._Label_reset['text']='Reseting...'
        self.visionUpdate()
        self.stop()
        while not self.LifeGame.isStop:
            pass
        Natural[0].destroy()
        self.LifeGame.destroy()
        Natural.clear()
        del self.LifeGame
        try:
            size_x=int(round(eval(self._Spinbox_Size_width.get())))
            size_y=int(round(eval(self._Spinbox_Size_height.get())))
        except:
            Natural.append(NaturalEnvironment((size[0],size[1]),"Conway's Life Game"))
        else:
            Natural.append(NaturalEnvironment((size_x,size_y),"Conway's Life Game"))
        NaturalRules.resetNatural()
        self.visionSize=1
        self.visionFocusPos=[0,0]
        initOrganism=int(round(eval(self._Spinbox_InitOrganism.get())))
        self.setLifeGame(initOrganism,self.colonyRate,self.villageRate,self.villageDistance)
        gc.collect()
        self._Label_reset['text']=''
        self._Scale_visionSize.set(self.visionSize)
        self.visionUpdate()
    
if __name__ == '__main__':
    Game=GUI()
    Game.setLifeGame(Game.initOrganism)
    Game.main()
