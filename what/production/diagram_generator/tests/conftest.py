"""Shared fixtures — one ``DiagramInput`` per diagram type + the default built canvas doc.

The ``flowchart`` fixture deliberately contains a **cycle** (c -> a) to prove a cyclic graph validates (its edges are
tagged ``dependency``, not the acyclicity-checked ``sequence``).
"""

from __future__ import annotations

import pytest

from diagram_generator.consume import build_diagram
from diagram_generator.model import DiagramEdge, DiagramInput, DiagramNode


@pytest.fixture
def flowchart() -> DiagramInput:
    return DiagramInput(
        title="Cyclic flowchart",
        id="urn:adna:canvas:diagram:flow",
        version="0.1.0",
        diagram_type="flowchart",
        direction="TD",
        refs=("[[spec_adna_canvas_standard]]",),
        nodes=(
            DiagramNode(id="a", label="Start", shape="round"),
            DiagramNode(id="b", label="Work", shape="rect"),
            DiagramNode(id="c", label="Check", shape="diamond"),
        ),
        edges=(
            DiagramEdge(from_id="a", to_id="b"),
            DiagramEdge(from_id="b", to_id="c"),
            DiagramEdge(from_id="c", to_id="a", label="retry"),  # the cycle
        ),
    )


@pytest.fixture
def sequence() -> DiagramInput:
    return DiagramInput(
        title="A handshake",
        id="urn:adna:canvas:diagram:seq",
        version="0.1.0",
        diagram_type="sequence",
        nodes=(DiagramNode(id="Client"), DiagramNode(id="Server")),
        edges=(
            DiagramEdge(from_id="Client", to_id="Server", label="request", relation="message"),
            DiagramEdge(from_id="Server", to_id="Client", label="response", relation="message"),
        ),
    )


@pytest.fixture
def class_diagram() -> DiagramInput:
    return DiagramInput(
        title="A small model",
        id="urn:adna:canvas:diagram:cls",
        version="0.1.0",
        diagram_type="class_diagram",
        nodes=(
            DiagramNode(id="Animal", members=("+name: str", "+speak()")),
            DiagramNode(id="Dog", members=("+breed: str",)),
        ),
        edges=(DiagramEdge(from_id="Dog", to_id="Animal", relation="inherits"),),
    )


@pytest.fixture
def state_diagram() -> DiagramInput:
    return DiagramInput(
        title="A lifecycle",
        id="urn:adna:canvas:diagram:state",
        version="0.1.0",
        diagram_type="state_diagram",
        nodes=(
            DiagramNode(id="Idle", shape="circle"),
            DiagramNode(id="Running", shape="circle"),
        ),
        edges=(
            DiagramEdge(from_id="Idle", to_id="Running", label="start", relation="transition"),
            DiagramEdge(from_id="Running", to_id="Idle", label="stop", relation="transition"),  # cycle ok
        ),
    )


@pytest.fixture
def gantt() -> DiagramInput:
    return DiagramInput(
        title="A plan",
        id="urn:adna:canvas:diagram:gantt",
        version="0.1.0",
        diagram_type="gantt",
        nodes=(
            DiagramNode(id="design", label="2d"),
            DiagramNode(id="build", label="3d"),
            DiagramNode(id="ship", label="1d"),
        ),
        edges=(
            DiagramEdge(from_id="design", to_id="build"),
            DiagramEdge(from_id="build", to_id="ship"),
        ),
    )


@pytest.fixture
def all_types(flowchart, sequence, class_diagram, state_diagram, gantt) -> dict[str, DiagramInput]:
    return {
        "flowchart": flowchart,
        "sequence": sequence,
        "class_diagram": class_diagram,
        "state_diagram": state_diagram,
        "gantt": gantt,
    }


@pytest.fixture
def diagram(flowchart: DiagramInput) -> DiagramInput:
    return flowchart


@pytest.fixture
def doc(diagram: DiagramInput) -> dict:
    return build_diagram(diagram)
