// Documentation Générer une clef Cavith Cavers
// =========================
//
// création d'une copie d'une clef cavith basée sur les coupes en mm
// paramètres :
// un, deux, trois, quatre, cinq, [0,1,2]
//
// manche: bool, de base true si on le specifie à false, créer un petit manche pour des impréssions plus rapide
//
// Vue de face de la clef :
//
//          ()
//       4     3    
//       5     2
//          1
//
// Utilisation:
// ------
//
// appel du module :
//
//     clef_cavith(un, deux, trois, quatre, cinq, [2,3,4]);
//
// Example:
// --------
//
//     clef_cavith(8,0,8,6.5,[2,1,4]);
//     clef_cavith(8,0,8,6.5,[2,1,4], manche=false);

module clef_cavith(un, deux, trois, quatre, cinq, dimple_cuts, manche=true){
    union() {
       rotate([0,0,90]){ 
            if (manche) {
                // Handle
                rotate([0, 90, 0]) translate([10, 0, - 3.5]) {
                    linear_extrude(7) {
                        difference() {
                            scale(0.7) polygon(points = [[- 15, - 10], [0, - 20], [15, - 20], [20, - 15], [20, 15], [15, 20]
                                , [0, 20], [- 15, 10]]);
                            scale(0.3) polygon(points = [[- 15, - 15], [0, - 30], [15, - 30], [30, - 20], [30, 20], [15, 30]
                                , [0, 30], [- 15, 15]]);
                        }
                    }
                }
            }
            else {
                //small handle
                translate([- 4, - 7, - 5]) cube([8, 14, 5]);
            }
        }
        // shape kiz
            
        cylinder(22, 2.5, 2.5, $fn = 50);  // Outer cylinder
        // ajout des barres de combinaison de la clef ( 6 barres, 360°/6 pour l'angle de rotation entre chaque barre, la 4 est celle des coupes de goupilles
        translate([0,0,22-15]){
            blankHeight = 15; 
            // barre 1
            translate([2,-0.5,0]) cube([2, 1, blankHeight-un]);
            // barre 2
            rotate([0,0,60]) translate([2,-0.5,0]) cube([2, 1, blankHeight-deux]);
            // barre 3
            rotate([0,0,60*2]) translate([2,-0.5,0]) cube([2, 1, blankHeight-trois]);
            // barre 4
            rotate([0,0,60*3]) translate([2,-0.5,0]) cube([2, 1, blankHeight]);
            // barre 5
            rotate([0,0,60*4]) translate([2,-0.5,0]) cube([2, 1, blankHeight-quatre]);
            // barre 6
            rotate([0,0,60*5]) translate([2,-0.5,0]) cube([2, 1, blankHeight-cinq]);
        }
        // now cutting the dimple
        rotate([0,0,60*3]){
            cylinder([2,0.1,2.5]);
            translate([-dimple_cuts[1],0,22-8]) cylinder([2,0.1,2.5]);
            translate([-dimple_cuts[2],0,22-12]) cylinder([2,0.1,2.5]);
            }
    }
}

clef_cavith(8,0,8,6.5,3,[2,4,1]);
