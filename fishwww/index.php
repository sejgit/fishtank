<!DOCTYPE html>
<html>
  <body>

    <h1>Fishtank</h1>

    <h3>Temp data now</h3>

    <?php
       $myfilename = "user_annotate.txt";
       if(file_exists($myfilename)){
       echo file_get_contents($myfilename);
       }
       ?>

    <h3>Temp graph</h3>
    <img src="plot.png" alt="temp run chart" width="640" height="480">

    <h3>Fishtank now</h3>
    <img src="cam.jpg" alt="camera" width="1296" height="972">

  </body>
</html>

