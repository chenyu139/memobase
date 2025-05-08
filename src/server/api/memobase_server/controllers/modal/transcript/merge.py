import asyncio
from ....env import CONFIG, LOG
from ....models.utils import Promise, CODE
from ....models.response import ProfileData
from ....env import ProfileConfig, ContanstTable
from ....llms import llm_complete
from ....prompts.utils import (
    parse_string_into_merge_action,
)
from ....prompts.profile_init_utils import UserProfileTopic
from ....types import SubTopic
from .types import UpdateResponse, PROMPTS, AddProfile, UpdateProfile, MergeAddResult


async def merge_or_valid_new_memos(
    project_id: str,
    fact_contents: list[str],
    fact_attributes: list[dict],
    profiles: list[ProfileData],
    config: ProfileConfig,
    total_profiles: list[UserProfileTopic],
) -> Promise[MergeAddResult]:
    # 如果没有配置文件，则直接添加所有事实
    if len(profiles) == 0:
        add_profiles = []
        for fc in fact_contents:
            add_profiles.append(
                {
                    "content": fc["memo"],
                    "attributes": {
                        ContanstTable.topic: fc[ContanstTable.topic],
                        ContanstTable.sub_topic: fc[ContanstTable.sub_topic],
                    },
                }
            )
        return Promise.resolve(
            {
                "add": add_profiles,
                "update": [],
                "delete": [],
                "before_profiles": profiles,
                "update_delta": [],
            }
        )

    # 如果有配置文件，则需要合并
    USE_LANGUAGE = config.language or CONFIG.language
    prompt = PROMPTS[USE_LANGUAGE]["merge"]

    # 构建现有配置文件的提示
    existing_profiles_prompt = ""
    for i, p in enumerate(profiles):
        existing_profiles_prompt += f"[{i+1}] {p.attributes[ContanstTable.topic]}{CONFIG.llm_tab_separator}{p.attributes[ContanstTable.sub_topic]}{CONFIG.llm_tab_separator}{p.content}\n"

    # 构建新事实的提示
    new_facts_prompt = ""
    for i, fc in enumerate(fact_contents):
        new_facts_prompt += f"[{i+1}] {fc[ContanstTable.topic]}{CONFIG.llm_tab_separator}{fc[ContanstTable.sub_topic]}{CONFIG.llm_tab_separator}{fc['memo']}\n"

    # 调用LLM进行合并
    p = await llm_complete(
        project_id,
        prompt.pack_input(existing_profiles_prompt, new_facts_prompt),
        system_prompt=prompt.get_prompt(),
        temperature=0.2,  # precise
        **prompt.get_kwargs(),
    )
    if not p.ok():
        return p
    merge_result = p.data()

    # 解析合并结果
    try:
        merge_actions = parse_string_into_merge_action(merge_result)
        add_profiles = []
        update_profiles = []
        delete_profiles = []
        update_delta_profiles = []

        # 处理合并操作
        for ma in merge_actions:
            action = ma["action"]
            if action == "add":
                # 添加新配置文件
                topic, sub_topic = ma["memo"].split(CONFIG.llm_tab_separator, 1)
                content = ""
                for fc in fact_contents:
                    if (
                        fc[ContanstTable.topic] == topic
                        and fc[ContanstTable.sub_topic] == sub_topic
                    ):
                        content = fc["memo"]
                        break
                if content:
                    add_profiles.append(
                        {
                            "content": content,
                            "attributes": {
                                ContanstTable.topic: topic,
                                ContanstTable.sub_topic: sub_topic,
                            },
                        }
                    )
                    update_delta_profiles.append(
                        {
                            "content": content,
                            "attributes": {
                                ContanstTable.topic: topic,
                                ContanstTable.sub_topic: sub_topic,
                            },
                        }
                    )
            elif action == "update":
                # 更新现有配置文件
                profile_idx = int(ma["memo"].split("[", 1)[1].split("]", 1)[0]) - 1
                if 0 <= profile_idx < len(profiles):
                    profile = profiles[profile_idx]
                    for fc in fact_contents:
                        if (
                            fc[ContanstTable.topic]
                            == profile.attributes[ContanstTable.topic]
                            and fc[ContanstTable.sub_topic]
                            == profile.attributes[ContanstTable.sub_topic]
                        ):
                            update_profiles.append(
                                {
                                    "profile_id": profile.id,
                                    "content": fc["memo"],
                                    "attributes": profile.attributes,
                                }
                            )
                            update_delta_profiles.append(
                                {
                                    "content": fc["memo"],
                                    "attributes": profile.attributes,
                                }
                            )
                            break
            elif action == "delete":
                # 删除配置文件
                profile_idx = int(ma["memo"].split("[", 1)[1].split("]", 1)[0]) - 1
                if 0 <= profile_idx < len(profiles):
                    delete_profiles.append(profiles[profile_idx].id)

        return Promise.resolve(
            {
                "add": add_profiles,
                "update": update_profiles,
                "delete": delete_profiles,
                "before_profiles": profiles,
                "update_delta": update_delta_profiles,
            }
        )
    except Exception as e:
        LOG.error(f"Failed to parse merge result: {e}")
        return Promise.reject(CODE.SERVER_PARSE_ERROR, f"Failed to parse merge result: {e}")