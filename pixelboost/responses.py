from typing import Dict, Any

class Responses:
    PASSWORD_400: Dict[str, Any] = {"description": "Invalid Password", "content": {
        "application/json": {
            "example": {
                "detail": "Invalid current_password"}
        }}}
    STAT_400: Dict[str, Any] = {"description": "Invalid Stat", "content": {
        "application/json": {
            "example": {
                "detail": "Invalid stat"}
        }}}
    LOGIN_401: Dict[str, Any] = {"description": "Invalid Credentials", "content": {
        "application/json": {
            "example": {
                "detail": "Invalid username or password"}
        }}}
    TOKEN_401: Dict[str, Any] = {"description": "Invalid Token", "content": {
        "application/json": {
            "example": {
                "detail": "Could not validate credentials"}
        }}}
    USER_404: Dict[str, Any] = {"description": "User Not Found", "content": {
        "application/json": {
            "example": {
                "detail": "A user with this id does not exist"}
        }}}
    USERNAME_409: Dict[str, Any] = {"description": "Username Conflict", "content": {
        "application/json": {
            "example": {
                "detail": "Username in use"}
        }}}
