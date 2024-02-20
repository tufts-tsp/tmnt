# bang_pytm

## Installation
python -m pipreqs.pipreqs
pip install requirements.txt

## Usage
import bang_pytm.util.sources
sources.load_capec() # etc

## Standards Mapping
- TM : [CSAF](https://oasis-open.github.io/csaf-documentation/index.html)
    - A TM object should export to a CSAF format and this is what can be easily 
    consumed by the tool
- Threat : [STIX](https://oasis-open.github.io/cti-documentation/stix/intro)
- Vulnerability : 



AWS:
Threat Source + Prerequisites -> Action -> Impact (Requirements + Components)

Threat Source
- Actor
- Avenue

Prerequisites
- Desc

Action
- Desc
- Steps

Outcome
- Desc
- Requirements
- Elements

Scenario/Threat
- Threat Actor - Optional
- Avenue ([Theatre](https://pages.nist.gov/vulntology/specification/values/theater/)) - Optional 
- Weakness/Prerequisite - Required
- Action - 
- Outcome
- Impacted Requirements
- Impacted Assets/Flows/Actors

Requirement [Security, Safety, Physical]
Component