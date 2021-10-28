# Workestrator

API for a work "orchestration" service: unique work for a particular "pipeline" or task type is registered to be done with the service, and the service can be polled for work to be allocated.

The uniqiueness, for unique work within a pipeline, is described as a JSON object.

Here is an OpenAPI schema, and a Python FastAPI service derived from it.