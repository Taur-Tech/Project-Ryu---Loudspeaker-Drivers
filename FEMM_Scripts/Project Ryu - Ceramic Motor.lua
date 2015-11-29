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
--      in the code under User Variables to avoid being prompted all the time;
--2.	Set mtype parameter under User Variables to choose underhung (1) or 
--      overhung (0) motors;
--3.    If you are usign a copper sleeve over the central pole piece and inside
--      the gap set the cslv_th parameter under User Constants to the thickness
--      of the copper sleeve;
--4.    Set the save_path parameter under User Constants to your work folder 
--      path. Use double back-slashes between folders.

--Advanced Settings:
--1.    The script simulates various geometries including t-shaped central pole
--      piece. The T-shape trimming in the central pole piece is simulated from 
--      min_tscp to max_tscp values under User Constants;
--2.    You can set the minimum and maximum clearance between the voice coil
--      and the steel pieces inside the magnetic cap, by setting the min_cgap and 
--      max_cgap parameters under User Constants;
--3.    The script will only simulate Ceramic 5 magnets of various sizes. To add
--      a new magnet size, update the m_ringC5_metric array under Program Constants.
--      Use metric values and also increment m_ringC5_size parameter with the 
--      number of magnets added;
--4.    The script wil calculate a minimum value for the bottom plate thickness
--      to avoid saturation. You can set how much more over this value you want 
--      to use to have a safe overhead by modifying the st_overhead parameter 
--      under User Constants. The final value will be the product between
--      minimum plate thickness and st_overhead.

--Setting your objective:
--      This script will simulate a number of motor structures defined by the 
--      input parameters and will record results for structures that reach a
--      flux density value in the magnetic gap egual or higher than 
--      sqrt(2)*(target flux density value).
--      After all simulations are complete, the script will determine the best 
--      result by applying a weighted sum to three criteria: motor diameter, 
--      xmax and flux density. 
--      The weights vector is defined in w parameter under User Constants and 
--      take a value between 0 and 1 with 0 meaning ignore criteria and 1 meaning
--      most important criteria.
--      e.g.
--          Motor diameter and flux density are important but we can sacrifice
--          both to reach a better xmax value. Motor diameter can be sacrificed 
--          to get a better flux desnsity value.
--          w  = {['dia'] = 0.5, ['xmx'] = 1, ['flx'] = 0.7}

prompter    = 1
--User Variables
vcdia       = 50    --voice coil diameter [mm]
vch         = 15    --voice coil height [mm]
vcw         = 0.5   --voice coil width [mm]
xmax        = 5     --desired xmax in one direction [mm]
flux        = 1     --desired flux density in gap [mm]
mtype       = 0     --0 for overhang, 1 for underhung
filename    = 'default'

--User Constants
min_tscp        = 0
max_tscp        = 8	--this only is considered when the prompter is 0
min_cgap        = 0.2
max_cgap        = 0.5
cslv_th         = 0
st_overhead     = 1.2
save_path       = "C:\\temp\\"
w               = {['dia'] = 0.5, ['xmx'] = 0.5, ['flx'] = 0.5}

--Program Variables
d_candidates    = {}
m_list          = {}
obj             = {}

--Program Constants
m_ringC5_metric ={
                {['od']=60, ['id']=30, ['th']=16},
                {['od']=70, ['id']=32, ['th']=18},
                {['od']=75, ['id']=32, ['th']=20},
                {['od']=80, ['id']=32, ['th']=20},
                {['od']=80, ['id']=40, ['th']=20},
                {['od']=80, ['id']=60, ['th']=20},                
                {['od']=90, ['id']=32, ['th']=18},
                {['od']=90, ['id']=45, ['th']=18},
                {['od']=100, ['id']=45, ['th']=20},
                {['od']=100, ['id']=50, ['th']=20},
                {['od']=100, ['id']=60, ['th']=20},
                {['od']=120, ['id']=45, ['th']=20},
                {['od']=120, ['id']=60, ['th']=20},
                {['od']=133, ['id']=60, ['th']=20},
                {['od']=140, ['id']=62, ['th']=20},
                {['od']=140, ['id']=65, ['th']=20},
                {['od']=140, ['id']=70, ['th']=20},
                {['od']=140, ['id']=75, ['th']=20},
                {['od']=145, ['id']=60, ['th']=24},
                {['od']=156, ['id']=60, ['th']=25},
                {['od']=156, ['id']=80, ['th']=25},
                {['od']=169, ['id']=85, ['th']=25},
                {['od']=180, ['id']=80, ['th']=25},
                {['od']=180, ['id']=85, ['th']=25},
                {['od']=180, ['id']=95, ['th']=25},
                {['od']=190, ['id']=90, ['th']=25},
                {['od']=200, ['id']=86, ['th']=25},
                {['od']=211, ['id']=89, ['th']=25},
                {['od']=210, ['id']=110, ['th']=25},
                {['od']=220, ['id']=110, ['th']=25},
            }
