from typing import Dict, Any

from fastapi import HTTPException, status

ACTIVITY_CONFLICT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='An activity is already in progress')

ACTIVITY_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='An activity with this id does not exist')

BAD_LOGIN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid username or password',
    headers={"WWW-Authenticate": "Bearer"})

BAD_STAT = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid stat")

BAD_TOKEN = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},)

INCORRECT_PASSWORD = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid current password")

NOT_OWNER = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User does not own activity with this id",
    headers={"WWW-Authenticate": "Bearer"})

USER_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='A user with this id does not exist')

USERNAME_CONFLICT = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='Username in use')

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
    ACTIVITY_401: Dict[str, Any] = {"description": "Unauthorized", "content": {
        "application/json": {
            "example": {
                "detail": "User does not own an activity with this id"}
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
    ACTIVITY_404: Dict[str, Any] = {"description": "Activity Not Found", "content": {
        "application/json": {
            "example": {
                "detail": "An activity with this id does not exist"}
        }}}
    USER_404: Dict[str, Any] = {"description": "User Not Found", "content": {
        "application/json": {
            "example": {
                "detail": "A user with this id does not exist"}
        }}}
    ACTIVITY_409: Dict[str, Any] = {"description": "Current Activity Conflict", "content": {
        "application/json": {
            "example": {
                "detail": "An activity is already in progress"}
        }}}
    USERNAME_409: Dict[str, Any] = {"description": "Username Conflict", "content": {
        "application/json": {
            "example": {
                "detail": "Username in use"}
        }}}
