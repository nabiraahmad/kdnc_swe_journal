# Manuscript requirements

## Data fields:

- title: str
- author: str
- author_email: str
- state: int or str
- referees: dictionary, keyed by referee_id (email), with fields:
    - report: str
    - verdict: str, one of 'ACCEPT', 'ACCEPT_W_REV', 'REJECT'
- text: str  (the body of the manuscript)
- abstract: str (a summary)
- history: list of state changes
- editor: str (email address of the editor)