# coding=utf-8
import time
import datetime
from coap import coap
from influxdb import InfluxDBClient

# Definiciones
N_MOTE = 3      # definimos el número de motes en la red

# open
c = coap.coap(udpPort=5683)
client = InfluxDBClient(host='127.0.0.1', port=8086, username='root', password='root', database='grafana')

while(True):
    for x in range(2, N_MOTE+1):
        #### GET FROM MOTES ######
        # retrieve value of 'test' resource
        p = c.GET('coap://[bbbb::1415:92cc:0:{0}]:5683/IoT'.format(str(x)), )

        ##### PUT ON DB ######
        json_body = [
            {
                "measurement": "VariableIoT",
                "tags": {
                    "host": "Nodo"+format(x),
                    "region": "us-west"
                },
                "time": format(datetime.datetime.now()),
                "fields": {
                    "value": p[0]
                }
            }
        ]


        client.write_points(json_body)
        result = client.query('select value from VariableIoT;')
        print("Result: {0}/n".format(result))
        time.sleep(1)


# close
c.close()


