# Project Overview

This project contains the following key files:

- **main.py** — The main file, likely the entry point.
- **wiki_utils.py** — Utilities for working with Wikipedia.
- **pyproject.toml** — Likely contains dependencies for installation.
- **uv.lock** — Dependency lock file.
- **.streamlit** — Possibly indicates that the project uses Streamlit for a web interface.

## Setup Instructions

To run the project, follow these steps:

### 1. Install Dependencies

The project requires **Python 3.11+** and the following libraries:

```sh
pip install streamlit==1.43.1 trafilatura==2.0.0 translate==3.6.1 wikipedia==1.4.0 wikipedia-api==0.8.1
```

### 2. Run the Main File

If the project uses Streamlit, you can start it with:

```sh
streamlit run main.py
```

## Additional Information

For further customization or modifications, refer to `pyproject.toml` to check for additional dependencies or project configurations.

