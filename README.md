# README

## Tech Stack
This project uses a Vue frontend, a Django backend, and SQlite for the database currently.

## Setup
1. Install `pnpm` if you do not have it installed. If you have `npm` try `npm install pnpm`

2. For the frontend, `pnpm` is the package manager and may need to run `pnpm install` in the frontend directory for Vue/Vite. Using npm and pnpm in the same project is not advised.

For the backend, `uv` is the python package manager. 
1. Run the `uv sync` command and all backend dependencies should be handled.
2. It is also strongly recommended to run the `uv run python manage.py migrate` command.

## Backend Stuff
- To create an admin user for database managerment, `uv run python manage.py createsuperuser`. It will prompt for username, email, and password but they can be throwaway. You can then log into the admin backend with http://127.0.0.1:8000/admin and view users and profiles.
- The frontend url that is being used to test stuff is http://localhost:5173/#/Hello

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

## Note
- any time you pull or get an updated files you may need to install additional packages with `npm install` or `pnpm install`
