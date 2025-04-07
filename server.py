
import uvicorn
from fastapi import FastAPI
from fastapi_mcp import add_mcp_server
from fastapi.responses import RedirectResponse

from routers.web import web_search
from routers.wiki import wiki_search
from routers.arxiv import arxiv_search

app = FastAPI()


# @app.get("/")
# def root():
#     return RedirectResponse("/docs")


app.include_router(web_search)
app.include_router(wiki_search)
app.include_router(arxiv_search)

mcp_server = add_mcp_server(
    app,
    mount_path="/mcp",
    name="My API MCP",
    describe_all_responses=True,
    describe_full_response_schema=True
    )

@mcp_server.tool()
async def get_server_time() -> str:
    from datetime import datetime
    return {"server_time": str(datetime.now().isoformat())}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True, workers=2)
