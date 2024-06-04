## Docker Setup

You are able to run the app using Docker. You'll want to install [Docker Desktop](https://docs.docker.com/desktop/). Right now you can either:
- After every push/pull request to the `dev` branch a new version of the app will be built and available on Docker Hub. To run this version you simply need to run `docker run -it -p 8000:8000 zenw00kie/tmnt_ui:latest`. If you have already done this before, you'll need to make sure you pull the latest version of the image, which you can either do in Docker Desktop or you can run `docker pull zenw00kie/tmnt_ui:latest`.
- Build a new docker image on your local version using `docker build -t "tmnt_ui" .`. This will create a Docker image for you to run the app. You then can run `docker run -it -p 8000:8000 tmnt_ui` or you can run the image from the Docker Desktop app (if you do the latter make in the optional settings that you set the host port to 8000).

Once the container is running you can navigate to `http://localhost:8000/tmnt/asset_view/` to use the app.

## Local Setup
NOTE: If you are running this locally, we highly recommend using [`venv`](https://docs.python.org/3/library/venv.html) to ensure you are using the correct packages and their versions. You can install these with the `requirements.txt` file in this directory (`tmnt.ui.requirements.txt`) and you'll need to install the `tmnt` package.

If you want to run the app on your local machine, without using Docker you can. First you'll need to make sure that you've migrated everything for Django by running `python manage.py migrate` (anytime you make changes you'll need to do this). Then you can run `python manage.py runserver`, and you can navigate to `http://localhost:8000/tmnt/asset_view/` to use the app.

## Capstone notes

### What is Currently Implemented:
1. What are we working on?
    * Ability to click on asset buttons, name the asset, and have asset appear
    on screen
    * Ability to click on assets and have information about it appear in bottom
    bar
    * Ability to drag elements
    * Ability to assign and label dataflows between assets
2. What could go wrong?
    * Ability to assign threat (threat name, optional CVE number, threat
    description) to a specific asset
    * What are we doing about it?
    * Ability to assign control (control name, control description) to a
    specific asset
3. Did we do a good enough job?
    * Ability to create a finding for a specific asset and threat
        * Select controls associated with threat
        * Select Finding status
        * Select Technical and Safety Impact
        * Set Assessment Date and Assessor
        * Write any Notes
