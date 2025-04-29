# Raw Sockets Notes

* Sockets are abstraction provided by the OS to enable communication between diferent process
    * in the same machine or over a network
* Acts as endpoints in a two way communication channel
* Socket = Protocol (TCP/UDP) + IP Address + Port Number
* When two process wants to communicate with each other,
    * they will both create sockets
* Socket is the phone, ip address + port is the phone number

* Two main types of transport (Socket)
    * TCP
        * SYN, SYN + ACK + ACT & communicate
            * 3 way handshake
        * reliable, ordered, error-checked data transmission
        * useful for web browsing, database access or file transfers
        * unicast
    * UPD
        * Connectionless & unreliable (No handshake)
        * But fast & light-weight
        * Ideal for Real-Time Application
            * Video & Audio streaming
        * unicast, multicast or broadcast

* Server Side Socket Life Cycle
    * create listening socket
    * bind to a ip address + port
    * accept connections
    * create a new socket for the accepcted connection
        * receive messages
        * send messages
        * will probably close as well after the communication is done
    * close socket
* we can handle multiple client connection each with it's own dedicated socket
* If synchronous,
    * handled with mutli-threading or multi-processing
    * doesn't scale well
    * context switching overhead
* Asynchronous (Nonblocking IO/Event driven architecture)
    * Single thread
    * Event loop
        * Manage thousands of open sockets concurrently
        * using select or poll
        * multiplexing
            * processing multiple input/output events from a single event loop with system calls like pool & select
            * no idle waiting or polling
        * used in nodejs, nginx, asyncio
* File descriptor:
    * when you open a file in linux, it will create an entry to store its openness & metadata
    * the entry key is an integer => that is the file descriptor
* Socket descriptor:
    * similar thing happens when a new socket is opened.

* UDS (Unix Domain Socket)
    * Used for inter process communication on the same host
    * UDS uses file path instead of ip address because it's on the same host
        * Eg: /tmp/app.sock
    * UDS are much faster because it uses transport layer & skips network layer (IP Routing etc)
    * Postgres & Redis default to UDS on communication on same host

# OSI Model:
7. Application Layer
    * HTTP, FTP, SMTP
6. Presentation Layer
    * TLS, SSL
5. Session Layer
    * Sockets
4. Transport Layer
    * TCP, UDP
3. Network Layer
    * IP, ICMP, IPSec
2. Data Link Layer
    * Ethernet, Wifi
1. Physical Layer
    * Fiber



> Notes on sockets & patterns ZMQ Guide

Recap from chapter:
* ZMQ is sockets on steroids
* It gives us the following things
    * speed of raw socket
    * built-in support for safety in terms of queuing, connection issues, etc
    * built-in support variety of different messaging patterns
        * request-reply
        * pub-sub
        * fan-out
        * push-pull
        * some type of load balancing
    * built-in support for multiple transport protocols:
        * tcp
        * inproc
        * ipc,
        * pgm
        * epgm, etc
    * Helps build scalable distributed software that can talk to each other using various messaging pattern as is requried
* Zero MQ means no broker is involved
* You just have a lightweight framework, which enables you to build your own broker easily
    * Benefit:
        * We don't need to install & maintain an extra software (the message broker)
        * just the sockets and your code
* Notes:
    * cleanup:
        * set linger to 0 & close the socket
        * then close the context
        * if you don't close all sockets before closing the context
            * it will hang forever
        * if you don't set the linger to 0
            * socket will wait for the reply or something like that. (Need to investigate this more)

# Chapter 2: Sockets & Patterns

## The socket API
* ZMQ is more like a socket API than a message broker
    * but it also hides the message processing engines behind the framework
* 4 parts of ZeroMQ sockets:
    1. creating & destroying sockets:
        * zmq_socket(), zmq_close()
    2. configuring socket options:
        * zmq_setsockopt(), zmq_getsockopt()
    3. connecting to transport/ports (plugging sockets into topology)
        * zmq_bind(), zmq_connect()
    4. sending & receiving messages
        * zmq_msg_send(), zmq_msg_recv()
> Note: sockets belong to zmq library, message/data are owned by us


### Pluging socket into topology
* "server" binds to a network address
* "client" connects to the network address
* zmq connection are diff from class tocp conection
    * connection can be zmq_ipc, zmq_tcp, zmq_pgm, etc
    * 1 socket may have many outgoing & incoming connections
    * when a socket is bound (like a server), it will automaticaly accepts conections from client
        * no zmq_accept
    * connectino happens in bg & zmq will auto reconnect if network connection is broken
    * your code can't work with the conection directly

> Note: zmq clients & server can start in any order. client doesn't have to start before
the sever. client can connect to a port & send messages. Server can bind later & deliver
messages (But there's a case if messages from client queue so much they will start to get discarded.)

* a single server socket can conect to multiple endpoint or network addresses
```c
zmq_bind( socket, "tcp://*:5555");
zmq_bind( socket, "tcp://*:9999");
zmq_bind( socket, "inproc://somename");
```

* zmq sockets carry messageat like udp rather than raw tcp. so there's some difference in how they work

* Side learning:
    * unicast
        * sending msg from one node to another node
        * 1 to 1 communication
    * broadcast
        * sending msg to all nodes in another network
        * limited
            * sending message to all nodes within your own network
            * your network address: 90.0.0.0 
            * dest address: 255.255.255.255
        * direct
            * sending message to all nodes within another network
            * your network: 90.0.0.0
            * another network: 92.0.0.0
            * dest address: 92.255.255.255
    * multicast
        * sending messages to groups
            * like sending email to a group of people