m_ringC5_size   = 30
miu_zero        = 1.2566370614*10^6
_pi             = 3.14159265359
steel_sat		= 16000


--Init 
newdocument(0)
showconsole()
clearconsole()
print("Ceramic Motor Simulation Script")
if prompter==1 then
	repeat	
		messagebox("Please input your specific data in millimiters")
		vcdia = tonumber(prompt("Voice Coil Diameter [mm]"))
		vch = tonumber(prompt("Voice Coil Height [mm]"))
		vcw = tonumber(prompt("Voice Coil Thickness [mm]"))
		xmax = tonumber(prompt("Desired One Way Xmax [mm]"))
		flux = tonumber(prompt("Desired Flux Density [T]"))
		print("User Input Data")		
		print("Voice Coil Dia:"..vcdia.."mm")
		print("Voice Coil Height:"..vch.."mm")
		print("Voice Coil Width:"..vcw.."mm")
		print("Xmax:"..xmax.."mm")	
		print("Flux Density:"..flux.."T")
		messagebox("Verify Input Data...Voice Coil Dia:"..vcdia.."mm Voice Coil Height:"..vch.."mm Voice Coil Thickness:"..vcw.."mm Xmax:"..xmax.."mm Flux Density:"..flux.."T")
		local confirm = prompt("Confirm? [type yes if data is ok, press return to go back]")
		if confirm == "yes" then 
			max_tscp = vcdia/6
			prompter = 0				
		end
	until prompter==0 
end
key = 0
for index=1,30,1 do
    if (m_ringC5_metric[index]['id']-5) > vcdia and (m_ringC5_metric[index]['id']-25) <= vcdia then
        m_list[key] = m_ringC5_metric[index]
        key = key+1
    end
end

--Preprocessor Script
mi_probdef(0,"millimeters","axi",1E-8)
mi_addboundprop("MBound", 0,0,0,0,0,0,0,0,0)

--Boundary
function draw_boundary()
    mi_addnode(0,-20)
    mi_addnode(150,-20)
    mi_addnode(0,100)
    mi_addnode(150,100)
    mi_addsegment(0,-20,150,-20)	
    mi_addsegment(0,-20,0,100)
    mi_addsegment(0,100,150,100)
    mi_addsegment(150,-20,150,100)
    mi_selectsegment(0,-20,150,-20)	
    mi_selectsegment(0,-20,0,100)
    mi_selectsegment(0,100,150,100)
    mi_selectsegment(150,-20,150,100)
    mi_setsegmentprop("MBound",0,1,0,0)
end

function clear_boundary()
    mi_clearselected()
    mi_selectnode(0,-20)
    mi_selectnode(150,-20)
    mi_selectnode(0,100)
    mi_selectnode(150,100)
    mi_deleteselectednodes()
end

