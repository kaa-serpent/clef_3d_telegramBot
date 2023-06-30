// Documentation Générer une clef fontaine
// =========================
//
// création d'une copie d'une clef fontaine basée sur les coupes en mm
// paramètres :
// un, deux, trois, quatre, cinq
//
// manche: bool, de base true si on le specifie à false, créer un petit manche pour des impréssions plus rapide 
//
// protected: bool, de base false, permet de réduire le diamètre pour les fontaines protégées
//
// Vue de face de la clef :
//        3
//   2          4
//   1          5
//       
// Utilisation:
// ------
//
// appel du module :
//
//     clef_fontaine(un, deux, trois, quatre, cinq);
//
// Example:
// --------
//
//     clef_fontaine(8,0,8,6.5,3);
//     clef_fontaine(8,0,8,6.5,3, manche=false);
//     clef_fontaine(8,0,8,6.5,3, protected=true);

module clef_fontaine(un, deux, trois, quatre, cinq, manche=true, protected=false){
    union() {
        if (manche) { 
            // Handle
            rotate([0,90,0]) translate([10,0,-3.5]){
                linear_extrude(7){
                    difference(){
                        scale(0.7) polygon(points=[[-15,-10],[0,-20],[15,-20],[20,-15],[20,15],[15,20],[0,20],[-15,10]]);
                        scale(0.3) polygon(points=[[-15,-15],[0,-30],[15,-30],[30,-20],[30,20],[15,30],[0,30],[-15,15]]);
                    }
                }
            }
        }
        else{
            //small handle
            translate([-4,-7,-5]) cube([8,14,5]);
        }
        // shape kiz
        difference(){
            if (protected){
                cylinder(30, 3.5, 3.5, $fn=50);
            }
            else{
                cylinder(30, 4, 4, $fn=50);
            }
            translate([2,-0.75,15]) cube([3, 1.5, 16]);
            translate([-4,-0.75,15]) cube([2, 1.5, 16]);
            rotate(-120) translate([-4,-0.75,15]) cube([2, 1.5, 16]);
            rotate(-60) translate([-4,-0.75,15]) cube([2, 1.5, 16]);
            // cut the key
            //1
            translate([-3,-2.5,30-un]) cylinder(20, 2, 2,$fn=50);
            //2
            translate([-3.5,2,30-deux]) cylinder(20, 2, 2,$fn=50);
            //3
            translate([0,4,30-trois]) cylinder(20, 2, 2,$fn=50);
            //4
            translate([3.5,2,30-quatre]) cylinder(20, 2, 2,$fn=50);
            //5
            translate([3,-2.5,30-cinq]) cylinder(20, 2, 2,$fn=50);
        }
    }   
  }