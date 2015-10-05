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
            //echo 'update has been scheduled for run, please do not disconct box while update is in progress. <br>';
            $python = `python update.py`;
            echo '<br>';
            echo $python;
	    //echo $python;
	
        ?>
    <br>
    <br>
    <br>	
    </body>
    <div align="center">
            <a id="btnBack" href="/systeminfo/content.html">Back </a>
    </div>
</html>


