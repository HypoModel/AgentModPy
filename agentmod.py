
import os
import random
import math
from datetime import datetime

from matplotlib import text
import wx

from HypoModPy.hypomods import(
    Mod,
    ModThread,
    ModThreadEvent,
    ModThreadCompleteEvent,
)
from HypoModPy.hypoparams import ParamBox
from HypoModPy.hypodat import PlotDat, datarray, pdata
from HypoModPy.hypogrid import GridBox
from HypoModPy.hypotools import DiagWrite

from agentpanels import AgentBox, AgentProtoBox
from agentdat import AgentDat, FoodDat, FoodChoice, FoodGut


class AgentMod(Mod):
    def __init__(self, mainwin, tag, label="", type=""):
        Mod.__init__(self, mainwin, tag, label, type)

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

        self.agentdata = AgentDat(100000)
        self.foodtype = [FoodDat(100000) for _ in range(10)]


        self.PlotData()
        self.graphload = True



    ## PlotData() defines all the available plots, each linked to a data array in agentdata
    ##
    def PlotData(self):
        # Data plots
        #
        # AddPlot(PlotDat(data array, xfrom, xto, yfrom, yto, label string, plot type, bin size, colour), tag string)
        # ----------------------------------------------------------------------------------
        scalefactor = 1 / 60

        self.plotbase.AddPlot(PlotDat(self.agentdata.energy, 0, 2000, 0, 2000, "energy (hours)", "line", scalefactor, "blue"), "energy")
        #self.plotbase.AddPlot(PlotDat(self.agentdata.appetite, 0, 2000, 0, 2000, "appetite", "line", 1, "red"), "appetite")
        #self.plotbase.AddPlot(PlotDat(self.agentdata.glyco, 0, 2000, 0, 2000, "glyco", "line", 1, "red"), "glyco")
        #self.plotbase.AddPlot(PlotDat(self.agentdata.insulin, 0, 2000, 0, 2000, "insulin", "line", 1, "blue"), "insulin")
        #self.plotbase.AddPlot(PlotDat(self.agentdata.chamber, 0, 2000, 0, 2000, "chamber", "line", 1, "green"), "chamber")
        self.plotbase.AddPlot(PlotDat(self.agentdata.gut, 0, 2000, 0, 2000, "gut", "line", scalefactor, "green"), "gut")
        self.plotbase.AddPlot(PlotDat(self.agentdata.feeding, 0, 2000, 0, 2000, "feeding", "line", scalefactor, "red"), "feeding")
        self.plotbase.AddPlot(PlotDat(self.agentdata.food, 0, 2000, 0, 100, "available food", "line", scalefactor, "blue"), "food")
        self.plotbase.AddPlot(PlotDat(self.agentdata.reward, 0, 2000, 0, 100, "reward", "line", scalefactor, "green"), "reward")
        self.plotbase.AddPlot(PlotDat(self.agentdata.reward_def, 0, 2000, 0, 100, "reward def", "line", scalefactor, "red"), "reward_def")
        self.plotbase.AddPlot(PlotDat(self.agentdata.fullness, 0, 2000, 0, 100, "fullness", "line", scalefactor, "red"), "fullness")
        self.plotbase.AddPlot(PlotDat(self.agentdata.ghrelin, 0, 2000, 0, 100, "ghrelin", "line", scalefactor, "lightred"), "ghrelin")

        self.plotbase.AddPlot(PlotDat(self.agentdata.energyLong, 0, 2000, 0, 2000, "energy (days)", "line", 60, "blue", 1440), "energyLong")
        self.plotbase.GetPlot("energyLong").synchx = False

        self.plotbase.AddPlot(PlotDat(self.agentdata.rewardLong, 0, 2000, 0, 2000, "reward (days)", "line", 60, "green", 1440), "rewardLong")
        self.plotbase.GetPlot("rewardLong").synchx = False

        self.plotbase.AddPlot(PlotDat(self.agentdata.reward_oral, 0, 2000, 0, 100, "reward oral", "line", scalefactor, "green"), "reward_oral")
        self.plotbase.AddPlot(PlotDat(self.agentdata.reward_gut, 0, 2000, 0, 100, "reward gut", "line", scalefactor, "blue"), "reward_gut")
        self.plotbase.AddPlot(PlotDat(self.agentdata.reward_new, 0, 2000, 0, 100, "reward new", "line", scalefactor, "purple"), "reward_new")

        self.plotbase.AddPlot(PlotDat(self.agentdata.food1, 0, 2000, 0, 100, "food1", "line", scalefactor, "green"), "food1")
        self.plotbase.AddPlot(PlotDat(self.agentdata.food2, 0, 2000, 0, 100, "food2", "line", scalefactor, "red"), "food2")
        self.plotbase.AddPlot(PlotDat(self.foodtype[0].consumed, 0, 2000, 0, 100, "food1 consumed", "line", 1, "green"), "food1consumed")
        self.plotbase.AddPlot(PlotDat(self.foodtype[1].consumed, 0, 2000, 0, 100, "food2 consumed", "line", 1, "red"), "food2consumed")


    def DefaultPlots(self):
        if len(self.mainwin.panelset) > 0: self.mainwin.panelset[0].settag = "energy"
        if len(self.mainwin.panelset) > 1: self.mainwin.panelset[1].settag = "gut"
        if len(self.mainwin.panelset) > 2: self.mainwin.panelset[2].settag = "feeding"


    def OnModThreadComplete(self, event):
        self.mainwin.scalebox.GraphUpdateAll()


    def OnModThreadProgress(self, event):
        self.agentbox.SetCount(event.GetInt())


    def RunModel(self):
        self.mainwin.SetStatusText("Agent Model Run")
        params = {
                "agent": self.agentbox.GetParams(),
                "proto": self.protobox.GetParams()
            }
        modthread = AgentModel(self, params)
        modthread.start()



