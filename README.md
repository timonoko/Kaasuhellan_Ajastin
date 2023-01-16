# Kaasuhellan_Ajastin

ESP32-vehje kelaa siimalla vipuvarren päässä olevaa lieden pääkatkaisinta. Säätää
myös puoliliekin.

Havaitsee palohälytyksen, koska palohälyttimessä oleva transistori vetää
kun kaijuttimesta tulee ääntä.

Vehkeissä on myös eri ruokalajeille viritetty menyy.

Askelmoottori on entisestä skannerista ja näyttönappimoduuli on TM1638.

Mitään raja-antureita ei ole, sillä kun virrat katkaistaan, painovoima vetää rullauskelan takasin nolla-asentoon.
Kytkin nyt A4988:n enable pinnin, niin että toiminnan alussa vipua nostetaan 50 pykälää ja annetaan
sen jälkeen vapaasti pudota, jolloin nollaus on tarkka.

https://youtu.be/Kd3liw780tA

<image src=perunat2.png>
<image src=Perunat.png>
