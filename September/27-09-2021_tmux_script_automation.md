# Script to setup tmux and vim for coding

### For django and vuejs setup

```bash 
#!/bin/bash

session=session1
if (tmux has -t $session&>/dev/null); then
  tmux attach -t $session
else
  # create session and django window
  tmux new-session -d -s $session -n 'django'
  tmux send-keys -t $session 'cd ./server/' C-m
  tmux send-keys -t $session 'vim -S vimsession' C-m
  # create vuejs window open vim session
  tmux new-window -t $session -n 'vuejs'
  tmux send-keys -t $session:2 'cd ./client/' C-m
  tmux send-keys -t $session:2 'vim -S vimsession' C-m
  # create runserver window and runser python and npm serve
  tmux new-window -t $session -n 'runserver'
  tmux send-keys -t $session:3 'cd ./server/ . venv/bin/activate && ./manage.py runserver 4502' C-m
  tmux split-window -h -t $session:3 \; \
    send-keys 'cd ./client/ && npm run serve' C-m \;
  tmux attach-session -t $session
fi
```

### For django only session
```bash
#!/bin/bash

session=session2
if (tmux has -t $session &> /dev/null); then
    tmux attach -t $session
else
    # create tmux session with window named django
    tmux new-session -d -s $session -n 'django'
    # start vim session for django
    tmux send-keys -t $session 'vim -S vimsession' C-m
    # create new window named runserver
    tmux new-window -t $session -n 'runserver'
    # activate virtualenv && runserver
    tmux send-keys -t $session:2 '. venv/bin/activate && ./run' C-m
    # vertical split window and and activate virtualenv
    tmux split-window -h -t $session:2 \; send-keys '. venv/bin/activate' C-m
    # attach session for tmux
    tmux attach-session -t $session
fi
```
