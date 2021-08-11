# Installing pgadmin in manjaro with docker

## Background
+ I was trying to install pgadmin on manjaro.
+ But unfortunately, it's not available on the pacman's repo.
+ So I searched on the aur. But unfortunately, the package was flagged
  out-of-date so even though it installed just fine, I was getting errors when
  I tried running it.
+ The only thing left was building the source code. But I found it too
  complicated with no .install file or the configure file.
+ My final option was running it on docker. And I finally succeededj

## Installation commands
+ sudo pacman -Syu
+ pacman -Ss docker
+ sudo pacman -S docker
+ sudo usermod -aG docker $USER 
+ reboot
+ docker pull dpage/pgadmin4
+ docker run --rm --network host -e 'PGADMIN_DEFAULT_EMAIL=mtnekros@gmail.com' -e 'PGADMIN_LISTEN_PORT=5050' -e 'PGADMIN_DEFAULT_PASSWORD=postgres' -d --name pgadmin dpage/pgadmin4 
    * --rm => remove after stoping (a pretty usefull command)
    * --network host => makes it so it uses the same network as the host (The
      most important command for my needs because I have my postgres on the host
      and not in a container. Also -p options is ignored with a warning when this
      is enabled.)
    * -e => add environment variables
    * -e 'PGADMIN_DEFAULT_PORT=5050' => I don't want pgadmin to run on port 80.
    * -d => run detached
    * --name pgadmin => give name to the container
    * !TODO figure out the way to backup & restore docker container using volumes
+ docker run --network host -e 'PGADMIN_DEFAULT_EMAIL=mtnekros@gmail.com' -e 'PGADMIN_LISTEN_PORT=5050' -e 'PGADMIN_DEFAULT_PASSWORD=postgres' -d --name pgadmin dpage/pgadmin4 
    * the same command but without the --rm so the container persists.

## Useful command
+ docker stop pgadmin
+ docker restart pgadmin
+ docker start pgadmin

And we are done.
