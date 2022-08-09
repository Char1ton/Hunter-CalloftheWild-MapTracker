from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import pandas as pd

#Button Functions---------------------------------------------------------------------------------------------------------------------------------
#Map Selection
def map_selection(root,map_sel):

    global Map

    Map=map_sel.get()
    root.destroy()
    #Fault Exception
    if Map=='':
        MainWidget.Init()
    else:
        MainWidget.MapView(Map)

#Map Marking  
def AnimalPopUp(top,anisel,medal,x,y):
    #Fault Exception
    ani=anisel.get()
    if anisel.get()=='':
        PopUpDestroy(top)
    elif medal.get()=='':
        medal='None'
        #Mark Maker
        MarkMaker(anisel.get(),medal,x,y)
        #Destroy PopUp
        PopUpDestroy(top)
    else:
        #Mark Maker
        MarkMaker(anisel.get(),medal.get(),x,y)
        #Destroy PopUp
        PopUpDestroy(top)

#Clear All Function
def ClearAll(top,MS):
    MSOther=MS[MS.Map != Map]
    MSMod=MSOther.reset_index(drop=True)
    MSMod.to_csv('Maps_Storage.csv')

    top.destroy()
    canv.delete('marks')
    
#Undo Function
def Undo(top,MS):
    MS=pd.read_csv('Maps_Storage.csv',index_col=0)
    MSOther=MS[MS.Map != Map]
    MSMap=MS[MS.Map == Map]
    MSMap=MSMap[:-1]
    MSMod=pd.concat([MSOther,MSMap],ignore_index=True)
    MSMod.reset_index(drop=True)
    MSMod.to_csv('Maps_Storage.csv')

    top.destroy()
    canv.delete('marks')
    for i in range(len(MSMod)):
            if MSMod.at[i,'Map'] == Map:
                OvalMaker(Animal_Color_Dict[Map][MSMod.at[i,'Animal']],MSMod.at[i,'x'],MSMod.at[i,'y'],canv)

#Reselect Map Functions
def Yes(top,window):
    top.destroy()
    window.destroy()
    MainWidget.Init()

#Filter Function for Medals
def Fil(bottom,name,animal):
    med=name.get()
    fsh=animal.get()
    FMS=pd.read_csv('Maps_Storage.csv',index_col=0)
    canv.delete('marks')

    for i in range(len(FMS)):
        if FMS.at[i,'Map'] == Map:
            if med=='All Medals':
                 if fsh=='All Animals':
                      OvalMaker(Animal_Color_Dict[Map][FMS.at[i,'Animal']],FMS.at[i,'x'],FMS.at[i,'y'],canv)
                 elif FMS.at[i,'Animal']==fsh:
                     OvalMaker(Animal_Color_Dict[Map][FMS.at[i,'Animal']],FMS.at[i,'x'],FMS.at[i,'y'],canv)
            elif FMS.at[i,'Medal']==med:
                if fsh=='All Animals':
                    OvalMaker(Animal_Color_Dict[Map][FMS.at[i,'Animal']],FMS.at[i,'x'],FMS.at[i,'y'],canv)
                elif FMS.at[i,'Animal']==fsh:
                    OvalMaker(Animal_Color_Dict[Map][FMS.at[i,'Animal']],FMS.at[i,'x'],FMS.at[i,'y'],canv)
    
    
    bottom.destroy()
#End Of Button Functions-----------------------------------------------------------------------------------------------------------------------

#Helper Functions-----------------------------------------------------------------------------------------------------------------------------
#Destroy Tk boxes
def PopUpDestroy(PopUp):
    PopUp.destroy()
#Make Mark
def OvalMaker(col,x,y,widg):  
    x1, y1 = (x - 4), (y - 4)
    x2, y2 = (x + 4), (y + 4)
    widg.create_oval(x1, y1, x2, y2, fill=col,tags='marks')

def MarkMaker(ani,med,x,y):
    #Marker Creation 
    col=Animal_Color_Dict[Map][ani]
    OvalMaker(col,x,y,canv)

    #Marker Storage
    MS=MS=pd.read_csv('Maps_Storage.csv',index_col=0)
    df=pd.DataFrame([[Map,ani,x,y,med]],columns=['Map','Animal','x','y','Medal'])
    pf=pd.concat([MS,df],ignore_index=True)
    pf.to_csv('Maps_Storage.csv')

    return
#End of Helper Functions--------------------------------------------------------------------------------------------------------------------------------

