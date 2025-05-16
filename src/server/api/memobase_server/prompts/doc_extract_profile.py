from . import user_profile_topics
from .utils import pack_profiles_into_string
from ..models.response import AIUserProfiles
from ..env import CONFIG

ADD_KWARGS = {
    "prompt_id": "doc_extract_profile",
}
EXAMPLES = [
    (
        """Document Content: Student Resume

I am a Computer Science student at Stanford University, currently in my junior year. I have a GPA of 3.8/4.0.
I have completed coursework in Data Structures, Algorithms, Machine Learning, and Database Systems.
I participated in the university's AI research program and contributed to a paper on natural language processing.
My contact information: Phone: 650-123-4567, Email: student@stanford.edu
""",
        AIUserProfiles(
            **{
                "facts": [
                    {
                        "topic": "education",
                        "sub_topic": "university",
                        "memo": "Stanford University",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "major",
                        "memo": "Computer Science",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "year",
                        "memo": "Junior year",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "gpa",
                        "memo": "3.8/4.0",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "coursework",
                        "memo": "Data Structures, Algorithms, Machine Learning, Database Systems",
                    },
                    {
                        "topic": "research",
                        "sub_topic": "experience",
                        "memo": "Participated in university's AI research program",
                    },
                    {
                        "topic": "research",
                        "sub_topic": "publication",
                        "memo": "Contributed to a paper on natural language processing",
                    },
                    {
                        "topic": "contact_info",
                        "sub_topic": "phone",
                        "memo": "650-123-4567",
                    },
                    {
                        "topic": "contact_info",
                        "sub_topic": "email",
                        "memo": "student@stanford.edu",
                    },
                ]
            }
        ),
    ),
    (
        """Document Content: Course Syllabus

Course Title: Advanced Machine Learning
Instructor: Dr. Emily Johnson
Semester: Fall 2023
Credits: 4

Course Description:
This graduate-level course covers advanced topics in machine learning, including deep learning architectures, reinforcement learning, and generative models. Students will complete a semester-long project implementing cutting-edge ML techniques.

Prerequisites:
Introduction to Machine Learning, Linear Algebra, Probability Theory
""",
        AIUserProfiles(
            **{
                "facts": [
                    {
                        "topic": "course",
                        "sub_topic": "title",
                        "memo": "Advanced Machine Learning",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "instructor",
                        "memo": "Dr. Emily Johnson",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "semester",
                        "memo": "Fall 2023",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "credits",
                        "memo": "4",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "description",
                        "memo": "Graduate-level course covering advanced topics in machine learning, including deep learning architectures, reinforcement learning, and generative models",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "project",
                        "memo": "Semester-long project implementing cutting-edge ML techniques",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "prerequisites",
                        "memo": "Introduction to Machine Learning, Linear Algebra, Probability Theory",
                    },
                ]
            }
        ),
    ),
]

DEFAULT_JOB = """You are a professional document analyst.
Your responsibility is to carefully read the user's document content and extract important user information in a structured format.
You should not only extract explicitly stated information but also infer what's implied in the document.
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
Consider using the same classification if the same topic/subtopic is mentioned again in the document.
#### Document Content
You will receive the user's document content, which contains user information, events, preferences, etc.

### Output
You need to extract facts and preferences from the document and list them in order:
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
- If you do not find anything relevant in the document below, you can return an empty list.
- Make sure to return the response in the format mentioned in the formatting & examples section.
- You should infer what's implied in the document, not just what's explicitly stated.
- Place all content related to this topic/sub_topic in one element, no repeat.

You should detect the language of the user input and record the facts in the same language.
If you do not find any relevant facts, user memories, and preferences in the document below, just return "NONE" or "NO FACTS".

#### Topic Guidelines
Below is the list of topics and subtopics that you should focus on collecting and extracting:
{{topic_examples}}

#### Special Education Information Extraction Guidelines
When extracting educational information, pay special attention to these sub-topics:

1. **country** - Identify the country where the education is taking place or the educational system being referenced (e.g., "United States", "China", "United Kingdom").

2. **education_stage** - Determine the specific educational stage or level, being as precise as possible. Examples:
   - "High school senior level (11-12th grade, university preparatory stage)"
   - "Middle school (7-9th grade)"
   - "Undergraduate level"
   - "Graduate level"

3. **subject** - Identify the specific academic subject or discipline, including any specialization areas. Examples:
   - "Biology (focusing on core areas of modern biology)"
   - "Physics (mechanics and electromagnetism)"
   - "Computer Science (algorithms and data structures)"

4. **depth_level** - Assess the depth or difficulty level of the educational content. Examples:
   - "First-year college introductory level (AP exam targeting US college foundation course difficulty)"
   - "Advanced high school level"
   - "Graduate entry level"

5. **importance** - Evaluate how important this educational content is for the student, based on context. Examples:
   - "Core required course"
   - "Elective supplementary course"
   - "Essential content for college entrance exams"

When these details aren't explicitly stated, make reasonable inferences based on context clues in the document.

Now perform your task.
"""


def pack_input(already_input, memo_str, strict_mode: bool = False):
    header = ""
    if strict_mode:
        header = "Do not extract topics/sub_topics not mentioned in #### Topic Guidelines, otherwise your answer will be invalid!"
    return f"""{header}
#### User Existing Topics
{already_input}
Do not output topics and subtopics not mentioned in the following document content.
#### Document Content
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