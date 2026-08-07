import random

prompts_b = {
    "long_thoughts_v2": """Your answer must contain 4 parts:
<format>
# 1. Thoughts about characters
Analyze and compare the characters/creatures visible in the image against known character tags, descriptions, or memories to identify each character accurately.
# 2. Key details
Identify and list the key visual details in the comic/image.
# 3. Long description
Provide a creative, long, and detailed description of the image content, incorporating all listed key details.
# 4. Detailed description for each character
## Name 1
Detailed description for the first character.
## Name 2
Detailed description for each additional character.
</format>
""",
    "long_thoughts": """Your answer must contain 6 parts:
<format>
# 1. Thoughts about characters
Analyze and compare the characters/creatures visible in the image against known tags, descriptions, or memories to identify each character. If no characters are present, write "No named characters".
# 2. General description
A 1-2 paragraph summary covering all elements, objects, characters, positions, and interactions.
# 3. Detailed description for each character
## Character name 1
In-depth description of features, pose, appearance, items, and interactions.
## Character name 2
Same structure for additional characters.
# 4. Individual Parts
Numbered list (5 to 20 items) of distinct objects and their relative positions.
# 5. Texts on image
List all visible text, specifying container type (speech bubble, sign, watermark) and content.
# 6. Background and effects
Describe background objects, setting, composition, style, camera angle, blur/depth of field, and optical effects.
</format>
""",
    "json": """Provide a JSON-formatted caption following this exact structure:
{
  "character_1": "Description of first character/object: identity, key traits, pose, position.",
  "character_2": "Description of second character if present.",
  "main_content": "Detailed description of primary subject if characters are absent.",
  "background": "Detailed description of background setting and elements.",
  "image_effects": "Visual style or camera effects (e.g., chromatic aberration, fisheye, depth of field). Omit if standard.",
  "texts": "Visible text, speech bubbles, marks, or signs. Set to null if absent.",
  "atmosphere": "Overall mood and lighting atmosphere."
}
""",
    "long": """Write a rich, vivid, natural language caption for the image spanning 2 to 5 paragraphs. Detail all subjects, actions, background elements, lighting, and textures.
""",
    "min_structured_md": """Your answer must contain 3 parts:
<format>
# 1. Thoughts about characters
Identify characters using visual traits or provided context. If none, write "No named characters".
# 2. Key details
Summarize key visual elements in concise text.
# 3. Structured description
## General
Composition, main subject focus, background, and non-character elements.
## Character name 1
Traits, outfit, pose, expression, and interactions for this character.
## Character name 2
Same for remaining characters.
## Image effects
Art style, rendering quality, camera angle, and visual effects.
</format>
""",
    "json_comic": """Provide a JSON caption describing the comic panel sequence:
{
  "comic_format": "Layout structure (e.g., 'Comic panel grid of 4 frames').",
  "1st_frame": "Description of first frame content.",
  "2nd_frame": "Description of second frame content.",
  "Nth_frame": "Description of subsequent frames.",
  "characters": "Overview of characters appearing in the comic.",
  "meaning": "Narrative arc, tone, and comedic/dramatic context."
}
""",
    "md_comic": """Use Markdown format to describe the comic breakdown:
<format>
# 1. Thoughts about characters
Identify characters present across panels.
# 2. Key details
Highlight critical plot items and visual cues.
# 3. Comic format
Format breakdown (page count, orientation, panel grid).
# 4. Details for each frame
## 4.1 Frame 1 (position)
Detailed breakdown of characters, dialogue/bubbles, actions, and scenery.
## 4.2 Frame 2 (position)
Same structure for each panel.
# 5. Summary & Vibe
Overall narrative context, atmosphere, and artistic style.
</format>
""",
    "min_structured_json": """Provide a concise JSON caption prioritizing tag-like descriptive phrases:
{
  "General": "Concise overview of scene composition and subjects. Avoid markdown or bullet points.",
  "character_1": "Brief descriptor for character 1.",
  "character_2": "Brief descriptor for character 2.",
  "image_effects": "Key visual effects or rendering style.",
  "texts": "Text contents or null.",
  "watermarks": "Watermark details or null."
}
""",
    "chroma-style": """Describe the image using the following 4-part structure:
### 1. Regular Summary:
[A single paragraph comprehensive narrative summary.]
### 2. Individual Parts:
[Numbered list of 5 to 30 elements with spatial placement.]
### 3. Midjourney-Style Summary:
[High concept-density prompt using comma-separated descriptors.]
### 4. DeviantArt Commission Request:
[Written as a direct commission prompt requesting this exact image.]
""",
    "short": """Write a concise, precise caption describing the core subject, key features, and background without verbose filler.
""",
    # =========================================================================
    # ANIMA HYBRID PROMPT FORMAT (Distilled from Anima Specification Guidelines)
    # =========================================================================
    "anima_style": """Generate an Anima Hybrid Prompt for the image, strictly adhering to the 2-layer prompt specification structure.

OUTPUT STRUCTURE REQUIREMENTS:
Output MUST contain ONLY two distinct sections in plain text:
Line 1: Hard Tags (Comma-separated list of tags)
Line 2+: Natural Language (2-3 sentences for single subject; 3-6 sentences for multi-subject scenes)

Do NOT include Markdown headers, code blocks, greetings, or conversational output.

---

LAYER 1: HARD TAGS RULES
1. Mandatory Quality/Meta Prefix:
   Must begin with: "masterpiece, best quality, score_7, safe, " (replace 'safe' with 'sensitive', 'nsfw', or 'explicit' based on image rating).
2. Strict Tag Hierarchy Order:
   [quality/meta/safety] -> [character count (e.g., 1girl, 2girls)] -> [character identity/name] -> [series/copyright] -> [@artist tag] -> [hair/eyes/face/body] -> [outfit/accessories] -> [pose/expression/action] -> [scene anchor tags].
3. Formatting Rules:
   - All tags must be lowercased.
   - Use SPACES instead of underscores for multi-word tags (e.g., "blue eyes", "school uniform"), EXCEPT for rating tags like "score_7".
   - Escape literal parentheses if used for weighting: \(tag\).
   - Use artist tags with an '@' prefix (e.g., @artist_name), max 3 artists.
   - Keep total tag counts bounded: Simple (16-30 tags), Standard (22-38 tags), Complex/Multi-character (30-48 tags).
4. Multi-Character Tags:
   Declare count first (e.g., 2girls). Group each character's identity, hair, eyes, and outfit sequentially. Never interlace attributes between different characters.

---

LAYER 2: NATURAL LANGUAGE RULES
Structure the narrative text into distinct sentences based on their operational roles:

Sentence 1 (Framing, Subject Scale & Composition):
- Specify shot type (close-up, upper body, cowboy shot, full body).
- State subject scale explicitly using screen percentage phrases (e.g., "the character dominates the frame", "occupies about two-thirds of frame height").
- Define primary background depth layer and enforce foreground restrictions (prevent unwanted dark framing/clutter).

Sentence 2 (Spatial Anchors, Poses & Interactions):
- Single Subject: Detail exact pose, gaze vector, physical prop contact, and orientation.
- Multi-Subject: Establish distinct spatial anchors for each subject using screen-relative coordinates ("On the left side of the image is [Character A]... On the right side is [Character B]..."). Provide 4-6 distinct visual identifiers per character (hair, top, bottom, shoes, prop, pose). Explicitly specify action initiators and targets.

Sentence 3 (Lighting, Subject Exposure & Color Hierarchy):
- Define primary key light source, illumination direction, and lit body regions ("well-exposed subject", "visible facial features", "clear details in shadows").
- Define background light interaction (rim lighting/backlight balance) to prevent accidental silhouetting.
- State dominant color palette balance and depth of field gradient.
""",
}

