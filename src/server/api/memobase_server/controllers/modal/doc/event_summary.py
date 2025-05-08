import asyncio
from ....env import CONFIG, LOG
from ....models.utils import Promise
from ....models.response import EventTag
from ....llms import llm_complete
from ....prompts.profile_init_utils import read_out_event_tags
from ...event import append_user_event
from ...project import get_project_profile_config
from .types import PROMPTS


async def tag_event(
    user_id: str,
    project_id: str,
    user_memo: str,
    delta_profile_data: list[dict],
    config,
) -> Promise[str]:
    p = await get_project_profile_config(project_id)
    if not p.ok():
        return p
    project_profiles = p.data()
    USE_LANGUAGE = project_profiles.language or CONFIG.language
    event_tags = read_out_event_tags(project_profiles)
    if len(event_tags) == 0:
        # 如果没有事件标签，则直接创建事件
        p = await append_user_event(
            user_id,
            project_id,
            user_memo,
            delta_profile_data,
            None,
            None,
        )
        if not p.ok():
            return p
        return Promise.resolve(p.data())

    # 构建事件标签提示
    event_tags_prompt = "\n".join([f"- {et.name}({et.description})" for et in event_tags])

    # 调用LLM进行事件标签
    prompt = PROMPTS[USE_LANGUAGE]["event_summary"]
    p = await llm_complete(
        project_id,
        prompt.pack_input(user_memo, event_tags_prompt),
        system_prompt=prompt.get_prompt(),
        temperature=0.2,  # precise
        **prompt.get_kwargs(),
    )
    if not p.ok():
        # 如果标签失败，则直接创建事件
        p = await append_user_event(
            user_id,
            project_id,
            user_memo,
            delta_profile_data,
            None,
            None,
        )
        if not p.ok():
            return p
        return Promise.resolve(p.data())

    # 解析事件标签
    try:
        event_summary = p.data()
        event_tip = None
        event_tags_list = []

        # 提取事件提示和标签
        lines = event_summary.strip().split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("Event Tip:"):
                event_tip = line[len("Event Tip:"):].strip()
            elif line.startswith("Event Tags:"):
                tags_str = line[len("Event Tags:"):].strip()
                for tag_str in tags_str.split(","):
                    tag_parts = tag_str.strip().split("=")
                    if len(tag_parts) == 2:
                        event_tags_list.append(
                            EventTag(tag=tag_parts[0].strip(), value=tag_parts[1].strip())
                        )

        # 创建事件
        p = await append_user_event(
            user_id,
            project_id,
            user_memo,
            delta_profile_data,
            event_tip,
            event_tags_list,
        )
        if not p.ok():
            return p
        return Promise.resolve(p.data())
    except Exception as e:
        LOG.error(f"Failed to parse event summary: {e}")
        # 如果解析失败，则直接创建事件
        p = await append_user_event(
            user_id,
            project_id,
            user_memo,
            delta_profile_data,
            None,
            None,
        )
        if not p.ok():
            return p
        return Promise.resolve(p.data())