--Geometry
function draw_geometry(v_dia, magnet, magnet_no, cp_trim, c_gap_i, c_gap_e, _xmax, pw)	
    local flare = magnet_no*magnet['th']/3
    if flare > 10 then
        flare = 10
    end
    local cpole = vcdia/2-vcw/2-c_gap_i
    local pdia = magnet['od']-8
    --central pole piece and bottom plate
    mi_addnode(v_dia/2, flare)
    mi_addnode(v_dia/2+flare, 0)
    if v_dia > 0 then
        mi_addarc(v_dia/2, flare, v_dia/2+flare, 0, 90, 10)
    else
        mi_addsegment(v_dia/2, flare, v_dia/2+flare, 0, 90)
    end    
    mi_addnode(pdia/4, 0)
    mi_addsegment(v_dia/2+flare, 0, pdia/4, 0)
    mi_addnode(pdia/2, pw/2)
    mi_addsegment(pdia/4, 0, pdia/2, pw/2)
    mi_addnode(pdia/2, pw)
    mi_addsegment(pdia/2, pw/2, pdia/2, pw)
    mi_addnode(cpole-cp_trim, pw)
    mi_addsegment(cpole-cp_trim, pw, pdia/2, pw)
    mi_addnode(cpole-cp_trim, pw+magnet_no*magnet['th'])
    mi_addsegment(cpole-cp_trim, pw, cpole-cp_trim, pw+magnet_no*magnet['th'])
    mi_addnode(cpole, pw+magnet_no*magnet['th'])
    mi_addsegment(cpole-cp_trim, pw+magnet_no*magnet['th'], cpole, pw+magnet_no*magnet['th'])
    local tpw = 0
    if mtype == 1 then
        tpw = vch+_xmax*2
    else
        tpw = vch-_xmax*2        
    end    
    mi_addnode(cpole, pw+magnet_no*magnet['th']+tpw)
    mi_addsegment(cpole, pw+magnet_no*magnet['th'], cpole, pw+magnet_no*magnet['th']+tpw)
    mi_addnode(v_dia/2+flare, pw+magnet_no*magnet['th']+tpw)
    mi_addsegment(cpole, pw+magnet_no*magnet['th']+tpw, v_dia/2+flare, pw+magnet_no*magnet['th']+tpw)
    mi_addnode(v_dia/2,  pw+magnet_no*magnet['th']+tpw-flare)
    mi_addsegment(v_dia/2,  pw+magnet_no*magnet['th']+tpw-flare, v_dia/2, flare)
    mi_addsegment(v_dia/2,  pw+magnet_no*magnet['th']+tpw-flare, v_dia/2+flare, pw+magnet_no*magnet['th']+tpw)
    --magnet
    mi_addnode(magnet['id']/2, pw)
    mi_addnode(magnet['od']/2, pw)
    mi_addsegment(magnet['id']/2, pw, magnet['od']/2, pw)
    mi_addnode(magnet['id']/2, pw+magnet_no*magnet['th'])
    mi_addsegment(magnet['id']/2, pw, magnet['id']/2, pw+magnet_no*magnet['th'])
    mi_addnode(magnet['od']/2, pw+magnet_no*magnet['th'])
    mi_addsegment(magnet['id']/2, pw+magnet_no*magnet['th'], magnet['od']/2, pw+magnet_no*magnet['th'])
    mi_addsegment(magnet['od']/2, pw+magnet_no*magnet['th'], magnet['od']/2, pw)
    --top plate
    mi_addnode(pdia/2, pw+magnet_no*magnet['th'])
    mi_addnode(pdia/2, pw+magnet_no*magnet['th']+tpw)
    mi_addsegment(pdia/2, pw+magnet_no*magnet['th'], pdia/2, pw+magnet_no*magnet['th']+tpw)
    cpole = vcdia/2+vcw+c_gap_e
    mi_addnode(cpole, pw+magnet_no*magnet['th'])
    mi_addnode(cpole, pw+magnet_no*magnet['th']+tpw)
    mi_addsegment(cpole, pw+magnet_no*magnet['th'], cpole, pw+magnet_no*magnet['th']+tpw)
    mi_addsegment(cpole, pw+magnet_no*magnet['th']+tpw, pdia/2, pw+magnet_no*magnet['th']+tpw)
    mi_addsegment(cpole, pw+magnet_no*magnet['th'], pdia/2, pw+magnet_no*magnet['th'])
    return pw+magnet_no*magnet['th']+tpw, tpw
end

