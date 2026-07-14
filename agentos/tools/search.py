from __future__ import annotations
from agentos.tools.base import BaseTool, ToolResult

class SearchTool(BaseTool):
    name = "search"
    description = "Search the web and return ranked results with snippets"

    async def execute(self, query: str = "", num_results: int = 10) -> ToolResult:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get("https://api.search.example.com/v1",
                                     params={"q": query, "num": num_results})
                r.raise_for_status()
                data = r.json()
                return ToolResult(success=True, output=data.get("results", []),
                                  metadata={"query": query, "total": data.get("total", 0)})
        except Exception as exc:
            return ToolResult(success=False, output=None, error=str(exc))



