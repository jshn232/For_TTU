#Get Docker IP
function getDockerIP()
{

  docker inspect --format '{{ .NetworkSettings.IPAddress }}' $1
}

#update /etc/hosts

rm /etc/hosts
touch /etc/hosts

echo "127.0.1.1       localhost.localdomain-001497179af4" > /etc/hosts
echo "127.0.1.1       localhost.localdomain-001497179af4-001497179af4" >> /etc/hosts
echo "127.0.1.1       -001497179af4" >> /etc/hosts

dockerip=$(getDockerIP msptl)
if [ $dockerip ]; then
strIP=$dockerip"  mstpl"
echo ${strIP} >> /etc/hosts
fi

dockerip=$(getDockerIP comRF)
if [ $dockerip ]; then
strIP=$dockerip"   comRF"
echo ${strIP} >> /etc/hosts
fi

dockerip=$(getDockerIP chp)
if [ $dockerip ]; then
strIP=$dockerip"   chp"
echo ${strIP} >> /etc/hosts
fi

dockerip=$(getDockerIP umeter)
if [ $dockerip ]; then
strIP=$dockerip"   umeter"
echo ${strIP} >> /etc/hosts
fi

dockerip=$(getDockerIP sample)
if [ $dockerip ]; then
strIP=$dockerip"   sample"
echo ${strIP} >> /etc/hosts
fi


dockerip=$(getDockerIP security)
if [ $dockerip ]; then
strIP=$dockerip"   security"
echo ${strIP} >> /etc/hosts
fi



