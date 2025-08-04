#rest ai uses to check wheter the user has the permision to do whatever thry want to do/change 
#we inheirt frpom django permission s that come wirh rest framework
from rest_framework import permissions
#permission module has all django permissions 

#ceate a new class callled upddate own profile and inherit from permissiom.BaseProfile
class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""
    #the permission class uses the has object permission method
    def has_object_permission(self,request,view,obj):
        """check user is trying to edit there own profile"""

        #we use the safe method list which is a safe non destructie http method that allows you to retriev data but not change or delete
        #we check it agaist the request method ,if it safe,we say true
        if request.method in permissions.SAFE_METHODS:
            return True#if method used is the safe permissions methods ,we return True
        #if they fail ,then they want to edit
        return obj.id == request.user.id
        #if object id is equal to authenticated id ,will return true and they will edit ,if not they will be denied 
#permissions
class PostOwnStatus(permissions.BasePermission):
    """Allow user to update their status"""
    def has_object_permission(self,request,view,obj):
        """checks the user is trying to update thheir own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

#go to views .py  and add the rest framework authentikation To get isauthenticated orReadOnly
class IsSuperUserOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow superusers to create/edit opportunities"""
    
    def has_permission(self, request, view):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed for superusers
        return request.user.is_authenticated and request.user.is_superuser