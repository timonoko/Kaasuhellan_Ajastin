# Kaasuhellan_Ajastin

ESP32-vehje kelaa siimalla vipuvarren päässä olevaa lieden pääkatkaisinta. Säätää
myös puoliliekin.

Havaitsee palohälytyksen, koska palohälyttimessä oleva transistori vetää
kun kaijuttimesta tulee ääntä.

Vehkeessä on myös eri ruokalajeille viritetty menyy.

Askelmoottori on entisestä skannerista ja näyttönappimoduuli on TM1638.

Mitään raja-antureita ei ole, sillä kun virrat katkaistaan, painovoima vetää rullauskelan takasin nolla-asentoon.
Kytkin myös A4988:n enable-pinnin, niin että toiminnan alussa vipua nostetaan 50 pykälää ja annetaan
sen jälkeen vapaasti pudota, jolloin nollaus on tarkka.

Hellan yläpuolella oleva lämpömittari TMP36GT9Z sammuttaa hanan, jos lämpötila on yli MAX_TEMP -- tai kun keittämistaä on kestänyt yli 3 minuuttia ja lämpötila on silti alle MIN_TEMP.

https://youtu.be/Kd3liw780tA

<image src=perunat2.png>
<image src=Perunat.png>
