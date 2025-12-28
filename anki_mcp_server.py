import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("anki")

ANKI_CONNECT_URL = "http://localhost:8765"


async def anki_request(action: str, **params):
    """Send request to AnkiConnect."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            ANKI_CONNECT_URL, json={"action": action, "version": 6, "params": params}
        )
        result = resp.json()
        if result.get("error"):
            raise Exception(result["error"])

        return result.get("result")


@mcp.tool()
async def list_decks() -> list[str]:
    """List all Anki decks."""
    return await anki_request("deckNames")


@mcp.tool()
async def add_note(deck: str, front: str, back: str) -> int:
    """Add a basic card to a deck. Returns note ID."""
    note = {
        "deckName": deck,
        "modelName": "Basic",
        "fields": {"Front": front, "Back": back},
        "options": {"allowDuplicate": False},
    }
    return await anki_request("addNote", note=note)


@mcp.tool()
async def search_cards(query: str) -> list[int]:
    """Search cards using Anki's search syntax."""
    return await anki_request("findCards", query=query)


@mcp.tool()
async def get_card_info(card_ids: list[int]) -> list[dict]:
    """Get detailed info for cards by ID."""
    return await anki_request("cardsInfo", cards=card_ids)


# Deck CRUD operations


@mcp.tool()
async def create_deck(deck_name: str) -> int:
    """Create a new deck. Returns deck ID."""
    return await anki_request("createDeck", deck=deck_name)


@mcp.tool()
async def delete_deck(deck_name: str, cards_too: bool = True) -> None:
    """Delete a deck. If cards_too is True, also deletes cards in the deck."""
    return await anki_request("deleteDecks", decks=[deck_name], cardsToo=cards_too)


@mcp.tool()
async def rename_deck(old_name: str, new_name: str) -> int:
    """Rename an existing deck by creating new deck, moving cards, and deleting old deck."""
    # Get all cards in the old deck
    card_ids = await anki_request("findCards", query=f'"deck:{old_name}"')

    # Create the new deck
    new_deck_id = await anki_request("createDeck", deck=new_name)

    # Move cards to new deck if there are any
    if card_ids:
        await anki_request("changeDeck", cards=card_ids, deck=new_name)

    # Delete the old deck (cards already moved)
    await anki_request("deleteDecks", decks=[old_name], cardsToo=False)

    return new_deck_id


@mcp.tool()
async def move_cards_to_deck(card_ids: list[int], deck_name: str) -> None:
    """Move cards to a different deck."""
    return await anki_request("changeDeck", cards=card_ids, deck=deck_name)


# Card/Note CRUD operations


@mcp.tool()
async def update_note(note_id: int, front: str | None = None, back: str | None = None) -> None:
    """Update the fields of an existing note (Basic card type)."""
    fields = {}
    if front is not None:
        fields["Front"] = front
    if back is not None:
        fields["Back"] = back

    if not fields:
        raise ValueError("At least one of 'front' or 'back' must be provided")

    return await anki_request("updateNoteFields", note={"id": note_id, "fields": fields})


@mcp.tool()
async def delete_notes(note_ids: list[int]) -> None:
    """Delete notes by their IDs. This also deletes all cards associated with the notes."""
    return await anki_request("deleteNotes", notes=note_ids)


@mcp.tool()
async def get_note_info(note_ids: list[int]) -> list[dict]:
    """Get detailed info for notes by ID."""
    return await anki_request("notesInfo", notes=note_ids)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
