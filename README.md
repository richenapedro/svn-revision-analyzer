# SVN Revision Analyzer

A lightweight desktop application for browsing SVN revisions and
exporting complete revision packages for AI-assisted code review.

The application is designed for local SVN working copies, especially
projects managed with TortoiseSVN.

------------------------------------------------------------------------

## Features

-   Browse a local SVN working copy
-   Load the latest SVN revisions
-   View revision author, date, and commit message
-   Display the list of changed files for a selected revision
-   Export a complete revision package as a ZIP archive
-   Preserve the original repository folder structure

------------------------------------------------------------------------

## Exported ZIP Structure

``` text
Revision_1281.zip
├── revision_info.txt
├── diff.patch
├── before/
│   └── trunk/
│       └── ...
└── after/
    └── trunk/
        └── ...
```

### Package Contents

  File                  Description
  --------------------- ----------------------------------------------------
  `revision_info.txt`   SVN log information for the selected revision
  `diff.patch`          Complete SVN diff generated with `svn diff -c`
  `before/`             Files as they existed before the selected revision
  `after/`              Files as they exist in the selected revision

------------------------------------------------------------------------

## Requirements

-   Python 3.12+
-   SVN Command Line Tools (`svn.exe`)
-   `svn.exe` available in the system `PATH`

------------------------------------------------------------------------

## Installation

``` powershell
git clone https://github.com/YOUR_USERNAME/svn-revision-analyzer.git

cd svn-revision-analyzer

python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

------------------------------------------------------------------------

## Running

``` powershell
python app.py
```

------------------------------------------------------------------------

## Building the Executable

Install PyInstaller:

``` powershell
pip install pyinstaller
```

Build:

``` powershell
pyinstaller --noconfirm --onefile --windowed --name "SVN Revision Analyzer" app.py
```

The executable will be created in:

``` text
dist/
```

------------------------------------------------------------------------

## Project Structure

``` text
svn-revision-analyzer/
│
├── app.py
├── requirements.txt
├── config.json
├── README.md
│
├── exporter/
├── svn/
├── ui/
├── utils/
└── output/
```

------------------------------------------------------------------------

## Architecture

``` text
MainWindow
     │
     ▼
RevisionExporter
     │
     ├── SvnClient
     ├── ExportWorkspace
     ├── FileExporter
     └── ZipBuilder
```

The application follows a modular architecture where:

-   **UI** is responsible only for presentation.
-   **SvnClient** communicates with the SVN command line.
-   **RevisionExporter** orchestrates the export process.
-   **ExportWorkspace** manages temporary folders.
-   **FileExporter** writes files to disk.
-   **ZipBuilder** creates the final ZIP archive.

------------------------------------------------------------------------

## Roadmap

Future improvements:

-   Revision search
-   Author and date filters
-   Export revision ranges
-   Integrated diff viewer
-   Open exported files in VS Code
-   OpenAI integration for automatic revision analysis
-   Multi-language support (EN / PT-BR / DE)

------------------------------------------------------------------------

## Notes

-   This application is **read-only**.
-   It never modifies the SVN repository or the working copy.
-   All exported files are generated locally.

------------------------------------------------------------------------

## License

MIT License
