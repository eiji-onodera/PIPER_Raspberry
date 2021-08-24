import mesure
from datetime import datetime
from time import sleep

ring=mesure.measure_brix(16,18,18)
ring.move(1500)
sleep(3)