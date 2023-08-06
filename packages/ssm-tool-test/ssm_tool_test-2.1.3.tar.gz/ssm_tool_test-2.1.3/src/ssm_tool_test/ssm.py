# Definitions of methods to get parameter store from aws
# Note: using aws credentials
import boto3
from botocore.exceptions import ClientError


SSM_CLIENT = boto3.client('ssm')

class ParameterStore():
    """
    Structure class of SSM parameter store

    Method availables: get_parameter, get_parameters
    """

    @staticmethod
    def get_parameter(name: str):
        try:
            ssm_parameter = SSM_CLIENT.get_parameter(
                Name=str(name),
                WithDecryption=True|False
            )
            return ssm_parameter['Parameter']
        except SSM_CLIENT.exceptions.ParameterNotFound as message:
            print(f"Error: {message}")

    @staticmethod
    def get_parameters(names: list):
        # Throw only a valid parameters
        try:
            ssm_parameters = SSM_CLIENT.get_parameters(
                Names=names,
                WithDecryption=True|False
            )
            return ssm_parameters['Parameters']
        except SSM_CLIENT.exceptions.InternalServerError as message:
            print(f"Error: {message}")

    @staticmethod
    def get_describe_parameters(attributes=None):
        """
        Method to get a filter parameters

        filters (list): Filters=[
            {
                'Key': 'Name'|'Type'|'KeyId',
                'Values': ['string'],
            }
        ]

        params (list): ParameterFilters=[
            {
                'Key': 'string',
                'Option': string',
                'Values': ['string'],
            }
        ]
        """
        try:
            filters, flag = ParameterStore.__set_attributes(attributes)
            if filters:
                if "params" == flag:
                    ssm_parameter = SSM_CLIENT.describe_parameters(
                        ParameterFilters=filters
                    )
                else:
                    ssm_parameter = SSM_CLIENT.describe_parameters(
                        Filters=filters
                    )
            else: 
                ssm_parameter = SSM_CLIENT.describe_parameters()
            return ssm_parameter['Parameters']
        
        except ClientError as e:
            print(e)
        except SSM_CLIENT.exceptions.InvalidFilterKey as message:
            print(f"Error: {message}")
        except SSM_CLIENT.exceptions.InvalidFilterValue as message:
            print(f"Error: {message}")

    def __set_attributes(attributes):
        if not attributes:
            # return all describe parameters
            return None, None
        if isinstance(attributes, list):
            filters = [attribute for attribute in attributes if 'Option' in attribute]
            if not filters:
                return attributes, None
            return filters, "params"
        return
    
    @staticmethod
    def get_parameters_by_path(path: str):
        try:
            ssm_paramters = SSM_CLIENT.get_parameters_by_path(
                Path=path,
                Recursive=True
            )
            return ssm_paramters['Parameters']
        except SSM_CLIENT.exceptions.InternalServerError as message:
            print(f"Error: {message}")
