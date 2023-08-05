from django.shortcuts import render
from credential.form_builder.builder import builder
from credential.models import CredentialType, Credential
from django.http import JsonResponse
import json
from rest_framework.viewsets import ViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from .serializers import CredentialRenderedFormResponseSerializer


class CredentialsView(ViewSet):
    @swagger_auto_schema(
        method="get",
        manual_parameters=[
            openapi.Parameter(
                "credential_type_id",
                openapi.IN_QUERY,
                description="",
                type=openapi.TYPE_NUMBER,
            ),
            openapi.Parameter(
                "object_id",
                openapi.IN_QUERY,
                description="This is the credential id",
                type=openapi.TYPE_NUMBER,
            ),
        ],
        responses={200: openapi.Response("", CredentialRenderedFormResponseSerializer)},
    )
    @action(detail=False, methods=["get"])
    def get_new_form_rendered(self, request):
        credential_type_id = request.GET.get("credential_type_id")
        object_id = request.GET.get("object_id")

        if not object_id:
            return JsonResponse(
                {
                    "form": render(
                        request,
                        "render_form.html",
                        {
                            "form": builder(
                                CredentialType.objects.get(id=credential_type_id).schema
                            )()
                        },
                    )
                    .serialize()
                    .decode("utf-8")
                }
            )

        credetial: Credential = Credential.objects.get(id=int(object_id))
        form = builder(credetial.credential_type.schema)(
            data={"credential": json.dumps(json.loads(credetial.credential["value"]), indent=4)}
        )
        return JsonResponse(
            {
                "form": render(request, "render_form.html", {"form": form})
                .serialize()
                .decode("utf-8")
            }
        )