function clear_geometry(v_dia, magnet, magnet_no, cp_trim, c_gap_i, c_gap_e, _xmax, pw)
    mi_clearselected()
    local flare = magnet_no*magnet['th']/3
    if flare > 10 then
        flare = 10
    end
    local cpole = vcdia/2-vcw/2-c_gap_i
    local pdia = magnet['od']-8
    --central pole piece and bottom plate
    mi_selectnode(v_dia/2, flare)
    mi_selectnode(v_dia/2+flare, 0)    
    mi_selectnode(pdia/4, 0)
    mi_selectnode(pdia/2, pw/2)    
    mi_selectnode(pdia/2, pw)    
    mi_selectnode(cpole-cp_trim, pw)    
    mi_selectnode(cpole-cp_trim, pw+magnet_no*magnet['th'])    
    mi_selectnode(cpole, pw+magnet_no*magnet['th'])    
    local tpw = 0
    if mtype == 1 then
        tpw = vch+_xmax*2        
    else
        tpw = vch-_xmax*2        
    end
    mi_selectnode(cpole, pw+magnet_no*magnet['th']+tpw)    
    mi_selectnode(v_dia/2+flare, pw+magnet_no*magnet['th']+tpw)    
    mi_selectnode(v_dia/2,  pw+magnet_no*magnet['th']+tpw-flare)    
    --magnet
    mi_selectnode(magnet['id']/2, pw)
    mi_selectnode(magnet['od']/2, pw)    
    mi_selectnode(magnet['id']/2, pw+magnet_no*magnet['th'])
    mi_selectnode(magnet['od']/2, pw+magnet_no*magnet['th'])
    --top plate
    mi_selectnode(pdia/2, pw+magnet_no*magnet['th'])
    mi_selectnode(pdia/2, pw+magnet_no*magnet['th']+tpw)    
    cpole = vcdia/2+vcw+c_gap_e
    mi_selectnode(cpole, pw+magnet_no*magnet['th'])
    mi_selectnode(cpole, pw+magnet_no*magnet['th']+tpw)   
    mi_deleteselectednodes()
end
    
--Materials
mi_addmaterial("Air",1,1,0,0,0,0,1,0,0,0,0,0)
mi_addmaterial("Steel",902.6,902.6,0,0,5.8,0,20,1,0,0,0,0,0)
mi_addmaterial("Ceramic5",1.886,1.886,191262,0,0,0,0,0,0,0,0,0,0)
mi_addbhpoint("Steel", 0.000000, 0.000000)
mi_addbhpoint("Steel", 0.211862, 79.577472)
mi_addbhpoint("Steel", 0.265665, 100.182101)
mi_addbhpoint("Steel", 0.332377, 126.121793)
mi_addbhpoint("Steel", 0.414377, 158.777930)
mi_addbhpoint("Steel", 0.513811, 199.889571)
mi_addbhpoint("Steel", 0.631899, 251.646061)
mi_addbhpoint("Steel", 0.767784, 316.803620)
mi_addbhpoint("Steel", 0.917018, 398.832128)
mi_addbhpoint("Steel", 1.070353, 502.099901)
mi_addbhpoint("Steel", 1.214255, 632.106325)
mi_addbhpoint("Steel", 1.334637, 795.774715)
mi_addbhpoint("Steel", 1.422981, 1001.821011)
mi_addbhpoint("Steel", 1.480634, 1261.217929)
mi_addbhpoint("Steel", 1.517214, 1587.779301)
mi_addbhpoint("Steel", 1.544515, 1998.895710)
mi_addbhpoint("Steel", 1.571296, 2516.460605)
mi_addbhpoint("Steel", 1.602049, 3168.036204)
mi_addbhpoint("Steel", 1.638404, 3988.321282)
mi_addbhpoint("Steel", 1.680490, 5020.999013)
mi_addbhpoint("Steel", 1.727311, 6321.063250)
mi_addbhpoint("Steel", 1.776659, 7957.747155)
mi_addbhpoint("Steel", 1.825401, 10018.210114)
mi_addbhpoint("Steel", 1.870557, 12612.179293)
mi_addbhpoint("Steel", 1.910809, 15877.793010)
mi_addbhpoint("Steel", 1.947222, 19988.957103)
mi_addbhpoint("Steel", 1.982328, 25164.606052)
mi_addbhpoint("Steel", 2.018252, 31680.362037)
mi_addbhpoint("Steel", 2.055398, 39883.212823)
mi_addbhpoint("Steel", 2.092545, 50209.990127)
mi_addbhpoint("Steel", 2.128095, 63210.632497)
mi_addbhpoint("Steel", 2.161612, 79577.471546)
mi_addbhpoint("Steel", 2.194644, 100182.101136)
mi_addbhpoint("Steel", 2.230339, 126121.792926)
mi_addbhpoint("Steel", 2.272386, 158777.930096)
mi_addbhpoint("Steel", 2.324282, 199889.571030)
mi_addbhpoint("Steel", 2.389356, 251646.060522)
mi_addbhpoint("Steel", 2.471238, 316803.620370)

