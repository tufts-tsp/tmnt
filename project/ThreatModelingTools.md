# Threat Modeling Tools

There have been several tools and domain-specific languages that have been previously developed to aid system designers with threat modeling. However, we found that many people don't actually use these tools, and when they do it's for diagramming mainly.  We expect this is because existing systems do not support the ad-hoc, flexible ways that we found software architects and threat modelers review systems when threat modeling in practice.

We recommend trying out a few of these tools. If you do not have Windows and want to try [Microsoft Threat Modeling Tool](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool) or [Threats Manager Studio](https://threatsmanager.com/), please use `vm-winresearch.eecs.tufts.edu`.

## Diagramming Only
### [draw.io](https://app.diagrams.net/)
Status:
Summary:
Advantages:
Limitations:

### [C4](https://c4model.com/)
Status:
Summary:
Advantages:
Limitations:

### [Mermaid](https://mermaid.live/)
Status: 
There is a team behind Mermaid that is keeping the product maintained and updated (last commit on GitHub 1-3 weeks ago).


Summary:
Mermaid is an open-source diagramming and charting tool that allows users to create complex diagrams and charts. It is designed to streamline documentation processes and improve workflows, making it easier and faster for teams to communicate and collaborate effectively, leveraging the best of text, voice, and automation.

A key feature of Mermaid is its text-based diagramming, which aims to "simplify documentation processes - improving workflows and communication among teams." This allows the creation of various diagrams, such as flowcharts, sequence diagrams, and class diagrams, accessible to all users without requiring graphic design skills.

Mermaid currently has three different plans with the offered features presented below:
    - FREE: 5 diagrams, basic editor, presentations, comments
    - PRO ($80/year): unlimited storage, visual editor, ChatGPT editor, AI diagram repair, AI diagram generator, teams, folders &, sharing, multi-user editing, version history
    - ENTERPRISE ($204/year): SSO/SAML, custom integrations, on-premise installation


Advantages:
    - Simplistic Design: easy to see where everything goes and how components are connected
    - Variety of Diagram Options: allows for different types of diagrams (e.g., flowcharts, class diagrams, ER diagrams, etc.)
    - AI Assistant (subscription required): assists in creating or changing diagrams


Limitations:
    - Separate Diagram Syntax: while relatively simple to learn, it might feel unnecessary compared to more intuitive drag-and-drop methods
    - Limited to 2D Representation: only supports 2D diagrams, which may not be sufficient for all users.
    - Fixed Positioning: users cannot move individual components, only the entire diagram.
    - Single-Purpose: primarily used for diagramming and lacks additional functionalities 
    - Additional Costs: incorporating other features


### [Structurizr](https://structurizr.com/)
Status:
Summary:
Advantages:
Limitations:

### [Diagrams](https://diagrams.mingrammer.com/)
Status:
Summary:
Advantages:
Limitations:

### [PlantUML](https://plantuml.com/)
Status:
Summary:
Advantages:
Limitations:

## DSLs/Threat Modeling as Code
### [pytm](https://github.com/izar/pytm)
Status:
pytm is being semi-maintained/updated (last commit 3 weeks ago). 


Summary:
pytm is a Pythonic framework designed for threat modeling. The focus of pytm is to shift threat modeling to make it more automated and developer-centric. By leveraging your input and architectural definitions, pytm can automatically generate the following essential components:
    - Data Flow Diagram (DFD)
    - Sequence Diagram
    - Relevant threats to your system

These capabilities streamline the threat modeling process, allowing developers to integrate security considerations early in the development lifecycle.


Advantages:
    - Multitude of Supported Threats: covers a wide range of threats, including API Manipulation (LB01) and Cross-Site Request Forgery (AC21), ensuring comprehensive threat coverage
    - pytmGPT Integration: allows for creating threat models from prose using AI
    - Customizable Threats: provides the option to supply your own threats file, enabling customization
    - Pythonic Framework: being Python-based makes it accessible and straightforward to integrate into existing development workflows for Python-centric projects


Limitations:
    - Simplistic Diagram Designs: diagrams are simplistic in design, lacking complexity or visual sophistication
    - Scope Limited to Python Projects: may limit its applicability for organizations using diverse languages


### [MAL](https://mal-lang.org/)
Status:
Summary:
Advantages:
Limitations:

### [Threagile](https://threagile.io/)
Status:
Summary:
Advantages:
Limitations:

### [threatcl](https://threatcl.github.io/)
Status:
Summary:
Advantages:
Limitations:

### [threatspec](https://github.com/threatspec/threatspec)
Status:
Summary:
Advantages:
Limitations:

### [threat-composer](https://awslabs.github.io/threat-composer/workspaces/default/home?mode=Full)
Status:
Summary:
Advantages:
Limitations:

## UIs
### [IriusRisk](https://www.iriusrisk.com/)
Status:
Summary:
Advantages:
Limitations:

### [Threat Dragon](https://www.threatdragon.com/#/)
Status:
Summary:
Advantages:
Limitations:

### [Microsoft Threat Modeling Tool](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
Status:
Summary:
Advantages:
Limitations:

### [Threats Manager Studio](https://threatsmanager.com/)
Status:
Summary:
Advantages:
Limitations:

### [Theat Modeler](https://threatmodeler.com/threatmodeler/#threatmodeler)
Status:
There is a company behind ThreatModeler that is keeping the product maintained and updated.


Summary:
ThreatModeler is a highly awarded tool in the industry. It helps companies in various sectors like cloud, finance, retail, and health protect their systems. The software is designed for today's complex system architectures, showing how hackers might attack, identifying potential attack points, and suggesting necessary controls to prevent attacks. It requires little to no security expertise or learning curve, eliminating the need for costly outside security consultants emphasizing “‘1-Click” threat modeling. Key features of the ThreatModeler include:
    - An intelligent threat engine (ITE)
    - An automated threat intelligence framework
    - Threat model templates
    - Threat model chaining

The new version, ThreatModeler v7.0, brings many improvements, including:
    - ThreatModeler Wingman™, an AI Virtual Security Assistant
    - Better real-time collaboration
    - Advanced features for large, complex organizations


Advantages:
    - Appealing UI: relatively user-friendly and visually attractive interface
    - Model Type: ability to choose from various models (AWS, Azure, Google, etc.)
    - Multiple Methods for Creating Models: options include starting from blank, using previous models/templates, importing files, using CloudModeler, or Solutions Hub
    - ThreatModeler Wingman: recommends the next element and automatically adds flow/connection
    - Version Comparison: allows comparison of models with different versions already built
    - Version History: tracks changes and maintains a history of model versions
    - Collaboration: enables sharing and collaborating on the same model
    - Commenting: users can add comments to the model
    - Task Management: ability to create tasks needed in the model


Limitations:
    - Overwhelming Information: provides a list of threats, security requirements, and test cases (though they are separated into sections for each corresponding component)
    - Static 2D Representation: only supports static 2D models and is limited to the movement of individual components
    - Components Customization: offers a variety of options for components but does not allow for customization
    - Tracking Issues: lacks space in keeping track of how controls map to threat


### [Trike](https://www.octotrike.org/tools)
Status:
Summary:
Advantages:
Limitations:

### [Tutamantic](https://www.tutamantic.com/)
Status:
Summary:
Advantages:
Limitations:

### [ADTool](https://satoss.uni.lu/members/piotr/adtool/)
Status:
Summary:
Advantages:
Limitations:

### [AT-AT](https://github.com/yathuvaran/AT-AT)
Status:
Summary:
Advantages:
Limitations:

### [Ent](https://github.com/jimmythompson/ent)
Status:
Summary:
Advantages:
Limitations:

### [SeaMonster](https://sourceforge.net/projects/seamonster/?source=navbar)
Status:
Summary:
Advantages:
Limitations:

### [IsoGraph](https://www.isograph.com/software/attacktree/)
Status:
Summary:
Advantages:
Limitations:

### [SecurITree](https://www.amenaza.com/)
Status:
Summary:
Advantages:
Limitations:

### [RiskTree](https://risktree.2t-security.co.uk/)
Status:
Summary:
Advantages:
Limitations:

### [Deciduous](https://kellyshortridge.com/blog/posts/deciduous-attack-tree-app/)
Status:
Summary:
Advantages:
Limitations:

### [Sparta](https://sparta.distrinet-research.be/)
Status:
Summary:
Advantages:
Limitations:
