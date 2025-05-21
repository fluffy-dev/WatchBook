# Some backend(Python+FastAPI->RestAPI) conventions used in this project.

#### EVERYTHING THERE IS JUST MY OPINION.

## HTTP status codes:
to prevent some misunderstanding in what HTTP status code returns from successful actions on different endpoints and methods, there is a little mark for it:
```
GET: 200 OK
PUT: 200 OK
POST: 201 Created
PATCH: 200 OK
DELETE: 204 No Content
```

## Endpoint naming 

Always use plural names for endpoints, for example do not name it like this.

`GET: /book/{id}` 
or 
`GET: /book/`


Cause it makes some troubles to understand are we GETting the one and only book in the library, couple of them, or all of them?

instead do this:

`GET: /books/{id}` or 
`POST: /books/` 

That's make more sense and more intuitively.

---

Do not use nested endpoints structure, cause when it grows it can cause some problems to understand what exactly will be returned.

for example, we need to make endpoint that returns some author book, endpoint for example looks like this:

`GET: /authors/Cagan/books/`

Some architects recommend that way, but it's not clear anymore what we would receive from this endpoint, is that books or authors? 

So better to use flat style endpoints, like this: 

`GET: /books?author=Cagan`

There is a clear what we would receive. 

BUT, if we want to get some author books, and we sort authors by PK the first approach is easier to understand, it will be looks like this:

`GET: /authors/{author_id}/books` or `GET: /authors/3/books` and it's fine.

---

**ALWAYS USE TRAILING SLASH** (e.g always end the endpoint url by the slash)



# Some namings

properties that related to user is always UserProperties or user_properties
