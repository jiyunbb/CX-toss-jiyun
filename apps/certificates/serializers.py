from rest_framework import serializers

from apps.certificates.models import User, Certificate, Transfer


class UserSerializer(serializers.ModelSerializer):
    """
    유저 상세 조회
    """
    id = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = User
        fields = ('id', 'name')


class TransferIDSerializer(serializers.ModelSerializer):
    """
    송금 아이디 리스트
    """
    id = serializers.IntegerField()

    class Meta:
        model = Transfer
        fields = ('id',)


class CertificateSerializer(serializers.ModelSerializer):
    """
    송금확인증 목록 조회
    """
    id = serializers.IntegerField()
    user = UserSerializer()
    status = serializers.CharField()
    transfers = TransferIDSerializer(many=True, source="certificate_transfer_map_info")

    def to_representation(self, instance):
        data = super(CertificateSerializer, self).to_representation(instance)
        data['transfers'] = [f"T000{item['id']}" for item in data['transfers']]
        return data

    class Meta:
        model = Certificate
        fields = ('id', 'user', 'status', "transfers")
