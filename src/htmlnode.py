from typing import Union


class HTMLnode:
    def __init__(
        self,
        tag: str = "",
        value: str = "",
        children: list[Union["LeafNode", "ParentNode"]] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        s = ""
        for key, value in self.props.items():
            s += f' {key}="{value}"'
        return s

    def __repr__(self) -> str:
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"


class ParentNode(HTMLnode):
    def __init__(
        self,
        tag: str,
        children: list[Union["LeafNode", "ParentNode"]],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, children=children, props=props)

    def to_html(self) -> str:
        if self.tag is None or self.children is None:
            raise ValueError("Parent Node does not have a children")
        result = f"<{self.tag}>"
        while self.children:
            result += self.children[0].to_html()
            del self.children[0]

        result += f"</{self.tag}>"
        return result


class LeafNode(HTMLnode):
    def __init__(
        self, tag: str, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, props=props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf node does not have a value")

        if self.tag == "":
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        if self.tag == "codeblock":
            return f"<pre><code>{self.value}</code></pre>"
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


def main():
    pass


if __name__ == "__main__":
    main()
