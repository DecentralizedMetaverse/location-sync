import subprocess
subprocess.call("tmux new-window -t ':3' -d", shell=True)
subprocess.call("tmux send-keys -t ':3' 'sh exe2.sh 3' C-m", shell=True)
subprocess.call("tmux new-window -t ':4' -d", shell=True)
subprocess.call("tmux send-keys -t ':4' 'sh exe2.sh 4' C-m", shell=True)
subprocess.call("tmux new-window -t ':5' -d", shell=True)
subprocess.call("tmux send-keys -t ':5' 'sh exe2.sh 5' C-m", shell=True)
subprocess.call("tmux new-window -t ':6' -d", shell=True)
subprocess.call("tmux send-keys -t ':6' 'sh exe2.sh 6' C-m", shell=True)
subprocess.call("tmux new-window -t ':7' -d", shell=True)
subprocess.call("tmux send-keys -t ':7' 'sh exe2.sh 7' C-m", shell=True)
subprocess.call("tmux new-window -t ':8' -d", shell=True)
subprocess.call("tmux send-keys -t ':8' 'sh exe2.sh 8' C-m", shell=True)
subprocess.call("tmux new-window -t ':9' -d", shell=True)
subprocess.call("tmux send-keys -t ':9' 'sh exe2.sh 9' C-m", shell=True)
subprocess.call("tmux new-window -t ':10' -d", shell=True)
subprocess.call("tmux send-keys -t ':10' 'sh exe2.sh 10' C-m", shell=True)