--Blocks
function draw_blocks(magnet, magnet_no, pw)	
    mi_addblocklabel(magnet['od']/6,2)
    mi_selectlabel(magnet['od']/6,2)
    mi_setblockprop("Steel",1,0,"",0,0,0)
    mi_clearselected()
    mi_addblocklabel(magnet['id']/2+2, pw+2)
    mi_selectlabel(magnet['id']/2+2, pw+2)
    mi_setblockprop("Ceramic5",1,0,"",270,0,0)
    mi_clearselected()
    mi_addblocklabel(140, 90)
    mi_selectlabel(140, 90)
    mi_setblockprop("Air",1,0,"",0,0,0)
    mi_clearselected()
    mi_addblocklabel(magnet['od']/2-6,pw+magnet_no*magnet['th']+2)
    mi_selectlabel(magnet['od']/2-6,pw+magnet_no*magnet['th']+2)
    mi_setblockprop("Steel",1,0,"",0,0,0)
    mi_clearselected()
end

function clear_blocks(magnet, magnet_no, pw)
    mi_clearselected()
    mi_selectlabel(magnet['od']/6,2)
    mi_selectlabel(magnet['id']/2+2, pw+2)
    mi_selectlabel(140, 90)
    mi_selectlabel(magnet['od']/2-6,pw+magnet_no*magnet['th']+2)
    mi_deleteselectedlabels()
end

--Analyser
function store_result(vd, mg, mn, ct, ci, ce, xm, pt, bn)
    local r     = {}
    r['vdia']   = vd      --vent diameter 
    r['magnet'] = mg    --magnet data    
    r['mag_no'] = mn    --magnet number
    r['cp_tr']  = ct    --T-shape central pole trim value
    r['cgap_i'] = ci    --gap clearance between the inside of the voice coil and 
                        --central pole piece
    r['cgap_e'] = ce    --gap clearance between the outside of the voice coil and
                        --top plate
    r['xmax']   = xm    --xmax value
    r['pl_th']  = pt    --bottom plate thickness
    r['flux']   = bn    --average flux density value in the gap
    return r
end
function min_plate_th(xm, gw, cpd, magnet, b)	
    if mtype == 1 then
        gh = vch+xm*2        
    else
        gh = vch-xm*2        
    end
    local p_gap     = _pi*miu_zero*(cpd+gw)*gh/gw
    local p_near    = 0.264*_pi*miu_zero*(cpd+gw)
    local p_above   = miu_zero*(cpd+gw)*log(1+cpd/gw)
    local tmp		= magnet['id']+2*gw-cpd
    local p_below   = 2*miu_zero*(cpd+gw)*log(tmp/gw+1)
    local k_leak    = (p_gap+3*p_near+p_above+p_below)/p_gap
    local flux      = b*10000*_pi*(cpd+gw)*gh*k_leak
    local thickness = flux/(steel_sat*_pi*cpd)
    return thickness
end
vent_dim = { vcdia/4, vcdia/3, vcdia/2 }
if tshape == 0 then
    min_tscp = 0
    max_tscp = 0
