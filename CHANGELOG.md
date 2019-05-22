# Changelog

## [1.0.9] -  May, 22, 2019
### Added
- Add the method of `estimate_step`

### Changed
N/A

### Removed
N/A

## [1.0.8] -  Apr, 23, 2019
### Added
N/A

### Changed
- Fix: Convert the negative value into hex str correctly by using `hex` function 
- Fix: Convert hex str to bytes correctly by using `fromhex` method 

### Removed
N/A

## [1.0.7] -  Dec, 7, 2018
### Added
N/A

### Changed
- Fix: The data type of the Message type transaction's data is changed from string to hex string prefixed with '0x'

### Removed
N/A


## [1.0.6] -  Nov, 22, 2018
### Added
N/A

### Changed
- Fix: convert_params_value_to_hex_str() converts first item of dict only

### Removed
N/A


## [1.0.5] -  Nov, 15, 2018
### Added
- Add the method of `get_max_step_limit`
- Make the call and transaction have the method of `from_dict` to convert the dict to call or transaction object
- Make the call and transaction have the method of `to_dict` to convert call or transaction object to the dict

### Changed
- Upgrade requests to version 2.20.0 or later
- Amend `gen_deploy_data_content` not to load tests directory

### Removed
N/A


## [1.0.4] -  Sep, 17, 2018
### Added
- Add quickstart module
    - Add samples and README.md for quickstart
- Add Converter to convert return data from hex str into an int
- Add repeater for calling the decorated function
    - To check returning transaction result after consensus

### Changed
- Amend the way to load a key file having 'bom'

### Removed
N/A


## [1.0.3] -  August, 31, 2018
### Added
- Add FileNotFountError while loading the key file

### Changed
- Set the function `create_keyfile_json`'s param 'kdf' into 'scrypt'
    - To set the params 'kdf' into 'scrypt' while creating key file json

### Removed
N/A


## [1.0.1] -  August, 30, 2018
### Added
N/A

### Changed
- Revise the package names and update the version to 1.0.1.
    - `IconService` to `iconsdk`
    - `Icon_service` to `icon_service`

### Removed
N/A


## [1.0.0] -  July, 31, 2018
### Added
 - Initialize version.

### Changed
N/A

### Removed
N/A




