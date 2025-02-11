def create_prompt(full_transcript: str, target_audience: str = "general"):

    if target_audience == "general":
        youtube_prompt = f"""
            You are an educational content creator that transforms YouTube video transcripts into engaging, interactive worksheets designed to enhance active learning.

            Below is the full transcript of a YouTube video:
            {full_transcript}

            Your task is to analyze the transcript and identify the key segments or sections of the video in chronological order. Then, create a worksheet in Markdown format with the following features:

            1. **Chronological Organization:**
            Arrange all questions and activities in the order of the video’s timeline.

            2. **Engaging Questions:**
            Include a mix of question types (e.g., multiple-choice, short-answer, reflection, fill-in-the-blanks) that encourage the viewer to actively listen and process the content.

            3. **Interactive Activities:**
            Add engaging tasks such as summarizing key points, predicting what will come next, or reflective prompts that require personal insights.

            4. **Segment Headers:**
            Clearly label each section of the worksheet (e.g., “Introduction,” “Main Content,” “Conclusion”) so viewers can easily follow along with the video's flow.

            5. **Ample Space for Answers:**
            For each question or activity, provide generous space for users to write down their responses. Use blank lines, underscores, or designated write-in areas (e.g., "____________________") to indicate where users should write their answers. They should receive a minimum of two lines for each answer, unless a single word answer is required.

            6. **Active Learning Focus:**
            Ensure that the questions and activities reinforce the major concepts covered in the video and encourage personal reflection on the content.

            Ensure that the final output is entirely formatted in Markdown. Do not include any bibliographic references or additional information beyond the worksheet.

            Produce the completed worksheet as your final output.

            The user needs 3-5 new lines worth of space between each question for answers. This is a priority.
            """

    elif target_audience == "age":  # Keep the Age of Empires prompt
        youtube_prompt = f"""
You are an experienced real-time strategy game coach specializing in Age of Empires. Your objective is to transform the transcript of a YouTube video into a comprehensive strategy guide and build order that players can use to improve their gameplay.

Below is the full transcript of a YouTube video:
{full_transcript}

Your task is to analyze the transcript thoroughly and extract the essential details needed to create a structured and actionable guide. The final guide should include the following components:

#### 1. Build Order Timeline:
- **Chronological Steps:** Detail the sequence from the early game (e.g., initial villager production, starting resource gathering and scouting) through the mid-game, and if applicable, late-game phases.
- **Timings and Milestones:** Clearly indicate when specific actions should be taken, such as transitioning to another age, setting up defenses, and initiating attacks.

#### 2. Villagers & Resource Management:
- **Villager Production:** Specify how many villagers to produce at various stages of the game.
- **Task Assignments:** Clearly outline what each group of villagers should do (e.g., gathering food, wood, gold, and stone).
- **Resource Prioritization:** Include advice on resource distribution to balance economic growth with military expansion.

#### 3. Building Strategy:
- **Essential Buildings:** List which buildings to construct, the order in which to build them, and the rationale behind each decision.
- **Construction Timing:** Detail when to initiate the construction of each building (e.g., town centers, barracks, archery ranges, stables) to maintain a steady economy and preparation for conflict.

#### 4. Civilization-Specific Tactics:
- **Civilization Details:** Identify the civilization featured in the transcript and highlight its unique attributes, strengths, and potential weaknesses.
- **Tactical Advice:** Provide tailored tips on how to leverage the civilization’s bonuses, such as unique units or technology advantages, and counter opponents effectively.

#### 5. Offensive and Defensive Strategies:
- **Balancing Strategies:** Include actionable tips on when to focus on economy versus military buildup.
- **Attack & Defense Tips:** Offer strategies for both launching proactive attacks and preparing for enemy counter-attacks. Discuss scenarios like early rush defenses and timing your own offensive maneuvers.
- **Additional Tricks:** Incorporate any extra advice or hidden tactics mentioned in the video that might give players an edge.

#### 6. Actionable Steps:
- **Step-by-Step Instructions:** Consolidate the information into a clear, step-by-step build order accompanied by detailed strategic advice.
- **Ease of Use:** Ensure that the instructions are precise, easy to follow, and cater to both beginners and experienced players.

Please format your final output entirely in Markdown. Do not include any extraneous bibliographical information or unrelated context. Your completed build order and strategy guide should serve as a practical and accessible reference for players looking to excel at Age of Empires.

Produce the completed guide as your final output.
"""
    return youtube_prompt