prompts_names_only = {
    "long_thoughts_v2": True,
    "long_thoughts": True,
    "json": False,
    "long": False,
    "json_comic": False,
    "md_comic": True,
    "min_structured_md": True,
    "min_structured_json": False,
    "chroma-style": False,
    "short": False,
    "anima_style": False,
}

system_prompt = "You are an expert anime image captioning model. Generate accurate image descriptions strictly following the requested prompt structure and formatting constraints."


def make_user_query(
    item,
    c_type,
    use_names,
    add_tags,
    add_characters,
    add_char_tags,
    add_description,
    underscores_replace=False,
):
    tags = item.get("tags", [])
    random.shuffle(tags)

    if underscores_replace:
        tags = [a.replace("_", " ") if len(a) > 3 else a for a in tags]
        tags_string = ", ".join(tags)
    else:
        tags_string = " ".join(tags)

    user_request = "# Captioning format:\n"
    user_request += prompts_b[c_type]
    user_request += "\n"

    if add_tags:
        user_request += f"# Booru tags for the image\n[{tags_string}]\n\n"

    chars_tags = item.get("characters", [])

    if use_names:
        has_character_grounding = (
            bool(chars_tags)
            or add_characters
            or add_char_tags
            or add_description
        )

        if has_character_grounding:
            if underscores_replace:
                chars_tags = [a.replace("_", " ") for a in chars_tags]
                chars_string = ", ".join(chars_tags)
            else:
                chars_string = ", ".join(chars_tags)

            if chars_string:
                user_request += (
                    f"# Characters on picture:\n"
                    f"Here are names/tags for characters from the picture, make sure to use them: [{chars_string}].\n\n"
                )

            chars_popular_tags = item.get(
                "char_p_tags", {"chars": {}, "skins": {}}
            )
            chars_description = item.get(
                "char_descr", {"chars": {}, "skins": {}}
            )

            has_tags = (
                len(chars_popular_tags["chars"]) > 0
                or len(chars_popular_tags["skins"]) > 0
            )
            has_descriptions = (
                len(chars_description["chars"]) > 0
                or len(chars_description["skins"]) > 0
            )

            if (add_char_tags and has_tags) or (
                add_description and has_descriptions
            ):
                user_request += "# Known traits for characters\n"
                user_request += (
                    "Use the following character traits as authoritative grounding for the named characters. "
                    "When describing each named character, include these traits and do not replace them with "
                    "unrelated visual traits from another identity. If the image appears to show conflicting "
                    "hair, eyes, clothing, accessories, or outfit details for a named character, prefer the "
                    "provided traits below over the conflicting visual evidence. This is especially important "
                    "for clothing and accessories: describe the named character wearing the outfit given in "
                    "their tags/descriptions instead of copying the outfit from the source image.\n"
                )
                char_underscores = underscores_replace

                if add_char_tags and has_tags:
                    user_request += (
                        "Here are popular tags for each character on picture:\n"
                    )

                    for c_name, c_tags in chars_popular_tags["chars"].items():
                        name = (
                            c_name.replace("_", " ")
                            if char_underscores
                            else c_name
                        )
                        tags_s = (
                            ", ".join(
                                [
                                    a.replace("_", " ") if len(a) > 3 else a
                                    for a in c_tags
                                ]
                            )
                            if char_underscores
                            else ", ".join(c_tags)
                        )
                        user_request += f"{name}: [{tags_s}]\n"

                    if len(chars_popular_tags["skins"]) > 0:
                        user_request += "Extra tags for character skins:\n"
                        for c_name, c_tags in chars_popular_tags[
                            "skins"
                        ].items():
                            name = (
                                c_name.replace("_", " ")
                                if char_underscores
                                else c_name
                            )
                            tags_s = (
                                ", ".join(
                                    [
                                        a.replace("_", " ") if len(a) > 3 else a
                                        for a in c_tags
                                    ]
                                )
                                if char_underscores
                                else ", ".join(c_tags)
                            )
                            user_request += f"{name}: [{tags_s}]\n"

                if add_description and has_descriptions:
                    user_request += "Here are general descriptions for each character on the picture:\n"
                    for c_name, c_descr in chars_description["chars"].items():
                        name = (
                            c_name.replace("_", " ")
                            if char_underscores
                            else c_name
                        )
                        user_request += f"## {name}\n{c_descr}\n\n"
                    if len(chars_description["skins"]) > 0:
                        user_request += "Here are also descriptions for specific skins of characters:\n"
                        for c_name, c_descr in chars_description[
                            "skins"
                        ].items():
                            name = (
                                c_name.replace("_", " ")
                                if char_underscores
                                else c_name
                            )
                            user_request += f"## {name}\n{c_descr}\n\n"
        else:
            user_request += "# Characters on picture:\nTry to recognize the characters in the picture and use their names.\n"

        user_request += "\n"
    else:
        user_request += (
            "# Characters on picture:\nAvoid guessing names for characters.\n"
        )

    return user_request
