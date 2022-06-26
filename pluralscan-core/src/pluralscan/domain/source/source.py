from dataclasses import dataclass

from pluralscan.domain.package.package_id import PackageId
from pluralscan.domain.source.source_id import SourceId
from pluralscan.domain.technology.language import Language


@dataclass
class Source:
    """Source"""

    source_id: SourceId
    package_id: PackageId
    name: str
    path: str
    langage: Language = Language.UNKNOWN
