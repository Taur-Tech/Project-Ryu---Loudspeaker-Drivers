
// 31mm Voice Coil Design for F144
// All units are in mm
former_thickness    = 0.1;
former_height       = 28;
former_outer_radius = 15.5;

winding_height      = 6;
wire_diameter       = 0.173;
layers_per_side     = 1;
turns_per_layer     = 32;

// Draw former
color("black"){
    rotate_extrude($fn=1000)
        translate([former_outer_radius-former_thickness, 0, 0])
            square([former_thickness, former_height]);        
}

// Draw outer side coil
color("gold"){
    rotate_extrude($fn=1000)
        translate([former_outer_radius, 0, 0])
            square([wire_diameter*layers_per_side, wire_diameter*turns_per_layer]);
}
// Draw inner side coil
color("gold"){
    rotate_extrude($fn=1000)
        translate([former_outer_radius-former_thickness-(wire_diameter*layers_per_side), 0, 0])
            square([wire_diameter*layers_per_side, wire_diameter*turns_per_layer]);
}
