from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from xhtml2pdf import pisa

from apps.certificates.serializers import CertificateSerializer
from apps.certificates.services import CertificateCreateService, CertificateListService, CertificateDetailService
from apps.certificates.validate_serializers import UserIdSerializer, CertificateRequestDataSerializer, \
    CertificateIdSerializer


class CertificateListCreateView(ListCreateAPIView):
    serializer_class = CertificateSerializer

    def __get_user_id(self):
        """
        header로 부터 가져온 유저 id 값 검증.
        """
        user_id: int = int(self.request.META.get('HTTP_USER_ID', 0))
        validator = UserIdSerializer(data={'user_id': user_id})
        validator.is_valid(raise_exception=True)
        user_id: int = validator.validated_data['user_id']
        return user_id

    def get_queryset(self):
        user_id = self.__get_user_id()
        result = CertificateListService(user_id=user_id).get_certificates()
        return result

    def post(self, request, *args, **kwargs):
        """
        송금확인증 등록 API
        """
        validator = CertificateRequestDataSerializer(data=request.data)
        validator.is_valid(raise_exception=True)
        CertificateCreateService(request_data=request.data).create_certificate()
        return Response(status=status.HTTP_201_CREATED)


class CertificateHTML(View):

    def __get_user_id(self):
        """
        header로 부터 가져온 유저 id 값 검증.
        """
        user_id: int = int(self.request.META.get('HTTP_USER_ID', 0))
        validator = UserIdSerializer(data={'user_id': user_id})
        validator.is_valid(raise_exception=True)
        user_id: int = validator.validated_data['user_id']
        return user_id

    def __get_certificate_id(self):
        """
        url parameter로 부터 가져온 송금확인증 id 값 검증.
        """
        validator = CertificateIdSerializer(data=self.kwargs)
        validator.is_valid(raise_exception=True)
        certificate_id: int = validator.validated_data['certificate_id']
        return certificate_id

    def get(self, request, *args, **kwargs):
        user_id = self.__get_user_id()
        certificate_id = self.__get_certificate_id()
        certificate = CertificateDetailService(user_id=user_id, certificate_id=certificate_id).get_certificate()
        serializer_data = CertificateSerializer(certificate).data

        html_template = 'certificate_list.html'
        context_data = {'certificate': serializer_data}

        output_type = self.request.GET.get('type')
        if not output_type:
            # type 쿼리 파라미터가 없는 경우
            return render(request, html_template, context_data)

        # TODO PDF로 만들었지만.. 한글깨짐을 해결하지 못했음.
        rendered_html = render_to_string(html_template, context_data)

        result = pisa.CreatePDF(rendered_html, encoding='utf-8', dest=BytesIO())
        response = HttpResponse(content_type='application/pdf')
        response.write(result.dest.getvalue())
        return response
