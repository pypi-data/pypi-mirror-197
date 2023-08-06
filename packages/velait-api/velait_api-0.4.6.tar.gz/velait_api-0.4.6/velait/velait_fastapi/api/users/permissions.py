from typing import Iterable

from fastapi import Request

from velait.velait_fastapi.api.users.exceptions import NoPermissionError


class UserGroups:
    BUSINESS_ADMINS = "BusinessAdmins"
    BUSINESS_USERS = "BusinessUsers"
    REQUEST_MANAGERS = "OrgRequestsManagers"
    REQUEST_READERS = "OrgRequestsReaders"
    PLATFORM_ADMINS = "PlatformAdmins"
    PLATFORM_REQUEST_MANAGER = "PlatformRequestsManagers"
    PLATFORM_REQUESTS_READERS = "PlatformRequestsReaders"


class PermissionChecker:
    def __init__(self, permissions: Iterable[str]):
        self.permissions = set(permissions)

    def __call__(self, request: Request = None):
        if not set(request.user.permissions) & set(self.permissions):
            raise NoPermissionError()


__all__ = ['NoPermissionError', 'UserGroups', 'PermissionChecker']
