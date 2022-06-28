#!/bin/bash

PY_CLEAN_DB_CMD=$(cat <<EOF
from tinydb import TinyDB, Query

db_camera = TinyDB('src/backend/database/camera.json')
db_processes = TinyDB('src/backend/database/processes.json')
db_sensors = TinyDB('src/backend/database/sensors.json')
db_system = TinyDB('src/backend/database/system.json')

db_camera.truncate()
db_processes.truncate()
db_sensors.truncate()
db_system.truncate()

db_system.insert({'Broker_IP': "", 'mqtt_connection': "false", 'start_time': "2021-06-19T00:00:00.000Z",
 'lastCarCount': 0, 'lastTruckCount': 0, 'lastBikeCount': 0, 'jsonLogicCarCount': 0, 'jsonLogicTruckCount': 0, 'jsonLogicBikeCount': 0
})


EOF
)

PY_SET_IP_CMD=$(cat <<EOF
from tinydb import TinyDB, Query

db_system = TinyDB('src/backend/database/system.json')

broker_ip = input("Enter the IP of the MQTT broker: ")

db_system.update({'Broker_IP': "{}".format(broker_ip)})
db_system.update({'mqtt_connection': "false"})


EOF
)

PY_SET_PASSWORD_CMD=$(cat <<EOF
from getpass import getpass
from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash

db_auth = TinyDB('src/backend/database/auth.json')

done = 0

while done == 0:

    pswd = getpass('Insert web interface password: ')
    confirm_pswd = getpass('Confirm password: ')

    if pswd == confirm_pswd:
        hash_pswd = generate_password_hash(pswd)
        db_auth.update({'password': "{}".format(hash_pswd)})
        done = 1
    else:
        print("\n[Error]: Passwords must match!\n")
        done = 0
EOF
)

PY_START_SCRIPTS_CMD=$(cat <<EOF

EOF
)


PS3='Please enter your choice: '
options=("Resume System" "Initialize System" "Reset System" "Change Web Interface Password" "Change MQTT Broker IP" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Resume System")
            echo
            echo "Starting System..."
            echo
            trap "exit" INT TERM ERR
            trap "kill 0" EXIT
            export FLASK_APP=src/backend/http_rest/app.py 
            flask run -h 0.0.0.0 &
            python3 src/backend/app.py &
            wait
            ;;
        "Initialize System")
            echo
            read -p 'This should be run only at the first time! Do you still want to proceed? (y/n): ' confirm_init_var

            if [[ $confirm_init_var == "y" ]]; then
                echo "Installing Python3 dependencies..."
                pip install -r backend/dependencies/dependencies.txt
                echo
                echo "Preparing database system..."
                echo
                python3 -c "$PY_CLEAN_DB_CMD"
                echo "[CONFIGURATION]"
                python3 -c "$PY_SET_IP_CMD"
                echo
                python3 -c "$PY_SET_PASSWORD_CMD"
                echo
                echo "Configuration Finished!"
                echo
                echo "Starting System..."
                echo
                trap "exit" INT TERM ERR
                trap "kill 0" EXIT
                export FLASK_APP=src/backend/http_rest/app.py 
                flask run -h 0.0.0.0 &
                python3 src/backend/app.py &
                wait

            elif [[ $confirm_init_var == "n" ]]; then
                echo
                echo "Abort Operation"
                echo
                break
            else 
                echo "Insert a valid answer!"
                echo
                break
            fi
            ;;
        "Reset System")
            echo
            read -p 'This will delete all files from database! Do you still want to proceed? (y/n): ' confirm_clean_var

            if [[ $confirm_clean_var == "y" ]]; then
                echo
                echo "Cleaning database..."
                echo
                python3 -c "$PY_CLEAN_DB_CMD"
                echo "[CONFIGURATION]"
                python3 -c "$PY_SET_IP_CMD"
                echo
                python3 -c "$PY_SET_PASSWORD_CMD"
                echo
                echo "Configuration Finished!"
                echo
                echo "Starting System..."
                echo
                trap "exit" INT TERM ERR
                trap "kill 0" EXIT
                export FLASK_APP=src/backend/http_rest/app.py 
                flask run -h 0.0.0.0 &
                python3 src/backend/app.py &
                wait

            elif [[ $confirm_clean_var == "n" ]]; then
                echo
                echo "Abort Operation"
                echo
                break
            else 
                echo "Insert a valid answer!"
                echo
                break
            fi
            ;;
        "Change Web Interface Password")
            echo
            python3 -c "$PY_SET_PASSWORD_CMD"
            echo
            echo "Password Changed!"
            echo
            break
            ;;
        "Change MQTT Broker IP")
            echo
            python3 -c "$PY_SET_IP_CMD"
            echo
            echo "Broker Updated!"
            echo
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done


