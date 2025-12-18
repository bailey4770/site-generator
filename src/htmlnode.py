from typing import Self, override


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[Self] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[Self] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> None:
        raise NotImplementedError

    def props_to_html(self):
        html = ""

        if self.props is not None:
            for k, v in self.props.items():
                html += f' {k}="{v}"'

        return html

    @override
    def __repr__(self):
        return f"HTMLNode(Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props})"
