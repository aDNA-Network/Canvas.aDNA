"""gdoc_export — Google Doc carrier substrate for canvas artifacts.

Exports canvas-element streams (paragraphs, headings, bullet lists, inline
images) to a new Google Doc, preserving structure, optional Pillar B
typography tokens, and full-resolution Imagen 4 Ultra image sources via
Drive multipart upload (not base64-inline — Drive carriage avoids Google
re-encoding on the Docs side per ADR-011 §D3).

Substrate-neutral per ADR 001 § Substrate Scope — the doc-export carrier
is application-agnostic; consumers (deck pipelines, comic pipelines,
diagram pipelines, future applications) assemble `DocElement` streams
and hand them to `GdocExporter` / `export_canvas_to_gdoc`.

Authored at M-V1-2-D-01 S1 (2026-05-28) per Pillar D charter and Stanley
auth-model election (AskUserQuestion 2026-05-28): service-account JSON +
share-on-save, MVP element scope (Paragraph + Heading(1-3) + BulletList +
InlineImage), and Exit Gate (b) round-trip deferral per ADR-011 §D6.
Library election: `google-api-python-client` + `google-auth` (first-party
Google; ~5 transitive deps) over zero-dep hand-rolled JWT/REST — the
"lean reuse" analog at this scope (ADR-011 §D1).

Substrate-additive opt-in-gated discipline (Memory A
`feedback_substrate_additive_opt_in_gated_pattern.md`): this module is
pure additive. No mutation to `canvas_core/print.py`, `pdf_export.py`,
`html_renderer.py`, `design_tokens.py`, or `typography.py` public API.
`typography_tokens` defaults to `None` — opt-in style mapping; consumers
pass `TYPOGRAPHY_TOKENS_PUBLICATION` (or any `TypographyToken`) to
activate Pillar B token-driven font/size/weight emission. Re-baseline
gate Q5 does NOT fire (CR1 LOCKED for Pillar D by charter; Wilhelm 8.80
+ Issue 01 8.43 baselines preserved verbatim).

Re-merge rationale: lattice-labs/who/coordination/coord_2026_04_16_forge_split.md
(2026-04-16 canvas-as-substrate collapse made the canvas the load-bearing
primitive; Google Doc export is the fourth substrate carrier — alongside
HTML, JPG/CMYK print, and PDF — riding the same primitive).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Literal, Union

from PIL import Image

from .typography import TypographyToken


__all__ = [
    "DocElement",
    "Paragraph",
    "Heading",
    "BulletList",
    "InlineImage",
    "GdocExporter",
    "export_canvas_to_gdoc",
    "GdocAuthError",
    "GdocApiError",
]


# --- Constants -----------------------------------------------------------

_DOCS_SCOPES = (
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
)

_DEFAULT_SECRETS_PATH = Path.home() / ".lattice" / "secrets.json"
_SECRETS_KEY = "GOOGLE_DOC_SERVICE_ACCOUNT_PATH"

_HEADING_NAMED_STYLES = {
    1: "HEADING_1",
    2: "HEADING_2",
    3: "HEADING_3",
}

_PARAGRAPH_ROLE_NAMED_STYLES = {
    "display": "TITLE",
    "h1": "HEADING_1",
    "h2": "HEADING_2",
    "h3": "HEADING_3",
    "body": "NORMAL_TEXT",
    "caption": "NORMAL_TEXT",
    "label": "NORMAL_TEXT",
}

ElementRole = Literal["display", "h1", "h2", "h3", "body", "caption", "label"]


# --- Exceptions ----------------------------------------------------------


class GdocAuthError(RuntimeError):
    """Raised when service-account credential resolution or validation fails."""


class GdocApiError(RuntimeError):
    """Raised when the Docs or Drive API rejects a request."""


# --- Element dataclasses -------------------------------------------------


@dataclass(frozen=True)
class Paragraph:
    """Plain paragraph (NORMAL_TEXT or role-mapped namedStyleType)."""

    text: str
    role: ElementRole = "body"

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError(
                f"Paragraph.text must be str, got {type(self.text).__name__}"
            )
        if self.role not in _PARAGRAPH_ROLE_NAMED_STYLES:
            raise ValueError(
                f"Paragraph.role must be one of "
                f"{sorted(_PARAGRAPH_ROLE_NAMED_STYLES)}, got {self.role!r}"
            )


@dataclass(frozen=True)
class Heading:
    """Heading (level 1-3 maps to HEADING_1..HEADING_3)."""

    text: str
    level: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.text, str):
            raise TypeError(
                f"Heading.text must be str, got {type(self.text).__name__}"
            )
        if self.level not in _HEADING_NAMED_STYLES:
            raise ValueError(
                f"Heading.level must be 1, 2, or 3; got {self.level!r}"
            )


@dataclass(frozen=True)
class BulletList:
    """Bullet list (unordered = disc-circle-square; ordered = numbered decimal)."""

    items: list[str]
    ordered: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.items, list):
            raise TypeError(
                f"BulletList.items must be a list, got {type(self.items).__name__}"
            )
        if not self.items:
            raise ValueError("BulletList.items must contain at least one item")
        for i, item in enumerate(self.items):
            if not isinstance(item, str):
                raise TypeError(
                    f"BulletList.items[{i}] must be str, got {type(item).__name__}"
                )


@dataclass(frozen=True)
class InlineImage:
    """Inline image (PIL.Image or filesystem Path; optional caption + width)."""

    source: Union[Image.Image, Path, str]
    caption: str | None = None
    width_pt: float | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.source, (Image.Image, Path, str)):
            raise TypeError(
                "InlineImage.source must be PIL.Image.Image or Path or str, "
                f"got {type(self.source).__name__}"
            )
        if self.caption is not None and not isinstance(self.caption, str):
            raise TypeError(
                f"InlineImage.caption must be str or None, "
                f"got {type(self.caption).__name__}"
            )


DocElement = Union[Paragraph, Heading, BulletList, InlineImage]


# --- Auth resolution -----------------------------------------------------


def _resolve_credentials_path(credentials_path: str | None) -> Path:
    """Resolve service-account JSON path from arg or ~/.lattice/secrets.json.

    Raises:
        GdocAuthError: if path cannot be resolved or file does not exist.
    """
    if credentials_path:
        path = Path(credentials_path).expanduser()
        if not path.exists():
            raise GdocAuthError(
                f"Service-account credentials file not found: {path}"
            )
        return path

    if not _DEFAULT_SECRETS_PATH.exists():
        raise GdocAuthError(
            f"Secrets vault not found at {_DEFAULT_SECRETS_PATH}; provide "
            f"credentials_path= explicitly or populate the vault per "
            f"~/.claude/projects/...memory/reference_secrets_canonical_location.md"
        )

    try:
        secrets = json.loads(_DEFAULT_SECRETS_PATH.read_text())
    except json.JSONDecodeError as exc:
        raise GdocAuthError(
            f"Failed to parse {_DEFAULT_SECRETS_PATH}: {exc}"
        ) from exc

    pointer = secrets.get(_SECRETS_KEY)
    if not pointer:
        raise GdocAuthError(
            f"Key {_SECRETS_KEY!r} missing from {_DEFAULT_SECRETS_PATH}; add "
            f"a pointer entry per ADR-011 §D1 (Pillar D credential onboarding)"
        )

    path = Path(str(pointer)).expanduser()
    if not path.exists():
        raise GdocAuthError(
            f"Service-account file pointed to by {_SECRETS_KEY} not found: {path}"
        )
    return path


def _build_services(credentials_path: Path) -> tuple[object, object]:
    """Build Docs + Drive service clients from a service-account JSON path.

    Imported lazily so the module can be inspected (and tested for
    substrate-neutrality) without requiring google libs at import time.
    """
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise GdocAuthError(
            "google-api-python-client + google-auth are required for "
            "Google Doc export; install via `pip install google-api-python-client "
            "google-auth` (ADR-011 §D1)"
        ) from exc

    try:
        credentials = service_account.Credentials.from_service_account_file(
            str(credentials_path), scopes=list(_DOCS_SCOPES)
        )
    except Exception as exc:
        raise GdocAuthError(
            f"Failed to load service-account credentials from {credentials_path}: {exc}"
        ) from exc

    docs = build("docs", "v1", credentials=credentials, cache_discovery=False)
    drive = build("drive", "v3", credentials=credentials, cache_discovery=False)
    return docs, drive


# --- Style mapping (Pillar B token consumption; opt-in) ------------------


def _text_style_from_token(token: TypographyToken | None, role: ElementRole | str) -> dict:
    """Map a Pillar B TypographyToken + element role to a Docs textStyle.

    Maps the subset of token fields that Docs textStyle natively supports:
    `font_family_body` / `font_family_heading` → `weightedFontFamily`;
    `weight_h1/h2/h3/body` → `weightedFontFamily.weight` + `bold` flag.

    Returns an empty dict when ``token`` is None (Memory A default-None
    opt-in semantics: no style overrides emitted; Docs default styling
    applies). Font-size, kerning, optical-sizing, tracking, and
    line-height-multiplier mappings are deferred per ADR-011 §D5 (Docs
    textStyle does not natively support all of them; size mapping
    requires a design_tokens.TYPE_SIZES px→pt translation that is
    out-of-MVP-scope).
    """
    if token is None:
        return {}

    style: dict = {}

    is_heading = role in ("display", "h1", "h2", "h3")
    family = token.font_family_heading if is_heading else token.font_family_body
    weight: int | None = None
    if role == "h1":
        weight = token.weight_h1
    elif role == "h2":
        weight = token.weight_h2
    elif role == "h3":
        weight = token.weight_h3
    elif role == "body":
        weight = token.weight_body

    if family:
        wff: dict = {"fontFamily": family}
        if weight is not None:
            wff["weight"] = weight
        style["weightedFontFamily"] = wff

    if weight is not None:
        style["bold"] = weight >= 600

    return style


# --- Image upload (Drive multipart; preserves Imagen 4 Ultra full-res) ---


def _image_to_bytes(image: Image.Image) -> tuple[bytes, str]:
    """Serialize a PIL image to bytes for Drive upload.

    PNG for lossless preservation (preserves Imagen 4 Ultra full-resolution
    source pixels; no Google re-encoding visible per ADR-011 §D3).
    """
    import io

    buffer = io.BytesIO()
    # Convert CMYK to RGB for Google compatibility (CMYK images upload but
    # Docs renders RGB; conversion stays here, not mutating source).
    if image.mode == "CMYK":
        image_rgb = image.convert("RGB")
        image_rgb.save(buffer, format="PNG", optimize=False, compress_level=0)
    else:
        image.save(buffer, format="PNG", optimize=False, compress_level=0)
    return buffer.getvalue(), "image/png"


def _upload_image_to_drive(drive_service, image_source, title: str) -> str:
    """Upload an image to Drive via multipart; return public-link URI.

    Sets `anyone with link` reader permission so the Docs API can fetch
    the image when resolving `insertInlineImage`. Returns the direct image
    URL suitable for the `uri` field.

    Raises:
        GdocApiError: if Drive upload or permission grant fails.
    """
    try:
        from googleapiclient.http import MediaIoBaseUpload
        import io
    except ImportError as exc:
        raise GdocAuthError(
            "googleapiclient required for image upload; see ADR-011 §D1"
        ) from exc

    if isinstance(image_source, Image.Image):
        data, mime = _image_to_bytes(image_source)
    elif isinstance(image_source, (str, Path)):
        path = Path(str(image_source))
        if not path.exists():
            raise GdocApiError(f"InlineImage source path not found: {path}")
        data = path.read_bytes()
        suffix = path.suffix.lower().lstrip(".")
        mime = f"image/{suffix if suffix in ('png', 'jpeg', 'jpg', 'webp') else 'png'}"
        if suffix == "jpg":
            mime = "image/jpeg"
    else:
        raise GdocApiError(
            f"Unsupported InlineImage source type: {type(image_source).__name__}"
        )

    media = MediaIoBaseUpload(io.BytesIO(data), mimetype=mime, resumable=False)
    try:
        uploaded = (
            drive_service.files()
            .create(body={"name": title}, media_body=media, fields="id")
            .execute()
        )
        file_id = uploaded["id"]
        drive_service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"},
            fields="id",
        ).execute()
    except Exception as exc:
        raise GdocApiError(f"Drive upload failed: {exc}") from exc

    # Direct content URL form that Docs `insertInlineImage` can fetch
    return f"https://drive.google.com/uc?export=view&id={file_id}"


# --- Request builder (pure; testable without network) --------------------


def _build_text_inserts(
    elements: list[DocElement],
    typography_tokens: TypographyToken | None,
) -> tuple[list[dict], list[tuple[DocElement, int, int]]]:
    """Build batchUpdate insertText requests + element-range index.

    Returns:
        (requests, ranges) where `ranges` is a list of
        (element, start_index, end_index) tuples for downstream styling
        passes. Indices are 1-based Docs offsets.
    """
    requests: list[dict] = []
    ranges: list[tuple[DocElement, int, int]] = []
    cursor = 1  # Docs body starts at index 1

    for element in elements:
        if isinstance(element, Paragraph):
            text = element.text + "\n"
        elif isinstance(element, Heading):
            text = element.text + "\n"
        elif isinstance(element, BulletList):
            text = "\n".join(element.items) + "\n"
        elif isinstance(element, InlineImage):
            # Image placeholder: insert a single newline; image replaces
            # this position in pass 3. Caption (if any) follows as a
            # separate insert below.
            text = "\n"
        else:
            raise TypeError(
                f"Unknown DocElement type: {type(element).__name__}"
            )

        if text:
            requests.append({
                "insertText": {
                    "location": {"index": cursor},
                    "text": text,
                }
            })

        start = cursor
        end = cursor + len(text)
        ranges.append((element, start, end))
        cursor = end

        # Caption follows as its own paragraph
        if isinstance(element, InlineImage) and element.caption:
            cap_text = element.caption + "\n"
            requests.append({
                "insertText": {
                    "location": {"index": cursor},
                    "text": cap_text,
                }
            })
            cap_start = cursor
            cap_end = cursor + len(cap_text)
            # Caption tracked as a synthesized Paragraph(role=caption)
            ranges.append((Paragraph(text=element.caption, role="caption"),
                           cap_start, cap_end))
            cursor = cap_end

    return requests, ranges


def _build_style_requests(
    ranges: list[tuple[DocElement, int, int]],
    typography_tokens: TypographyToken | None,
) -> list[dict]:
    """Build paragraph-style + text-style requests from element ranges."""
    requests: list[dict] = []

    for element, start, end in ranges:
        if isinstance(element, Heading):
            named = _HEADING_NAMED_STYLES[element.level]
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": named},
                    "fields": "namedStyleType",
                }
            })
            ts = _text_style_from_token(typography_tokens, f"h{element.level}")
            if ts:
                requests.append({
                    "updateTextStyle": {
                        "range": {"startIndex": start, "endIndex": end},
                        "textStyle": ts,
                        "fields": ",".join(ts.keys()),
                    }
                })
        elif isinstance(element, Paragraph):
            named = _PARAGRAPH_ROLE_NAMED_STYLES[element.role]
            requests.append({
                "updateParagraphStyle": {
                    "range": {"startIndex": start, "endIndex": end},
                    "paragraphStyle": {"namedStyleType": named},
                    "fields": "namedStyleType",
                }
            })
            ts = _text_style_from_token(typography_tokens, element.role)
            if ts:
                requests.append({
                    "updateTextStyle": {
                        "range": {"startIndex": start, "endIndex": end},
                        "textStyle": ts,
                        "fields": ",".join(ts.keys()),
                    }
                })
        elif isinstance(element, BulletList):
            preset = (
                "NUMBERED_DECIMAL_ALPHA_ROMAN"
                if element.ordered
                else "BULLET_DISC_CIRCLE_SQUARE"
            )
            requests.append({
                "createParagraphBullets": {
                    "range": {"startIndex": start, "endIndex": end},
                    "bulletPreset": preset,
                }
            })
        elif isinstance(element, InlineImage):
            # Image insertion handled in a separate pass (needs upload URI)
            pass

    return requests


# --- Exporter ------------------------------------------------------------


@dataclass
class GdocExporter:
    """Stateful Google Doc emitter for canvas-element streams.

    Usage:
        exporter = GdocExporter(title="My deck", share_with=["me@x.com"])
        exporter.add(Heading("Intro", level=1))
        exporter.add(Paragraph("Hello world."))
        exporter.add(BulletList(["a", "b", "c"]))
        exporter.add(InlineImage(source=pil_image, caption="Fig 1"))
        doc_id = exporter.save()
        print(exporter.doc_url)

    Substrate-additive Memory A discipline: ``typography_tokens`` defaults
    to ``None`` (no font/size/weight overrides). Pass a Pillar B
    ``TypographyToken`` (e.g. ``TYPOGRAPHY_TOKENS_PUBLICATION``) to
    activate token-driven style emission.
    """

    title: str
    credentials_path: str | None = None
    typography_tokens: TypographyToken | None = None
    share_with: list[str] = field(default_factory=list)
    _elements: list[DocElement] = field(default_factory=list, init=False, repr=False)
    _doc_id: str | None = field(default=None, init=False, repr=False)

    def add(self, element: DocElement) -> None:
        """Append an element to the document buffer."""
        if not isinstance(element, (Paragraph, Heading, BulletList, InlineImage)):
            raise TypeError(
                "GdocExporter.add expected a DocElement (Paragraph, Heading, "
                f"BulletList, InlineImage); got {type(element).__name__}"
            )
        self._elements.append(element)

    def save(self) -> str:
        """Materialize the document on Google Docs; return its doc_id.

        Three-pass write algorithm (ADR-011 §D4):
            1. Resolve credentials + build Docs/Drive services.
            2. Create empty doc; batchUpdate text inserts + styling.
            3. Upload images to Drive; batchUpdate insertInlineImage at
               tracked positions; grant `share_with` permissions.

        Raises:
            ValueError: if no elements have been added.
            GdocAuthError: if credentials cannot be resolved or loaded.
            GdocApiError: if the Docs or Drive API rejects a request.
        """
        if not self._elements:
            raise ValueError("GdocExporter.save called with no elements added")

        creds_path = _resolve_credentials_path(self.credentials_path)
        docs_service, drive_service = _build_services(creds_path)

        try:
            doc = docs_service.documents().create(
                body={"title": self.title}
            ).execute()
        except Exception as exc:
            raise GdocApiError(f"documents.create failed: {exc}") from exc
        doc_id = doc["documentId"]
        self._doc_id = doc_id

        text_requests, ranges = _build_text_inserts(
            self._elements, self.typography_tokens
        )
        style_requests = _build_style_requests(ranges, self.typography_tokens)

        all_requests = text_requests + style_requests
        if all_requests:
            try:
                docs_service.documents().batchUpdate(
                    documentId=doc_id, body={"requests": all_requests}
                ).execute()
            except Exception as exc:
                raise GdocApiError(f"documents.batchUpdate failed: {exc}") from exc

        # Pass 3: images
        image_requests: list[dict] = []
        for element, start, _end in ranges:
            if isinstance(element, InlineImage):
                uri = _upload_image_to_drive(
                    drive_service, element.source, title=f"{self.title} — image"
                )
                req: dict = {
                    "insertInlineImage": {
                        "location": {"index": start},
                        "uri": uri,
                    }
                }
                if element.width_pt is not None:
                    req["insertInlineImage"]["objectSize"] = {
                        "width": {"magnitude": float(element.width_pt), "unit": "PT"}
                    }
                image_requests.append(req)
        if image_requests:
            try:
                docs_service.documents().batchUpdate(
                    documentId=doc_id, body={"requests": image_requests}
                ).execute()
            except Exception as exc:
                raise GdocApiError(f"insertInlineImage batchUpdate failed: {exc}") from exc

        # Pass 4: share
        for email in self.share_with:
            try:
                drive_service.permissions().create(
                    fileId=doc_id,
                    body={"type": "user", "role": "writer", "emailAddress": email},
                    fields="id",
                    sendNotificationEmail=False,
                ).execute()
            except Exception as exc:
                raise GdocApiError(
                    f"permissions.create for {email} failed: {exc}"
                ) from exc

        return doc_id

    @property
    def doc_url(self) -> str | None:
        """Editable URL for the saved document; None until save() succeeds."""
        if self._doc_id is None:
            return None
        return f"https://docs.google.com/document/d/{self._doc_id}/edit"


def export_canvas_to_gdoc(
    elements: Iterable[DocElement],
    title: str,
    *,
    credentials_path: str | None = None,
    typography_tokens: TypographyToken | None = None,
    share_with: list[str] | None = None,
) -> str:
    """Convenience wrapper: build a GdocExporter, add elements, save, return doc_id.

    Single-call API for the common path where the caller already has the
    full ordered list of canvas elements ready.

    Args:
        elements: ordered iterable of DocElement (Paragraph, Heading,
            BulletList, InlineImage).
        title: document title.
        credentials_path: service-account JSON path. None = resolve from
            ``~/.lattice/secrets.json`` key ``GOOGLE_DOC_SERVICE_ACCOUNT_PATH``.
        typography_tokens: optional Pillar B TypographyToken for font
            mapping. None = no style overrides (Docs default styling).
        share_with: list of email addresses to grant editor access at save().

    Returns:
        the new doc_id (string).

    Raises:
        ValueError: if `elements` is empty.
        GdocAuthError: if credentials cannot be resolved.
        GdocApiError: if Docs or Drive APIs reject a request.
    """
    elements_list = list(elements)
    if not elements_list:
        raise ValueError("export_canvas_to_gdoc called with empty elements")

    exporter = GdocExporter(
        title=title,
        credentials_path=credentials_path,
        typography_tokens=typography_tokens,
        share_with=share_with or [],
    )
    for element in elements_list:
        exporter.add(element)
    return exporter.save()