#MainWidget--------------------------------------------------------------------------------------------------------------------------------------------------    
#Class Contains All Widgets; Init widget is recallable with canvas interaction, restarting the map selection from the tkinter root
class MainWidget:
    def Init():
        
        global Map_Animal_Dict, Animal_Color_Dict, Map_Pic_Dict, Map_Storage
        
        Maps=['Hirschfelden','Layton Lakes','Vurhonga','Parque Fernando','Yukon Valley','Cuatro Colinas','Silver Ridge Peaks','Te Awaroa','Rancho del Arroyo','Mississippi Acres','Revontuli Coast']

        Map_Animal_Dict={'Hirschfelden':['Canada Goose','European Rabbit','Red Fox','Roe Deer','Fallow Deer','Wild Boar','Red Deer','European Bison'],
                         'Layton Lakes':['White-Tailed Jackrabbit','Mallard','Coyote','Blacktail Deer','Whitetail Deer','Black Bear','Roosevelt Elk','Moose'],
                         'Vurhonga':['Scrub Hare','Side Striped Jackal','Springbok','Warthog','Lesser Kudu','Blue Wildebeest','Gemsbok','Cape Buffalo','Lion'],
                         'Parque Fernando':['Cinnamon Teal','Blackbuck','Axis Deer','Puma','Mule Deer','Red Deer','Water Buffalo'],
                         'Yukon Valley':['Harlequin Duck','Red Fox','Gray Wolf','Caribou','Grizzly Bear','Moose','Plains Bison'],
                         'Cuatro Colinas':['European Hare','Roe Deer','Iberian Mouflon','Ronda Ibex','Beceite Ibex','Gredos Ibex','Southeastern Spanish Ibex','Wild Boar','Iberian Wolf'],
                         'Silver Ridge Peaks':['Merriam Turkey','Pronghorn','Mountain Goat','Bighorn Sheep','Mountain Lion','Mule Deer','Black Bear','Rocky Mountain Elk','Plains Bison'],
                         'Te Awaroa':['Merriam Turkey','European Rabbit','Chamois','Feral Goat','Sika Deer','Fallow Deer','Feral Pig','Red Deer'],
                         'Rancho del Arroyo':['Rio Grande Turkey','Ring-Necked Pheasant','Antelope Jackrabbit','Coyote','Mexican Bobcat','Collard Peccary','Bighorn Sheep','Whitetail Deer','Mule Deer'],
                         'Mississippi Acres':['Bobwhite Quail','Eastern Cottontail Rabbit','Eastern Wild Turkey','Gray Fox','Common Raccoon','Whitetail Deer','Wild Hog','American Alligator','Black Bear'],
                         'Revontuli Coast':['Eurasion Widgeon','Tundra Bean Goose','Eurasian Teal','Black Grouse','Goldeneye','Hazel Grouse','Mallard','Western Capercaillie','Tufted Duck','Rock Ptarmigan','Canada Goose','Willow Ptarmigan','Greylag Goose','Mountain Hare','Eurasian Lynx','Raccoon Dog','Whitetail Deer','Eurasian Brown Bear','Moose']}

        Animal_Color_Dict={'Hirschfelden':{'Canada Goose':'black','European Rabbit':'blue','Red Fox':'magenta','Roe Deer':'green','Fallow Deer':'white','Wild Boar':'yellow','Red Deer':'red','European Bison':'grey'},
                           'Layton Lakes':{'White-Tailed Jackrabbit':'gray','Mallard':'green','Coyote':'orange','Blacktail Deer':'black','Whitetail Deer':'white','Black Bear':'gold4','Roosevelt Elk':'magenta','Moose':'pink1'},
                           'Vurhonga':{'Scrub Hare':'white','Side Striped Jackal':'red','Springbok':'green','Warthog':'yellow','Lesser Kudu':'orange','Blue Wildebeest':'blue','Gemsbok':'gray','Cape Buffalo':'black','Lion':'gold'},
                           'Parque Fernando':{'Cinnamon Teal':'cyan','Blackbuck':'black','Axis Deer':'white','Puma':'gold','Mule Deer':'blue','Red Deer':'red','Water Buffalo':'gray'},
                           'Yukon Valley':{'Harlequin Duck':'green','Red Fox':'red','Gray Wolf':'gray','Caribou':'yellow','Grizzly Bear':'orange','Moose':'blue','Plains Bison':'black'},
                           'Cuatro Colinas':{'European Hare':'white','Roe Deer':'red','Iberian Mouflon':'blue','Ronda Ibex':'yellow','Beceite Ibex':'magenta','Gredos Ibex':'gray','Southeastern Spanish Ibex':'green','Wild Boar':'black','Iberian Wolf':'gold'},
                           'Silver Ridge Peaks':{'Merriam Turkey':'green','Pronghorn':'blue','Mountain Goat':'white','Bighorn Sheep':'gray','Mountain Lion':'gold','Mule Deer':'red','Black Bear':'black','Rocky Mountain Elk':'yellow','Plains Bison':'orange'},
                           'Te Awaroa':{'Merriam Turkey':'green','European Rabbit':'yellow','Chamois':'black','Feral Goat':'white','Sika Deer':'blue','Fallow Deer':'orange','Feral Pig':'magenta','Red Deer':'red'},
                           'Rancho del Arroyo':{'Rio Grande Turkey':'green','Ring-Necked Pheasant':'gold','Antelope Jackrabbit':'black','Coyote':'orange','Mexican Bobcat':'red','Collard Peccary':'blue','Bighorn Sheep':'gray','Whitetail Deer':'white','Mule Deer':'yellow'},
                           'Mississippi Acres':{'Bobwhite Quail':'gold','Eastern Cottontail Rabbit':'blue','Eastern Wild Turkey':'green','Gray Fox':'gray','Common Raccoon':'magenta','Whitetail Deer':'white','Wild Hog':'orange','American Alligator':'red','Black Bear':'black'},
                           'Revontuli Coast':{'Eurasion Widgeon':'DeepPink2','Tundra Bean Goose':'khaki','Eurasian Teal':'DeepSkyBlue4','Black Grouse':'LightBlue1','Goldeneye':'goldenrod1','Hazel Grouse':'yellow4','Mallard':'lime green','Western Capercaillie':'NavajoWhite2','Tufted Duck':'DarkOliveGreen2','Rock Ptarmigan':'cyan','Canada Goose':'saddle brown','Willow Ptarmigan':'blue','Greylag Goose':'gray','Mountain Hare':'red','Eurasian Lynx':'yellow','Raccoon Dog':'gold','Whitetail Deer':'white','Eurasian Brown Bear':'black','Moose':'green'}}
        
        Map_Pic_Dict={'Hirschfelden':'Hirschfelden.jpg','Layton Lakes':'LaytonLakes.jpg','Vurhonga':'Vurhonga.jpg','Parque Fernando':'Parque.jpg','Yukon Valley':'Yukon.jpg','Cuatro Colinas':'CuatroColinas.jpg','Silver Ridge Peaks':'SilverRidge.jpg','Te Awaroa':'TeAwaroa.jpg','Rancho del Arroyo':'Rancho.jpg','Mississippi Acres':'Mississippi.jpg','Revontuli Coast':'Revontuli.jpg'}

        Map_Storage=pd.read_csv('Maps_Storage.csv',index_col=0)

        #Root; Map and Animal Containers
        root=Tk()
        root.title('Hunter Maps')
        root.geometry('150x100')

        #Label
        label0=Label(root,text='Select Map')
        label0.place(x=5,y=5)
        
        #Buttons
        map_sel=Combobox(root,values=Maps)
        map_sel.place(x=5,y=25)
        confirm_butt=Button(root,text="Select",width=5,font=("Comic Sans",12),command=lambda:map_selection(root,map_sel))
        confirm_butt.place(x=5,y=50)

        root.mainloop()

    def MapView(Map):
        #Map root; Canvas Init and Interaction Creation

        global window

        window=Tk()
        window.title(Map)
        window.resizable(False,False)
        image=Image.open(Map_Pic_Dict[Map])
        image=image.resize((1200,800))
        img = ImageTk.PhotoImage(image)

        #Canvas Creation

        global canv

        canv = Canvas(window, width=1200, height=800, bg='white')
        canv.create_image(0,0,anchor=NW,image=img)
        canv.pack()

        FilMarks=Button(window,text='Filter',width=7,font=("Comic Sans",12))
        FilMarks.pack(side=LEFT,fill=BOTH,expand=YES)
        Legn=Button(window,text='Legend',width=7,font=("Comic Sans",12))
        Legn.pack(side=LEFT,fill=BOTH,expand=YES)
        UndBut=Button(window,text='Undo Previous Animal',width=10,font=("Comic Sans",12))
        UndBut.pack(side=LEFT,fill=BOTH,expand=YES)
        CleAll=Button(window,text='Clear All',width=7,font=("Comic Sans",12),bg='red')
        CleAll.pack(side=LEFT,fill=BOTH,expand=YES)
        
        #Init Filling For Map on Canvas
        for i in range(len(Map_Storage)):
            if Map_Storage.at[i,'Map'] == Map:
                OvalMaker(Animal_Color_Dict[Map][Map_Storage.at[i,'Animal']],Map_Storage.at[i,'x'],Map_Storage.at[i,'y'],canv)

        #Canvas Interaction
        canv.bind("<Button-1>",MainWidget.AniSel)
        canv.bind("<Button-3>",MainWidget.MapReset)
        FilMarks.bind("<Button-1>",MainWidget.FilMarks)
        Legn.bind("<Button-1>",MainWidget.Legend)
        UndBut.bind("<Button-1>",MainWidget.Undo)
        CleAll.bind("<Button-1>",MainWidget.Clear)

        window.mainloop()


    def Clear(self):
        top=Tk()
        top.geometry('200x100')

        #Label
        label=Label(top,text='Clear All Animals?')
        label.place(x=50,y=10)
        #Yes or No Buttons
        yes=Button(top,text='Yes',width=5,font=("Comic Sans",12),command=lambda:ClearAll(top,Map_Storage))
        yes.place(x=50,y=30)
        no=Button(top,text='No',width=5,font=("Comic Sans",12),command=lambda:PopUpDestroy(top))
        no.place(x=50,y=60)
        
    def MapReset(event):
        #Popup root
        top=Tk()
        top.geometry('200x100')
        #Label
        label=Label(top,text='Change Map?')
        label.place(x=50,y=10)
        #Yes or No Buttons
        yes=Button(top,text='Yes',width=5,font=("Comic Sans",12),command=lambda:Yes(top,window))
        yes.place(x=50,y=30)
        no=Button(top,text='No',width=5,font=("Comic Sans",12),command=lambda:PopUpDestroy(top))
        no.place(x=50,y=60)

    def FilMarks(self):
        bottom=Tk()
        bottom.geometry('300x300')

        #Label
        label0=Label(bottom,text='Select Medal')
        label0.place(x=50,y=15)
        label3=Label(bottom,text='Animal')
        label3.place(x=50,y=70)
        #Entry
        name=Combobox(bottom,values=['None','Bronze','Silver','Gold','Diamond','Great One','All Medals'])
        name.place(x=30,y=35)
        fish=Combobox(bottom,values=Map_Animal_Dict[Map]+['All Animals'])
        fish.place(x=30,y=90)
        
        #Button
        okay=Button(bottom,text='Okay',width=5,font=("Comic Sans",12),command=lambda:Fil(bottom,name,fish))
        okay.place(x=80,y=125)

    #Self Closing with Ex-out Button; No close Func
    def Legend(self):
        bottom=Tk()
        bottom.geometry('250x400')
        bottom.title("Legend")

        #Canvas
        LCanv=Canvas(bottom,width=250,height=400,bg='white')
        LCanv.pack()

        #Placements
        for i in range(len(Map_Animal_Dict[Map])):
            ov=OvalMaker(Animal_Color_Dict[Map][Map_Animal_Dict[Map][i]],50,i*20+20,LCanv)
            LCanv.create_text(150,i*20+20,text=Map_Animal_Dict[Map][i],fill='black',font=('Helvetica',12))
        
    def Undo(self):
        top=Tk()
        top.geometry('200x100')

        #Label
        label=Label(top,text='Undo Previous Animal?')
        label.place(x=50,y=10)
        #Yes or No Buttons
        yes=Button(top,text='Yes',width=5,font=("Comic Sans",12),command=lambda:Undo(top,Map_Storage))
        yes.place(x=50,y=30)
        no=Button(top,text='No',width=5,font=("Comic Sans",12),command=lambda:PopUpDestroy(top))
        no.place(x=50,y=60)
        
    def AniSel(event):
        top=Tk()
        top.geometry('220x180')

        #Animal Combobox
        label0=Label(top,text='Select Animal')
        label0.place(x=50,y=5)
        anisel=Combobox(top,values=Map_Animal_Dict[Map])
        anisel.place(x=50,y=35)

        #Medal Combobox
        label1=Label(top,text='Select Medal')
        label1.place(x=50,y=65)
        medal=Combobox(top,values=['None','Bronze','Silver','Gold','Diamond','Great One'])
        medal.place(x=50,y=95)

        #Select Button
        sel_button=Button(top,text='Mark',width=5,font=("Comic Sans",12),command=lambda:AnimalPopUp(top,anisel,medal,event.x,event.y))
        sel_button.place(x=90,y=120)
#End of MainWidget---------------------------------------------------------------------------------------------------------------------------------

if __name__== '__main__':
    MainWidget.Init()

        
    
