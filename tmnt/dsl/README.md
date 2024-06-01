# tmnt_dsl

## Installation

python -m pipreqs.pipreqs
pip install requirements.txt

## Usage

import tmnt_dsl

### Parent / Child

Only support parent / child, no grandparents right now

### Flow

Flow assignments should only happen on the parent level

## Standards Mapping

- TM : [CSAF](https://oasis-open.github.io/csaf-documentation/index.html)
  - A TM object should export to a CSAF format and this is what can be easily
    consumed by the tool
- Threat : [STIX](https://oasis-open.github.io/cti-documentation/stix/intro)
- Vulnerability :
