# Creating a chatroom with Django channels

### 1. What is channels in Django?
Django channels provides a wrapper around Django's native asynchronous view
support, to work with protocols that require long-running connections such as
WebSockets, MQTT, chatbots, amateur radio and more.

### 2. Channel Layer
A channel layer allows multiple consumer instances to talk to each other and
with other parts of Django.
It provides:
* *Channel*: A channel is a mailox where messages can be sent to. Each channel
has a name and anyone who has the channel name can send messages to the
channel.
* *Group*: A group is a group of related channels. It has a name. Anyone that
knows the name of the group can add/remove channels by name and send a message
to all channels in the group. (Not possible to enumerate what channels are in a
group)

* Consumer instances has an automatically generated unique channel name and, so
can be communicated with via a channel layer.
