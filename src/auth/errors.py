import enum


class UserErrors(str, enum.Enum):
    username_unique = "The username already exists!"
    unknown_user = "Unknown user!"
    incorrect_password = "Incorrect password!"
    unauthorized = "Unauthorized!"
    invalid_token = "Invalid token!"
    not_access_token = "Use access token!"
    not_refresh_token = "Use refresh token!"
