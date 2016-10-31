naotime=`ssh nao@169.254.28.227 'date +%s%3N'`
ourtime=`date +%s%3N`
difference=`expr $ourtime - $naotime`
echo $difference

