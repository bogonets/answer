# -*- coding: utf-8 -*-

from typing import Optional, List, Dict, Any
from docker.models.volumes import Volume
from recc.container.container_manager_interface import VolumeInfo
from recc.container.docker.mixin.docker_base import DockerBase


def _create_volume_info(volume: Volume) -> VolumeInfo:
    key = volume.id
    name = volume.name
    labels = volume.attrs["Labels"]
    if labels is None:
        labels = dict()
    # created_at = volume.attrs["CreatedAt"]
    # driver = volume.attrs["Driver"]
    # mount_point = volume.attrs["Mountpoint"]
    # options = volume.attrs["Options"]
    # scope = volume.attrs["Scope"]
    assert key is not None
    assert name is not None
    assert labels is not None
    return VolumeInfo(key, name, labels)


class DockerVolume(DockerBase):
    async def volumes(
        self, filters: Optional[Dict[str, Any]] = None, **kwargs
    ) -> List[VolumeInfo]:
        updated_kwargs = dict()
        updated_kwargs.update(kwargs)
        if filters:
            updated_kwargs["filters"] = filters
        volumes = self.docker.volumes.list(**updated_kwargs)
        return [_create_volume_info(v) for v in volumes]

    def _get_volume(self, key: str) -> Volume:
        return self.docker.volumes.get(key)

    async def exist_volume(self, key: str) -> bool:
        try:
            return self._get_volume(key) is not None
        except:  # noqa
            return False

    async def create_volume(self, name: str, **kwargs) -> VolumeInfo:
        volume = self.docker.volumes.create(name, **kwargs)
        return _create_volume_info(volume)

    async def remove_volume(self, key: str, force=False) -> None:
        self._get_volume(key).remove(force)
