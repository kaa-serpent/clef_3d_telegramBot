// Documentation Générer une clef Pollux 7
// =========================
//
// création d'une copie d'une clef Pollux basée sur les coupes en mm
// paramètres :
// un, deux, trois, quatre, cinq, six, sept
//
// manche: bool, de base true si on le specifie à false, créer un petit manche pour des impréssions plus rapide
//
// Vue de face de la clef :
//
//          4
//       5     3
//     6         2
//       7     1
//         |_|
//
// Utilisation:
// ------
//
// appel du module :
//
//     clef_pollux7(un, deux, trois, quatre, cinq, six, sept);
//
// Example:
// --------
//
//     clef_pollux7(8,0,8,6.5,3,4,3);
//     clef_pollux7(8,0,8,6.5,3,4,3, manche=false);

module clef_pollux7(un, deux, trois, quatre, cinq, six, sept, manche=true){
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
            difference() {
                cylinder(22, 2.5, 2.5, $fn = 50);  // Outer cylinder
                translate([0,0,5]) cylinder(18, 1.5, 1.5, $fn = 50);  // Inner cylinder
            }
            // ajout des barres de combinaison de la clef ( 8 barres, 360°/8 pour l'angle de rotation entre chaque barre la 1 est l'entraineur)
            translate([0,0,4]){
                blankHeight = 12 + 3; // 14 is the blank size, 3 is the already cut part on the key
                 // barre 1
                
        difference(){
            union() {
                translate([2,-0.5,0]) cube([3.5, 1, blankHeight]);
                // barre 2
                rotate([0,0,45]) translate([2,-0.5,0]) cube([2.5, 1, blankHeight-un]);
                // barre 3
                rotate([0,0,45*2]) translate([2,-0.5,0]) cube([2.5, 1, blankHeight-deux]);
                // barre 4
                rotate([0,0,45*3]) translate([2,-0.5,0]) cube([2.5, 1, blankHeight-trois]);
                // barre 5
                rotate([0,0,45*4]) translate([2,-0.5,0]) cube([2.5, 1, blankHeight-quatre]);
                // barre 6
                rotate([0,0,45*5]) translate([2,-0.5,0]) cube([2.5, 1, blankHeight-cinq]);
                // barre 7
                rotate([0,0,45*6]) translate([2,-0.5,0]) cube([2.5, 1, blankHeight-six]);
                // barre 8
                rotate([0,0,45*7]) translate([2,-0.5,0]) cube([2.5, 1, blankHeight-sept]);
            }
            
        difference(){
            cylinder(4,6,6);
            cylinder(5,2.5,5);
            }
        }
    }}
}

clef_pollux7(8,0,8,6.5,3,4,3);
