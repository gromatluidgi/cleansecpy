import re
from pluralscan.application.usecases.packages.get_package_list import GetPackageListQuery

import rest_framework.status as status
from pluralscan.application.processors.fetchers.package_fetcher import \
    AbstractPackageFetcher

from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .factories import list_packages_use_case
from .serializers import PackageSerializer


class PackageViewSet(ListModelMixin, GenericViewSet):
    """AnalyzersView"""

    permission_classes = [AllowAny]
    serializer_class = PackageSerializer

    def get_queryset(self):
        """get_queryset"""
        command = GetPackageListQuery()
        result = list_packages_use_case().handle(command)
        return result.packages

    # @action(
    #     detail=False,
    #     methods=["get"],
    #     url_path=r"remote/(?P<url>[-_a-zA-Z0-9.:/?]+)",
    #     url_name="remote",
    # )
    # def remote_package_info(self, _: Request, url=None):
    #     """remote_package_info"""
    #     try:
    #         command = GetRemotePackageInfoCommand(url)
    #         package_fetcher = self._get_package_fetcher(url)
    #         result = get_remote_package_info_use_case(package_fetcher).handle(command)
    #         serializer: PackageSerializer = self.get_serializer(result)
    #         return Response(serializer.data)
    #     except RuntimeError:
    #         return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # def _get_package_fetcher(self, uri: str) -> AbstractPackageFetcher:
    #     github_re = re.compile(
    #         r"(http(s)?)(:(//)?)(github.com/)([a-zA-Z0-9.]*)(/)([a-zA-Z0-9.]*)(/)?"
    #     )
    #     gitlab_re = re.compile(
    #         r"(http(s)?)(:(//)?)(gitlab.com/)([a-zA-Z0-9.]*)(/)([a-zA-Z0-9.]*)(/)?"
    #     )

    #     if github_re.match(uri):
    #         return GithubPackageFetcher()

    #     if gitlab_re.match(uri):
    #         return GitlabPackageFetcher()

    #     raise RuntimeError()
