
import wx

from HypoModPy.hypoparams import ParamBox



class AgentBox(ParamBox):
    def __init__(self, mod, tag, title, position, size):
        ParamBox.__init__(self, mod, title, position, size, tag, 0, 1)

        self.autorun = True

        # Initialise Menu 
        self.InitMenu()

        # Model Flags
        #ID_randomflag = wx.NewIdRef()   # request a new control ID
        self.AddFlag("randomflag", "Fixed Random Seed", 0)         # menu accessed flags for switching model code

        
        # Parameter controls
        #
        # AddCon(tag string, display string, initial value, click increment, decimal places)
        # ----------------------------------------------------------------------------------
        #self.paramset.AddCon("runtime", "Run Time", 2000, 1, 0)
        #self.paramset.AddCon("hstep", "h Step", 1, 0.1, 1)
        #self.paramset.AddCon("waterloss", "Water Loss", 0, 0.00001, 5)

        paneltype = "Bristol"

        if paneltype == "Default": self.DefaultPanel()
        if paneltype == "Bristol": self.BristolPanel()
        if paneltype == "Work": self.WorkPanel()

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
        self.mainbox.Add(self.buttonbox, 0, wx.ALIGN_CENTRE_HORIZONTAL | wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 0)
        self.mainbox.AddSpacer(5)
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

        self.AddFlag("randfood", "Random Food", 0)
        self.AddFlag("adlibflag", "Ad Libitum", 0)

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


        self.AddFlag("randfood", "Random Feed", 0)
        self.AddFlag("adlibflag", "Ad Libitum", 0)
        self.AddFlag("newrewardflag", "New Reward", 0)
        self.AddFlag("multifoodflag", "Multi Food", 0)
        self.AddFlag("gutrewardflag", "Gut Reward", 0)
        self.AddFlag("rewardbaseflag", "Reward Base", 0)


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
