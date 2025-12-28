# Anki MCP Server

An MCP (Model Context Protocol) server that allows AI assistants to interact with Anki via AnkiConnect.

## Prerequisites

- [Anki](https://apps.ankiweb.net/) installed and running
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed in Anki
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/anki-mcp-server.git
   cd anki-mcp-server
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Install AnkiConnect in Anki:
   - Open Anki
   - Go to Tools > Add-ons > Get Add-ons
   - Enter code: `2055492159`
   - Restart Anki

## Usage

### Running the server

```bash
uv run python anki_mcp_server.py
```

### Configuring with Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "anki": {
      "command": "uv",
      "args": ["run", "python", "anki_mcp_server.py"],
      "cwd": "/path/to/anki-mcp-server"
    }
  }
}
```

### Configuring with Claude Code

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "anki": {
      "command": "uv",
      "args": ["run", "python", "anki_mcp_server.py"],
      "cwd": "/path/to/anki-mcp-server"
    }
  }
}
```

## Available Tools

### Deck Operations

| Tool | Description |
|------|-------------|
| `list_decks` | List all Anki decks |
| `create_deck(deck_name)` | Create a new deck |
| `delete_deck(deck_name, cards_too)` | Delete a deck (optionally with cards) |
| `rename_deck(old_name, new_name)` | Rename an existing deck |
| `move_cards_to_deck(card_ids, deck_name)` | Move cards to a different deck |

### Card/Note Operations

| Tool | Description |
|------|-------------|
| `add_note(deck, front, back)` | Add a basic card to a deck |
| `search_cards(query)` | Search cards using Anki's search syntax |
| `get_card_info(card_ids)` | Get detailed info for cards by ID |
| `get_note_info(note_ids)` | Get detailed info for notes by ID |
| `update_note(note_id, front, back)` | Update fields of an existing note |
| `delete_notes(note_ids)` | Delete notes and their associated cards |

## Examples

Once configured, you can ask your AI assistant things like:

- "List all my Anki decks"
- "Create a new deck called 'Spanish Vocabulary'"
- "Add a card to my Spanish deck with 'Hola' on the front and 'Hello' on the back"
- "Search for all cards in my Spanish deck"
- "Delete the card with ID 12345"

## Requirements

- Anki must be running with AnkiConnect for the server to work
- AnkiConnect listens on `http://localhost:8765` by default

## License

MIT
