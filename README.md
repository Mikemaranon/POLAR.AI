# POLAR.AI: the open-source AI ecosystem

![POLAR.AI Logo](/assets/POLAR.AI-t-small.png)

`POLAR.AI` is a project to develop an `open-source ecosystem` fully capable of **designing**, **creating**, **training** and **deploying** artificial inteligent models in on-premise and cloud infrastructures.  
The ecosystem has 3 main software components:

| Component        | Description                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------- |
| **POLAR Node**   | Component made to `connect every single enviroment component with it.` This is the `central node` that will control all the trafic in the POLAR.AI enviroment. The main feature of this component is the `user and roles management`. Its interface will be accesible via a web portal connection simulating a `terminal` or a connection via local shell |
| **POLAR Core**   | Component responsible of storing and managing all the logic that will determine the inference of locally stored models and external connections such as Azure or OpenAI models via API keys. This component serves as the `deployment environment` for models. |
| **POLAR Forge**   | Module for `creating models` based on **neural networks** or **foundational models**. Its functionality includes providing services for `creation, training, and fine-tuning` for various scenarios, either with **base models or from scratch**. |
| **POLAR Studio** | `Main user-side component` that will offer the user experience. from the POLAR studio every user in the domain will be able to interact with every model imported in POLAR core and external models registered via APIs. |

## Project Description

This project aims to be completely free and open-source. It is not a commercial venture offering services. The POLAR.AI ecosystem is being developed to be released and published, allowing any user or company to use it at no cost.  
POLAR is being designed to be compatible with both cloud and on-premise architectures, making it adaptable to any environment through Docker or kubernetes deployment. 

## Documentation

Project documentation can be found [here](/DOC/documentation/POLAR%20doc.pdf)