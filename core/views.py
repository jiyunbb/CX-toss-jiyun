from django.http import JsonResponse
from django.views import View


class HealthAPI(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {
                "ok": True,
            }
        )
