ps -fu $USER|grep qqtt_socket|grep -v grep|awk '{print $2}' |xargs kill -9
