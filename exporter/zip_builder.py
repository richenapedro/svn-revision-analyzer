from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


class ZipBuilder:
    @staticmethod
    def build_zip(source_dir: Path, zip_path: Path) -> Path:
        if zip_path.exists():
            zip_path.unlink()

        with ZipFile(zip_path, "w", ZIP_DEFLATED) as zip_file:
            for file_path in source_dir.rglob("*"):
                if file_path.is_file():
                    zip_file.write(
                        file_path,
                        arcname=file_path.relative_to(source_dir),
                    )

        return zip_path
