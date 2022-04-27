--Copyright 2015 Stefan Andrei Chelariu
--
--Licensed under the Apache License, Version 2.0 (the "License");
--you may not use this file except in compliance with the License.
--You may obtain a copy of the License at
--
--    http://www.apache.org/licenses/LICENSE-2.0
--
--Unless required by applicable law or agreed to in writing, software
--distributed under the License is distributed on an "AS IS" BASIS,
--WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
--See the License for the specific language governing permissions and
--limitations under the License.

--Settings: 
--1.    Set prompter to zero if you set your variables
--      in the code under User Variables to avoid being prompted all the time
--2.    Set the height of the motor by modifying 
--      the mheight parameters under User Variables
--3.    Limit the number of simulations by lowering
--      the range of motor diameters which is max_mdia - min_mdia
--      under User Constants
--4.    Limit the number of simulations by lowering 
--      the range of wire diameters used which is max_ecwdia - min_ecwdia
--      under User Constants
--5.    Set a maximum field coil voltage value by modifying the 
--      max_voltage parameter under User Constants. The script will move to 
--      the next simulation if the voltage on the field coil will get higher
--      than this value.
--6.    Set a maximum field coil current value by modifying the 
--      max_current parameter under User Constants. The script will move to 
--      the next simulation if the current through the field coil will get higher
--      than this value.
--7.    Set the project folder by modifying the save_path parameter under 
--      User Constants, use double back-slashes between folders

--Advanced Settings:
--1.    Set the thickness of the bottom plate by modifying the botplate parameter
--      under Program Constants
--2.    Set the thickness of the steel can around the field coil by modifying
--      the canplate parameter under Program Constants
--3.    canplate parameter under Program Constants is reserved for later use
--4.    The script will calculate the flux density at different current values
--      through the field coil. Set the start current value by modifying the 
--      start_i parameter under Program Constants
--5.    Set the field coil current step value by modifying the current_step
--      parameter under Program Constants
--6.    The distance between the voice coil and the steel in the gap is set by
--      gaclear parameter under Program Constants. If you plan to use a copper 
--      sleeve on the central pole piece you should add half of the sleeve's 
--      thickness to this value.

--Setting Simulation Objective:
--      The script will simulate a number of motor size, field coil sizes
--      and field coil currents. After all simulations are done it will go 
--      through the results and pick the best solution based on a defined objetive.
--      The best solution is chose based on three parameters: motor size, field
--      coil power and flux density in the gap. The score of each simulation is 
--      determined with a weighted sum of these three parameters. Under User
--      Constants we can find the weight vector w with w['dia'] being the wight 
--      for motor size, w['pow'] - weight for field coil power and w['flx'] - 
--      weight for flux density.
--      The weights take values between 0 and 1 with 0 meaning ignore and 1 meaning
--      the most important
--      e.g.
--          Objective: dont care about motor size, sacrifice a bit from flux
--          density value for the best field coil power value
--          Weight vector:
--              w = { ['dia'] = 0, ['pow'] = 1, ['flx'] = 0.7 }
--          Score:
--              s = w['dia']*(motor diameter)+w['pow']*(fc power)+w['flx']*(flux)


prompter	= 0
--User Variables
mdia            = 0
mheight         = 120
vcdia           = 39
vcheight        = 4
gapwidth        = 1
gapheight       = 5
flux		= 2.0


--User Constants
max_voltage	= 24
max_current	= 4
min_mdia        = 120
max_mdia        = 180
min_ecwdia      = 0.3
max_ecwdia      = 1.5
w 		= { ['dia'] = 0.5, ['pow'] = 0.5, ['flx'] = 1 }
save_path       = "C:\\temp\\"
filename        = "default"

--Program Variable
d_candidates    = {}
obj             = {}
score           = {}
current 	= 0
voltage		= 0
avg_Bn          = 0

--Program Constants
botplate        = 20
canplate        = 10
coredia         = 0
start_i 	= 0.1
gapclear	= 0.3
current_step	= 0.1
fc_wind_factor	= 0.7
count           = 1

