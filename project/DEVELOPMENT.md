# DEVELOPMENT GUIDE

## General Information

- Please ensure that all code conforms to the [PEP 8 Standards](https://peps.python.org/pep-0008/). You should feel free to leverage tools such as [`black`](https://github.com/psf/black).
- All objects must include detailed docstrings that conform to [PEP 257](https://peps.python.org/pep-0257/). Please see prior work in `tmnt_dsl.core` for reference.
- Only work off the `dev` branch, and create branches for each aspect of the project that you are working on. You do not need to create a new branch for each feature you develop, but this is recommended. To the extent possible please create issues for each feature/bug and associate those with a branch/pull request. When you are finished with a feature/bug, please generate a pull request back to `dev`.
  - When generating a pull request, ensure that you assign either @dvotipka or @zenw00kie as a reviewer.
  - Pull requests will be rejected if they do not conform to the two PEP standards specify or if they do not contain sufficient detail in the docstrings.

## To Dos - Summer 2024

### DSL (tmnt.dsl)

Team member(s): Ron Thompson (@zenw00kie)

### Knowledge Base (tmnt.kb)

Team member(s):

This is where all of the threats, controls, etc. are found. You can load specific data sources with a simple call, ex. `tmnt.kb.load_capec()`. This will allow you to inspect and use various threats and controls as TMNT DSL objects. These are called upon and assigned in the various Engines that are available.

### Engines (tmnt.engines)

Team member(s):

This is where threats and controls are assigned to specific components, set of components, and/or flows based from the KB. Engines can leverage other engines, the KB, or other sources of information (such as logs from the UI in the case of the Natural Suggestion Engine)

Tasks:

- Create initial `rules` that are set of deterministic rules based on the current data loaded in `tmnt_dsl.utils.sources`. These rules should assign
  weaknesses (and in turn threats and mitigations) to various `Asset` and `Flow` objects that are created by the user. - The applicability should change as the user provides more information - These rules should be expanded as more data is incorporated into `tmnt_dsl.utils.sources`. - Users should be able to specify their own rules as well, so there should be an API to do this, via creating a `Rule` object
- Using a LLM (feel free to experiment with various models such as GPT-3), create an engine that can assign weaknesses, threats, and mitigations to an user's threat model as well as provide suggestions of other weaknesses, threats, and mitigations that have not been specified in `tmnt_dsl.utils.sources`.
  - This implementation should ensure that it follows the natural pattern that we have previously discussed, i.e. an user specifies if they want to identify threats, add current controls, generate a finding, or look at/edit another part of the threat model

### UI
Team member(s):


#### Bonus

This should not be attempted until all other requirements have been satisfied and approved.

- Deploy the web app to a hosted service
- Add the ability for users to create accounts and save threat models to the hosted service
- Allow users to create sessions that they can share with other users that allows:
  1. For the other users to "observe" the threat model
  2. Actively edit the threat model
  3. Permissions (such as read/write/access) can be specified by an user

#### Notes from End of Spring 2024

other

- type annotation for different python versions (generic list type works currently with python 3.11, but would be better to have lists of specific types)
- property getters/setters missing in various places
- enforce unique controls, implement control catalog
- remove_introduction, remove_detection_method in Weakness

update yaml/documentation

- required_skills, required_resources in Threat should be lists of dicts, not strings
- conditions in Weakness should be something else
- mitigations is list of dict for weakness and list of str for threat
- change description to desc
- add_elem/remove_elem removed in component
- required attributes for Control
- added related attr for Control
