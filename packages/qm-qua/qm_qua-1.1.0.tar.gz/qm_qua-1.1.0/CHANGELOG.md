# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## Unreleased

## [1.1.0] - 2023-03-16

### Deprecation
- The `hold_offset` entry in the config is deprecated and is replaced by a new `sticky` entry with an improved API
- Moved `_Program` path to `qm.program.program.Program`. Old path will be removed in 1.2.0
- Moved `QmJob` path to `qm.jobs.qm_job.QmJob`. Old path will be removed in 1.2.0
- Moved `QmPendingJob` path to `qm.jobs.pending_job.QmPendingJob`. Old path will be removed in 1.2.0
- Moved `QmQueue` path to `qm.jobs.job_queue.QmQueue`. Old path will be removed in 1.2.0
- Renamed `JobResults` into `StreamingResultFetcher`. Old name will be removed in 1.2.0
- Moved `StreamingResultFetcher` path to `qm.results.StreamingResultFetcher`. 
- `QmJob.id()` is deprecated, use `QmJob.id` instead, will be removed in 1.2.0
- `QmJob` no longer has `manager` property 
- `QmPendingJob.id()` is deprecated, use `QmPendingJob.id` instead, will be removed in 1.2.0
- `QuantumMachine` no longer has `manager` property
- `QuantumMachine.peek` is removed (was never implemented)
- `QuantumMachine.poke` is removed (was never implemented)
- `IsInt()` function for qua variables is deprecated, use `is_int()` instead, will be removed in 1.2.0
- `IsFixed()` function for qua variables is deprecated, use `is_fixed()` instead, will be removed in 1.2.0 
- `IsBool()` function for qua variables is deprecated, use `is_bool()` instead, will be removed in 1.2.0 
- `set_clock` method of the octave changed API, old API will be removed in 1.2.0.

### Added
- Added auto correction for config dict in IDEs, when creating a config, add the following: `config: DictQuaConfig = {...}`.
- :guardswoman: Added the option to invert the digital markers in a quantum machine by indicating it in the config.
- :guardswoman: Support `fast_frame_rotation`, a frame rotation with a cosine and sine rotation matrix rather than an angle.  
- Added support for floating point numbers in the `intermediate_frequency` field of `element` .
- :guardswoman: Conditional `play` is extended to both the digital pulse if defined for operation. 
- :guardswoman: Extended the sticky capability to include the digital pulse (optional)
- Added option to validate QUA config with protobuf instead of marshmallow. It is usually faster when working with large configs, to use this feature, set `validate_with_protobuf=True` while opening a quantum machine.
- Added type hinting for all `qua` functions and programs
- Added another way of getting results from job results: `job.result_handles["result_name"]`.`
- Octave reset request command added to "Octave manager".
- Added support for octave configuration inside the QUA-config dictionary, this will later deprecate the `OctaveConfig` object, which is still supported
- Added objects that reflects the elements in the `QuantumMachine` instance.

### Changed
- Updated `play` docstrings to reflect that the changes to conditional digital pulse.
- Changed octave's `set_clock` API.
- Changed and improved internal grpc infrastructure
- Changed and improved async infrastructure 

## [1.0.2] - 2023-01-01
### Removed
- Removed deprecated `math` library (use `Math` instead).
- Removed deprecated `qrun_` context manager (use `strict_timing_` instead).

### Added
- Better exception error printing.
- An api to add more information to error printing `activate_verbose_errors`.
- :guardswoman: Add support for OPD (Please check [the OPD documentation](https://qm-docs.qualang.io/hardware/dib) for more details).
- :guardswoman: Added timestamps for play and measure statements.
- Support for numpy float128.
- Added the function `create_new_user_config()` under `qm.user_config` to create a configuration file with the QOP host IP & Port to allow opening `QuantumMachinesManager()` without inputs.
- Added infrastructure for anonymous log sending (by default, no logs are sent). 

### Fixed
- Serializer - Added support for averaging on different axes.
- Serializer - Remove false message about lacking `play(ramp()...)` support.
- Serializer - Fixed the serialization when `.length()` is used.
- Serializer - Fixed cases in which the serializer did not deal with `adc_trace=true` properly. 
- Serializer - The serializer does not report failed serialization when the only difference is the streams' order. 
- Serializer - The serializer now correctly serialize the configuration when an element's name has a `'`.

## [1.0.1] - 2022-09-22
### Changed
- Octave - Added a flag to not close all the quantum machines in `calibrate_element`.
- Octave - The quantum machine doing the calibrations will be closed after the calibration is done.

## [1.0.0] - 2022-09-04
- Removed deprecated entries from the configuration schema
- Removed dependency in `qua` package
### Fixed
- QuantumMachineManager - Fixed a bug where you could not connect using SSL on python version 3.10+
- Serializer - Fixed `declare_stream()` with `adc_true=True`
### Changed
- Update betterproto version.
- OctaveConfig: changed `set_device_info` name to `add_device_info`
- OctaveConfig: changed `add_opx_connections` name to `add_opx_octave_port_mapping`
- OctaveConfig: changed `get_opx_octave_connections` name to `get_opx_octave_port_mapping`
### Added
- :guardswoman: API to control Octave - an up-conversion and down-conversion module with built-in Local Oscillator (LO) sources.
- Support Numpy as input - Support numpy scalars and arrays as valid input. Numpy object can now be used interchangeably with python scalars and lists. This applies to all statements imported with `from qm.qua import *`
- Serializer - Added support for legacy save