--Init 
newdocument(0)
showconsole()
clearconsole()
print("PROJECT RYU")
print("Field Coil Motor Simulation v0.1")
if prompter==1 then
	repeat	
		messagebox("Please input your specific data in millimiters")
                filename = prompt("Project Name")
		vcdia = tonumber(prompt("Voice Coil Diameter [mm]"))
		vcheight = tonumber(prompt("Voice Coil Height [mm]"))
		local vcwidth = tonumber(prompt("Voice Coil Width [mm]"))
		local xmax = tonumber(prompt("Desired One Way Xmax [mm]"))
		flux = tonumber(prompt("Desired Flux Density [T]"))
		print("User Input Data")
		print("Voice Coil Dia:"..vcdia.."mm")
		print("Voice Coil Height:"..vcheight.."mm")
		print("Voice Coil Width:"..vcwidth.."mm")
		print("Xmax:"..xmax.."mm")	
		print("Flux Density:"..flux.."T")
		messagebox("Verify Input Data...Voice Coil Dia:"..vcdia.."mm Voice Coil Height:"..vcheight.."mm Voice Coil Width:"..vcwidth.."mm Xmax:"..xmax.."mm Flux Density:"..flux.."T")
		local confirm = prompt("Confirm? [type yes if data is ok, press return to go back]")		if confirm == "yes" then 
			prompter = 0	
			gapheight = 2*xmax+vcheight
			gapwidth = 2*gapclear+vcwidth
		end
	until prompter==0 
end
	
--Preprocessor Script
mi_probdef(0,"millimeters","axi",1E-8)

--Boundary
mi_addboundprop("MBound", 0,0,0,0,0,0,0,0,0)
function draw_boundary(motor_dia)
	mi_addnode(0,-10)
	mi_addnode(motor_dia+50,-10)
	mi_addnode(motor_dia+50,mheight+50)
	mi_addnode(0,mheight+50)
	mi_addsegment(0,0,0,-10)
	mi_addsegment(motor_dia+50,-10,0,-10)
	mi_addsegment(motor_dia+50,-10,motor_dia+50,mheight+50)
	mi_addsegment(0,mheight+50,motor_dia+50,mheight+50)
	mi_addsegment(0,mheight+50,0,0)
	mi_selectsegment(0,-5)
	mi_selectsegment(0,10)
	mi_selectsegment(0,mheight+10)
	mi_selectsegment(motor_dia,-10)
	mi_selectsegment(motor_dia+50,0)
	mi_selectsegment(motor_dia-10,mheight+50)
	mi_setsegmentprop("MBound",0,1,0,0)
end

function clear_boundary(motor_dia)
	mi_clearselected()
	mi_selectnode(0,-10)
	mi_selectnode(motor_dia+50,-10)
	mi_selectnode(motor_dia+50,mheight+50)
	mi_selectnode(0,mheight+50)
	mi_deleteselectednodes()
end
	
