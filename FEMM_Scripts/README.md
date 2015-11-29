__This is also an H1__
==================

These scripts are meant to be used with FEMM software. Please visit the [FEMM homepage](http://www.femm.info/wiki/HomePage) for more information and download.
The purpose of these scripts is to provide a starting point for a loudspeaker magnetic circuit design by simulating various geometries and parameter sets and choosing the best result.
More details about each script is provided below.

__Usage__
------------------

1. Launch FEMM
2. Click the left bar button or go to File menu  to import Lua Script
3. Browse and select the desired script
4. If the script prompts you for information, provide the information
5. Wait for the simulation to finish
6. Inspect results
7. Make your own adjusments or export geomtry by going to File menu and export dxf

__Project Ryu Field Coil Motor__
------------------
Settings: 
1.    Set prompter to zero if you set your variables
      in the code under User Variables to avoid being prompted all the time
2.    Set the height of the motor by modifying 
      the mheight parameters under User Variables
3.    Limit the number of simulations by lowering
      the range of motor diameters which is max_mdia - min_mdia
      under User Constants
4.    Limit the number of simulations by lowering 
      the range of wire diameters used which is max_ecwdia - min_ecwdia
      under User Constants
5.    Set a maximum field coil voltage value by modifying the 
      max_voltage parameter under User Constants. The script will move to 
      the next simulation if the voltage on the field coil will get higher
      than this value.
6.    Set a maximum field coil current value by modifying the 
      max_current parameter under User Constants. The script will move to 
      the next simulation if the current through the field coil will get higher
      than this value.
7.    Set the project folder by modifying the save_path parameter under 
      User Constants, use double back-slashes between folders

Advanced Settings:
1.    Set the thickness of the bottom plate by modifying the botplate parameter
      under Program Constants
2.    Set the thickness of the steel can around the field coil by modifying
      the canplate parameter under Program Constants
3.    canplate parameter under Program Constants is reserved for later use
4.    The script will calculate the flux density at different current values
      through the field coil. Set the start current value by modifying the 
      start_i parameter under Program Constants
5.    Set the field coil current step value by modifying the current_step
      parameter under Program Constants
6.    The distance between the voice coil and the steel in the gap is set by
      gaclear parameter under Program Constants. If you plan to use a copper 
      sleeve on the central pole piece you should add half of the sleeve's 
      thickness to this value.

Setting Simulation Objective:
      The script will simulate a number of motor size, field coil sizes
      and field coil currents. After all simulations are done it will go 
      through the results and pick the best solution based on a defined objetive.
      The best solution is chose based on three parameters: motor size, field
      coil power and flux density in the gap. The score of each simulation is 
      determined with a weighted sum of these three parameters. Under User
      Constants we can find the weight vector w with w['dia'] being the wight 
      for motor size, w['pow'] - weight for field coil power and w['flx'] - 
      weight for flux density.
      The weights take values between 0 and 1 with 0 meaning ignore and 1 meaning
      the most important
      e.g.
          Objective: dont care about motor size, sacrifice a bit from flux
          density value for the best field coil power value
          Weight vector:
              w = { ['dia'] = 0, ['pow'] = 1, ['flx'] = 0.7 }
          Score:
              s = w['dia']*(motor diameter)+w['pow']*(fc power)+w['flx']*(flux)

__Project Ryu Ceramic Motor__
------------------
Settings: 
1.    Set prompter to zero if you set your variables
      in the code under User Variables to avoid being prompted all the time;
2.	Set mtype parameter under User Variables to choose underhung (1) or 
      overhung (0) motors;
3.    If you are usign a copper sleeve over the central pole piece and inside
      the gap set the cslv_th parameter under User Constants to the thickness
      of the copper sleeve;
4.    Set the save_path parameter under User Constants to your work folder 
      path. Use double back-slashes between folders.

Advanced Settings:
1.    The script simulates various geometries including t-shaped central pole
      piece. The T-shape trimming in the central pole piece is simulated from 
      min_tscp to max_tscp values under User Constants;
2.    You can set the minimum and maximum clearance between the voice coil
      and the steel pieces inside the magnetic cap, by setting the min_cgap and 
      max_cgap parameters under User Constants;
3.    The script will only simulate Ceramic 5 magnets of various sizes. To add
      a new magnet size, update the m_ringC5_metric array under Program Constants.
      Use metric values and also increment m_ringC5_size parameter with the 
      number of magnets added.

Setting your objective:
      This script will simulate a number of motor structures defined by the 
      input parameters and will record results for structures that reach a
      flux density value in the magnetic gap egual or higher than 
      sqrt(2)*(target flux density value).
      After all simulations are complete, the script will determine the best 
      result by applying a weighted sum to three criteria: motor diameter, 
      xmax and flux density. 
      The weights vector is defined in w parameter under User Constants and 
      take a value between 0 and 1 with 0 meaning ignore criteria and 1 meaning
      most important criteria.
      e.g.
          Motor diameter and flux density are important but we can sacrifice
          both to reach a better xmax value. Motor diameter can be sacrificed 
          to get a better flux desnsity value.
          w  = {['dia'] = 0.5, ['xmx'] = 1, ['flx'] = 0.7}
