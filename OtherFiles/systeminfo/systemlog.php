<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
To change this template file, choose Tools | Templates
and open the template in the editor.
-->
<html>
    <head>
        <meta charset="UTF-8">
        <style>
        .styleLable
            {
                font-size: 22px;
            }
        .stylebutton
            {
                background-color: #FE5200;
                text-decoration: none;
                color: #FFEEF9;
                display: block;
                line-height: 40px;
                height: 40px;
                border-radius: 5px;
                width: 150px;
                text-align: center;
            }
#header {
    background-color:black;
    color:white;
    text-align:center;
    padding:5px;
}
#nav {
    line-height:30px;
    background-color:black;
    height:500px;
    width:150px;
    float:left;
    padding:5px;
}
#section {
    border:none;
    background-color:white;
    width:1150px;
    height:485px;
    float:left;
    padding:10px;
}
#footer {
    background-color:#FE5200;
    color:white;
    clear:both;
    text-align:center;
    padding:5px;
}
/*<style type="text/css">
            .styleLable
            {
                font-size: 22px;
            }
            .stylebutton
            {
                background-color: #FE5200;
                text-decoration: none;
                color: #FFEEF9;
                display: block;
                line-height: 40px;
                height: 40px;
                border-radius: 5px;
                width: 150px;
            }
            .styleContinue
            {
                color: #ACACAC;
                padding-top: 20px;
            }*/
</style>
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

        ?>
        <a id="btnVersion" href="/systeminfo/downloadlog.php" target="section" class="stylebutton">Dwonload Log</a>
    </body>
</html>
