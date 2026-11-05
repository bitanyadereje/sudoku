# A Little Puzzle Book — Volume One

## Open in VS Code
1. Extract this ZIP to a folder, for example `a-little-puzzle-book`.
2. In VS Code, choose **File → Open Folder...** and select that folder.
3. Open the integrated terminal (**Terminal → New Terminal**).
4. Install the PDF dependency:
   ```bash
   python -m pip install reportlab
   ```
5. Generate the PDF:
   ```bash
   python a_little_puzzle_book_source.py
   ```

The generated PDF will appear in the same folder.

## Files
- `a_little_puzzle_book_source.py` — page layout and PDF-generation code.
- `puzzle_book_editable_data.json` — editable Sudoku grids and Word Search content.
- `a_little_puzzle_book_volume_one.pdf` — current 40-page PDF.
- `private_validation_report.txt` — validation notes.

## Editing
- Change puzzle text, grids, themes, or word lists in `puzzle_book_editable_data.json`.
- Change page layout, fonts, spacing, and colors in `a_little_puzzle_book_source.py`.
- The current Sudoku puzzles were uniqueness-validated. If you edit a Sudoku grid, validate it again before printing.