## [0.3.8] - 2022-07-10
### Fixed
- Serializer - Fixed a bug which caused binary expression to fail
### Changed
- QuantumMachineManager will try to connect to 80 before 9510 if the user did not specify a port.
- QuantumMachineManager will give an error if no host is given and config file does not contain one.
- :guardswoman: QRun - Change qrun to strict_timing
- :guardswoman: Input Stream - Fixed API for input stream
### Added
- Serializer - add strict_timing to serializer
- Logger - Can now add an environment variable to disable the output to stdout 

## [0.3.7] - 2022-05-31
### Fixed
- Serializer - Fixed a bug which caused the serializer to fail when given completely arbitrary integration weights
- Serializer - Fixed a bug which caused the serializer to fail when given a list of correction matrices
- Serializer - Added support for "pass" inside blocks (if, for, etc). "pass" inside "else" is not supported.
### Added
- :guardswoman: play - Add support for continue chirp feature
- :guardswoman: High Resolution Time Tagging - Add support for high resolution time-tagging measure process
- :guardswoman: Input Stream - Add support for streaming data from the computer to the program
- :guardswoman: OPD - Added missing OPD timetagging function
### Changed
- set_dc_offset - 2nd input for function was renamed from `input_reference` to `element_input`
- QuantumMachineManager will try to connect to ports 9510 and 80 if the user did not specify a port.
- set_output_dc_offset_by_element - can now accept a tuple of ports and offsets
- `signalPolarity` in the timetagging parameters (`outputPulseParameters` in configuration) now accept `Above` and `Below` instead of `Rising` and `Falling`, which better represent it's meaning.

## [0.3.6] - 2022-01-23
### Added
- `signalPolarity` in the timetagging parameters (`outputPulseParameters` in configuration) now accept also `Rising` and `Falling`, which better represent it's meaning. 
- `derivativePolarity` in the timetagging parameters (`outputPulseParameters` in configuration) now accept also `Above` and `Below`, which better represent it's meaning. 
- Add unsafe switch to `generate_qua_config` function
- Add library functions and *amp() in measure statement to `generate_qua_config` function
### Changed
- Better error for library functions as save source

## [0.3.5] - 2021-12-27
### Added
- Raises an error when using Python logical operators 
- Add elif statement to `generate_qua_config` function

### Changed
- Fix indentation problem on the end of for_each block in `generate_qua_config` function
- The `generate_qua_config` now compresses lists to make the resulting file smaller and more readable

## [0.3.4] - 2021-12-05
### Added
- :guardswoman: Define multiple elements with shared oscillator.
- :guardswoman: Define an analog port with channel weights.
- Add measure and play features to `generate_qua_config` function
- format `generate_qua_config` function output
- improve `wait_for_all_values` execution time

## [0.3.3] - 2021-10-24
### Added
- :guardswoman: Define an analog port with delay.
- :guardswoman: New `set_dc_offset()` statement that can change the DC offset of element input in real time.
- :guardswoman: New input stream capabilities facilitating data transfer from job to QUA.
- :guardswoman: New flag for stream processing fft operator to control output type.
- :page_with_curl: Add information about demod on a tuple.
- :page_with_curl: Added best practice guide.
### Changed
- Validate that element has one and only one of the available input type QMQUA-26

## [0.3.2] - 2021-10-03
### Added
- :guardswoman: QuantumMachinesManager health check shows errors and warnings.
- :guardswoman: Fetching job results indicates if there were execution errors.
- :guardswoman: Define an element with multiple input ports.
- :guardswoman: Stream processing demod now supports named argument `integrate`. If `False` is provided
the demod will not sum the items, but only multiply by weights.
### Changed
- Documentation structure and content.

## [0.3.1] - 2021-09-13
### Fixed
- Fixed serialization of IO values.
- Support running `QuantumMachinesManager` inside ipython or jupyter notebook.
### Changed
- Removing deprecation notice from `with_timestamps` method on result streams.
- Setting `time_of_flight` or `smearing` are required if element has `outputs` and
must not appear if it does not.

## [0.3.0] - 2021-09-03
### Changed
- Support for result fetching of both versions of QM Server.
- Now the SDK supports all version of QM server.

## [0.2.1] - 2021-09-01
### Changed
- Default port when creating new `QuantumMachineManager` is now `80` and user 
config file is ignored.

## [0.2.0] - 2021-08-31
### Added
- The original QM SDK for QOP 2.

## [0.1.0] - 2021-08-31
### Added
- The original QM SDK for QOP 1.

[Unreleased]: https://github.com/qm-labs/qm-qua-sdk/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/qm-labs/qm-qua-sdk/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.8...v1.0.0
[0.3.8]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.7...v0.3.8
[0.3.7]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.6...v0.3.7
[0.3.6]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.5...v0.3.6
[0.3.5]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.4...v0.3.5
[0.3.4]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.3...v0.3.4
[0.3.3]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.2...v0.3.3
[0.3.2]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/qm-labs/qm-qua-sdk/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/qm-labs/qm-qua-sdk/releases/tag/v0.1.0

## Legend 
* :guardswoman: Features that are server specific and depend on capabilities and version
* :page_with_curl: Documentation only change
