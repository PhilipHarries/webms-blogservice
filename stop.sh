[[ -f ../blogservice.pid ]] && kill -9 $( cat ../blogservice.pid )
for Y in $( ps -ef|grep python|grep blogservice|awk '{print $2}' );do
    echo $Y
    kill -9 $Y
done
