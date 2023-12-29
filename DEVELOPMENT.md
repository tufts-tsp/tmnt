# DEVELOPMENT GUIDE 

## General Information
- Please ensure that all code conforms to the [PEP 8 Standards](https://peps.python.org/pep-0008/). You should feel free to leverage tools such as [`black`](https://github.com/psf/black).
- All objects must include detailed docstrings that conform to [PEP 257](https://peps.python.org/pep-0257/). Please see prior work in `bang_pytm.core` for reference. 
- Only work off the `dev` branch, and create branches for each aspect of the project that you are working on. You do not need to create a new branch for each feature you develop, but this is recommended. To the extent possible please create issues for each feature/bug and associate those with a branch/pull request. When you are finished with a feature/bug, please generate a pull request back to `dev`. 
    - Pull requests will be rejected if they do not conform to the two PEP standards specify or if they do not contain sufficient detail in the docstrings.

## To Dos - Spring 2024

We have provided detailed to do's for each part of `bang_pytm` that need to be built/modified as well as recommended number of team members. Additionally, we have given more detailed requirements for the Web Application, but we are not specifying the exact steps needed to be taken. Feel free to use your own organizational methods to assign tasks, track progress etc. 

Each week, we'd like the following to be done for the Wednesday meeting:
- An updated waterfall of where the project stands across each of the four workflows (specified below)
- All code that needs to be reviewed either to be merged in `dev` or at least have a pull request.
- A version of the web app available for testing via Docker. We understand that this may not change every week, but we would like to ensure that we are able to test the app/play around with it at our leisure, i.e. there's a working build available.

Before our first meeting on January 24, please make sure all the following items (and any other related items) are added as issues in this project and/or the [web app](https://github.com/mirarj/nltm_tool). Also update this document to reflect who's working on which section (and assign the issues to these team members). There are several issues currently logged that can be used as a starting point. 

### DSL (bang_pytm.core)
Team member(s): @mrtoaf

- Create `Actor` object ([Issue 3](https://github.com/ZenW00kie/bang_pytm/issues/3)) and `Boundary` ([Issue 8](https://github.com/ZenW00kie/bang_pytm/issues/8))
- Create the children objects for `Asset` (all should be found in `asset.py`) - Issues [4](https://github.com/ZenW00kie/bang_pytm/issues/4), [5](https://github.com/ZenW00kie/bang_pytm/issues/5), [6](https://github.com/ZenW00kie/bang_pytm/issues/6), [7](https://github.com/ZenW00kie/bang_pytm/issues/7)
- Modify the following object referencing the To Dos for each: `TM`, 
- Modify an other objects as needed

### DSL Utils (bang_pytm.core)
Team member(s): @mrtoaf

- Create object relationships when data is being loaded in `bang_pytm.utils.source`, for example after calling `load_cwes()`, the `relationships` attribute should contain objects rather than dicts specifying the relationships ([Issue 2](https://github.com/ZenW00kie/bang_pytm/issues/2))

### Recommendation Engines (bang_pytm.engine)
Team member(s): To Be Assigned (Recommend 2)

- Create initial `rules` that are set of deterministic rules based on the current data loaded in `bang_pytm.utils.sources`. These rules should assign 
weaknesses (and in turn threats and mitigations) to various `Asset` and `Flow` objects that are created by the user. 
    - The applicability should change as the user provides more information
    - These rules should be expanded as more data is incorporated into `bang_pytm.utils.sources`.
    - Users should be able to specify their own rules as well, so there should be an API to do this, via creating a `Rule` object
- Using a LLM (feel free to experiment with various models such as GPT-3), create an engine that can assign weaknesses, threats, and mitigations to an user's threat model as well as provide suggestions of other weaknesses, threats, and mitigations that have not been specified in `bang_pytm.utils.sources`.
    - This implementation should ensure that it follows the natural pattern that we have previously discussed, i.e. an user specifies if they want to identify threats, add current controls, generate a finding, or look at/edit another part of the threat model

### Visualizations (bang_pytm.visual)
Team member(s): To Be Assigned (Recommend 1)

- Create `Diagram` object, this should serve as a parent for additional objects that cover all the diagrams that `pytm` can generate i.e., a dataflow diagram and a sequence diagram. 
- Create `Report` object that produces skeleton HTML code that can be loaded into a web browser (and be leveraged by the web application you are developing). This should also be able to generate a pdf version of the report as well, similar to `pytm`.
- For both `Diagram` and `Report`, the user should be able to specify what parts of the TM they want to generate these for, whether that's specify specific objects or different levels of the diagram. 

### Web App ([repo](https://github.com/mirarj/nltm_tool))
Team member(s): To Be Assigned (Recommend 2)

Requirements:
- Place application in a container such that the application can be run in its own environment
- Users should be able to edit both via a GUI and via a code text box where they can write custom `bang_pytm` code. 
    - The GUI can follow a form layout, where they create new objects and specify the attributes/relationships.
    - The code editing should be both a full threat model as well as specifying certain objects (rather than everything) in the threat model.
    - Users should be able to export a `bang_pytm` project, where they could build their own reports etc
    - The entire `bang_pytm` API should be available to users via both these mechanisms.
- Users should be able to select aspects of the diagram (assets, flows, actors) and are then prompted if they want to look at related threats, controls, and flows. 
    - The user can specify which engine(s) they use
    - The information provided should be generated from `bang_pytm.engine`.
    - The diagram should be rendered using D3 (or an equivalent library) and making calls to `bang_pytm.visual` as needed (it is not required to use `bang_pytm.visual` to build the graphics). 
- Users should be able to save their threat models to their local machine as well as load a saved output (this does not necessarily have to be `bang_pytm` source files, but instead could be a pickle). 


#### Bonus
This should not be attempted until all other requirements have been satisfied and approved.

- Deploy the web app to a hosted service
- Add the ability for users to create accounts and save threat models to the hosted service
- Allow users to create sessions that they can share with other users that allows:
    1. For the other users to "observe" the threat model
    2. Actively edit the threat model
    3. Permissions (such as read/write/access) can be specified by an user