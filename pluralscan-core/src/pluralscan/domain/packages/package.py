from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List, Optional

from pluralscan.domain.packages.package_id import PackageId
from pluralscan.domain.packages.package_registry import PackageRegistry
from pluralscan.domain.projects.project_id import ProjectId
from pluralscan.domain.technologies.technology import Technology


@dataclass
class Package:
    """Package entity."""

    package_id: PackageId
    name: str
    version: str
    registry: PackageRegistry
    storage_path: str
    published_at: datetime
    project_id: Optional[ProjectId] = None
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    technologies: List[Technology] = field(default_factory=list)
    links: List[tuple[str, str]] = field(default_factory=list)

    def to_dict(self):
        """Transform entity object into dictonary representation."""
        return {
            "id": repr(self.package_id),
            "name": self.name,
            "version": self.version,
            "registry": self.registry.name,
            "storage_path": self.storage_path,
            "published_at": self.published_at,
            "project_id": repr(self.project_id),
            "description": self.description,
            "created_at": self.created_at,
            "technologies": [asdict(x) for x in self.technologies],
        }
