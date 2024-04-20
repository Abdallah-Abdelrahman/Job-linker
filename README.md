# Job Linker

The application links between recruiters and candidates in one unified platform.

## Technologies :

- **Frontend** :
    + [react](https://react.dev/) to build seamless user interfaces
    + [chakra-ui](https://v2.chakra-ui.com/getting-started) for styling components
    + [react-router-dom](https://reactrouter.com/en/main/start/overview) for client side routing
    + [vite](https://vitejs.dev/guide/) as the build tool
- **Backend** :
    + [flask](https://flask.palletsprojects.com/en/3.0.x/) to manage api services
    + [SQLAlchemy](https://www.sqlalchemy.org/) the so-called orm

## Installation :

+ clone the repo
+ navigate to project tree and run `yarn` or `npm install` if you're using `npm`
+ navigate to `api` directory:
    - run `python3 -m venv venv`
    - run `source venv/bin/activate`
    - run `pip install -r requirements`

## How to use :

 + In on terminal runs `api` service `yarn api` or `npm run api`
 + In another session runs the client `yarn dev` or `npm run dev`
 + You can read more about package.json `scripts` work in

 **_Notes_ :** <br/>
+ In order to proxy any endpoint you can edit `vite.config.ts` file.<br/>
+ All backend code lives in `server/` direcrtoy.<br/>
+ visit [npm](https://docs.npmjs.com/cli/v10/configuring-npm/package-json) to learn more about the `package.json` file.
