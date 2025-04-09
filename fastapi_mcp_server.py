
import uvicorn
from fastapi import FastAPI
from fastapi_mcp import add_mcp_server
from fastapi.responses import RedirectResponse

from routers.web import web_search
from routers.wiki import wiki_search
from routers.arxiv import arxiv_search

app = FastAPI()

app.include_router(web_search)
app.include_router(wiki_search)
app.include_router(arxiv_search)


#### MCP Adaptor #######
# 라우터 안에 있는 API들을 묶는 방식
mcp_server = add_mcp_server(
    app,
    mount_path="/mcp",
    name="My API MCP",
    describe_all_responses=True,
    describe_full_response_schema=True
    )   # 라우터 안에 있는 API들을 묶는 방식

# 개별적으로 다이렉트로 붙이는 방식
@mcp_server.tool()   
async def get_server_time() -> str:
    from datetime import datetime
    return {"server_time": str(datetime.now().isoformat())}

# 라우터로 묶든.. 개별적으로 추가든.. 최종적으로 MCP TOOL은 묶어서 제공된다.
# 자연스럽게.. 언어모델이 알아서 선택하는 방식으로 귀결되는데... 이게 효용이 있을지...

#### MCP Adaptor #######

if __name__ == "__main__":
    uvicorn.run("fastapi_mcp_server:app", host="0.0.0.0", port=8000, reload=True, workers=2)
