from rest_framework import serializers
from .models import Group
from ..users.models import StudentProfile, TeacherProfile, MyUser, Theuser


class GroupOwnerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('group_owner',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ['group_member']


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('quote',)  # Добавьте другие поля, если необходимо


class StudentAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('profile_avatar',)

class TheuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Theuser
        fields = ['name']


class StudentAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('profile_avatar',)

class MyUserSerializer(serializers.ModelSerializer):
    quote = serializers.SerializerMethodField()
    profile_avatar = serializers.SerializerMethodField()
    name = serializers.CharField(source='theuser.name', read_only=True)

    class Meta:
        model = Theuser
        fields = ('id', 'name', 'quote', 'profile_avatar',)

    def get_quote(self, obj):
        try:
            student_profile = obj.theuser.student_profile
            return student_profile.quote
        except StudentProfile.DoesNotExist:
            return None

    def get_profile_avatar(self, obj):
        try:
            student_profile = obj.theuser.student_profile
            if student_profile.profile_avatar:  # Проверяем, существует ли файл
                return student_profile.profile_avatar.url
            else:
                return None
        except StudentProfile.DoesNotExist:
            return None






class GroupDetailSerializer(serializers.ModelSerializer):
    group_member = MyUserSerializer(many=True)

    class Meta:
        model = Group
        fields = "__all__"


class GroupRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["group_member"]

    def update(self, instance, validated_data):
        instance.team_member = validated_data.get('group_member', instance.team_member)
        instance.requester = self.context['requester']  # Устанавливаем пользователя
        instance.save()
        return instance
