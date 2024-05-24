# Job Linker

Welcome to Job Linker, an innovative AI-powered platform designed to bridge the gap between recruiters and job seekers. Our application streamlines the recruitment process by providing advanced ATS (Applicant Tracking System) insights, facilitating the discovery of in-demand job opportunities, and simplifying the task of identifying qualified candidates with the assistance of cutting-edge AI technology.

## Key Features

- **ATS Insights**: Offers candidates valuable feedback on their resumes to increase their chances of getting noticed.
- **Job Discovery**: Connects job seekers with the latest and most relevant job openings in the market.
- **AI Recruitment**: Assists recruiters in finding the best-suited candidates for their vacancies efficiently.

## Technologies Used

### Frontend

- **React**: Utilized for crafting dynamic and responsive user interfaces. [React](https://react.dev/)
- **Chakra UI**: Employed for its intuitive and customizable component library. [Chakra UI](https://v2.chakra-ui.com/getting-started)
- **React Router DOM**: Handles client-side routing seamlessly. [React Router DOM](https://reactrouter.com/en/main/start/overview)
- **Vite**: Serves as a fast and modern build tool. [Vite](https://vitejs.dev/guide/)

### Backend

- **Flask**: Manages API services with simplicity and elegance. [Flask](https://flask.palletsprojects.com/en/3.0.x/)
- **SQLAlchemy**: Acts as the ORM of choice for database interactions. [SQLAlchemy](https://www.sqlalchemy.org/)

## Installation and Setup

### Cloning the Repository

```bash
git clone https://github.com/your-username/job-linker.git
cd job-linker
```

### Unix-like Systems

1. Ensure the `make` utility is installed on your machine.
2. Execute `make setup` to install all project libraries and dependencies for both frontend and backend.
3. Upon successful installation, run `make run` to start both backend and frontend services.
4. If any dependency fails to install, attempt manual installation.
5. Access the application by navigating to `localhost:5173` in your web browser.

### Windows Systems

1. Install frontend dependencies using `yarn` or `npm install` if you prefer npm.
2. Navigate to the `server` directory.
3. Set up a virtual environment with Python 3.10+:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. From the project root directory, start the backend API service with `yarn api`.
5. Launch the frontend development server with `yarn dev`.

## Usage

To leverage the full potential of AI within Job Linker:

1. Obtain a Google API key by visiting [Google Cloud Platform](https://aistudio.google.com/app/apikey).
2. Store the API key in your environment variables as `GOOGLE_API_KEY`.

Explore the platform, and if it meets your expectations, consider starring our repository!

## Inspiration

(Section to be completed)

## License

(Section to be completed)