--Geometry
function draw_geometry(motor_dia)
	mi_addnode(0,0)
	mi_addnode(0,mheight-10)
	mi_addsegment(0,0,0,mheight-10)
	mi_addnode(10,mheight)
	mi_addsegment(0,mheight-10,10,mheight)
	mi_addnode(vcdia/2-gapwidth/2,mheight)
	mi_addsegment(10,mheight,vcdia/2-gapwidth/2,mheight)
	mi_addnode(vcdia/2-gapwidth/2,mheight-gapheight)
	mi_addsegment(vcdia/2-gapwidth/2,mheight,vcdia/2-gapwidth/2,mheight-gapheight)
	mi_addnode(vcdia/2-gapwidth/2+10,mheight-gapheight-10)
	mi_addsegment(vcdia/2-gapwidth/2,mheight-gapheight,vcdia/2-gapwidth/2+10,mheight-gapheight-10)
	mi_addnode(vcdia/2-gapwidth/2+10,botplate)
	mi_addsegment(vcdia/2-gapwidth/2+10,mheight-gapheight-10,vcdia/2-gapwidth/2+10,botplate)
	mi_addnode(motor_dia/2-canplate, botplate)
	mi_addsegment(vcdia/2-gapwidth/2+10,botplate,motor_dia/2-canplate, botplate)
	mi_addnode(motor_dia/2-canplate,mheight-gapheight)
	mi_addsegment(motor_dia/2-canplate, botplate,motor_dia/2-canplate,mheight-gapheight)
	mi_addnode(vcdia/2+gapwidth/2,mheight-gapheight)
	mi_addsegment(motor_dia/2-canplate,mheight-gapheight,vcdia/2+gapwidth/2,mheight-gapheight)
	mi_addnode(vcdia/2+gapwidth/2,mheight)
	mi_addsegment(vcdia/2+gapwidth/2,mheight-gapheight,vcdia/2+gapwidth/2,mheight)
	mi_addnode(motor_dia/2-10,mheight)
	mi_addsegment(vcdia/2+gapwidth/2,mheight,motor_dia/2-10,mheight)
	mi_addnode(motor_dia/2,mheight-10)
	mi_addarc(motor_dia/2,mheight-10,motor_dia/2-10,mheight,90,1)
	mi_addnode(motor_dia/2,10)
	mi_addsegment(motor_dia/2,mheight-10,motor_dia/2,10)
	mi_addnode(motor_dia/4,0)
	mi_addsegment(motor_dia/2,10,motor_dia/4,0)
	mi_addsegment(motor_dia/4,0,0,0)
	mi_addnode(motor_dia/2-canplate,mheight-gapheight-10)
	mi_addsegment(vcdia/2-gapwidth/2+10,mheight-gapheight-10,motor_dia/2-canplate,mheight-gapheight-10)
	mi_addnode(vcdia/2,mheight)
	mi_addnode(vcdia/2,mheight-gapheight)
end

function clear_geometry(motor_dia)
	mi_clearselected()
	mi_selectnode(0,0)
        mi_selectnode(0,mheight-10)
        mi_selectnode(10,mheight)
        mi_selectnode(vcdia/2-gapwidth/2,mheight)
        mi_selectnode(vcdia/2-gapwidth/2,mheight-gapheight)
        mi_selectnode(vcdia/2-gapwidth/2+10,mheight-gapheight-10)
        mi_selectnode(vcdia/2-gapwidth/2+10,botplate)
        mi_selectnode(motor_dia/2-canplate, botplate)
        mi_selectnode(motor_dia/2-canplate,mheight-gapheight)
        mi_selectnode(vcdia/2+gapwidth/2,mheight-gapheight)
        mi_selectnode(vcdia/2+gapwidth/2,mheight)
        mi_selectnode(motor_dia/2-10,mheight)
        mi_selectnode(motor_dia/2,mheight-10)
        mi_selectnode(motor_dia/2,10)
        mi_selectnode(motor_dia/4,0)
        mi_selectnode(motor_dia/2-canplate,mheight-gapheight-10)
        mi_selectnode(vcdia/2,mheight)
        mi_selectnode(vcdia/2,mheight-gapheight)
        mi_deleteselectednodes()
end

