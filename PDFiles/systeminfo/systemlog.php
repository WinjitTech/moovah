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
         
            $file = fopen("/home/pi/default.log","r");
            while(! feof($file))
            {
                echo fgets($file). "<br />";
            }
            fclose($file);  
//            $file = fopen("textfile.txt","r");
//            while(! feof($file))
//            {
//                echo fgets($file). "<br />";
//            }
//            fclose($file);
       
        ?>
        <div align="center">
            <a id="btnBack" href="generatelog.html">Back </a>
        </div>
    </body>
</html>
