from __future__ import annotations
from typing import override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        html = ""

        if self.props is not None:
            for k, v in self.props.items():
                html += f' {k}="{v}"'

        return html

    @override
    def __repr__(self):
        raise NotImplementedError


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, None, props)

    @override
    def to_html(self) -> str:
        if not self.value:
            raise ValueError("Leaf Node missing value")

        if not self.tag:
            return self.value

        props_html = ""
        if self.props:
            props_html = super().props_to_html()

        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

    @override
    def __repr__(self):
        return (
            f"\n   LeafNode(Tag: {self.tag}, Value: {self.value}, Props: {self.props})"
        )


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)

    @override
    def to_html(self):
        if not self.tag:
            raise ValueError("Parent node missing tags")
        elif not self.children:
            raise ValueError("Parent node mising children")

        children_html: str = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}>{children_html}</{self.tag}>"

    @override
    def __repr__(self):
        return f"\nParentNode(Tag: {self.tag}, Children: \n{self.children}\n, Props: {self.props})"
