from . import user_profile_topics
from .utils import pack_profiles_into_string
from ..models.response import AIUserProfiles
from ..env import CONFIG

ADD_KWARGS = {
    "prompt_id": "doc_extract_profile",
}
EXAMPLES = [
    (
        """Document Content: AP Biology Textbook Chapter

Chapter 5: Cell Structure and Function

This chapter explores the fundamental unit of life - the cell. We will examine eukaryotic and prokaryotic cell structures, membrane transport mechanisms, and cellular communication. This material aligns with the AP Biology curriculum requirements for the Cell Communication and Cell Cycle units (Units 3-4).

Learning Objectives:
- Compare and contrast prokaryotic and eukaryotic cells
- Explain the structure and function of cellular organelles
- Analyze how cell membranes regulate the passage of materials

This content is designed for high school students in grades 11-12 preparing for the AP Biology examination, which can earn college credit at most U.S. universities.
""",
        AIUserProfiles(
            **{
                "facts": [
                    {
                        "topic": "education",
                        "sub_topic": "country",
                        "memo": "United States / AP Biology",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "education_stage",
                        "memo": "Upper High School: Grades 11-12",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "subject",
                        "memo": "Biology - Cell Biology",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "depth_level",
                        "memo": "Advanced Placement (College Introductory Level)",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "importance",
                        "memo": "Critical for exam credit at U.S. universities",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "learning_objectives",
                        "memo": "Compare prokaryotic and eukaryotic cells; Explain cellular organelles; Analyze membrane transport",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "curriculum_alignment",
                        "memo": "AP Biology Cell Communication and Cell Cycle units (Units 3-4)",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "education_level",
                        "memo": "High School Student (Grade 11-12)",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "subject_interest",
                        "memo": "Biology, particularly cellular biology",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "learning_purpose",
                        "memo": "AP Exam Preparation for college credit",
                    },
                ]
            }
        ),
    ),
    (
        """Document Content: Mathematics Lecture Notes

Introduction to Calculus
Professor: Dr. Zhang Wei
Beijing Normal University

These lecture notes cover the fundamental concepts of differential calculus, including limits, continuity, and derivatives. The material is presented at a first-year undergraduate level and assumes prior knowledge of pre-calculus and basic algebraic manipulation.

Topics covered:
1. Limits and continuity
2. Differentiation rules
3. Applications of derivatives

This course serves as a foundation for all science and engineering majors and is a required core mathematics course in the Chinese university curriculum.
""",
        AIUserProfiles(
            **{
                "facts": [
                    {
                        "topic": "education",
                        "sub_topic": "country",
                        "memo": "China / University Curriculum",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "education_stage",
                        "memo": "Undergraduate: First Year",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "subject",
                        "memo": "Mathematics - Calculus",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "depth_level",
                        "memo": "Introductory College Level",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "importance",
                        "memo": "Core required course for science and engineering majors",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "instructor",
                        "memo": "Dr. Zhang Wei",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "institution",
                        "memo": "Beijing Normal University",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "prerequisites",
                        "memo": "Pre-calculus and basic algebraic manipulation",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "topics",
                        "memo": "Limits and continuity, Differentiation rules, Applications of derivatives",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "education_level",
                        "memo": "First-year university student",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "subject_interest",
                        "memo": "Mathematics, possibly science or engineering major",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "learning_purpose",
                        "memo": "Core curriculum requirement for degree program",
                    },
                ]
            }
        ),
    ),
    (
        """Document Content: Middle School Science Workbook

Chapter 3: The Water Cycle

This chapter introduces students to the basic concepts of the water cycle in nature. We will explore evaporation, condensation, precipitation, and collection. The material is designed for 7th grade science curriculum and includes simple experiments that can be performed at home.

Activities in this chapter:
- Create a mini water cycle in a plastic bag
- Measure rainfall using a homemade rain gauge
- Complete the water cycle diagram worksheet

Parents: This material aligns with the national middle school science standards and will help prepare your child for their end-of-term examination.
""",
        AIUserProfiles(
            **{
                "facts": [
                    {
                        "topic": "education",
                        "sub_topic": "country",
                        "memo": "National curriculum (country not specified)",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "education_stage",
                        "memo": "Middle School: 7th Grade",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "subject",
                        "memo": "Science - Earth Science/Hydrology",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "depth_level",
                        "memo": "Basic Middle School Level",
                    },
                    {
                        "topic": "education",
                        "sub_topic": "importance",
                        "memo": "Required for end-of-term examination",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "learning_activities",
                        "memo": "Hands-on experiments, diagram completion, measurement activities",
                    },
                    {
                        "topic": "course",
                        "sub_topic": "curriculum_alignment",
                        "memo": "National middle school science standards",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "education_level",
                        "memo": "Middle School Student (7th Grade)",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "subject_interest",
                        "memo": "Basic Earth Science",
                    },
                    {
                        "topic": "user_profile",
                        "sub_topic": "learning_purpose",
                        "memo": "Required coursework and exam preparation",
                    },
                ]
            }
        ),
    ),
]

DEFAULT_JOB = """You are a professional educational analyst and user profiler.
Your responsibility is to carefully analyze learning content and extract important educational information in a structured format.
You should identify key aspects of the learning material such as subject area, educational level, difficulty, and relevance to learners.
Additionally, you should infer the likely educational background of the user who uploaded this document.
For example, if the document is a middle school textbook, the user is likely a middle school student.
If the document is a university-level research paper, the user is likely a university student or researcher.
You will use the same language as the input content to record these educational insights and user profile inferences.
"""

FACT_RETRIEVAL_PROMPT = """{system_prompt}
## Format Requirements
### Input
#### Topic Guidelines
You will be given some topics and subtopics that you should focus on collecting and extracting.
You should not create your own topics/sub_topics.
#### Existing Topics
You will be given topics and subtopics that have already been identified.
Consider using the same classification if the same topic/subtopic appears in the learning content.
#### Learning Content
You will receive learning content to analyze, which may include course materials, textbook excerpts, lecture notes, or other educational resources.

### Output
You need to extract educational information from the content and list them in order:
- TOPIC{tab}SUB_TOPIC{tab}MEMO
For example:
- education{tab}subject{tab}Biology - Molecular & Cellular
- course{tab}difficulty{tab}Introductory College Level
- user_profile{tab}education_level{tab}High School Student (Grade 11-12)

Each line contains:
1. TOPIC: represents the category of educational information
2. SUB_TOPIC: the specific aspect of educational information
3. MEMO: the extracted educational content, facts, or insights
These elements should be separated by `{tab}` and each line should be separated by `\n` and started with "- ".

## Examples
Here are some examples:
{examples}
Return the educational information in a markdown list format as shown above.

Remember the following:
- Focus on educational aspects like subject area, difficulty level, target audience, and learning objectives.
- Be concise and pedagogically focused in your extraction.
- If you do not find relevant educational information, you can return an empty list.
- Make sure to return the response in the format mentioned in the formatting section.
- You should infer pedagogical implications, not just what's explicitly stated.
- Place all content related to this topic/sub_topic in one element, no repeat.
- Always include user profile inferences based on the document content.

You should detect the language of the input content and record the information in the same language.
If you do not find any relevant educational information in the content below, just return "NONE" or "NO EDUCATIONAL INFORMATION".

#### Topic Guidelines
Below is the list of topics and subtopics that you should focus on collecting and extracting:
{topic_examples}

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