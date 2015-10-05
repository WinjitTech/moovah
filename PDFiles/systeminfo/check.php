<html>
<head></head>
<body>
<!--<div align="center">
  <a id="btnBack" href="demo.html">Back</a>
</div>-->
<div align="center">
<?php
function is_connected()
{
    $connected = @fsockopen("www.google.com", 80); 
                                        //website, port  (try 80 or 443)
    if ($connected){
        $is_conn = true; //action when connected
	echo "You are connected to internet";
        fclose($connected);
    }else{
        $is_conn = false; //action in connection failure
	echo "You are not connected to internet";
    }
    return $is_conn;

}
is_connected();
?>
</div>
</body>
</html>