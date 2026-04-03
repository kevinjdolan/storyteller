from app.services.story_formatting import build_story_reader_document


def test_build_story_reader_document_preserves_structure_and_simple_emphasis() -> None:
    document = build_story_reader_document(
        "\n".join(
            [
                "Chapter 1: Lantern Wake",
                "",
                "Mira carried a *soft* lantern toward the **steady** harbor.",
                "",
                "## A Quiet Promise",
                "",
                "Otis promised the cove would stay ***bright and calm*** tonight.",
            ]
        )
    )

    assert document.chapter_count == 1
    assert document.has_structure is True
    assert [block.kind for block in document.blocks] == [
        "chapter_heading",
        "paragraph",
        "heading",
        "paragraph",
    ]
    assert document.blocks[0].text == "Chapter 1: Lantern Wake"
    assert [span.model_dump() for span in document.blocks[1].spans] == [
        {"text": "Mira carried a ", "style": "plain"},
        {"text": "soft", "style": "emphasis"},
        {"text": " lantern toward the ", "style": "plain"},
        {"text": "steady", "style": "strong"},
        {"text": " harbor.", "style": "plain"},
    ]
    assert [span.model_dump() for span in document.blocks[3].spans] == [
        {"text": "Otis promised the cove would stay ", "style": "plain"},
        {"text": "bright and calm", "style": "strong_emphasis"},
        {"text": " tonight.", "style": "plain"},
    ]


def test_build_story_reader_document_joins_wrapped_paragraph_lines() -> None:
    document = build_story_reader_document(
        "\n".join(
            [
                "# Chapter 2",
                "",
                "The lantern drifted across the cove",
                "while Mira counted each reflection.",
                "",
                "Then the bell settled.",
            ]
        )
    )

    assert [block.text for block in document.blocks] == [
        "Chapter 2",
        "The lantern drifted across the cove while Mira counted each reflection.",
        "Then the bell settled.",
    ]
