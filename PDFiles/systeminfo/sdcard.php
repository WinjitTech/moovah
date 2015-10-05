<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
<html>
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <?php
            echo '<br>';
            $python = `python /home/pi/sdcard.py`;
	    //echo '<br>';
            //echo $python;
	    $res = split('/', $python);
            foreach ($res as $value){
                echo "$value <br>";
            }
        ?>
    <br>
    <br>
    <br>	
    <div align="center">
            <a id="btnBack" href="/systeminfo/content.html">Back </a>
    </div>			
    </body>
</html>
