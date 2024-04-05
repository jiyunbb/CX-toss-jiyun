from rest_framework import serializers

from apps.certificates.models import Certificate


class UserIdSerializer(serializers.Serializer):
    """
    유저 아이디 검증 from header
    """
    user_id = serializers.IntegerField(min_value=1)


class UserInfoSerializer(serializers.Serializer):
    """
    유저 정보 검증
    """
    id = serializers.IntegerField(min_value=1)
    name = serializers.CharField(max_length=20)


class CertificateIdSerializer(serializers.Serializer):
    """
    송금확인증 아이디 검증
    """
    certificate_id = serializers.IntegerField(min_value=1)


class CertificateRequestDataSerializer(serializers.Serializer):
    """
    유저 입력 요청 데이터 검증
    """
    user = UserInfoSerializer()
    status = serializers.ChoiceField(choices=Certificate.STATUS_TYPE.choices)
    transfers = serializers.ListField(child=serializers.CharField())

    def validate_transfers(self, value):
        # 리스트가 비어있는지 확인
        if not value:
            raise serializers.ValidationError("Transfers list is empty")

        # 각 항목이 "T000"으로 시작하는지 확인
        for item in value:
            if not item.startswith("T000"):
                raise serializers.ValidationError("'T000'로 ID 값이 시작되어야 합니다.")

        return value
