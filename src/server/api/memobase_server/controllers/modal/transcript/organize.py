import asyncio
from collections import defaultdict
from .types import MergeAddResult, PROMPTS, AddProfile
from ....prompts.profile_init_utils import get_specific_subtopics
from ....prompts.utils import parse_string_into_subtopics, attribute_unify
from ....models.utils import Promise
from ....models.response import ProfileData
from ....env import CONFIG, LOG, ProfileConfig, ContanstTable
from ....llms import llm_complete


async def organize_profiles(
    project_id: str,
    profile_options: MergeAddResult,
    config: ProfileConfig,
) -> Promise[None]:
    profiles = profile_options["before_profiles"]
    USE_LANGUAGE = config.language or CONFIG.language
    STRICT_MODE = (
        config.profile_strict_mode
        if config.profile_strict_mode is not None
        else CONFIG.profile_strict_mode
    )
    if not STRICT_MODE:
        return Promise.resolve(None)

    # 获取所有主题和子主题
    topics = defaultdict(set)
    for p in profiles:
        topic = attribute_unify(p.attributes[ContanstTable.topic])
        sub_topic = attribute_unify(p.attributes[ContanstTable.sub_topic])
        topics[topic].add(sub_topic)

    # 检查是否有需要组织的主题
    need_organize = False
    for topic, sub_topics in topics.items():
        if len(sub_topics) > CONFIG.max_subtopics_per_topic:
            need_organize = True
            break

    if not need_organize:
        return Promise.resolve(None)

    # 构建配置文件提示
    profiles_prompt = ""
    for i, p in enumerate(profiles):
        profiles_prompt += f"[{i+1}] {p.attributes[ContanstTable.topic]}{CONFIG.llm_tab_separator}{p.attributes[ContanstTable.sub_topic]}{CONFIG.llm_tab_separator}{p.content}\n"

    # 调用LLM进行组织
    prompt = PROMPTS[USE_LANGUAGE]["organize"]
    p = await llm_complete(
        project_id,
        prompt.pack_input(profiles_prompt),
        system_prompt=prompt.get_prompt(),
        temperature=0.2,  # precise
        **prompt.get_kwargs(),
    )
    if not p.ok():
        return p
    organize_result = p.data()

    # 解析组织结果
    try:
        subtopics = parse_string_into_subtopics(organize_result)
        for st in subtopics:
            topic = st["topic"]
            sub_topic = st["sub_topic"]
            profiles_to_merge = []
            for p in profiles:
                if attribute_unify(p.attributes[ContanstTable.topic]) == attribute_unify(topic):
                    profiles_to_merge.append(p)
            if len(profiles_to_merge) > 0:
                # 将相同主题的配置文件合并到新的子主题中
                for p in profiles_to_merge:
                    profile_options["delete"].append(p.id)
                # 创建新的配置文件
                content = "\n".join([p.content for p in profiles_to_merge])
                profile_options["add"].append(
                    {
                        "content": content,
                        "attributes": {
                            ContanstTable.topic: topic,
                            ContanstTable.sub_topic: sub_topic,
                        },
                    }
                )
        return Promise.resolve(None)
    except Exception as e:
        LOG.error(f"Failed to parse organize result: {e}")
        return Promise.reject(CODE.SERVER_PARSE_ERROR, f"Failed to parse organize result: {e}")