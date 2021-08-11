# What is JWT & how does it work?

## What's JWT?
JWT(JSON Web Token is a method of authentication that stores user's session information entirely on the client in the form of a token.

## How's it different from session authentication?
Session authentication stores the session information in a database. After logging in, a cookie is stored on the browser which that cookie is sent from the client on every request to the browser. The cookie is then used to query the session information from the database.
JWT however get's rid of the need to use the database for session information storage. Because the actual information about the authenticated user and the token expiration date is stored in the form of the token.

## How does it composed?
A JWT token is composed of three parts separated by dots.
1. The first part, the header, is the base64encoded information about the hashing algorithm used.
2. The second part, the payload, is the base64encoded information about the session (user_id, token issued date or expiration date, token type: access or refresh)
3. The third part, the hash value, is the hashed output of the first and the second part using the secret key stored on the server.

## How does the server authenticate user with the token?
1. When you login with the credentials, server creates two tokens (access & refresh) and sends it to the client.
2. Client sends these token in all it's subsequent requests.
3. The server takes the first and the second part of the token and hashes it using the secret key. If the output matches with the last part, then the token is untampered and the information is untampered & trustworthy.
4. It can also read the payload data for the expiration to check if the token's are outdated.

## What's the benefit of using jwt token?
1. No need for the table to store the session information. (Probably not the biggest benefit unless you have tons of clients)
2. Since the verification is entirely dependent on only the secret key, we can have a distributed set of servers with the same secret key. And the token created by on of the servers will be recognized by the another server. Also important reminder to keep the secret key very secret.


