$fn = 100;
cut_size = 2;
spacing = 1.5;
initial_spacing = 3 - 1.5; 

// Function to create a cylinder with a rectangle hole
module cutter(cut, cut_index, position) {
    // Parameters for the sizes
    cylinder_diameter = 5.9;
    rectangle_size = 3.3;
    // every cut need to be rotated 15°, 0 cut = no rotation, 6 cut = 90°
    
    // move to desire place and rotate to cut angle
    translate(position){
        if (cut == 6) {
            difference(){
                cylinder(2, d = cylinder_diameter*2);
                cylinder(4, d = 3.9);
            }
        }
        else if (cut == 0){
            // do nothing already good shape
            }
        else{
            // Cutting shape for the right side
            rotate([0,0, cut * -15])
            difference(){
                cylinder(2, d = cylinder_diameter*2);
                cube([rectangle_size, cylinder_diameter, 4 ], center = true);
            }
            // Cutting shape for the left side
            rotate([0,0,90 - cut*15])
            difference(){
                cylinder(2, d = cylinder_diameter*2);
                cube([rectangle_size, cylinder_diameter, 4 ], center = true);
            }
        }
    }
}


module abloy_dislock_pro(list){
    difference() {
        import("blanks/abloy_dislockpro_blank.stl");
        union(){
            translate([0, 0, 29]){
                for (cut_index = [0 : len(list) - 1]) {
                    cut = list[cut_index];
                    // for each cut create a cut disc 2mm height
                    position = [0, 0, -(initial_spacing + spacing * (cut_index + 1) + 1)];
                    cutter(cut, cut_index, position);
                }
            }
        }
    }
}


abloy_dislock_pro([0,2,4,5,3,4,2,0,2,6,2]);