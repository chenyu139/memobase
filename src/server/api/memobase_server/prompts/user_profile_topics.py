from ..env import CONFIG, LOG
from .profile_init_utils import (
    UserProfileTopic,
    formate_profile_topic,
    modify_default_user_profile,
)


CANDIDATE_PROFILE_TOPICS: list[UserProfileTopic] = [
    UserProfileTopic(
        "basic_info",
        sub_topics=[
            "Name",
            {
                "name": "Age",
                "description": "integer",
            },
            "Gender",
            "birth_date",
            "nationality",
            "ethnicity",
            "language_spoken",
        ],
    ),
    UserProfileTopic(
        "contact_info",
        sub_topics=[
            "email",
            "phone",
            "city",
            "country",
        ],
    ),
    UserProfileTopic(
        "education",
        sub_topics=[
            "school",
            "degree",
            "major",
            "country",  # 所属国家
            "education_stage",  # 所属阶段，例如：高中高年级（11-12年级，大学预科阶段）
            "subject",  # 所属学科，例如：生物学（侧重现代生物学的核心领域）
            "depth_level",  # 所属深度，例如：大学一年级入门水平（AP考试对标美国大学基础课程难度）
            "importance",  # 对当前学生的重要度
        ],
    ),
    UserProfileTopic(
        "demographics",
        sub_topics=[
            "marital_status",
            "number_of_children",
            "household_income",
        ],
    ),
    UserProfileTopic(
        "work",
        sub_topics=[
            "company",
            "title",
            "working_industry",
            "previous_projects",
            "work_skills",
        ],
    ),
    UserProfileTopic(
        "interest",
        sub_topics=[
            "books",
            "movies",
            "music",
            "foods",
            "sports",
        ],
    ),
    UserProfileTopic(
        "psychological",
        sub_topics=["personality", "values", "beliefs", "motivations", "goals"],
    ),
    UserProfileTopic(
        "life_event",
        sub_topics=["marriage", "relocation", "retirement"],
    ),
]

CANDIDATE_PROFILE_TOPICS = modify_default_user_profile(CANDIDATE_PROFILE_TOPICS)


def get_prompt(profiles: list[UserProfileTopic] = CANDIDATE_PROFILE_TOPICS):
    return "\n".join([formate_profile_topic(up) for up in profiles]) + "\n..."


if CONFIG.language == "en":
    LOG.info(f"User profiles: \n{get_prompt()}")

if __name__ == "__main__":
    print(get_prompt())
