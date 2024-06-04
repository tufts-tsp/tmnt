# TMNT

Welcome to the Tufts Security & Privacy Lab's (TSP) Threat Modeling Naturally Tool! This tool is part of ongoing work by TSP into threat modeling and leverages findings from our work.

You can use TMNT in one of two ways: via a Python package (see [Python Package README](tmnt/README.md)) or via our UI (see [UI README](ui/README.md)).

The TMNT Python package consists of the code for the DSL (`tmnt.dsl`), the various engines (`tmnt.engines`), and the knowledge base of threats and controls (`tmnt.kb`). The UI can be self-hosted (see [UI README](ui/README.md) for details) or can be accessed at [tsp.cs.tufts.edu/tmnt](https://tsp.cs.tufts.edu/tmnt), where you can test out the tool and create a user profile and save your threat models.

The rough system design looks like this:
![system design](project/img/TMNT.drawio.png)

## Using TMNT

You can download this repository and install the `tmnt` python package with `pip install ./tmnt`.

To run the UI, please refer to the [UI README](ui/README.md).

## Contributing to TMNT

If you plan on working on TMNT, please look at our [Contributing Guide](project/CONTRIBUTING.md) for details. Additionally, we recommend reviewing our guides: [TMNT Overview](project/OVERVIEW.md), [Intro to Threat Modeling](project/IntroThreatModeling.md), and [Review of Threat Modeling Tools](project/ThreatModelingTools.md).

## Wall of Contributors

- Ron Thompson (2023 - pres.)
- Christopher Pellegrini, now at Northeastern (2023 - 2024)
- Madison Red (2023 - 2024)
- Richard Zhang (2023 - 2024)
- Mira Jain (2023 - 2024)
- Caroline Chin (2023 - 2024)

## Related Research from TSP

```
Ronald Thompson, Madeline McLaughlin, Carson Powers, and Daniel Votipka.
"There are rabbit holes I want to go down that I'm not allowed to go
down": An Investigation of Security Expert Threat Modeling Practices for
Medical Devices. In 33rd USENIX Security Symposium (USENIX Security 24),
Philadelphia, PA, August 2024. USENIX Association.
```
[Link](https://www.usenix.org/conference/usenixsecurity24/presentation/thompson)


## Citing TMNT
We hope that you'll use TMNT in your research! If you plan on using it, can you please cite with the following:
```

```
