# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Changes are grouped as follows
- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [0.23.0] - 2020-09-xx
### Added
- Entity matching pipelines, which allows you to deploy an entity matching model with confirmed matches and rules.

### Changed
- Entity matching list calls have a limit parameter which defaults to 100.
- ContextualizationJobs now have timestamp fields consistently as members, and no longer return them in result.

## [0.22.3] - 2020-09-15
### Changed
- `/fit` in entity matcher supports defining which field in matchFrom and matchTo to use as the id field by specifying `id_field`

## [0.22.2] - 2020-09-14
### Changed
- `/detect, /convert, /extractpattern, /ocr` supports referring to a file using file_id and/or file_external_id. file_id and file_external_id are returned in the responses.

## [0.22.1] - 2020-09-09
### Added
- `/detect` in Pnid Parser can accept entities with type `List[Union[str, dict]]` and returns `entities` if the type of input `entities` has type of `List[dict]`

## [0.22.0] - 2020-09-09
### Added
- Added `/findobjects` in Pnid Object Detection

## [0.21.0] - 2020-09-09
### Removed
- Removed `/parse` in Pnid Parser
### Added
- Added `/convert` in Pnid Parser

## [0.20.1] - 2020-09-07
### Fixed
- Fix in EntityMatcher predict method.

## [0.20.0] - 2020-09-01
### Added
- Entity matcher `predict` and `refit` methods now exist on `client.entity_matching` in addition to the model object.

## [0.19.0] - 2020-08-31
### Changed
- Entity matcher methods now all take and return `id` instead of `model_id` and accept `id` or `external_id`.
- Entity matcher uses the new `/entitymatching` endpoints

### Removed
- `fit_ml` and `predict_ml` methods in entity matcher.

## [0.18.0] - 2020-08-25
### Added
- Add py.typed file to inform that package is typed

## [0.17.0] - 2020-08-20
### Changed
- Some methods in entity matcher now take `id` instead of `model_id`

### Added
- Update and retrieve_multiple methods for entity matcher.
- Changed entity matching methods to take external_id where possible.

## [0.16.0] - 2020-08-13
### Changed
- Change list-method to list all models instead of jobs.
- Changed endpoints used for list and list_jobs to comply with updates to the API.
### Added
- Add list_jobs-method that behaves as old list-method, that is returns all jobs. 
- Option to filter returned models on based on all input parameters. 

## [0.15.4] - 2020-08-13
### Added
- Add name, description and external-id parameters to fit entity matcher.

## [0.15.3] - 2020-08-13
### Fixed
- Fix `import time` bug in functions.

## [0.15.2] - 2020-08-13
### Added
- Insert sleep cycles for files api queries in functions creation

## [0.15.1] - 2020-08-10
### Added
- Add model info for entity matcher models (classifier, feature_type, model_to, keys_from_to) to the output of retrieve.

## [0.15.0] - 2020-08-10
### Changed
- Changed name of the parameter indicating the type of features created from model_type to feature_type, entity matcher.

## [0.14.5] - 2020-08-07
### Added
- Allow users to specify custom path to handle function by setting function_path.

## [0.14.4] - 2020-08-06
### Removed
- Removed everything related to resource typing (contextualization).

## [0.14.3] - 2020-08-06
### Added
- A class for Document parsing, allowing detecting entity in documents
- Detect function also for pnid, similar to the old parse function, which may get deprecated
- min_tokens parameter for entity detecting endpoints. Allowing to set the mimimum number of tokens needed for a detection

## [0.14.2] - 2020-08-05
### Changed
- Renamed refitml refit entity matcher.

## [0.14.1] - 2020-08-03
### Added
- Added retry to functions POST endpoints. 

## [0.14.0] - 2020-08-03
### Changed
- Merge fit_ml and fit, and predict_ml and predict endpoints entity matcher - major changes to required parameters and responses.

## [0.13.0] - 2020-07-23
### Changed
- Base version of the SDK changed to 2.x

## [0.12.1] - 2020-07-07
### Added
- The entity matching methods now have additional options for classifier and feature types.
- PNID detect patterns endpoint added.
- Schema completion endpoint added.

