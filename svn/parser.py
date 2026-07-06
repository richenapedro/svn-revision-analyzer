import xml.etree.ElementTree as ET

from svn.models import ChangedPath, Revision


def parse_log_xml(xml_content: str) -> list[Revision]:
    root = ET.fromstring(xml_content)

    revisions: list[Revision] = []

    for logentry in root.findall("logentry"):
        revision_number = int(logentry.attrib["revision"])

        author = _get_text(logentry, "author")
        date = _get_text(logentry, "date")
        message = _get_text(logentry, "msg")

        changed_paths: list[ChangedPath] = []

        paths_element = logentry.find("paths")
        if paths_element is not None:
            for path_element in paths_element.findall("path"):
                changed_paths.append(
                    ChangedPath(
                        path=path_element.text or "",
                        action=path_element.attrib.get("action", ""),
                    )
                )

        revisions.append(
            Revision(
                revision=revision_number,
                author=author,
                date=date,
                message=message,
                changed_paths=changed_paths,
            )
        )

    return revisions


def _get_text(parent: ET.Element, tag: str) -> str:
    element = parent.find(tag)
    return element.text if element is not None and element.text else ""
