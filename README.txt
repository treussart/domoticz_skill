Exemples phrases :
python say_command.py turn on light living room
python say_command.py turn off light living room
python say_command.py turn off the light in the living room
python say_command.py turn on the light in the living room

python say_command.py allume la lumiére du salon
python say_command.py eteind la lumiere du salon

python say_command.py turn on light corridor
python say_command.py turn off light corridor

python say_command.py get temperature living room
python say_command.py get next trains
python say_command.py can I get the next trains

API Domoticz :
curl -sS "http://192.168.0.8:8080/json.htm?type=command&param=switchlight&idx=58&switchcmd=On"

curl -sS "http://192.168.0.8:8080/json.htm?type=devices&rid=52"

curl -sS "http://192.168.0.8:8080/json.htm?type=devices&rid=152"

curl -sS "http://192.168.0.8:8080/json.htm?type=devices&rid=81"

Principe config :
what-where
exemple (la case ne compte pas) :
temperature-living room

Dev:
sudo service mycroft-skills restart

sudo tailf /var/log/mycroft-skills.log