# Job Linker

It's an AI powered application that links between recruiters and candidates in one unified platform.<br>
Tt helps candidates refine their cv by giving them ats insights, find in-demand jobs, ease the process for recruiters to find skilled candidates through the help of AI.

## Technologies :

- **Frontend** :
    + [react](https://react.dev/) to build seamless user interfaces
    + [chakra-ui](https://v2.chakra-ui.com/getting-started) for styling components
    + [react-router-dom](https://reactrouter.com/en/main/start/overview) for client side routing
    + [vite](https://vitejs.dev/guide/) as the build tool
- **Backend** :
    + [flask](https://flask.palletsprojects.com/en/3.0.x/) to manage api services
    + [SQLAlchemy](https://www.sqlalchemy.org/) the so-called orm

## Installation and Run :
+ clone the repo.
+ navigate to the project tree.
- #### unix-like systems:
    + ensure you have `make` utility installed on your machine.
    + run `make setup` to install all project libraries and dependencies (front and back altogether).
    + on successful installation, run `make run` to run backend and frontend altogether.
    + if any dependancy fail on installation, try to install it manually.
    + now you're good to go, open up your browser and type `localhost:5173`. voila!
+ #### windows system: 
    - run `yarn` or `npm install` if you're using `npm` to install frontend dependancies.
    - navigate to `server` directory:
    - run `python3 -m venv venv`, make sure you have python3.9+ installed.
    - run `source venv/bin/activate`.
    - run `pip install -r requirements`.
    - from the project root directory run `yarn api` to start backend api service.
    - run `yarn dev` to startoff your frontend. 

## How to use :
 + head over to [google](https://aistudio.google.com/app/apikey) and generate an api key, and put it in your environment variable under the name `GOOGLE_API_KEY`, to utilize the power of ai.
 + Explore the platform and if you like it, please give us a star.

## Inspiration :
<!-- TODO -->

## License :