--Materials
ecwdia	= 0 
mi_addmaterial("Air",1,1,0,0,0,0,1,0,0,0,0,0)
mi_addmaterial("Steel",1404,1404,0,0,5.8,0,20,1,0,0,0,0,0)
mi_addbhpoint("Steel", 0, 0)
mi_addbhpoint("Steel", 0.388330, 79.577472)
mi_addbhpoint("Steel", 0.482524, 100.182101)
mi_addbhpoint("Steel", 0.595293, 126.121793)
mi_addbhpoint("Steel", 0.726634, 158.777930)
mi_addbhpoint("Steel", 0.873453, 199.889571)
mi_addbhpoint("Steel", 1.028101, 251.646061)
mi_addbhpoint("Steel", 1.178099, 316.803620)
mi_addbhpoint("Steel", 1.308718, 398.832128)
mi_addbhpoint("Steel", 1.408663, 502.099901)
mi_addbhpoint("Steel", 1.475645, 632.106325)
mi_addbhpoint("Steel", 1.516957, 795.774715)
mi_addbhpoint("Steel", 1.544297, 1001.821011)
mi_addbhpoint("Steel", 1.567545, 1261.217929)
mi_addbhpoint("Steel", 1.592042, 1587.779301)
mi_addbhpoint("Steel", 1.619381, 1998.895710)
mi_addbhpoint("Steel", 1.649135, 2516.460605)
mi_addbhpoint("Steel", 1.679984, 3168.036204)
mi_addbhpoint("Steel", 1.710511, 3988.321282)
mi_addbhpoint("Steel", 1.740077, 5020.999013)
mi_addbhpoint("Steel", 1.769441, 6321.063250)
mi_addbhpoint("Steel", 1.800555, 7957.747155)
mi_addbhpoint("Steel", 1.835625, 10018.210114)
mi_addbhpoint("Steel", 1.876121, 12612.179293)
mi_addbhpoint("Steel", 1.922187, 15877.793010)
mi_addbhpoint("Steel", 1.972386, 19988.957103)
mi_addbhpoint("Steel", 2.023674, 25164.606052)
mi_addbhpoint("Steel", 2.071950, 31680.362037)
mi_addbhpoint("Steel", 2.113538, 39883.212823)
mi_addbhpoint("Steel", 2.147083, 50209.990127)
mi_addbhpoint("Steel", 2.174427, 63210.632497)
mi_addbhpoint("Steel", 2.199604, 79577.471546)
mi_addbhpoint("Steel", 2.226937, 100182.101136)
mi_addbhpoint("Steel", 2.259850, 126121.792926)
mi_addbhpoint("Steel", 2.300931, 158777.930096)
mi_addbhpoint("Steel", 2.352597, 199889.571030)
mi_addbhpoint("Steel", 2.417636, 251646.060522)
mi_addbhpoint("Steel", 2.499516, 316803.620370)

--Circuits
mi_addcircprop("FieldCoil", start_i, 1)

--Blocks
function draw_blocks(motor_dia, wire_dia)
	mi_addmaterial("Magnet Wire",1,1,0,0,58,0,0,1,3,0,0,1,wire_dia)
	mi_addblocklabel(vcdia/4,botplate)
	mi_selectlabel(vcdia/4,botplate)
	mi_setblockprop("Steel",1,0,"",0,0,0)
	mi_clearselected()
	mi_addblocklabel(motor_dia/2+20, mheight+20)
	mi_selectlabel(motor_dia/2+20, mheight+20)
	mi_setblockprop("Air",1,0,"",0,0,0)
	mi_clearselected()
	mi_addblocklabel(vcdia/2+12,botplate+10)
	mi_selectlabel(vcdia/2+12,botplate+10)
	local fcw		= motor_dia/2-canplate-vcdia/2-10
	local fch		= mheight-botplate-gapheight-10
	local fcrounds	= (fcw/wire_dia)*(fch/wire_dia)*fc_wind_factor
	mi_setblockprop("Magnet Wire",1,0,"FieldCoil",0,0,fcrounds)
end

function clear_blocks(motor_dia)
	mi_clearselected()
	mi_selectlabel(vcdia/4,botplate)
    mi_selectlabel(motor_dia/2+20, mheight+20)
    mi_selectlabel(vcdia/2+20,botplate+10)
	mi_deleteselectedlabels()
	mi_deletematerial("Magnet Wire")
end

--Analyzer
function store_result(md, wd, cr, vt, pw, bn)
	local val = {}
	val['motordia'] = md
	val['wiredia']  = wd
	val['current']  = cr
	val['voltage']  = vt
	val['power']	= pw
	val['fluxden']  = bn
	return val
