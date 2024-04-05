from django.db import models
from django.db.models import TextChoices


class User(models.Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '유저'
        app_label = 'certificates'
        db_table = 'user'


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id', related_name='transfers')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '송금내역'
        app_label = 'certificates'
        db_table = 'transfer'


class Certificate(models.Model):
    class STATUS_TYPE(TextChoices):
        CREATED = 'CREATED', '생성됨'
        DOWNLOADED = 'DOWNLOADED', '다운로드됨'

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='user_id', related_name='certificates')
    status = models.TextField(choices=STATUS_TYPE.choices, default=STATUS_TYPE.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '송금확인증'
        app_label = 'certificates'
        db_table = 'certificate'


class CertificateTransferMap(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.DO_NOTHING, db_column='certificate_id',
                                    related_name='certificate_transfers_maps')
    transfer = models.ForeignKey(Transfer, on_delete=models.DO_NOTHING, db_column='transfer_id',
                                 related_name='certificate_transfers_maps')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '송금 확인증 매핑 테이블'
        app_label = 'certificates'
        db_table = 'certificate_transfer_map'
