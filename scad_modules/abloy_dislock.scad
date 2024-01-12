$fn = 100;

cut_size = 2; // size of the cut on the key
spacing = 1.5; // spacing between each center of cut
initial_spacing = 1.5; // the blank space in the tip of the key before disc
disc_angle = 15; // angle rotation between each cut
key_blade_height = 29; // height of the keyblade from handle to tip
key_thickness_y = 5.9; // blank measurements if it was a square Y
key_thickness_x = 3.3; // blank measurements if it was a square X

// Function to create a cylinder with a rectangle hole
module cutter(cut, cut_index, position) {
    // every cut need to be rotated , 0 cut = no rotation, 6 cut = max rotation
    // move to desire place and rotate to cut angle
    translate(position){
        if (cut == 6) {
            difference(){
                cylinder(cut_size, d = key_thickness_y*2);
                cylinder(cut_size*2, d = key_thickness_y/2);
            }
        }
        else if (cut == 0){
            // do nothing already good shape
            }
        else{
            // Cutting shape for the right side
            rotate([0,0, cut * -disc_angle])
            difference(){
                cylinder(cut_size, d = key_thickness_x*2);
                cube([key_thickness_y, key_thickness_x*1.2, cut_size*2], center = true);
            }
            // Cutting shape for the left side
            rotate([0,0,90 - cut*disc_angle])
            difference(){
                cylinder(cut_size, d = key_thickness_x*2);
                cube([key_thickness_y, key_thickness_x*1.2, cut_size*2], center = true);
            }
        }
    }
}


module abloy_dislock_pro(list){
    difference() {
        import("abloy_dislockpro_blank.stl");
        union(){
            translate([0, 0, key_blade_height]){
                for (cut_index = [0 : len(list) - 1]) {
                    cut = list[cut_index];
                    // for each cut create a cut disc 2mm height
                    position = [0, 0, -(initial_spacing + spacing * (cut_index + 1) + cut_size/2)];
                    cutter(cut, cut_index, position);
                }
            }
        }
    }
}


abloy_dislock_pro([0,1,2,3,4,5,6,0,5,4,3]);