# TMNT

Welcome to the Tufts Security & Privacy Lab's (TSP) Threat Modeling Naturally Tool! This tool is part of ongoing work by TSP into threat modeling and leverages findings from our work.

You can use TMNT in one of two ways: via a Python package (see [Python Package README](tmnt/README.md)) or via our UI (see [UI README](ui/README.md)).

The TMNT Python package consists of the code for the DSL (`tmnt.dsl`), the various engines (`tmnt.engines`), and the knowledge base of threats and controls (`tmnt.kb`). The UI can be self-hosted (see [UI README](ui/README.md) for details) or can be accessed at [tsp.cs.tufts.edu/tmnt](https://tsp.cs.tufts.edu/tmnt), where you can test out the tool and create a user profile and save your threat models.

The rough system design looks like this:
![system design](project/img/TMNT.drawio.png)

## Using TMNT

You can download this repository and install the `tmnt` python package with
```
cd tmnt
pip install .
```

To run the UI, please refer to the [UI README](ui/README.md).

## TMNT Development

If you plan on working on TMNT, please look at our [Contributing Guide](docs/source/contributing.md) for details. Additionally, we recommend reviewing our [documentation](https://tsp.cs.tufts.edu/tmnt).

### Wall of Contributors

- Ronald E. Thompson, Tufts (2023 - pres.)
- Daniel Votipka, Tufts (2023 - pres.)
- Lisa Dang, Tufts (Summer 2024 - pres.)

#### Alumni
- Yaejie (Gia) Kwon, Swathmore (Summer 2024)
- Esam Nesru, UMBC (Summer 2024)
- Christopher Pellegrini, Tufts (Spring 2024) - now at Northeastern
- Madison Red, Tufts (Spring 2024)
- Richard Zhang, Tufts (Spring 2024)
- Mira Jain, Tufts (Spring 2024)
- Caroline Chin, Tufts (Spring 2024)

## Related Research from TSP
```
Ronald E. Thompson, Madison Red, Richard Zhang, Yaejie Kwon, Lisa Dang, Christopher Pellegrini, Esam Nesru, Mira Jain, Caroline Chin and Daniel Votipka. "The Threat Modeling Naturally Tool: An Interactive Tool Supporting More Natural Flexible and Ad-Hoc Threat Modeling. In 10th Workshop on Security Information Workers (WSIW 24), Philadelphia, PA, August 2024. USENIX Association.
```
[Paper](https://security-information-workers.github.io/downloads/wsiw2024-final18.pdf)

```
Ronald Thompson, Madeline McLaughlin, Carson Powers, and Daniel Votipka.
"There are rabbit holes I want to go down that I'm not allowed to go
down": An Investigation of Security Expert Threat Modeling Practices for
Medical Devices. In 33rd USENIX Security Symposium (USENIX Security 24),
Philadelphia, PA, August 2024. USENIX Association.
```
[Paper](https://www.usenix.org/conference/usenixsecurity24/presentation/thompson)



## Citing TMNT
We hope that you'll use TMNT in your research! If you plan on using it, can you please cite with the following:
```
```

## Funding
The TMNT project has been generously funded by Cisco and MedCrypt.
