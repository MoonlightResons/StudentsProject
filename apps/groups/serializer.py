from rest_framework import serializers
from .models import Group


class GroupOwnerNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('group_owner',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ['group_member']


class GroupDetailSerializer(serializers.ModelSerializer):
    # team_owner = TeamOwnerNameSerializer(many=True)
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