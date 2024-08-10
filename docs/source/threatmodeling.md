# Overview of Threat Modeling
[Source](https://owasp.org/www-community/Threat_Modeling)

Threat modeling works to identify, communicate, and understand threats and mitigations within the context of protecting something of value.

A threat model is a structured representation of all the information that affects the security of an application. In essence, it is a view of the application and its environment through the lens of security.

Threat modeling can be applied to a wide range of things, including software, applications, systems, networks, distributed systems, Internet of Things (IoT) devices, and business processes.

A threat model typically includes:

- Description of the subject to be modeled
- Assumptions that can be checked or challenged in the future as the threat landscape changes
- Potential threats to the system
- Actions that can be taken to mitigate each threat
- A way of validating the model and threats, and verification of success of actions taken

Threat modeling is a process for capturing, organizing, and analyzing all of this information. Applied to software, it enables informed decision-making about application security risks. In addition to producing a model, typical threat modeling efforts also produce a prioritized list of security improvements to the concept, requirements, design, or implementation of an application.

In 2020 a group of threat modeling practitioners, researchers and authors got together to write the [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/) in order to “…share a distilled version of our collective threat modeling knowledge in a way that should inform, educate, and inspire other practitioners to adopt threat modeling as well as improve security and privacy during development”. The Manifesto contains values and principles connected to the practice and adoption of Threat Modeling, as well as identified patterns and anti-patterns to facilitate it.

## Four Questions

Adam Shostack first introduced the Four Questions in his book, [Threat Modeling: Designing for Security](https://shostack.org/books/threat-modeling-book), and it has since been adopted by many organizations as well as serves as the foundation for [Threat Modeling Manifesto](https://www.threatmodelingmanifesto.org/).

### What are we working on?
[Source](https://shostack.org/resources/threat-modeling#4steps)

The first step is defining what you’re working on. For example, you might choose to model:

- What you’re working on this sprint or improvement
- Software or applications
- Enterprise architecture
- Operational technology
- Mobile apps
- Internet of Things (IoT)

When you decide what you’re working on, you also start to build models. Diagrams are models of what you’re working on. A lot of people confuse form and function here. What's important is creating data- and process-flow diagrams that help you share what’s in your head with the people around you.


#### Specifics
[Source](https://www.microsoft.com/en-us/securityengineering/sdl/practices/secure-by-design)

**Identify use cases, scenarios, and assets** - An essential part of threat modeling and reviewing threat models is understanding what business functions or “use cases” the system has. Scenarios describing the sequence of steps for typical interactions with the system illustrate its intended purposes and workflows. They also describe the different roles of users and external systems that connect to it. The first step in threat modeling is to document the business functions the system performs and how users or other systems interact with it. Supplement textual descriptions of use cases and scenarios with flowcharts and UML sequence diagrams as needed. Whether you use formal documentation such as use cases and scenarios, or take a more informal approach, ensure you provide context that answers these questions:

- What are the business functions of the system?
- What are the roles of the actors that interact with it?
- What kind of data does the system process and store?
- Are there special business or legal requirements that impact security?
- How many users and how much data is the system expected to handle?
- What are the real-world consequences if the system fails to provide confidentiality, integrity, or availability of the data and services it handles?

An asset is something of value in a system that needs to be protected. Some assets are obvious such as money in financial transactions or secrets such as passwords and crypto keys. Others are more intangible like privacy, reputation, or system availability. Once you properly identify the system’s assets, it is easier to identify threats against them. Document the list of system assets.

Examples of tangible assets:

- Personal photos and contacts stored on a smartphone
- Compute resources in a cloud environment
- Software supply chain integrity in a development environment
- Medical imaging and diagnostic data
- Financial accounting data
- Biometric authentication data
- Proprietary formulae and manufacturing processes
- Military and government secrets
- Machine learning models and training data
- Credit card data

Examples of intangible assets:

- Customer trust
- User privacy
- System availability

**Create an architecture overview -** In addition to documenting business functionality and assets, create diagrams and tables to depict the architecture of your application, including subsystems, trust boundaries, and data flows between actors and components. At minimum, a Data Flow Diagram (DFD) is recommended, and other supplementary diagrams such as UML Sequence Diagrams to illustrate complex flows may also be helpful. A DFD is a high-level way to visualize data flows between the major components of a system. It is a simplified view that does not include every detail—just enough to understand the security properties and attack surface of the system. It is a recommended practice to label the following in your DFD arrows:

- Data types (business function)
- Data transfer protocols

A trust boundary is a logical construct used to demarcate areas of the system with different levels of trust such as:

- Public Internet vs. private network
- Service APIs
- Separate operating system processes
- Virtual machines
- User vs. kernel memory space
- Containers

Trust boundaries are important to consider when threat modeling because calls that cross them often need to be authenticated and authorized. Data that crosses a trust boundary may need to be treated as untrusted and validated or blocked from flowing altogether. There may be business/regulatory rules related to trust boundaries. For example, sovereign clouds must ensure that data is stored only within their trust boundaries, and in some cases, HIPAA Protected Health Information (PHI) shouldn’t cross trust boundaries. Trust boundaries are often illustrated in DFDs with dashed red lines.

![contoso cast diagram](https://cdn-dynmedia-1.microsoft.com/is/image/microsoftcorp/ContosoCastSimpleDFD?scl=1)

### What can go wrong?
[Source](https://shostack.org/resources/threat-modeling#4steps)

Once you know what you’re working on, you can start thinking about all the different things that can go wrong. If you’re a glass-half-empty person, this is where you’ll shine. The glass-half full folks will creatively brainstorm.

Some considerations include:
- Who’s the intended user?
- What’s the intended use?
- Can an unintended user get access to it?
- Can someone use it in an unintended way?


#### Specifics
[Source](https://www.microsoft.com/en-us/securityengineering/sdl/practices/secure-by-design)

**Identify the threats** – Threat modeling is most effective when performed by a group of people familiar with the system architecture and business functions who are prepared to think like attackers. Here are some tips for scheduling an effective threat modeling session:

- Prepare the list of use cases/scenarios and, if possible, a first draft of DFDs in advance.
- Limit the scope of your threat modeling activity primarily to the system or features that you are developing or directly interface with.
- Designate an official notetaker to capture and record threats, mitigations and action items during the meeting.
- Reserve at least 2 hours for the meeting. The first hour will usually be spent on getting a common understanding of system architecture and what scenarios you are modeling so you can spend the second hour identifying threats and mitigations.
- If you can’t cover it all in two hours, decompose the system into smaller chunks and threat model them separately.
- Invite people of varied backgrounds, including:
    - Engineers who are developing and testing the system
    - Product owners who can weigh security risk against business goals
    - Security analysts/engineers
    - People who are proficient at software testing (violating system assumptions, testing boundary conditions, generating invalid input, etc.)

STRIDE is a common methodology for enumerating potential security threats that fall into these categories:

|Category   | Definition   |
|---|---|
|**S**poofing|Making false identity claims|
|**T**ampering|Unauthorized data modification|
|**R**epudiation|Performing actions and then denying that you did|
|**I**nformation Disclosure|Leaking sensitive data to unauthorized parties|
|**D**enial of Service|Crashing or overloading a system to impact its availability|
|**E**levation of Privilege|Manipulating a system to gain unauthorized privileges|

People and threat modeling tools apply this methodology by considering all the elements in a dataflow diagram and asking if threats in any of the STRIDE categories apply to them. STRIDE is useful for novice threat modelers who have not been exposed to all these threat categories and so might miss some important threats. However, STRIDE is not a substitute for thinking like an attacker. **STRIDE may miss important design flaws that only thinking like an attacker will catch.**

Thinking like an attacker is the most important and difficult part of threat modeling. Once you and your team understand the system architecture, use scenarios, and assets you need to protect, you must imagine what could go wrong with your system if a motivated, capable attacker attempts to compromise it. Thinking like an attacker is not as simple as applying a methodology like STRIDE to enumerate threats. You must also challenge the security assumptions in your design and contemplate what-if scenarios in which some or all your security controls fail as attackers actively try to compromise your assets. Examples of security assumptions:

- We assume our open-source dependencies don’t have malicious code.
- We assume that cloud computing services are inherently trustworthy.
- We assume that app users will not root their mobile devices.
- We assume that all authenticated users have benign intent.

Validate that your security assumptions are correct and consider what happens if they are not. Determine if any assumptions are invalid based on the threat landscape and the value of the assets you need to protect. It helps to study historical incidents to gain insight into the attacker mindset.

Many threats and mitigations are highly technical, and you are unlikely to think of them all on your own. Educate yourself on threats and associated mitigation techniques that apply to the domain you are working in. For instance, every web developer should be aware of attacks like cross-site scripting (XSS), cross-site request forgery (CSRF), and command injection. Study resources like the [CWE Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/) and the [OWASP Top Ten](https://owasp.org/www-project-top-ten/) to learn more.

Record the threats you identify in your engineering team's work tracking system and rate their security severity so they can be prioritized accordingly. Document the threats you identify with sufficient detail that those reading them later can understand them. Well-written threats clearly describe:

- The threat actor who exploits the vulnerability
- Any preconditions required for exploitation
- What the threat actor does
- The consequences for affected assets and users

### What are we going to do?
[Source](https://shostack.org/resources/threat-modeling#4steps)

The question “what can go wrong” helps you figure out the threats. When you look at what you’re going to do, you address each threat.

Some types of actions include:

- Mitigating threats: Make it harder for someone to take advantage of a threat.
- Eliminating threats: Remove the feature or interface that creates the threat.
- Transferring threats: Have someone else be responsible, like having a customer change default settings.
- Accepting threats: Recognize that the time and effort to mitigate or eliminate the threat undermines the purpose of the project.

While these sound like, and are aligned to, risk management strategies, they are subtly different. Remember: threats are the things that can go wrong. Risk management focuses on the likelihood and impact of threats. You can use implicit agreement when choosing because it can be faster and easier than formal risk management approaches.


#### Specifics
[Source](https://www.microsoft.com/en-us/securityengineering/sdl/practices/secure-by-design)

**Identify and track mitigations** - Secure Design Philosophy: When identifying mitigations, keep in mind that security is not “all or nothing”. A partial mitigation that raises the cost for an attacker, slows them down to give defenders time to detect them, or limits the scope of damage is much better than no mitigation at all. Think in terms of layered defenses. Attackers don’t just exploit a single vulnerability and stop there. They chain multiple vulnerabilities together, pivoting from one target system to the next until they achieve their objective (or get caught.) Each layered defense increases the likelihood that attackers will be blocked or detected. Also, assume that other layers’ security controls will be bypassed or disabled. This is the essence of the Assume Breach philosophy which results in a resilient set of layered defenses rather than relying solely on external defenses that, if bypassed, result in a major breach.

Recommended Secure Design Practices:
- Design and Threat Model as a Team
- Prefer Platform Security to Custom Code
- Secure Configuration is the Default
- Never Trust Data from the Client
- Assume Breach
- Enforce Least Privilege
- Minimize Blast Radius
- Minimize Attack Surface
- Consider Abuse Cases
- Monitor and Alert on Security Events

Threat modeling is not complete until you create work items to track your threat findings and the related development and testing tasks to mitigate them. Consider tagging the work items and writing queries so they are easy to find. A threat model provides the seeds for a good security test plan. Be sure to test that your mitigations work as intended and use automated testing when possible.

### Did we do a good job?
[Source](https://shostack.org/resources/threat-modeling#4steps)

Finally, you need to validate your threat model by checking your work to make sure it’s as complete as possible.

This step includes checking:
- The model: make sure it matches what you built, starting with the diagram.
- Each threat: review that you found all the possible threats and did the right thing with them.
- Tests: ensure you have a good test to detect the problem, one that is in line with other software tests and the risks that failures expose.

## Additional Resources

### Guides and Trainings
- Microsoft: [Threat Modeling Security Fundamentals](https://learn.microsoft.com/en-us/training/paths/tm-threat-modeling-fundamentals/)
- Adam Shostack: [Worlds Shortest Threat Modeling Course](https://www.youtube.com/watch?v=2pvprvsr1lo&list=PLCVhBqLDKoOOZqKt74QI4pbDUnXSQo0nf)
- ShellSharks: [A Threat Modeling Field Guide](https://shellsharks.com/threat-modeling)
- NIST: [800-30 Guide for Conducting Risk Assessments](https://csrc.nist.gov/pubs/sp/800/30/r1/final)
- OWASP: [Threat Modeling Process](https://owasp.org/www-community/Threat_Modeling_Process)

## Tools
There have been several tools and domain-specific languages that have been previously developed to aid system designers with threat modeling. However, we found that many people don't actually use these tools, and when they do it's for diagramming mainly.  We expect this is because existing systems do not support the ad-hoc, flexible ways that we found software architects and threat modelers review systems when threat modeling in practice.

We recommend trying out a few of these tools. If you do not have Windows and want to try [Microsoft Threat Modeling Tool](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool) or [Threats Manager Studio](https://threatsmanager.com/), please use `vm-winresearch.eecs.tufts.edu`.

### Diagramming Only
#### [draw.io](https://app.diagrams.net/)
Status:
Summary:
Advantages:
Limitations:

#### [C4](https://c4model.com/)
Status:
Summary:
Advantages:
Limitations:

#### [Mermaid](https://mermaid.live/)
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


#### [Structurizr](https://structurizr.com/)
Status:
Summary:
Advantages:
Limitations:

#### [Diagrams](https://diagrams.mingrammer.com/)
Status:
Summary:
Advantages:
Limitations:

#### [PlantUML](https://plantuml.com/)
Status: PlantUML is actively being developed. The most recent version was released on May 26th, 2024 and the most recent commit to the GitHub repository was a few days ago.
Summary: PlantUML is an open-source tool that allows users to create a variety of diagrams using a simple text-based language. It supports multiple diagram types such as sequence, deployment, and mind maps, and can output images in formats like PNG and SVG. PlantUML is highly versatile, integrating with various tools and aiding in effective communication and collaboration among developers and stakeholders.
Advantages:
    - The plain text used by PlantUML is very straightforward and easy to understand for even novice users.
    - Users can define their diagrams using intuitive and concise textual descriptions, speeding up the diagram creation process
    - Supports all important UML diagrams and can be used in a wide variety of scenarios and modeling approaches
    - A very versatile tool as it Is able to integrate with a variety of documentation platforms and it has a wide range of supported output formats.

Limitations:
    - Does not provide any features such as drag-and-drop components or the ability to click and toggle through various system views.
    - It is more of a drawing tool, rather than a modeling tool. It cannot track relationships between diagram elements or information about those elements, hence it cannot give suggested threats and mitigations to users.
    - Using plain text to describe diagrams results in loss of control. There is no way to determine the position and layout of diagram elements, as the algorithm does it for you.

### DSLs/Threat Modeling as Code
#### [pytm](https://github.com/izar/pytm)
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


#### [MAL](https://mal-lang.org/)
Status:
Summary:
Advantages:
Limitations:

#### [Threagile](https://threagile.io/)
Status:
Summary:
Advantages:
Limitations:

#### [threatcl](https://threatcl.github.io/)
Status: Actively being developed, with the last commit to the GitHub repository being two days ago.
Summary: Threagile is an open-source toolkit for agile threat modeling, enabling teams to model architectures and their assets as YAML files. Upon execution, it performs security checks using standard and custom risk rules, generates risk reports with mitigation advice, and creates detailed data-flow diagrams.
Advantages:
    - Is open-source and free for anyone to use. A support subscription is also offered for anyone who needs additional guidance and assistance when using Threagile.
    - Automatically generates data-flow diagrams for efficiency, including detailed model elements
    - Includes a set of risk-rules that check the security of the architecture and generate a report of potential risks and mitigation advice.
    - Users may include their own custom coded risk rules when executing security checks against their architecture model. This allows practitioners in different domains to tailor the system to their particular context.
Limitations:
    - No features like drag-and-drop components or the ability to click and toggle through various system views, since the YAML file is the only source of input to Threagile. This makes it difficult for more inexperienced users to learn how to use the tool.
    - There is no way to change the look and layout of the data-flow diagrams as they are automatically generated
    - Does not provide a way to filter threat and mitigation suggestions to the users’ current focus. Only provides the full overwhelmingly long lists of suggestions all at once.

#### [threatspec](https://github.com/threatspec/threatspec)
Status:
Summary:
Advantages:
Limitations:

#### [threat-composer](https://awslabs.github.io/threat-composer/workspaces/default/home?mode=Full)
Status:
Summary:
Advantages:
Limitations:

### UIs
#### [IriusRisk](https://www.iriusrisk.com/)
Status: IriusRisk is being actively developed with their most recent product release being two weeks ago
Summary: IriusRisk is an open threat modeling platform that automates the creation of threat models and architectural risk analysis at the design stage. It allows teams to generate system architecture diagrams, identify threats, and suggest countermeasures, facilitating collaboration between security and development teams.
Advantages:
    - Accessible for non-security experts. Its user-friendly interface and built-in guidance make it usable for developers and product managers
    - Automatically creates threat models based on your system architecture with real-time analysis
    - Drag and drop features as well as a quick start video make IriusRisk especially accessible and intuitive for novice users to learn as they use
Limitations:
    - Does not consider different possible ways the system could be deployed when analyzing the system
    - All threats and countermeasures are presented on one screen, which may make it difficult for users to parse.
    - Does not provide the ability to switch between different system views

#### [Threat Dragon](https://www.threatdragon.com/#/)
Status:
Summary:
Advantages:
Limitations:

#### [Microsoft Threat Modeling Tool](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool)
Status:
Summary:
Advantages:
Limitations:

#### [Threats Manager Studio](https://threatsmanager.com/)
Status:
Summary:
Advantages:
Limitations:

#### [Theat Modeler](https://threatmodeler.com/threatmodeler/#threatmodeler)
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


#### [Trike](https://www.octotrike.org/tools)
Status:
Summary:
Advantages:
Limitations:

#### [Tutamantic](https://www.tutamantic.com/)
Status:
Summary:
Advantages:
Limitations:

#### [ADTool](https://satoss.uni.lu/members/piotr/adtool/)
Status:
Summary:
Advantages:
Limitations:

#### [AT-AT](https://github.com/yathuvaran/AT-AT)
Status:
Summary:
Advantages:
Limitations:

#### [Ent](https://github.com/jimmythompson/ent)
Status:
Summary:
Advantages:
Limitations:

#### [SeaMonster](https://sourceforge.net/projects/seamonster/?source=navbar)
Status:
Summary:
Advantages:
Limitations:

#### [IsoGraph](https://www.isograph.com/software/attacktree/)
Status:
Summary:
Advantages:
Limitations:

#### [SecurITree](https://www.amenaza.com/)
Status:
Summary:
Advantages:
Limitations:

#### [RiskTree](https://risktree.2t-security.co.uk/)
Status:
Summary:
Advantages:
Limitations:

#### [Deciduous](https://kellyshortridge.com/blog/posts/deciduous-attack-tree-app/)
Status:
Summary:
Advantages:
Limitations:

#### [Sparta](https://sparta.distrinet-research.be/)
Status:
Summary:
Advantages:
Limitations:
