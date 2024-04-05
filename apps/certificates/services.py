from django.db import transaction
from django.db.models import Prefetch

from apps.certificates.models import Certificate, Transfer, CertificateTransferMap


class CertificateCreateService:
    def __init__(self, request_data):
        self.request_data = request_data
        self.transfer_ids = self.__get_transfer_ids()
        self.user_id = self.__validate_user()

    def __validate_user(self):
        """
        유저애 연결되지 않은 송금번호 조회를 체크하기 위한 함수
        """
        user = self.request_data.get('user')

        is_users_tranfer = Transfer.objects.filter(user_id=user['id']).exists()
        if not is_users_tranfer:
            raise PermissionError("유저와 관련없는 않은 송금 아이디 조회 발견")

        return user['id']

    def __get_transfer_ids(self):
        """
        T0001, T0002 같은 송금 ID의 prefix인 T000을 제거하여 1,2 로 만드는 함수
        """
        modified_list = [int(item.replace("T000", "")) for item in self.request_data['transfers'] if
                         item.startswith("T000")]
        return modified_list

    @transaction.atomic
    def create_certificate(self):
        transfer_ids = Transfer.objects.filter(pk__in=self.transfer_ids).values_list('pk', flat=True)
        certificate = Certificate.objects.create(user_id=self.user_id)
        certi_trans_maps = [CertificateTransferMap(certificate_id=certificate.pk, transfer_id=transfer_id) for
                            transfer_id in transfer_ids]

        CertificateTransferMap.objects.bulk_create(certi_trans_maps)


class CertificateListService:
    """
    송금확인증 목록 조회 서비스
    """

    def __init__(self, user_id):
        self.user_id = user_id

    def get_certificates(self):
        return Certificate.objects.filter(user_id=self.user_id).select_related("user").prefetch_related(
            Prefetch(
                lookup='certificate_transfers_maps',
                queryset=CertificateTransferMap.objects.only("transfer_id", "certificate_id"),
                to_attr='certificate_transfer_map_info'
            )
        ).only("user_id", "user__name", "status")


class CertificateDetailService:
    """
    송금확인증 상세 조회 서비스
    """

    def __init__(self, user_id, certificate_id):
        self.user_id = user_id
        self.certificate_id = certificate_id

    def get_certificate(self):
        return Certificate.objects.filter(pk=self.certificate_id, user_id=self.user_id).select_related(
            "user").prefetch_related(
            Prefetch(
                lookup='certificate_transfers_maps',
                queryset=CertificateTransferMap.objects.only("transfer_id", "certificate_id"),
                to_attr='certificate_transfer_map_info'
            )
        ).only("user_id", "user__name", "status").first()
