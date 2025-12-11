from rest_framework import serializers
from .models import Organization, Team
from apps.users.serializers import UserSerializer


class OrganizationListSerializer(serializers.ModelSerializer):
    total_members = serializers.IntegerField(read_only=True)
    total_teams = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'email', 'phone', 'website',
            'city', 'country', 'industry', 'size', 'owner_name',
            'total_members', 'total_teams', 'is_active', 'created_at'
        ]


class OrganizationDetailSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    administrators = UserSerializer(many=True, read_only=True)
    total_members = serializers.IntegerField(read_only=True)
    total_teams = serializers.IntegerField(read_only=True)

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'email', 'phone', 'website',
            'address', 'city', 'country', 'industry', 'size',
            'owner', 'administrators', 'total_members', 'total_teams',
            'is_active', 'created_at', 'updated_at'
        ]


class OrganizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'name', 'description', 'email', 'phone', 'website',
            'address', 'city', 'country', 'industry', 'size'
        ]

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class OrganizationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'name', 'description', 'email', 'phone', 'website',
            'address', 'city', 'country', 'industry', 'size', 'is_active'
        ]


class TeamListSerializer(serializers.ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    team_lead_name = serializers.CharField(source='team_lead.full_name', read_only=True, allow_null=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'organization', 'organization_name',
            'team_lead_name', 'department', 'project', 'member_count',
            'is_active', 'created_at'
        ]


class TeamDetailSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    team_lead = UserSerializer(read_only=True)
    organization = OrganizationListSerializer(read_only=True)
    member_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'organization', 'members',
            'team_lead', 'department', 'project', 'member_count',
            'is_active', 'created_at', 'updated_at'
        ]


class TeamCreateSerializer(serializers.ModelSerializer):
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Team
        fields = [
            'name', 'description', 'organization', 'team_lead',
            'department', 'project', 'member_ids'
        ]

    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        team = Team.objects.create(**validated_data)
        if member_ids:
            team.members.set(member_ids)
        return team


class TeamUpdateSerializer(serializers.ModelSerializer):
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Team
        fields = [
            'name', 'description', 'team_lead', 'department',
            'project', 'is_active', 'member_ids'
        ]

    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if member_ids is not None:
            instance.members.set(member_ids)
        return instance
