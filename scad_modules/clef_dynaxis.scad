// Documentation Générer une clef dynaxis
// =========================
//
// création d'une copie d'une clef dynaxis basée sur les coupes en mm
// paramètres :
// un, deux, trois, quatre, cinq, six, sept
//
// manche: bool, de base true si on le specifie à false, créer un petit manche pour des impréssions plus rapide
//
// Vue de face de la clef :
//
//          4
//       3     5
//     2         6
//       1     7
//         |_|
//
// Utilisation:
// ------
//
// appel du module :
//
//     clef_dynaxis(un, deux, trois, quatre, cinq, six, sept);
//
// Example:
// --------
//
//     clef_dynaxis(8,0,8,6.5,3,4,3);
//     clef_dynaxis(8,0,8,6.5,3,4,3, manche=false);

module clef_dynaxis(un, deux, trois, quatre, cinq, six, sept, manche=true){
    union() {
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
        // shape kiz
        cylinder(22, 2.5, 2.5, $fn = 50); // base

        // ajout des barres de combinaison de la clef ( 8 barres, 360°/8 pour l'angle de rotation entre chaque barre la 8 est forcément 0)

        // barre 1
        translate([1.75, 1, 22-14]) rotate([0,0,45]) cube([1.4, 1, 14-un]);
        // barre 2
        translate([2.4, -0.5, 22-14]) cube([1, 1, 14-deux]);
        // barre 3
        translate([1, -1.75, 22-14]) rotate([0,0,-45]) cube([1.4, 1, 14-trois]);
        // barre 4
        translate([-0.5, -3.3, 22-14]) cube([1, 1, 14-quatre]);
        // barre 5
        translate([-1, -1.75, 22-14]) rotate([0,0,135]) cube([1, 1.4, 14-cinq]);
        // barre 6
        translate([-2.4, 0.5, 22-14]) rotate([0,0,-180]) cube([1, 1, 14-six]);
        // barre 7
        translate([-1, 1.75, 22-14]) rotate([0,0,135]) cube([1.4, 1, 14-sept]);
        // barre 8
        translate([-0.5, 2.3, 22-14]) cube([1, 1, 14]);

    }
}
