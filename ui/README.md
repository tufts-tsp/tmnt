## Docker Setup

You are able to run the app using Docker. You'll want to install [Docker Desktop](https://docs.docker.com/desktop/). Whenever you want to build a new version, i.e. you've made some changes to the app, you'll run `docker build -t "tmnt_ui" .`. This will create a Docker image for you to run the app. Then go to Docker Desktop and you should see the image there, and you can just hit run. You'll want to note the port you set as you'll then get to the app with that (for ease, recommend just doing 8000 which is what we are using right now on the container side). You'll then navigate to `http://localhost:8000/tmnt/asset_view/` to use the app.

## Capstone notes

### Run Server:
`python3 manage.py runserver`

### Access Web App:
http://localhost:8000/tmnt/asset_view/

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

### Future Work:
1. What are we working on?
    * Ability to add trust boundaries
    * Ability to add workflows
    * Ability to remove assets
    * Improved handling of double-headed arrow (currently just decreases
    x-value of label if a dataflow already exists in opposite direction)
    * (nice to have) Descriptions of what each of the types of assets mean
2. What could go wrong?
    * Connect to backend to pull potential threats from the recommendation
    engine
    * Display descriptions of threats somewhere useful
3. What are we doing about it?
    * Connect to backend to pull potential controls from the recommendation
    engine
    * Display descriptions of controls somewhere useful
4. Did we do a good enough job?
    * (nice to have) Descriptions of each of the fields and what they mean
5. Other elements
    * Ability to pan view of DFD
    * Ability to show badges on elements of DFD that have any of:
        * Open threats
        * Any threats or controls
        * Suggested threats or controls
    * Connection with backend
    * Make bottom bar collapsible
    * Ability to export DFD
    * Ability to save threat modeling document and create new ones

### Docker Info:
run the docker image
`docker run -it -p 8000:8000 mrtoaf/nltm_tool`

single tag w/ latest
`docker build -t mrtoaf/nltm_tool:latest -t mrtoaf/nltm_tool:latest .`

multiple tags
`docker build -t mrtoaf/nltm_tool:version-whatever -t mrtoaf/nltm_tool:latest .`

pushing
`docker push mrtoaf/nltm_tool:tagname`
