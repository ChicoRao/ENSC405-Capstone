#!/bin/bash
export FLASK_APP=server.py
export FLASK_ENV=development
# socketio run > ~/backend & pids=$!
npm start --prefix ./frontend & pids+=" $!"
python3 ~/Desktop/ENSC405-Capstone/management_software/backend/server.py

trap "kill $pids" SIGTERM SIGINT
wait $pids