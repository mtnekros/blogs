# Script to setup tmux and vim for coding

```bash 
#!/bin/bash

if (tmux has -t mep&>/dev/null); then
  tmux attach -t mep
else
  # create session and django window
  tmux new-session -d -s mep -n 'django'
  tmux send-keys -t mep 'cd ~/allProject/MEPWithVue/server/' C-m
  tmux send-keys -t mep 'vact' C-m
  tmux send-keys -t mep 'vim -S vimsession' C-m
  # create vuejs window open vim session
  tmux new-window -t mep -n 'vuejs'
  tmux send-keys -t mep:2 'cd ~/allProject/MEPWithVue/client/' C-m
  tmux send-keys -t mep:2 'vim -S vimsession' C-m
  # create runserver window and runser python and npm serve
  tmux new-window -t mep -n 'runserver'
  tmux send-keys -t mep:3 'cd ~/allProject/MEPWithVue/server/ && . venv/bin/activate && ./manage.py runserver 4502' C-m
  tmux split-window -v -t mep:3 \; \
    send-keys 'cd ~/allProject/MEPWithVue/client/ && npm run serve' C-m \;
  tmux attach-session -t mep
fi
```
