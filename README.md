# Icinga plugin  check_fortiwlc_ap

This is a plugin for Icinga to check status of AP devices on Fortinet WLC

Currently this plugin has the ability to monitor AP connection status on Fortinet WLC .

## Description

External plugin Check command check_ap_connection_status is added
and configured to icinga2 .Check command check_fortiwlc_ap
connects to WLS and return status of AP.

### Icinga

A check command is defined called `check_fortiwlc_ap`. It takes four arguments:

* `url`: url address of WLC   
* `l`: Username to login with   
* `p`: Password to login with   
* `ap`: FQDN of AP


### Usage

```yaml
check_fortiwlc_ap --url "https://nekaj.si" -l "admin" -p "password" --ap w1-nekaj.si
```  

## Developing

### Versioning

Update version info in `check_fortiwlc_ap.spec` and `forti_api_rest.py`. Also update the
changes in `check_fortiwlc_ap.py`.

### Building

The script and Icinga command definition are packaged as RPM. See `build.sh`.
 
 ### Tests
 
 ```yaml
python test_forti_api.py
```  

