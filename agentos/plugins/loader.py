from __future__ import annotations
import importlib, logging
from pathlib import Path
from typing import Any
from agentos.core.config import Config

logger = logging.getLogger(__name__)

class PluginLoader:
    def __init__(self, config: Config) -> None:
        self.config = config
        self._plugins: dict[str, Any] = {}

    def load(self, path: Path) -> None:
        manifest = path / "manifest.json"
        if not manifest.exists():
            raise ValueError(f"No manifest at {manifest}")
        import json
        meta = json.loads(manifest.read_text())
        name = meta["name"]
        module = importlib.import_module(meta["entrypoint"])
        self._plugins[name] = module
        logger.info("Loaded plugin: %s v%s", name, meta.get("version", "?"))

    def get(self, name: str) -> Any:
        if name not in self._plugins:
            raise KeyError(f"Plugin not loaded: {name}")
        return self._plugins[name]

    @property
    def loaded(self) -> list[str]:
        return list(self._plugins.keys())
