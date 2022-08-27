# How RESTFul are your REST APIs and how to measure them?

## Introduction
Do you know how RESTFul your web APIs are? Richardson Maturity Model is a model
to measure just that. We are going to take a quick look at this model in this blog.
By the end of the blog, I hope you can have an idea of how to measure the
RESTfulness of web services.

## Richardson Maturity Model 
Richardson Maturity Model, developed by Leonard Richardson, is a maturity model
that classifies Web APIs. According to the model, there are 4 levels of how
RESTFul an API can be.

### 1. Level 0: The Swamp of POX(Plain Old XML)
When we are not using any concept of REST like resource URIs, HTTP methods, etc,
api is on level *zero* of the model. Here, we would be using something like SOAP
webservices with following properties:
   * There is only one URL and all the request are sent to this URL.
   * Both the resource and the operation to be performed on it is defined in
     the request body in XML. Hence the name The swamp of POX, Plain Old XML.
   ```xml
   POST /airlines HTTP/1.1
   <book-flight>
      <from>Biratnagar</from>
      <to>Kathmandu</to>
      <at>2022-08-27 13:15:00</at>
      <for>Diwash Tamang</for>
   </book-flight>
   ```
   ```xml
   POST /airlines HTTP/1.1
   <cancel-flight>
      <request-id>12</request-id>
      <flight-id>12</flight-id>
   <\cancel-flight>
   ```
   ```xml
   POST /airlines HTTP/1.1
   <create-user>
      <name>Diwash Tamang</name>
      <age>40</age>
      <country>Nepal</country>
   <create-user>
   ```
### 2. Level 1: Resources
On level 1, we follow on the important feature of REST, resource URIs. Every
resource will have a different URIs. For eg:
   * To perform any operation on messages, we will have a `/messages` URI.
   * For comments, we will  have a `/comments/` URI and so on.
The request body can contain the information on the operation, which ideally should
be handled by the HTTP method and this will still be considered level 1 on the RMM.

### 3. Level 2: HTTP Verbs
Level 2 webservices make use of the HTTP methods for specifying the operation
that needs to be performed on the resource. And the server also sends back
the right status codes.
For eg:
   * For creating a new message.
   ```
   POST /messages HTTP/1.1
   {
      "text": "Hi! How are yooou?"
   }

   Response
   HTTP/1.1 201 OK
   ```

   * HTTP GET /messages for get all messages.
   ```
   GET /messages HTTP/1.1

   Response
   HTTP/1.1 200 OK
   [
      { "id": 30, "text": "Hi! How are youuu?"},
      ...
   ]

   ```
   * HTTP PUT /messages/<id> to update the message
   ```
   POST /messages/30 HTTP/1.1
   {
      "text": "Hi! How are you? \nEdit: typo"
   }

   Response
   HTTP/1.1 200/204 OK
   ```
   * HTTP DELETE /messages/<id> to delete a message
   ```
   DELETE /messages/30 HTTP/1.1

   Response
   HTTP/1.1 200/204
   ```

### 4. Level 3: Hypermedia Controls
Finally, for a web service to be considered a fully RESTful, in addition to
following all the rules above, it should also have in the response, URIs to
related resource. This principle of sending hyperlinks/hypermedia in the
response is called HATEOAS, Hypermedia As The Engine Of an Application State.
The main idea is that if the client doesn't have to worrying about remembering
and constructing API URLs every time. They should be able to find that in the
response.
```json
POST /posts/21 HTTP/1.1

HTTP/1.1 200 OK

{
   "id": 21,
   "caption": "To be or not to be. - Sun Tzu",
   "image_url": "https://hostname.com/media/posing-on-the-beach.jpg"
   "links": {
      "self": "posts/21",
      "comments": "posts/21/comments",
      "reactions": "posts/21/reactions",
      "user": "users/21"
   }
}
```

## Conclusion
We have looked at the different levels of REST API. It goes without saying
that if we are writing REST APIs, we should aspire to make them as RESTful as
possible. But I haven't seen many Level 3 APIs, to be honest. The constraint of
implementing the list of hyperlinks for every resource sounds like it will
complicate the work on both the Backend and the Frontend. But Roy T. Fielding,
the originator of REST architecture, insists that REST APIs must be
[hypertext-driven](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven?fbclid=IwAR0Ayi1YPQCRcOWQJtK6matCfFDntjqbNv-NeSEiM6ihTpNmKLfxdmWQ-7A).
So, I will be trying it out in the future.


## References
* [More on HATEOAS](https://en.wikipedia.org/wiki/HATEOAS#:~:text=Hypermedia%20as%20the%20Engine%20of,provide%20information%20dynamically%20through%20hypermedia)
* [Roy T. Fielding on hypertext-driven REST](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven?fbclid=IwAR0Ayi1YPQCRcOWQJtK6matCfFDntjqbNv-NeSEiM6ihTpNmKLfxdmWQ-7A)
* [Java Brains](https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven?fbclid=IwAR0Ayi1YPQCRcOWQJtK6matCfFDntjqbNv-NeSEiM6ihTpNmKLfxdmWQ-7A)
* [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)

If you feel like you learn something new in this post, please give a clap 👏👏👏.