class AgentModel(ModThread):
    def __init__(self, mod, params):
        ModThread.__init__(self, mod.modbox, mod.mainwin)

        self.mod = mod
        self.params = params
        self.agentbox = mod.agentbox
        self.mainwin = mod.mainwin
        self.scalebox = mod.mainwin.scalebox

    ## run() is the thread entry function, used to initialise and call the main Model() function    
    def run(self):
        # Read model flags
        modflags = self.agentbox.modflags
        self.randomflag = modflags["randomflag"]      # model flags are useful for switching elements of the model code while running
        self.randfood = modflags["randfood"]
        #glycoflag = modflags["glycoflag"]
        #chamberflag = modflags["chamberflag"]
        self.adlibflag = modflags["adlibflag"]
        #self.newrewardflag = modflags["newrewardflag"]
        #self.multifoodflag = modflags["multifoodflag"]
        #self.gutrewardflag = modflags["gutrewardflag"]
        #self.rewardbaseflag = modflags["rewardbaseflag"]

        # Set random seed
        if self.randomflag: random.seed(0)
        else: random.seed(datetime.now().microsecond)

        #self.Food_Initialise()
        self.Model_Basic()
        wx.QueueEvent(self.mod, ModThreadEvent(ModThreadCompleteEvent))


    def Food_Initialise(self):
        agentparams = self.params["agent"]
        foodtype = self.mod.foodtype

        foodtype[0].step = agentparams["food1step"]
        foodtype[0].interval = 1 / (agentparams["food1freq"] / 1440)
        foodtype[0].reward = agentparams["food1taste"]             # currently oral reward equals taste
        foodtype[0].density = agentparams["food1density"]          # energy units per unit volume
        foodtype[0].start = agentparams["food1start"] * 1440
        foodtype[0].stop = agentparams["food1stop"] * 1440

        foodtype[1].step = agentparams["food2step"]
        foodtype[1].interval = 1 / (agentparams["food2freq"] / 1440)
        foodtype[1].reward = agentparams["food2taste"]
        foodtype[1].density = agentparams["food2density"]
        foodtype[1].start = agentparams["food2start"] * 1440
        foodtype[1].stop = agentparams["food2stop"] * 1440



    def Model_Basic(self):
        agentdata = self.mod.agentdata
        agentbox = self.mod.agentbox
        agentparams = self.params["agent"]
        protoparams = self.params["proto"]

        # Read parameters
        runtime = 60 * int(agentparams["runtime"])                  # convert hours to minutes
        basecost = agentparams["basecost"] / 1440                  # convert per day to per minute

        # basic food parameters
        foodstep = agentparams["foodstep"]
        foodfreq = agentparams["foodfreq"] / 1440                  # convert per day to per minute

        # energy store and gut parameters
        absorp_rate = agentparams["absorp_rate"]
        energy_init = agentparams["energy_init"]
        gut_max = agentparams["gut_max"]
        gut_init = 0
        
        storecost_rate = agentparams["storecost_rate"] / 1440      # convert per day to per minute

        feed_rate = agentparams["feed_rate"]
        feedfreq = agentparams["feedfreq"] / 1440
       
        # reward parameters
        reward_base = agentparams["reward_base"]
        gut_factor = agentparams["gut_factor"]
        fat_factor = agentparams["fat_factor"]

        reward_factor = reward_base
        

        # prototype ghrelin/appetite signal model parameters
        ghrelin_secrate = agentparams["ghrelin_secrate"]
        ghrelin_decay = agentparams["ghrelin_decay"]

        
        # Calculated and control values
        gut_sum = 0
        intake_sum = 0
        gut_count = 0
        meal_offset = 30

        
        # Initialise variables
        appetite = 0
        energy = energy_init
        gut = gut_init
        tfood = -math.log(1 - random.random()) / foodfreq
        fullness = 0
        available_food = 0
        feeding = 0
        ghrelin = 0

        agentdata.energy[0] = energy
        agentdata.appetite[0] = appetite
        agentdata.gut[0] = gut
        agentdata.feeding[0] = feeding
        agentdata.food[0] = available_food
        agentdata.reward[0] = 0
        agentdata.fullness[0] = 0
        agentdata.reward_def[0] = 0
        agentdata.ghrelin[0] = 0

        agentdata.reward_oral[0] = 0
        agentdata.reward_gut[0] = 0
        agentdata.reward_new[0] = 0


        # Run model loop
        for step in range(1, runtime + 1):

            if step%100 == 0: agentbox.SetCount(step * 100 / runtime)     # Update run progress % in model panel

            # Reward - basic fixed reward
            reward = reward_factor * feeding

                
            fullness = gut_factor * (gut / gut_max) + fat_factor * (energy / 100000)
            if available_food and fullness > reward:
                available_food = 0   # discard available food when full         interval food
                feeding = 0   # stop eating                              adlib food
                DiagWrite(f"step {step} fullness {fullness:.4f} reward {reward:.4f}\n")         


            # Food Availability
            # Poisson random food events
            nfood = 0
            if self.randfood and foodfreq > 0:
                while tfood < step:
                    nfood += 1
                    available_food = available_food + foodstep
                    DiagWrite(f"\nfood event at {step}\n")
                    tfood = (-math.log(1 - random.random()) / foodfreq) + tfood

            # Regular food events
            foodinterval = 1 / foodfreq
            if not self.randfood and (step + meal_offset) % int(foodinterval) == 0: available_food = available_food + foodstep


            # Eating V2 - Ad Libitum
            if self.adlibflag:
                feedprob = feedfreq * (1 - gut_factor * (gut / gut_max))      # gut satiety signal reduces meal initiation probability
                DiagWrite(f"adlib test feedfreq {feedfreq:.4f} feedprob {feedprob:.4f}\n")
                if not feeding:
                    if (1 - random.random()) < feedprob:
                        feeding = feed_rate
                        #mod.diagbox.Write(" EAT\n")
                    #else: mod.diagbox.Write(" FAIL\n")

            # Eating V1 - single type food events
            else:
                if available_food >= feed_rate:      # eat whenever food available
                    feeding = feed_rate
                    available_food = available_food - feed_rate
                else:
                    feeding = 0
                  

            # Digestion - single type
            gut = gut + feeding
            if gut > gut_max: gut = gut_max

            if gut >= absorp_rate:
                energy_intake = absorp_rate
                gut = gut - absorp_rate
            else: energy_intake = 0


            # Energy consumption and intake
            storecost = energy * storecost_rate
            energy = energy - basecost - storecost + energy_intake
            if energy < 0: energy = 0
            

            # Ghrelin
            if not energy_intake: ghrelin_sec = ghrelin_secrate
            else: ghrelin_sec = 0
            ghrelin = ghrelin + ghrelin_sec - ghrelin_decay * ghrelin

            # Record model variables
            agentdata.energy[step] = energy
            agentdata.appetite[step] = appetite
            agentdata.gut[step] = gut   
            agentdata.feeding[step] = feeding
            agentdata.food[step] = available_food
            agentdata.fullness[step] = fullness
            agentdata.reward[step] = reward
            agentdata.ghrelin[step] = ghrelin

            agentdata.energyLong[step // 60] = energy
            agentdata.rewardLong[step // 60] = reward_factor



    ## Model() reads in the model parameters, initialises variables, and runs the main model loop
    def Model(self):
        agentdata = self.mod.agentdata
        agentbox = self.mod.agentbox
        agentparams = self.params["agent"]
        protoparams = self.params["proto"]
        foodtype = self.mod.foodtype

        # Read parameters
        runtime = 60 * int(agentparams["runtime"])                  # convert hours to minutes
        basecost = agentparams["basecost"] / 1440                  # convert per day to per minute
        feedthresh = agentparams["feedthresh"]

        # basic food parameters
        foodstep = agentparams["foodstep"]
        foodfreq = agentparams["foodfreq"] / 1440                  # convert per day to per minute

        # glycogen and glucose parameters - currently not in use
        gluco_set = agentparams["gluco_set"]
        glyco_rate = agentparams["glyco_rate"]
        glyco_max = agentparams["glyco_max"]
        glyco_init = agentparams["glyco_init"]
        glyco_feed = agentparams["glyco_feed"]

        # energy store and gut parameters
        absorp_rate = agentparams["absorp_rate"]
        energy_init = agentparams["energy_init"]
        energy_max = agentparams["energy_max"] # currently not in use
        gut_max = agentparams["gut_max"]
        gut_init = 0
        
        storecost_rate = agentparams["storecost_rate"] / 1440      # convert per day to per minute
        full_thresh = agentparams["fullthresh"]
        
        feed_rate = agentparams["feed_rate"]
        feedfreq = agentparams["feedfreq"] / 1440
        eatrate = agentparams["eatrate"]

        # reward parameters
        reward_base = agentparams["reward_base"]
        reward_init = agentparams["reward_init"]
        gut_factor = agentparams["gut_factor"]
        fat_factor = agentparams["fat_factor"]
        reward_tau = agentparams["reward_tau"]
        reward_def_factor = agentparams["reward_def_factor"]
        reward_tau_oral = agentparams["reward_tau_oral"]
        reward_weight_oral = agentparams["reward_weight_oral"]
        reward_tau_gut = agentparams["reward_tau_gut"]
        reward_weight_gut = agentparams["reward_weight_gut"]

        # prototype ghrelin/appetite signal model parameters
        ghrelin_secrate = agentparams["ghrelin_secrate"]
        ghrelin_decay = agentparams["ghrelin_decay"]

        
        # Calculated and control values

        # Dynamic Reward   -  October/November 2018
        reward_set_oral = 0
        reward_set_gut = 0
        reward_oral = 0
        reward_gut = 0
        reward_new = 0       # testing placeholder

        # Multi Food Types  -  December 2018/January 2019
        foodchoice = [FoodChoice() for _ in range(10)]
        foodgut = [FoodGut() for _ in range(10)]
        choicecount = 0
        choicesum = 0
        choicerand = 0
        choicetype = 0
        feedtype = 0

        gut_sum = 0
        intake_sum = 0
        gut_count = 0
        meal_offset = 60
        numfoodtypes = 2
        appetite_v1 = False
        appetite_v2 = True

        
        # Initialise variables
        appetite = 0
        feedgen = 0
        insulin = 0
        glyco = glyco_init
        chamber = 0

        energy = energy_init
        gut = gut_init
        tfood = -math.log(1 - random.random()) / foodfreq
        fullness = 0
        food = 0
        feed = 0
        ghrelin = 0

        if self.rewardbaseflag:
            reward_mod = reward_init
            reward_set = 0
            reward_def = 0
        else:
            reward_def = 0
            reward_set = 0
            reward_mod = 0

        reward_set_oral = 0
        reward_set_gut = 0
        reward_oral = 0
        reward_gut = 0

        feed1 = 0
        feed2 = 0

        for i in range(numfoodtypes):
            foodtype[i].amount = 0
            foodtype[i].gut = 0
            if foodtype[i].stop < 0: foodtype[i].stop = runtime
            for j in range(1000): foodtype[i].consumed[j] = 0

        gut_sum = 0

        # Initialise model variable recording arrays
        # agentdata.water.clear()
        # agentdata.salt.clear()
        # agentdata.osmo.clear()
        # agentdata.vaso.clear()

        agentdata.energy[0] = energy
        agentdata.appetite[0] = appetite
        agentdata.glyco[0] = glyco
        agentdata.insulin[0] = insulin
        agentdata.chamber[0] = chamber
        agentdata.gut[0] = gut
        agentdata.feed[0] = feed
        agentdata.food[0] = food
        agentdata.reward[0] = 0
        agentdata.fullness[0] = 0
        agentdata.reward_def[0] = 0
        agentdata.ghrelin[0] = 0

        agentdata.reward_oral[0] = 0
        agentdata.reward_gut[0] = 0
        agentdata.reward_new[0] = 0


        # Run model loop
        for step in range(1, runtime + 1):

            if step%100 == 0: agentbox.SetCount(step * 100 / runtime)     # Update run progress % in model panel

            # Appetite V1 - currently not in use
            if appetite_v1:
                fullness = gut / gut_max
                if fullness > full_thresh: food = 0

            ## Reward V1 - basic dynamic
            reward_def += (reward_set - reward_def) * reward_tau
            if self.rewardbaseflag:
                if reward_def < -reward_mod: reward_def = -reward_mod            # set reward_base minimum
            reward_factor = reward_base + reward_mod + reward_def
            reward = reward_factor * feed

            ## Reward V2 - oral+gut dynamic                      started 19/10/18

            # Reward Signals - including multi

            reward_oral += (reward_set_oral - reward_oral) * reward_tau_oral
            
            reward_gut += (reward_set_gut - reward_gut) * reward_tau_gut

            reward_new = reward_oral * reward_weight_oral + reward_gut * reward_weight_gut

            if self.newrewardflag: reward = reward_factor * reward_new

            # Appetite V2
            if self.multifoodflag:
                fullness = gut_factor * (gut_sum / gut_max) + fat_factor * (energy / 100000)
                if feed and fullness > reward:
                    feed = 0   # stop eating
                    for i in range(numfoodtypes): foodtype[i].amount = 0    # discard available food when full
                    DiagWrite(f"step {step} fullness {fullness:.4f} reward {reward:.4f}\n")
            else:
                if appetite_v2:
                    fullness = gut_factor * (gut / gut_max) + fat_factor * (energy / 100000)
                    if food and fullness > reward:
                        food = 0   # discard available food when full         interval food
                        feed = 0   # stop eating                              adlib food
                        DiagWrite(f"step {step} fullness {fullness:.4f} reward {reward:.4f}\n")


            # Poisson random food events
            nfood = 0
            if self.randfood and foodfreq > 0:
                while tfood < step:
                    nfood += 1
                    food = food + foodstep
                    DiagWrite(f"\nfood event at {step}\n")
                    tfood = (-math.log(1 - random.random()) / foodfreq) + tfood

            # Regular food events
            foodinterval = 1 / foodfreq
            if not self.randfood and (step + meal_offset) % int(foodinterval) == 0: food = food + foodstep

            for i in range(numfoodtypes):
                if step >= foodtype[i].start and step <= foodtype[i].stop and ((step + meal_offset + foodtype[i].start) % int(foodtype[i].interval) == 0):
                    foodtype[i].amount = foodtype[i].amount + foodtype[i].step


            # Eating V3 - multi type food events
            if self.multifoodflag:
                choicecount = 0
                choicesum = 0
                for i in range(numfoodtypes):          # create choice set - available food types
                    if foodtype[i].amount >= feed_rate:
                        foodchoice[choicecount].type = i
                        foodchoice[choicecount].reward = foodtype[i].GetReward()
                        choicesum = choicesum + foodchoice[choicecount].reward
                        choicecount += 1

                if choicecount:
                    for i in range(choicecount): foodchoice[i].prob = foodchoice[i].reward / choicesum      # normalise reward values to generate relative probabilities
                    choicerand = random.random()
                    choicetype = 0
                    while choicerand > foodchoice[choicetype].prob:                      # index random value to food choice type
                        choicerand = choicerand - foodchoice[choicetype].prob
                        choicetype += 1

                    feed = feed_rate
                    feedtype = foodchoice[choicetype].type
                    foodtype[feedtype].amount = foodtype[feedtype].amount - feed_rate
                    foodtype[feedtype].gut = foodtype[feedtype].gut + feed_rate
                    foodtype[feedtype].consumed[step // 1440] = foodtype[feedtype].consumed[step // 1440] + feed_rate * foodtype[feedtype].density      # record consumption per day
                    DiagWrite(f"step {step} day {step // 1440} consumed {foodtype[feedtype].consumed[step // 1440]:.2f}\n")
                    reward_set_oral = foodchoice[choicetype].reward
                else:
                    feed = 0
                    reward_set_oral = 0

            # Eating V2 - Ad Libitum
            elif self.adlibflag:

                feedprob = feedfreq * (1 - gut_factor * (gut / gut_max))      # gut satiety signal reduces meal initiation probability
                DiagWrite(f"adlib test feedfreq {feedfreq:.4f} feedprob {feedprob:.4f}\n")
                if not feed:
                    if (1 - random.random()) < feedprob:
                        feed = feed_rate
                        #mod.diagbox.Write(" EAT\n")
                    #else: mod.diagbox.Write(" FAIL\n")

            # Eating V1 - single type food events
            else:
                if food >= feed_rate:      # eat whenever food available
                    feed = feed_rate
                    food = food - feed_rate
                    feed1 = feed
                    feed2 = 0
                else:
                    feed = 0
                    feed1 = 0
                    feed2 = 0


            # Multi Digestion
            if self.multifoodflag:
                gut_sum = 0
                gut_count = 0
                intake_sum = 0

                for i in range(numfoodtypes):
                    if foodtype[i].gut > 0:
                        gut_sum = gut_sum + foodtype[i].gut
                        foodgut[gut_count].type = i
                        #foodgut[gut_count].reward = foodtype[i].GetReward()
                        gut_count += 1

                if gut_sum >= absorp_rate:
                    for i in range(gut_count):
                        foodgut[i].proportion = foodtype[foodgut[i].type].gut / gut_sum
                        intake_sum = intake_sum + foodgut[i].proportion * absorp_rate * foodtype[foodgut[i].type].density
                        foodtype[foodgut[i].type].gut = foodtype[foodgut[i].type].gut - foodgut[i].proportion * absorp_rate
                    energy_intake = intake_sum
                else: energy_intake = 0
            else:
                # Digestion - single type
                gut = gut + feed
                if gut > gut_max: gut = gut_max

                if gut >= absorp_rate:
                    energy_intake = absorp_rate
                    gut = gut - absorp_rate
                else: energy_intake = 0

            reward_set_gut = energy_intake


            # Energy consumption
            storecost = energy * storecost_rate
            #if energy > 0: energy = energy - basecost - storecost + energy_intake
            energy_diff = energy_intake - basecost - storecost
            if energy > 0: energy += energy_diff

            #if energy_diff < 0: reward_set = -(energy_diff * reward_def_factor)
            #else: reward_set = 0
            reward_set = -(energy_diff * reward_def_factor)


            # Ghrelin
            if not energy_intake: ghrelin_sec = ghrelin_secrate
            else: ghrelin_sec = 0
            ghrelin = ghrelin + ghrelin_sec - ghrelin_decay * ghrelin

            # Record model variables
            agentdata.energy[step] = energy
            agentdata.appetite[step] = appetite
            agentdata.glyco[step] = glyco
            agentdata.insulin[step] = insulin
            agentdata.gut[step] = gut   # 100   # gut
            agentdata.feed[step] = feed
            agentdata.food[step] = food
            agentdata.fullness[step] = fullness
            agentdata.reward[step] = reward
            agentdata.reward_def[step] = reward_factor   # reward_def
            agentdata.ghrelin[step] = ghrelin

            agentdata.energyLong[step // 60] = energy
            agentdata.rewardLong[step // 60] = reward_factor

            agentdata.food1[step] = foodtype[0].amount
            agentdata.food2[step] = foodtype[1].amount

            agentdata.gut1[step] = foodtype[0].gut
            agentdata.gut2[step] = foodtype[1].gut

            agentdata.taste1[step] = foodtype[0].GetReward()
            agentdata.taste2[step] = foodtype[1].GetReward()

            agentdata.reward_oral[step] = reward_oral
            agentdata.reward_gut[step] = reward_gut
            agentdata.reward_new[step] = reward_new