end
count = 1
step = 0
for i=1,key-1,1 do
    draw_boundary()
    for j=1,3,1 do
        for cpt=min_tscp,max_tscp,1 do
            for cg=min_cgap,max_cgap,0.1 do
                plate_th = min_plate_th(xmax, vcw+2*cg+cslv_th, vcdia-2*(cg+cslv_th), m_list[i], flux)*st_overhead
                if plate_th > 30 then
                	plate_th = 30
                end
                mheight, gapheight = draw_geometry(vent_dim[j], m_list[i], 1, cpt, cg+cslv_th, cg, xmax, plate_th)   --first use one magnet 
                draw_blocks(m_list[i], 1, plate_th)
                mi_saveas(save_path..filename..".fem")   
                mi_createmesh()
                mi_showmesh()
                mi_analyze(1)
                mi_loadsolution()
                mo_seteditmode("contour")
                mo_addcontour(vcdia/2,mheight)
                mo_addcontour(vcdia/2,mheight-gapheight)
                total_Bn, avg_Bn = mo_lineintegral(0)     
                print("[Step "..step.."]: Flux Density = "..avg_Bn.."T; Plate Thickness = "..plate_th.."mm")
                step = step+1
                if avg_Bn >= flux*0.7 then
                	print("Storing result")
                    d_candidates[count] = store_result(vent_dim[j], m_list[i], 1, cpt, cg+cslv_th, cg, xmax, plate_th, avg_Bn)
                    count = count + 1
                end     
                clear_blocks(m_list[i], 1, plate_th)           
                clear_geometry(vent_dim[j], m_list[i], 1, cpt, cg+cslv_th, cg, xmax, plate_th)                
            end
        end
    end 
    clear_boundary()
end

--Calculate scores
function normalize(min, max, val)
	if min == max then
		return 1
	else
		return (val - min)/(max - min)
	end    
end
min_bn = d_candidates[1]['flux']
max_bn = d_candidates[1]['flux']
min_dia = m_list[1]['od']
max_dia = m_list[key-1]['od']
for i=1,count-1,1 do
    if d_candidates[i]['flux'] < min_bn then
        min_bn = d_candidates[i]['flux']
    end
    if d_candidates[i]['flux'] > max_bn then
        max_bn = d_candidates[i]['flux']
    end
end
for i=1,count-1,1 do
    local score = 0
    score = (-1)*normalize(min_dia, max_dia, d_candidates[i]['magnet']['od'])*w['dia'] + normalize(min_bn, max_bn, d_candidates[i]['flux'])*w['flx']
    obj[i] = score
end
max_score = obj[1]
res_key = 0
for i=1,count-1,1 do
    if obj[i] > max_score then
        max_score = obj[i]
        res_key = i
    end
end
result  = d_candidates[res_key]
--Optimize plate thickness
plate_th = min_plate_th(result['xmax'], vcw+result['cgap_i']+result['cgap_e'], vcdia-2*result['cgap_i'], result['magnet'], result['flux'])*st_overhead
draw_boundary()
mheight, gapheight = draw_geometry(result['vdia'], result['magnet'], result['mag_no'], result['cp_tr'], result['cgap_i'], result['cgap_e'], result['xmax'], plate_th)
draw_blocks(result['magnet'], result['mag_no'], plate_th)
mi_saveas(save_path..filename..".fem")   
mi_createmesh()
mi_showmesh()
mi_analyze(1)
mi_loadsolution()
mo_seteditmode("contour")
mo_addcontour(vcdia/2,mheight)
mo_addcontour(vcdia/2,mheight-gapheight)
total_Bn, avg_Bn = mo_lineintegral(0)  
mo_makeplot(1,300)
print("[Result]: Flux Density = "..avg_Bn.."T")
print("[Result]: Xmax = "..result['xmax'].."mm")
print("[Result]: Magnet inner diameter = "..result['magnet']['id'].."mm")
print("[Result]: Magnet outer diameter = "..result['magnet']['od'].."mm")
print("[Result]: Magnet thickness = "..result['magnet']['th'].."mm")
print("[Result]: Bottom Plate thickness = "..result['pl_th'].."mm")
print ("Finish")
