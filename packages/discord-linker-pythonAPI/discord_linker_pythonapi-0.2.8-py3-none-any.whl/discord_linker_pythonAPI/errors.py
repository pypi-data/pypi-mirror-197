from typing import Optional


ALL_EXCEPTIONS = {} # NAME: CLASS REFERENCE
"""Holds all the exceptions of the API.


This variable is a dictionary where the following is True:

* key => Name of exception
* value => Reference to the exception's class
"""




class WP_Error(Exception):
    """Represents an API (wordpress) error.

    Args:
        details (Optional[dict]): The details to store to the object.
        default_code (Optional[str]): The default error code of the exception. Defaults to "UNKNOWN_ERROR".
        default_message (str, optional): The default error message of the exception. Defaults to "An unknown error occurred!".
    """
    def __init__(self, details:Optional[dict] = None, *args, default_code = "UNKNOWN_ERROR", default_message = "An unknown error occurred!", **kwargs):
        self.code = default_code
        self.message = default_message
        self.data = {}

        if details is not None:
            if "code" in details: self.code = details["code"]
            if "message" in details: self.message = details["message"]
            if "data" in details: self.data = details["data"]
            super().__init__('\n'.join(['{k}: {v}'.format(k=k, v=v) for k,v in details.items()]), *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)


    @staticmethod
    def sanitize_kwargs(kwargs:dict):
        """Remove some keyword-only parameters from the kwargs dictionary.
        Easy cleaning for child exception parameters.

        Args:
            kwargs (dict): The dictionary to sanitize.
        """

        if "default_code" in kwargs:
            kwargs.pop("default_code")
        
        if "default_message" in kwargs:
            kwargs.pop("default_message")




class UNKNOWN_ERROR(WP_Error):
    """Represents an unknown error.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(details, *args, **kwargs)
ALL_EXCEPTIONS["UNKNOWN_ERROR"] = UNKNOWN_ERROR



class LINK_TOKEN_NOT_FOUND(WP_Error):
    """Represents an error where the token was not found.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "LINK_TOKEN_NOT_FOUND",
            default_message = "Link token was not found!",
            **kwargs)
ALL_EXCEPTIONS["LINK_TOKEN_NOT_FOUND"] = LINK_TOKEN_NOT_FOUND


class ACCOUNT_NOT_LINKED(WP_Error):
    """Represents an error where the account was not linked.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "ACCOUNT_NOT_LINKED",
            default_message = "This discord is not linked to an account!",
            **kwargs)
ALL_EXCEPTIONS["ACCOUNT_NOT_LINKED"] = ACCOUNT_NOT_LINKED


class INVALID_TOKEN_SIZE(WP_Error):
    """Represents an error where the token size was not correct.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "INVALID_TOKEN_SIZE",
            default_message = "Wrong link token size!",
            **kwargs)
ALL_EXCEPTIONS["INVALID_TOKEN_SIZE"] = INVALID_TOKEN_SIZE


class INVALID_DISCORD_ID_TYPE(WP_Error):
    """Represents an error where the discord ID type was incorrect.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "INVALID_DISCORD_ID_TYPE",
            default_message = "Discord ID must be an integer!",
            **kwargs)
ALL_EXCEPTIONS["INVALID_DISCORD_ID_TYPE"] = INVALID_DISCORD_ID_TYPE


class INVALID_DISCORD_ID_SIZE(WP_Error):
    """Represents an error where the discord ID length was incorrect.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "INVALID_DISCORD_ID_SIZE",
            default_message = "Discord ID must be an 18-digit integer",
            **kwargs)
ALL_EXCEPTIONS["INVALID_DISCORD_ID_SIZE"] = INVALID_DISCORD_ID_SIZE



class ACCOUNT_ALREADY_LINKED(WP_Error):
    """Represents an error where the account is already linked.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "ACCOUNT_ALREADY_LINKED",
            default_message = "The discord or the account is already linked!",
            **kwargs)
ALL_EXCEPTIONS["ACCOUNT_ALREADY_LINKED"] = ACCOUNT_ALREADY_LINKED


class INSUFFICIENT_PERMISSIONS(WP_Error):
    """Represents an error where the user has insufficient permissions.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "INSUFFICIENT_PERMISSIONS",
            default_message = "You don't have enough permissions to perform this action",
            **kwargs)
ALL_EXCEPTIONS["INSUFFICIENT_PERMISSIONS"] = INSUFFICIENT_PERMISSIONS


class NOT_IMPERSONATING(WP_Error):
    """Represents an error where the user is not impersonating anyone.

    NOTE: This exception should not be thrown, but it's here since it exists.

    Args:
        details (dict): The details of the exception.
    """
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "NOT_IMPERSONATING",
            default_message = "You are not impersonating anyone!",
            **kwargs)
ALL_EXCEPTIONS["NOT_IMPERSONATING"] = NOT_IMPERSONATING








#################### DLXEDD Errors ####################

class INCORRECT_PRODUCT_ID_TYPE(WP_Error):
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "INCORRECT_PRODUCT_ID_TYPE",
            default_message = "Product ID must be integer!",
            **kwargs)
ALL_EXCEPTIONS["INCORRECT_PRODUCT_ID_TYPE"] = INCORRECT_PRODUCT_ID_TYPE




class PRODUCT_NOT_FOUND(WP_Error):
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "PRODUCT_NOT_FOUND",
            default_message = "There are no products with this ID!",
            **kwargs)
ALL_EXCEPTIONS["PRODUCT_NOT_FOUND"] = PRODUCT_NOT_FOUND


class PRODUCT_NOT_IN_CART(WP_Error):
    def __init__(self, details:dict, *args, **kwargs):
        WP_Error.sanitize_kwargs(kwargs)

        super().__init__(
            details,
            *args,
            default_code = "PRODUCT_NOT_IN_CART",
            default_message = "Your cart doesn't contain a product with this ID!",
            **kwargs)
ALL_EXCEPTIONS["PRODUCT_NOT_IN_CART"] = PRODUCT_NOT_IN_CART















def get_exception(details:dict, *args, **kwargs):
    if 'code' in details:
        if details['code'] in ALL_EXCEPTIONS:
            return ALL_EXCEPTIONS[details["code"]](details, *args, **kwargs)
        elif details['code'] == 'rest_invalid_param':
            if 'details' in details['data']:
                error_json = list(details['data']['details'].values())[0]
                return ALL_EXCEPTIONS[error_json['code']](error_json, *args, **kwargs)
    return UNKNOWN_ERROR(details, *args, **kwargs)