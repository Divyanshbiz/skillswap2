from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models.Member import Member  # Import Member model

class MemberBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            member = Member.objects.get(username=username)
            if check_password(password, member.password):
                return member
        except Member.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Member.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None