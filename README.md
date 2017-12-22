<h2>A basic API introduction</h2>
<b>Followed tutorial by Miguel Grinberg</b>
<italic>https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask</italic>

<p> A great guide for designing a simple RESTful API with python and Flask.
this application contains all the code from the tutorial and i intend to develop the applicaiton further.
Currently the API supports GET, POST, PUT and DELETE, as well as single user authentication wich can be enabled/disabled per function.

The API does not use a database but saves all changes directly in memory, needless to say this is not code that should run in production.

Example commands:
# curl -i http://localhost:5000/door/api/tasks
# curl -u admin:password -H "Content-Type: application/json" -X POST -d '{"title":"alarm", "description":"Turn alarm on/off"}' http://localhost:5000/door/api/tasks
# curl -u admin:password -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' http://localhost:5000/door/api/tasks/3
# curl -u admin:password -i -X DELETE http://localhost:5000/door/api/tasks/3
</p>
