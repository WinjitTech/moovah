<?php
function is_connected()
{
    $connected = @fsockopen("www.google.com", 80); 
                                        //website, port  (try 80 or 443)
    if ($connected){
        $is_conn = true; //action when connected
	echo "true";
        fclose($connected);
    }else{
        $is_conn = false; //action in connection failure
	echo "false";
    }
    return $is_conn;
}
is_connected();
?>