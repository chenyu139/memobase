import asyncio
from ....models.utils import Promise
from ....env import CONFIG, LOG
from ....utils import get_blob_str, get_encoded_tokens, truncate_string
from ....llms import llm_complete
from ....prompts import (
    summary_profile,
)
from .types import UpdateProfile, AddProfile


async def re_summary(
    project_id: str,
    add_profile: list[AddProfile],
    update_profile: list[UpdateProfile],
) -> Promise[None]:
    add_tasks = [summary_memo(project_id, ap) for ap in add_profile]
    await asyncio.gather(*add_tasks)
    update_tasks = [summary_memo(project_id, up) for up in update_profile]
    ps = await asyncio.gather(*update_tasks)
    return Promise.resolve(None)


async def summary_memo(project_id: str, profile: AddProfile | UpdateProfile) -> Promise[None]:
    content = profile["content"]
    # 检查内容长度，如果太长则需要汇总
    tokens = get_encoded_tokens(content)
    if tokens < CONFIG.max_profile_tokens:
        return Promise.resolve(None)

    # 调用LLM进行汇总
    p = await llm_complete(
        project_id,
        summary_profile.pack_input(content),
        system_prompt=summary_profile.get_prompt(),
        temperature=0.2,  # precise
        **summary_profile.get_kwargs(),
    )
    if not p.ok():
        LOG.error(f"Failed to summary profile: {p.msg()}")
        return Promise.resolve(None)
    summary = p.data()

    # 更新配置文件内容
    profile["content"] = summary
    return Promise.resolve(None)