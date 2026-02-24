
import wx
import random
import numpy as np

from HypoModPy.hypomods import *
from HypoModPy.hypoparams import *
from HypoModPy.hypodat import *
from HypoModPy.hypogrid import *

#ID_heatflag = wx.NewIdRef()



class AgentMod(Mod):
    def __init__(self, mainwin, tag):
        Mod.__init__(self, mainwin, tag)

        if mainwin.modpath != "": self.path = mainwin.modpath + "/Agent"
        else: self.path = "Agent"

        if os.path.exists(self.path) == False: 
            os.mkdir(self.path)

        self.mainwin = mainwin

        self.protobox = AgentProtoBox(self, "proto", "Input Protocols", wx.Point(0, 0), wx.Size(320, 500))
        self.gridbox = GridBox(self, "Data Grid", wx.Point(0, 0), wx.Size(320, 500), 100, 20)
        self.agentbox = AgentBox(self, "agent", "AgentMod", wx.Point(0, 0), wx.Size(320, 500))

        # link mod owned boxes
        mainwin.gridbox = self.gridbox

        self.AddTool(self.agentbox)
        self.AddTool(self.gridbox)
        self.AddTool(self.protobox)

        self.agentbox.Show(True)
        self.modbox = self.agentbox

        self.ModLoad()
        print("Agent Model OK")

        self.agentdata = AgentDat()
        self.PlotData()
        self.graphload = True

        #for i in range(1, 100):
        #    self.agentdata.water[i] = 100


    ## PlotData() defines all the available plots, each linked to a data array in agentdata
    ##
    def PlotData(self):
        # Data plots
        #
        # AddPlot(PlotDat(data array, xfrom, xto, yfrom, yto, label string, plot type, bin size, colour), tag string)
        # ----------------------------------------------------------------------------------
        self.plotbase.AddPlot(PlotDat(self.agentdata.water, 0, 2000, 0, 5000, "water", "line", 1, "blue"), "water")
        self.plotbase.AddPlot(PlotDat(self.agentdata.salt, 0, 2000, 0, 100, "salt", "line", 1, "red"), "salt")
        self.plotbase.AddPlot(PlotDat(self.agentdata.osmo, 0, 2000, 0, 100, "osmo", "line", 1, "green"), "osmo")
        self.plotbase.AddPlot(PlotDat(self.agentdata.vaso, 0, 2000, 0, 100, "vaso", "line", 1, "purple"), "vaso")


    def DefaultPlots(self):
        if len(self.mainwin.panelset) > 0: self.mainwin.panelset[0].settag = "water"
        if len(self.mainwin.panelset) > 1: self.mainwin.panelset[1].settag = "salt"
        if len(self.mainwin.panelset) > 2: self.mainwin.panelset[2].settag = "osmo"


    def OnModThreadComplete(self, event):
        #runmute->Lock();
        #runflag = 0;
        #runmute->Unlock();

        # plot store test code
        # for i in range(1, 100):
        #     self.agentdata.water[i] = 200
        #self.agentdata.water.label = "plot test"

        self.mainwin.scalebox.GraphUpdateAll()
        #DiagWrite("Model thread OK\n\n")


    def OnModThreadProgress(self, event):
        self.agentbox.SetCount(event.GetInt())


    def RunModel(self):
        self.mainwin.SetStatusText("Agent Model Run")
        modthread = AgentModel(self)
        modthread.start()



class AgentDat():
    def __init__(self):
        self.storesize = 10000

        # initialise arrays for recording model variables (or any model values)
        self.water = datarray(self.storesize + 1)
        self.salt = pdata(self.storesize + 1)
        self.osmo = pdata(self.storesize + 1)
        self.vaso = pdata(self.storesize + 1)



