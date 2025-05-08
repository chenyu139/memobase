from . import user_profile_topics
from .utils import pack_profiles_into_string
from ..models.response import AIUserProfiles
from ..env import CONFIG

ADD_KWARGS = {
    "prompt_id": "transcript_extract_profile",
}
EXAMPLES = [
    (
        """User Record: Attended a College Information Session
Record Date: 2023-05-15
Record Location: Stanford University Campus
Record Details: User attended an information session about Stanford's Computer Science program. The session covered admission requirements (3.8+ GPA, strong math background), curriculum highlights, and research opportunities. User asked questions about internship placements and graduate employment rates.
""",
        AIUserProfiles(
            **{
                "facts": [
                    {
                        "topic": "education",
                        "sub_topic": "interest",
                        "memo": "Interested in Stanford's Computer Science program [happen at 2023-05-15]",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "research",
                        "memo": "Showed interest in research opportunities at Stanford [happen at 2023-05-15]",
                    },
                    {
                        "topic": "career",
                        "sub_topic": "planning",
                        "memo": "Concerned about internship placements and employment prospects [happen at 2023-05-15]",
                    },
                ]
            }
        ),
    ),
    (
        """User Record: Completed an Online Course
Record Date: 2023-09-10
Record Location: Home Office
Record Details: User completed the 'Advanced Machine Learning' course on Coursera with a final grade of 95%. The 12-week course covered neural networks, deep learning, and natural language processing. User spent approximately 120 hours on coursework and received a verified certificate.
""",
        AIUserProfiles(
            **{
                "facts": [
                    {
                        "topic": "education",
                        "sub_topic": "online_learning",
                        "memo": "Completed 'Advanced Machine Learning' course on Coursera [happen at 2023-09-10]",
                    },
                    {
                        "topic": "achievement",
                        "sub_topic": "academic",
                        "memo": "Scored 95% in a 12-week advanced machine learning course [happen at 2023-09-10]",
                    },
                    {
                        "topic": "skill",
                        "sub_topic": "technical",
                        "memo": "Knowledge of neural networks, deep learning, and natural language processing",
                    },
                ]
            }
        ),
    ),
]

DEFAULT_JOB = """You are a professional record analyst.
Your responsibility is to carefully analyze the user's record content and extract important user information in a structured format.
You should not only extract explicitly stated information but also infer user characteristics, preferences, and habits implied in the records.
You will use the same language as the user's input to record these facts.
"""

FACT_RETRIEVAL_PROMPT = """{{system_prompt}}
## Format Requirements
### Input
#### Topic Guidelines
You will be given some topics and subtopics that you should focus on collecting and extracting.
You can create your own topics/sub_topics if you find it necessary, unless the user requests not to create new topics/sub_topics.
#### User Existing Topics
You will be given the topics and subtopics that the user has already shared.
Consider using the same classification if the same topic/subtopic is mentioned again in the record content.
#### Record Content
You will receive the user's record content, which contains user behaviors, events, preferences, etc.

### Output
You need to extract facts and preferences from the record content and list them in order:
- TOPIC{{tab}}SUB_TOPIC{{tab}}MEMO
For example:
- basic_info{{tab}}name{{tab}}melinda
- work{{tab}}title{{tab}}software engineer

Each line is a fact or preference, containing:
1. TOPIC: represents the category of this preference
2. SUB_TOPIC: the detailed topic of this preference
3. MEMO: the extracted `user` information, facts, or preferences
These elements should be separated by `{{tab}}` and each line should be separated by `\n` and started with "- ".

## Examples
Here are some examples:
{{examples}}
Return the facts and preferences in a markdown list format as shown above.

Remember the following:
- If the user mentions time-sensitive information, try to infer the specific date from the data.
- Use specific dates when possible, never use relative dates like "today" or "yesterday" etc.
- If you do not find anything relevant in the record content below, you can return an empty list.
- Make sure to return the response in the format mentioned in the formatting & examples section.
- You should infer what's implied in the record content, not just what's explicitly stated.
- Place all content related to this topic/sub_topic in one element, no repeat.

You should detect the language of the user input and record the facts in the same language.
If you do not find any relevant facts, user memories, and preferences in the record content below, just return "NONE" or "NO FACTS".

#### Topic Guidelines
Below is the list of topics and subtopics that you should focus on collecting and extracting:
{{topic_examples}}

Now perform your task.
"""


def pack_input(already_input, memo_str, strict_mode: bool = False):
    header = ""
    if strict_mode:
        header = "Do not extract topics/sub_topics not mentioned in #### Topic Guidelines, otherwise your answer will be invalid!"
    return f"""{header}
#### User Existing Topics
{already_input}
Do not output topics and subtopics not mentioned in the following record content.
#### Record Content
{memo_str}
"""


def get_default_profiles() -> str:
    return user_profile_topics.get_prompt()


def get_prompt(topic_examples: str) -> str:
    sys_prompt = CONFIG.system_prompt or DEFAULT_JOB
    examples = "\n\n".join(
        [
            f"""<example>
<input>{p[0]}</input>
<output>
{pack_profiles_into_string(p[1])}
</output>
</example>
"""
            for p in EXAMPLES
        ]
    )
    return FACT_RETRIEVAL_PROMPT.format(
        system_prompt=sys_prompt,
        examples=examples,
        tab=CONFIG.llm_tab_separator,
        topic_examples=topic_examples,
    )


def get_kwargs() -> dict:
    return ADD_KWARGS


if __name__ == "__main__":
    print(get_prompt(get_default_profiles()))