import pytest, asyncio
from agentos.core.config import Config
from agentos.tools.filesystem import FilesystemTool
from pathlib import Path
import tempfile

@pytest.fixture
def fs_tool(tmp_path):
    return FilesystemTool(Config(), workspace=tmp_path)

@pytest.mark.asyncio
async def test_write_and_read(fs_tool):
    r = await fs_tool.run(action="write", path="test.txt", content="hello world")
    assert r.success
    r2 = await fs_tool.run(action="read", path="test.txt")
    assert r2.success
    assert r2.output == "hello world"

@pytest.mark.asyncio
async def test_path_traversal_blocked(fs_tool):
    r = await fs_tool.run(action="read", path="../../etc/passwd")
    assert not r.success

@pytest.mark.asyncio
async def test_list_directory(fs_tool, tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    r = await fs_tool.run(action="list", path=".")
    assert r.success
    assert len(r.output) >= 2
