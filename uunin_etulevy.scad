include <roundedcube.scad>


$fn=80;
thei=6.5;
module tappi(th) {
  difference(){
    cylinder(d=5.5,h=th);
    translate([0,0,-1]) cylinder(d=2.5,h=10+th);
  }
}
module etulevy () {
  difference() {
  translate([-10,-10,0])cube([76.5+20,50+20,2]);
  //  cube([76.5,50,2]);
  for (x=[10.5:56/7:67])translate([x,50-3.5,-1])cylinder(d1=3,d2=8,h=4);
  for (x=[11.2:54.45/7:67])translate([x,5.8,-1])cylinder(d=6,h=4);
  translate([6.5,27,-1]) cube([63,15,4]);
  translate([1,11,-1])  cube([3,13,2.5]);
  }
  translate([4,5,-thei])tappi(thei);
  translate([76.5-4,5,-thei])tappi(thei);
  translate([4,50-4.5,-thei])tappi(thei);
  translate([76.5-4,50-4.5,-thei])tappi(thei);
}


module nappaimet () { 
  for (x=[11.2:54.45/7:67])translate([x,5.8,0])cylinder(d=5,h=8);
  for (x=[11.2:54.45/7:67])translate([x,5.8,0])cylinder(d=7,h=1);
  for (x=[11.2:54.45/7:67])translate([x-2,5.8,0])cube([4,20,1]);
  translate([9,22,0])cube([60,5,1]);
}


module kotelo () {
  difference() {
    roundedcube([120,90,50],radius=6);
    translate([2,2,2])roundedcube([116,86,46],radius=4);
    translate([0,0,-1])cube([120,92,11]);
    translate([14,20,0]) cube([80,60,60]);
    translate([110,30,30])rotate([0,90,0])cylinder(d=36,h=20);
    translate([105,35,20])cube(18);
  }
  translate([4.5,4.5,12])tappi(35);
  translate([120-4.5,4.5,12])tappi(35);
  translate([120-4.5,90-4.5,12])tappi(35);
  translate([4.5,90-4.5,12])tappi(35);
}

module kansi () {
  difference() {
    union (){
      difference() {
	translate([2.3,2.3,0])roundedcube([115.4,85.4,46],radius=3.4);
	translate([0,0,-1])cube([120,92,5]);
	translate([0,0,7])cube([120,92,50]);
      }
      translate([0,0,-3])difference() {
	translate([-5,-15,0])roundedcube([130,120,46],radius=3.4);
	translate([-10,-17,-1])cube([170,130,5]);
	translate([-10,-17,7])cube([170,130,50]);
      }
    }
    translate([4.5,4.5,-2])cylinder(d=3,h=10);
    translate([120-4.5,4.5,-2])cylinder(d=3,h=10);
    translate([120-4.5,90-4.5,-2])cylinder(d=3,h=10);
    translate([4.5,90-4.5,-2])cylinder(d=3,h=10);
    translate([8,8,-2])roundedcube([104,74,46],radius=4);
  }
}

//translate([-10,-10,2]) rotate([180,0,0]) color("RED") etulevy(); nappaimet();

//translate([16,25,50]) etulevy();
//kotelo();
kansi();