class AgentBox(ParamBox):
    def __init__(self, mod, tag, title, position, size):
        ParamBox.__init__(self, mod, title, position, size, tag, 0, 1)

        self.autorun = True

        # Initialise Menu 
        self.InitMenu()

        # Model Flags
        #ID_randomflag = wx.NewIdRef()   # request a new control ID
        self.AddFlag("randomflag", "Fixed Random Seed", 0)         # menu accessed flags for switching model code

        paneltype = "Default"

        if paneltype == "Default": self.DefaultPanel()
        if paneltype == "Bristol": self.BristolPanel()
        if paneltype == "Work": self.WorkPanel()

        # Parameter controls
        #
        # AddCon(tag string, display string, initial value, click increment, decimal places)
        # ----------------------------------------------------------------------------------
        #self.paramset.AddCon("runtime", "Run Time", 2000, 1, 0)
        #self.paramset.AddCon("hstep", "h Step", 1, 0.1, 1)
        #self.paramset.AddCon("waterloss", "Water Loss", 0, 0.00001, 5)

        self.ParamLayout(2)   # layout parameter controls in two columns

        # ----------------------------------------------------------------------------------

        runbox = self.RunBox()
        paramfilebox = self.StoreBoxSync()

        ID_Proto = wx.NewIdRef()
        self.AddPanelButton(ID_Proto, "Proto", self.mod.protobox)
        ID_Grid = wx.NewIdRef()
        self.AddPanelButton(ID_Grid, "Grid", self.mod.gridbox)

        self.mainbox.AddSpacer(5)
        self.mainbox.Add(self.pconbox, 1, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        self.mainbox.AddStretchSpacer(5)
        self.mainbox.Add(runbox, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        self.mainbox.AddSpacer(5)
        self.mainbox.Add(paramfilebox, 0, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)	
        #self.mainbox.AddStretchSpacer()
        self.mainbox.Add(self.buttonbox, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 0)
        self.mainbox.AddSpacer(5)
        #self.mainbox.AddSpacer(2)
        self.panel.Layout()



    def DefaultPanel(self):

        self.AddFlag("randfood", "Random Food", 0)
        self.AddFlag("glycoflag", "Use Glycogen", 0)
        self.AddFlag("chamberflag", "Use Chamber", 0)
        self.AddFlag("adlibflag", "Ad Libitum", 0)


        # Parameter controls
        #
        # AddCon(tag string, display string, initial value, click increment, decimal places)
        # ----------------------------------------------------------------------------------

        self.paramset.AddCon("runtime", "Run Time", 2000, 1, 0)
        self.paramset.AddCon("hstep", "h Step", 1, 0.1, 1)
        self.paramset.AddCon("basecost", "Base Cost", 0, 1, 4)
        self.paramset.AddCon("feedthresh", "Feed Thresh", 0, 1, 2)
        self.paramset.AddCon("foodstep", "Feed Step", 0, 1, 2)
        self.paramset.AddCon("foodfreq", "Feed Freq", 0.01, 0.001, 4)
        self.paramset.AddCon("gluco_set", "Gluco Set", 1000, 1, 2)
        self.paramset.AddCon("glyco_rate", "Glyco Rate", 0.1, 0.01, 4)
        self.paramset.AddCon("glyco_max", "Glyco Max", 10000, 10, 1)
        self.paramset.AddCon("glyco_init", "Glyco Init", 0, 10, 1)
        self.paramset.AddCon("glyco_feed", "Glyco Feed", 500, 10, 1)
        self.paramset.AddCon("absorprate", "Absorp Rate", 0, 10, 2)
        self.paramset.AddCon("fullthresh", "Full Thresh", 0, 10, 1)
        self.paramset.AddCon("storecost_rate", "Store Rate", 0, 0.01, 5)
        self.paramset.AddCon("feedrate", "Feed Rate", 0.01, 0.001, 3)
        self.paramset.AddCon("energy_init", "Energy Init", 10000, 10, 1)
        self.paramset.AddCon("energy_max", "Energy Max", 10000, 10, 1)
        self.paramset.AddCon("gut_max", "Gut Max", 1000, 10, 1)
        self.paramset.AddCon("rewardbase", "Reward Base", 0.01, 0.001, 3)
        self.paramset.AddCon("gutfactor", "Gut Factor", 0.01, 0.001, 3)
        self.paramset.AddCon("fatfactor", "Fat Factor", 0.01, 0.001, 3)
        self.paramset.AddCon("reward_def_factor", "Reward Def", 0.01, 0.001, 3)
        self.paramset.AddCon("reward_tau", "Reward Tau", 0.01, 0.001, 5)
        self.paramset.AddCon("ghrelin_secrate", "Ghrelin Sec", 0, 0.001, 5)
        self.paramset.AddCon("ghrelin_decay", "Ghrelin Decay", 0, 0.001, 5)


    def BristolPanel(self):
        if self.ostype == "Mac":
           numwidth = 60
           labelwidth = 80
        else:
            numwidth = 60
            labelwidth = 70

        self.SetModFlag("randfood", "Random Feed", 0)
        self.SetModFlag("adlibflag", "Ad Libitum", 0)

        # Parameter controls
        #
        # AddCon(tag string, display string, initial value, click increment, decimal places)
        # ----------------------------------------------------------------------------------

        self.paramset.AddCon("runtime", "Run Time", 2000, 1, 0, labelwidth, numwidth)
        self.paramset.AddCon("basecost", "basecost", 0, 10, 2, labelwidth, numwidth)
        self.paramset.AddCon("foodstep", "foodstep", 0, 100, 2, labelwidth, numwidth)
        self.paramset.AddCon("foodfreq", "foodfreq", 0.01, 0.1, 2, labelwidth, numwidth)
        self.paramset.AddCon("absorp_rate", "absorprate", 0, 0.1, 2, labelwidth, numwidth)
        self.paramset.AddCon("storecost_rate", "storecost", 0, 0.0001, 5, labelwidth, numwidth)
        self.paramset.AddCon("feed_rate", "feedrate", 0.01, 1, 3, labelwidth, numwidth)
        self.paramset.AddCon("energy_init", "energy_init", 10000, 10, 1, labelwidth, numwidth)
        self.paramset.AddCon("gut_max", "gut_max", 1000, 10, 1, labelwidth, numwidth)
        self.paramset.AddCon("reward_base", "Reward Base", 0.01, 0.001, 3, labelwidth, numwidth)
        self.paramset.AddCon("gut_factor", "gutfactor", 0.01, 0.1, 3, labelwidth, numwidth)
        self.paramset.AddCon("fat_factor", "fatfactor", 0.01, 0.01, 3, labelwidth, numwidth)

        self.paramset.AddCon("reward_def_factor", "Reward Def", 0.01, 0.001, 3, labelwidth, numwidth)
        self.paramset.AddCon("reward_tau", "Reward Tau", 0.01, 0.001, 5, labelwidth, numwidth)
        self.paramset.AddCon("ghrelin_secrate", "Ghrelin Sec", 0, 0.001, 5, labelwidth, numwidth)
        self.paramset.AddCon("ghrelin_decay", "Ghrelin Decay", 0, 0.001, 5, labelwidth, numwidth)
        self.paramset.AddCon("feedfreq", "Feed Freq", 0, 0.001, 5, labelwidth, numwidth)


    def WorkPanel(self):

        if self.ostype == "Mac":
            self.paramset.con_numwidth = 60
            self.paramset.con_labelwidth = 80
        else:
            self.paramset.con_numwidth = 60
            self.paramset.con_labelwidth = 70


        self.SetModFlag("randfood", "Random Feed", 0)
        self.SetModFlag("adlibflag", "Ad Libitum", 0)
        self.SetModFlag("newrewardflag", "New Reward", 0)
        self.SetModFlag("multifoodflag", "Multi Food", 0)
        self.SetModFlag("gutrewardflag", "Gut Reward", 0)
        self.SetModFlag("rewardbaseflag", "Reward Base", 0)


        # Parameter controls
        #
        # AddCon(tag string, display string, initial value, click increment, decimal places)
        # ----------------------------------------------------------------------------------

        self.paramset.AddCon("runtime", "Run Time", 2000, 1, 0)
        self.paramset.AddCon("basecost", "basecost", 0, 10, 2)
        self.paramset.AddCon("foodstep", "foodstep", 0, 100, 2)
        self.paramset.AddCon("foodfreq", "foodfreq", 0.01, 0.1, 2)

        self.paramset.AddCon("food1step", "food1step", 0, 100, 2)
        self.paramset.AddCon("food1freq", "food1freq", 0.01, 0.1, 2)
        self.paramset.AddCon("food1taste", "food1taste", 0.01, 0.1, 2)
        self.paramset.AddCon("food1density", "food1density", 0.01, 0.1, 2)
        self.paramset.AddCon("food1start", "food1start", 0, 1, 0)
        self.paramset.AddCon("food1stop", "food1stop", 0, 1, 0)

        self.paramset.AddCon("food2step", "food2step", 0, 100, 2)
        self.paramset.AddCon("food2freq", "food2freq", 0.01, 0.1, 2)
        self.paramset.AddCon("food2taste", "food2taste", 0.01, 0.1, 2)
        self.paramset.AddCon("food2density", "food2density", 0.01, 0.1, 2)
        self.paramset.AddCon("food2start", "food2start", 0, 1, 0)
        self.paramset.AddCon("food2stop", "food2stop", 0, 1, 0)

        self.paramset.AddCon("absorp_rate", "absorprate", 0, 0.1, 2)
        self.paramset.AddCon("storecost_rate", "storecost", 0, 0.0001, 5)
        self.paramset.AddCon("feed_rate", "feedrate", 0.01, 1, 3)
        self.paramset.AddCon("energy_init", "energy_init", 10000, 10, 1)
        self.paramset.AddCon("gut_max", "gut_max", 1000, 10, 1)
        self.paramset.AddCon("reward_base", "Reward Base", 0.01, 0.001, 3)
        self.paramset.AddCon("reward_init", "Reward Init", 0.0, 0.001, 3)
        self.paramset.AddCon("gut_factor", "gutfactor", 0.01, 0.1, 3)
        self.paramset.AddCon("fat_factor", "fatfactor", 0.01, 0.01, 3)

        self.paramset.AddCon("reward_def_factor", "Reward Def", 0.01, 0.001, 3)
        self.paramset.AddCon("reward_tau", "Reward Tau", 0.01, 0.001, 6)
        self.paramset.AddCon("ghrelin_secrate", "Ghrelin Sec", 0, 0.001, 5)
        self.paramset.AddCon("ghrelin_decay", "Ghrelin Decay", 0, 0.001, 5)
        self.paramset.AddCon("feedfreq", "Feed Freq", 0, 0.001, 5)

        self.paramset.AddCon("reward_tau_oral", "ROral Tau", 0, 0.001, 6)
        self.paramset.AddCon("reward_weight_oral", "ROral Weight ", 0, 0.01, 3)
        self.paramset.AddCon("reward_tau_gut", "RGut Tau", 0, 0.001, 6)
        self.paramset.AddCon("reward_weight_gut", "RGut Weight ", 0, 0.01, 3)

        self.paramset.AddCon("eatrate", "Eat Rate ", 1, 0.01, 5)



class AgentProtoBox(ParamBox):
    def __init__(self, mod, tag, title, position, size):
        ParamBox.__init__(self, mod, title, position, size, tag, 0, 1)

        self.autorun = True

        # Initialise Menu 
        #self.InitMenu()

        # Model Flags
    

        # Parameter controls
        #
        # AddCon(tag string, display string, initial value, click increment, decimal places)
        # ----------------------------------------------------------------------------------
        self.paramset.AddCon("drinkstart", "Drink Start", 0, 1, 0)
        self.paramset.AddCon("drinkstop", "Drink Stop", 0, 1, 0)
        self.paramset.AddCon("drinkrate", "Drink Rate", 10, 1, 0)

        self.ParamLayout(3)   # layout parameter controls in two columns

        # ----------------------------------------------------------------------------------

        self.mainbox.AddSpacer(5)
        self.mainbox.Add(self.pconbox, 1, wx.ALIGN_CENTRE_HORIZONTAL|wx.ALIGN_CENTRE_VERTICAL|wx.ALL, 0)
        self.mainbox.AddStretchSpacer(5)
        self.mainbox.AddSpacer(2)
        self.panel.Layout()



class AgentModel(ModThread):
    def __init__(self, mod):
        ModThread.__init__(self, mod.modbox, mod.mainwin)

        self.mod = mod
        self.agentbox = mod.agentbox
        self.mainwin = mod.mainwin
        self.scalebox = mod.mainwin.scalebox

    ## run() is the thread entry function, used to initialise and call the main Model() function 
    ##    
    def run(self):
        # Read model flags
        self.randomflag = self.agentbox.modflags["randomflag"]      # model flags are useful for switching elements of the model code while running

        if self.randomflag: random.seed(0)
        else: random.seed(datetime.now().microsecond)

        self.Model()
        wx.QueueEvent(self.mod, ModThreadEvent(ModThreadCompleteEvent))


    ## Model() reads in the model parameters, initialises variables, and runs the main model loop
    ##
    def Model(self):
        agentdata = self.mod.agentdata
        agentbox = self.mod.agentbox
        agentparams = self.mod.agentbox.GetParams()
        protoparams = self.mod.protobox.GetParams()

        # Read parameters
        runtime = int(agentparams["runtime"])
        waterloss = agentparams["waterloss"]

        # Initialise variables
        water = 50
        salt = 2000
        osmo = salt / water
        vaso = 0

        # Initialise model variable recording arrays
        agentdata.water.clear()
        agentdata.salt.clear()
        agentdata.osmo.clear()
        agentdata.vaso.clear()

        # Initialise model variables
        agentdata.water[0] = water
        agentdata.salt[0] = salt
        agentdata.osmo[0] = osmo
        agentdata.vaso[0] = vaso
        osmo_thresh = 280
        v_grad = 0.2
        v_max = 20

        # Run model loop
        for i in range(1, runtime + 1):

            if i%100 == 0: agentbox.SetCount(i * 100 / runtime)     # Update run progress % in model panel

            water = water - (water * waterloss)
            salt = salt
            osmo = salt / water
            if osmo < osmo_thresh: vaso = 0
            else: 
                vaso = v_grad * (osmo - osmo_thresh)
                if vaso > v_max: vaso = v_max

            # Record model variables
            agentdata.water[i] = water
            agentdata.salt[i] = salt
            agentdata.osmo[i] = osmo
            agentdata.vaso[i] = vaso


        # Set plot time range
        agentdata.water.xmax = runtime * 1.1
        agentdata.salt.xmax = runtime * 1.1
        agentdata.osmo.xmax = runtime * 1.1
        agentdata.vaso.xmax = runtime * 1.1