end
cstep = 0
for mdia=min_mdia,max_mdia,10 do
    draw_geometry(mdia)
    draw_boundary(mdia)
    mi_saveas(save_path..filename..".fem") 
    for ecwdia=min_ecwdia,max_ecwdia,0.1 do        
    	print("Record: "..count.."")
        draw_blocks(mdia, ecwdia)   
        local pass = 0   
        avg_Bn = 0
        current = 0
        voltage = 0     
        while (avg_Bn < flux and voltage < max_voltage and current < max_current) do 
                print("Motor Diameter: "..mdia.."mm")
                print("Wire Diameter: "..ecwdia.."mm")
                mi_modifycircprop("FieldCoil",1,start_i+current_step*pass)
                mi_createmesh()
                mi_showmesh()
                mi_analyze(1)
                mi_loadsolution()
                mo_seteditmode("contour")
                mo_addcontour(vcdia/2,mheight)
                mo_addcontour(vcdia/2,mheight-gapheight)
                total_Bn, avg_Bn = mo_lineintegral(0)
                print("Average Flux Density: "..avg_Bn.."T")
                current, voltage, flux_linkage = mo_getcircuitproperties("FieldCoil")
                print("Current: "..current.."A")
                print("Voltage: "..voltage.."V") 
                print("")
                pass = pass+1               
                --TODO: Break System
        end          
        local dpow = current*voltage      
        d_candidates[count]=store_result(mdia, ecwdia, current, voltage, dpow, avg_Bn)
        count = count+1
        clear_blocks(mdia)
    end
    clear_geometry(mdia)    
    clear_boundary(mdia)
end

--Optimization
print("Begin optimization")
min_bn = d_candidates[1]['fluxden']
max_bn = d_candidates[1]['fluxden']
min_pow = d_candidates[1]['power']
max_pow = d_candidates[1]['power']
for i=1,count-1,1 do
    if d_candidates[i]['power'] < min_pow then
    	min_pow = d_candidates[i]['power']
    elseif d_candidates[i]['power'] > max_pow then
    	max_pow = d_candidates[i]['power']
    end
    if d_candidates[i]['fluxden'] < min_bn then
    	min_bn = d_candidates[i]['fluxden']
    elseif d_candidates[i]['fluxden'] > max_bn then
    	max_bn = d_candidates[i]['fluxden']
    end
end 

function normalize(val, min, max)
	if min == max then
		return 1
	else
		return (val - min)/(max - min)
	end
end

for i=1,count-1,1 do
	local df = normalize(d_candidates[i]['motordia'], min_mdia, max_mdia)
	local dp = normalize(d_candidates[i]['power'], min_pow, max_pow)
	local db = normalize(d_candidates[i]['fluxden'], min_bn, max_bn)
	local sum = (-1)*w['dia']*df + (-1)*w['pow']*dp + w['flx']*db
	score[i] = sum
end
best_score = score[1]
best_result = 1
for i=1,count-1,1 do
	if score[i] > best_score then
		best_result = i
	end
end
obj = d_candidates[best_result]
	    
--Remodel
print("Modeling Result")
mdia = obj['motordia']
ecw = obj['wiredia']
mi_modifymaterial("Magnet Wire",11,ecwdia)
draw_geometry(mdia)
draw_boundary(mdia)
draw_blocks(mdia, ecw)   
mi_modifycircprop("FieldCoil",1,obj['current'])
mi_createmesh()
mi_showmesh()
mi_saveas(save_path..filename..".fem")
mi_analyze(1)
mi_loadsolution()
mo_seteditmode("contour")
mo_addcontour(vcdia/2,mheight)
mo_addcontour(vcdia/2,mheight-gapheight)
total_Bn, avg_Bn = mo_lineintegral(0)
print("Average Flux Density: "..avg_Bn.."T")
current, voltage, flux_linkage = mo_getcircuitproperties("FieldCoil")
print("Current: "..current.."A")
print("Voltage: "..voltage.."V") 
print("Wire diameter: "..ecw.."mm")
mo_makeplot(1,300)
messagebox("Simulation Finished")
