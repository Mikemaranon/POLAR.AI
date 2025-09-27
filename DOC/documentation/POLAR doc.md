<p align="center">
    <img src="./assets/POLAR.AI-t-small.png" alt="POLAR.AI Logo"/>
</p>

<div class="page-break"></div>

# Table of Contents (Provisional)

- [Introduction](#introduction)
- [1. POLAR Node: Central Management Hub](#1-polar-node-central-management-hub)
  - [1.1 API Module (`api_m`)](#11-api-module-api_m)
    - [1.1.1 Endpoints Overview](#111-endpoints-overview)
    - [1.1.2 Structure Overview](#112-structure-overview)
      - [Shared Components](#shared-components)
        - [POLAR Manager](#polar-manager)
        - [Database: PostgreSQL](#database-postgresql)
        - [Entities](#entities)
        - [Repositories](#repositories)
        - [Services](#services)
  - [1.2 Authentication and Roles](#12-authentication-and-roles)
  - [1.3 Web Interface](#13-web-interface)
- [2. POLAR Core: Model Deployment & Management](#2-polar-core-model-deployment--management)
- [3. POLAR Forge: Model Creation and Training](#3-polar-forge-model-creation-and-training)
- [4. POLAR Studio: User Interaction Layer](#4-polar-studio-user-interaction-layer)
- [5. Common Utilities and Configurations](#5-common-utilities-and-configurations)

<div class="page-break"></div>

# Introduction

`POLAR.AI` is an open-source ecosystem designed to fully manage the lifecycle of artificial intelligence models in both **on-premise** and **cloud** environments. Its main goal is to provide a modular, scalable, and maintainable architecture that allows developers, data scientists, and organizations to create, deploy, and interact with AI models seamlessly.

The ecosystem is structured around four core components:

1. **POLAR Node**: The central hub responsible for coordinating communication between all environment components, handling **user authentication**, **role management**, and exposing APIs to orchestrate services across the ecosystem. Its interface is accessible via a web portal or local shell, simulating a terminal experience.

2. **POLAR Core**: The deployment engine that manages and stores models. It handles inference, connections to external services (such as Azure or OpenAI APIs), and provides a secure environment to execute AI workloads.

3. **POLAR Forge**: A module focused on model creation, training, and fine-tuning. It supports both **neural networks** and **foundational models**, providing developers with tools to build models from scratch or adapt pre-existing ones.

4. **POLAR Studio**: The main user-facing interface that allows interaction with models, both local (from Core) and external (via registered APIs). Studio ensures a seamless experience for end-users to query, visualize, and analyze AI outputs.

**Key design principles:**

- **Open-source and free**: POLAR.AI is intended to be fully accessible, with no commercial restrictions.
- **SOLID architecture**: Every module follows the single-responsibility principle and other SOLID guidelines to ensure maintainability and scalability.
- **Cloud & on-premise compatibility**: The ecosystem can be deployed via Docker or Kubernetes, supporting hybrid environments.
- **Modular and extensible**: Each component is independent yet interoperable, allowing future expansion (e.g., integrating new modules or APIs).

This documentation provides a detailed breakdown of each module, including its structure, entities, repositories, services, and configuration, following best practices for maintainable software and secure operations.

---

