# What is systemd & where does it lie in the boot and startup process?


## What is systemd?
Systemd is a system and service manager for Linux
operating system. It is one of the popular init systems. Now, what is an init
system?. According to wikipedia:

> In Unix-based computer operating systems, init (short for initialization) is
> the first process started during booting of the computer system. Init is a
> daemon process that continues running until the system is shut down. It is
> the direct or indirect ancestor of all other processes and automatically
> adopts all orphaned processes. Init is started by the kernel during the
> booting process; a kernel panic will occur if the kernel is unable to start
> it. Init is typically assigned process identifier 1.

So, systemd is the mother of all processes. It can manage devices,
login, network connection, servies and network logging. It does a lot of cool
stuff and is a useful tool. But, in this blog, we are just concerned with
learning where it lies in the boot and startup process and what it does during
this process?

## Boot & Startup Process
The Linux boot and startup process is comprised of following steps:
1. BIOS POST
2. Boot loader
3. Kernel Initialization
4. Start systemd

When your computer is powered, it runs POST (Power On Self Test) which is a
part of BIOS (Computer's built in firmware). This is a test to ensure all the
hardware is working correctly. If the hardwares pass the test, BIOS locates
boot sector in any attached bootable devices and loads it into memory. (Boot sector
is a **sector** of a persistent data storage device like hard disk that contains
machine code to be loaded into RAM and executed by BIOS.) This concludes the
BIOS's work and now, the control is handed to the loaded boot sector code.

When BIOS/UEFI reads the information from the non volatile memory(hard-disk)
about the bootloader and loads it into memory, bootloader inturn loads the
kernel. The kernel and its associated files are located in the /boot directory.
The kernel files are identifiable as they are all named starting with vmlinuz.
The kernel first extracts itself since they are in compressed state initially.
It then loads **systemd** and **systemd** starts to do it's work.
This marks the end of the boot process and the start of the startup process.

Systemd first mounts the filesystem as defined by /etc/fstab file including any
swap files or partitions. It uses it's configuration file,
/etc/systemd/system/default.target, to determine which state or target to boot
the host into. This, in case of a personal computer, is likely to be a symlink to
graphical.target and for a server, multi-user.target. The target is said to be
reached after all the target before it and required by it is reached when all
the units required by that target is started. In simpler term, when the dependencies/services 
required for the computer to run at this target's specific level of functionality is started.
You might have seen "WantedBy=multi-user.target" when configuring a service or unit. That tells the
service to start with the multi-user.target but with a lesser level of
strictness than RequiredBy. (which means the multi-user.target will continue to
function even if the service wantedby multi-user.target fails)

## Notes:
1. For the sake of simplification, targets in systemd can be
thought of as the state of the computer. When the systemd has all the units
ready to have multiple user logging in(for example in a server), it's said to
have reached the multi-user.target. When you're in graphical user state, it's
said to have reached graphical.target. (multi-user.target precedes graphical-user
target.) Poweroff is a target and so is reboot. Rescue mode is also a target.
2. If you have multiple operating system running on your system(aka
multibooting), the menu you see too choose between operating systems, rescue
and recovery options is the bootloader's menu. GRUB2 and LILO are some of
the popular bootloaders.


## References
[Introduction to linux boot and startup process](https://opensource.com/article/17/2/linux-boot-and-startup)

[Init-Wikipedia](https://en.wikipedia.org/wiki/Init)

[Understanding systemd unit and unit files](https://www.digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files)

[Beginners guide to systemd target](https://www.thegeeksearch.com/beginners-guide-to-systemd-targets-runlevels/)

