$fn=100;

difference(){
  cylinder(d=30,h=14);
  translate([0,0,-1])cylinder(d=7.2,h=17);
   translate([0,0,2]) difference(){
    cylinder(d=32,h=10);
    translate([0,0,-1])cylinder(d=12,h=17);
   }
}
