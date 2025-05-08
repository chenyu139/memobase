import asyncio

from ....env import LOG, ProfileConfig
from ....models.blob import Blob
from ....models.utils import Promise
from ....models.response import IdsData, ChatModalResponse
from ...profile import add_user_profiles, update_user_profiles, delete_user_profiles
from ...event import append_user_event
from ..chat.extract import extract_topics
from ..chat.merge import merge_or_valid_new_memos
from ..chat.summary import re_summary
from ..chat.organize import organize_profiles
from ..chat.types import MergeAddResult
from ..chat.event_summary import tag_event
from ..chat.entry_summary import entry_summary


async def process_blobs(
    user_id: str, project_id: str, blob_ids: list[str], blobs: list[Blob]
) -> Promise[ChatModalResponse]:
    # 将DocBlob内容转换为用户备忘录字符串
    user_memo_str = "\n".join([blob.content for blob in blobs])
    
    # 1. 提取补丁配置文件
    p = await extract_topics(user_id, project_id, user_memo_str)
    if not p.ok():
        return p
    extracted_data = p.data()

    # 2. 将其合并到整个配置文件中
    p = await merge_or_valid_new_memos(
        project_id,
        fact_contents=extracted_data["fact_contents"],
        fact_attributes=extracted_data["fact_attributes"],
        profiles=extracted_data["profiles"],
        config=extracted_data["config"],
        total_profiles=extracted_data["total_profiles"],
    )
    if not p.ok():
        return p

    profile_options = p.data()
    delta_profile_data = [
        p for p in (profile_options["add"] + profile_options["update_delta"])
    ]
    p = await handle_session_event(
        user_id,
        project_id,
        user_memo_str,
        delta_profile_data,
        extracted_data["config"],
    )
    if not p.ok():
        return p
    eid = p.data()

    # 3. 检查是否需要组织配置文件
    p = await organize_profiles(
        project_id,
        profile_options,
        config=extracted_data["config"],
    )
    if not p.ok():
        LOG.error(f"Failed to organize profiles: {p.msg()}")

    # 4. 如果任何槽太大，则重新汇总配置文件
    p = await re_summary(
        project_id,
        add_profile=profile_options["add"],
        update_profile=profile_options["update"],
    )
    if not p.ok():
        LOG.error(f"Failed to re-summary profiles: {p.msg()}")

    # 数据库提交
    p = await exe_user_profile_add(user_id, project_id, profile_options)
    if not p.ok():
        return p
    add_profile_ids = p.data().ids
    p = await exe_user_profile_update(user_id, project_id, profile_options)
    if not p.ok():
        return p
    update_profile_ids = p.data().ids
    p = await exe_user_profile_delete(user_id, project_id, profile_options)
    if not p.ok():
        return p
    delete_profile_ids = p.data().ids
    return Promise.resolve(
        ChatModalResponse(
            event_id=eid,
            add_profiles=add_profile_ids,
            update_profiles=update_profile_ids,
            delete_profiles=delete_profile_ids,
        )
    )


async def handle_session_event(
    user_id: str,
    project_id: str,
    user_memo: str,
    delta_profile_data: list,
    config: ProfileConfig,
) -> Promise[str]:
    p = await tag_event(user_id, project_id, user_memo, delta_profile_data, config)
    if not p.ok():
        return p
    event_data = p.data()
    p = await append_user_event(user_id, project_id, event_data)
    if not p.ok():
        return p
    return Promise.resolve(p.data().id)


async def exe_user_profile_add(
    user_id: str, project_id: str, profile_options: MergeAddResult
) -> Promise[IdsData]:
    if not profile_options["add"]:
        return Promise.resolve(IdsData(ids=[]))
    p = await add_user_profiles(user_id, project_id, profile_options["add"])
    if not p.ok():
        return p
    return p


async def exe_user_profile_update(
    user_id: str, project_id: str, profile_options: MergeAddResult
) -> Promise[IdsData]:
    if not profile_options["update"]:
        return Promise.resolve(IdsData(ids=[]))
    p = await update_user_profiles(user_id, project_id, profile_options["update"])
    if not p.ok():
        return p
    return p


async def exe_user_profile_delete(
    user_id: str, project_id: str, profile_options: MergeAddResult
) -> Promise[IdsData]:
    if not profile_options["delete"]:
        return Promise.resolve(IdsData(ids=[]))
    p = await delete_user_profiles(user_id, project_id, profile_options["delete"])
    if not p.ok():
        return p
    return p