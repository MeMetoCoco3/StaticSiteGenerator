class HTMLnode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        s = ""
        for key, value in self.props.items():
            s += f' {key}="{value}"'
        return s

    def __repr__(self) -> str:
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"


class LeafNode(HTMLnode):
    def __init__(self, tag, value, props=None) -> None:
        # Cuidado aqui con el orden, que el HTMLnode acepta 4 argumentos, y
        # le he estado pasado props, como children, desde hace 20 mins.
        super().__init__(tag, value, props=props)

    def to_html(self):
        # A leaf must have a value
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


def main():
    pass


main()
