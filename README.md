# README

## Tech Stack
This project uses a Vue frontend, a Django backend, and SQlite for the database currently.

## Setup
For the frontend, `npm` is the package manager and may need to run `npm install` in the frontend directory for Vue/Vite. Note that you may need to force it (we gotta fix this, man).

For the backend, `uv` is the python package manager. Run the `uv sync` command and all backend dependencies should be handled. It is also strongly recommended to run the `uv run python manage.py migrate` command.

## Deployment
Create two terminals, one for the frontend and one for the backend.

For the frontend, launch the server with `npm run dev`. You should follow the link to open the site in your browser at host.

For the backend, launch the server with `uv run python manage.py runserver`.

To test the connection between the two servers, navigate to http://127.0.0.1:5173/#/hello and you should see a message from the backend. Note that if you do not launch the backend server, the message will not appear which confirms the connection.

## TODO
- database models
- api expansion
- frontend stuff
- everything