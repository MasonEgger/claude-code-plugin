# Temporal-Specific Writing Rules

When writing tutorials about Temporal applications, follow these additional conventions:

## Prerequisites for Temporal Tutorials

Common prerequisites for Temporal tutorials include:

* Installing the Temporal CLI tool
* Installing the appropriate Temporal SDK for the programming language being used

## Temporal Writing Conventions

### Headers

* All headers should use sentence case
* Example: "Creating your first workflow" (not "Creating Your First Workflow")

### Temporal Primitives

Capitalize official Temporal features and primitives:

* **Workflow** - Not "workflow"
* **Activity** - Not "activity"
* **Worker** - Not "worker"
* **Timer** - Not "timer"
* **Signal** - Not "signal"
* **Query** - Not "query"
* **Task Queue** - Not "task queue"
* **Workflow Execution** - Not "workflow execution"
* **Activity Execution** - Not "activity execution"

**Rule:** If it's an official Temporal feature or concept, capitalize it.

### Examples

**Correct:**
* "In this step, you will create a Workflow that processes orders."
* "The Activity will execute with automatic retry logic."
* "Configure the Worker to poll the Task Queue."
* "Use a Timer to add delays in your Workflow."

**Incorrect:**
* "In this step, you will create a workflow that processes orders."
* "The activity will execute with automatic retry logic."
* "Configure the worker to poll the task queue."

## Context-Specific Usage

When using these terms generically (not referring to the Temporal feature), use lowercase:

* "This workflow of steps helps you..." (generic workflow, not Temporal Workflow)
* "The worker process runs in the background..." (generic worker, not Temporal Worker)

When in doubt, ask: "Am I referring to the specific Temporal feature?" If yes, capitalize.
