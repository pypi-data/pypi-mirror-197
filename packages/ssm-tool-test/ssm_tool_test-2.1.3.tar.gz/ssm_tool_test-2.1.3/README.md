# Tool to get SSM parameter store (test)

This is a simple example package to get parameter store from aws account.
Using boto3 and credentials from aws.

### Definitions

- **get_parameter(name)**
    params:
    - name: The name of ssm parameter (string)
  
- **get_parameters(names)**
    params:
    - names: The names of ssm parameter (list)

- **get_describe_parameters(attributes)**
    params:
    - attributes: The name of ssm parameter (string)


### USAGE:
```
from ssm_tool_test import ssm

new_obj = ssm.ParameterStore()
new_obj.get_parameter("ssm_parameter")
new_obj.get_parameters(["param_1", "param_2"])
new_obj.get_describe_parameters([{'Key': 'Name'|'Type', 'Option': 'Equals', 'Values': ['string']}])
```

##### by jdroldan@playvox.com