## [0.12.0] - 2020-07-07
### Changed
- Synthetic time series and labels removed, as they were moved to non-experimental status in the main SDK.

## [0.11.2] - 2020-06-19
### Added
- The method `Function.update()`, which updates the function object.

## [0.11.1] - 2020-06-10
### Fixed
- Client no longer gives an error on using a token instead of an API key.

## [0.11.0] - 2020-06-08
### Changed
- Removed FunctionCallResponse class. Functions `FunctionCallsAPI.get_response()` and `FunctionCall.get_response()` now returns the actual function response (without being wrapped in an object with `call_id`, `function_id` and `response`).

## [0.10.0] - 2020-06-04
### Changed
- POST endpoints such as search and list will be retried in experimental endpoints, as they are in v1.

## [0.9.1] - 2020-06-04

### Changed
- Updated documentation for functions.

## [0.9.0] - 2020-05-29
### Changed
- Function response is no longer a property of the `FunctionCall` class. Instead, the response can be retrieved by the methods `FunctionCallsAPI.get_response()` or `FunctionCall.get_response()`.
- The documentation for function schedules is put under the expand/collapse header Function Schedules.

### Added
- Filtering of function calls given call attributes and added  an attribute for schedule id to the FunctionCall data class.

## [0.8.3] - 2020-05-28
### Fixed
- The method `Function.call()` now takes the argument `wait` (defaults to `True`) instead of `asynchronous`. This change was supposed to be a part of release 0.8.0.

## [0.8.2] - 2020-05-27
### Fixed
- Allow `true_matches` to be `None` in `fit_ml`.

## [0.8.1] - 2020-05-26
### Changed
- Function calls now returns `functionId`, so the getting logs of a call has a simplified internal structure.

## [0.8.0] - 2020-05-26
### Changed
- In `FunctionsAPI.call()`, the `asynchronous` argument has been removed, reflecting the Functions API which now only supports asynchronous calls. A new argument `wait` has been introduced. When `wait=True` (default), `FunctionsAPI.call()` will block until the call is finished.

## [0.7.3] - 2020-05-19
### Fixed
- Dosctring for `FunctionCallsAPI.list()` erroneously listed `external_id` as optional argument. This has been corrected to `function_external_id`.


## [0.7.2] - 2020-05-15
### Fixed
- Support for no entities passed on predict_ml.

## [0.7.1] - 2020-05-15
### Added
- Support for ML Entity matcher from/to columns and retrain.

## [0.7.0] - 2020-05-14

### Added
- Labels endpoint support
- Assets labelling support

## [0.6.0] - 2020-05-08

### Changed
- SDK updated for changes in ML Entity matcher endpoints.

### Fixed
- `FunctionSchedulesAPI.create()` works when argument `name` contains the character `/`.

## [0.5.8] - 2020-04-30
- Assets playground API uses playground for retrieve

## [0.5.7] - 2020-04-29

### Added
- Added checks that verify that the function handler in an uploaded function is correctly constructed.

### Fixed
- `FunctionSchedulesAPI.create()` works without providing the `data` argument.

## [0.5.6] - 2020-04-28

### Added
- Data classes for contextualization models and job now include time stamps for request_timestamp, start_timestamp, status_timestamp.
- Unstructured search endpoints added in client.files.unstructured.

## [0.5.5] - 2020-04-21

### Changed
- Data class `Function` now has the additional attribute `error`.

## [0.5.4] - 2020-04-20

### Added
- fit_ml function on entity matcher and predict_ml on model object.

## [0.5.3] - 2020-04-16

### Added
- Sphinx documentation for Cognite Functions

## [0.5.2] - 2020-04-16

### Added
- A `FunctionSchedule` class and corresponding api attached to the `Functions` api to interact with function schedules. 
Function schedules can now also be listed using the `Function` object through the `list_schedules` method. 

## [0.5.1] - 2020-04-15

### Added
- Argument `function_handle` to `FunctionsAPI.create()`, which can be used to create a function directly from code.

## [0.5.0] - 2020-04-08

### Added
- FunctionsAPI to interact with the Cognite Functions API in CDF.

### Changed
- Refactor of contextualization endpoints to not use asyncio and block later.
