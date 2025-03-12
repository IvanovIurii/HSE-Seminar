import pathlib

from language_parser.common.consts import NUMBER, IDENTIFIER


def save_mermaid_to_markdown(node, name):
    node = __assign_mermaid_id(node)

    lines = []
    __append_children(node, lines)

    current_dir = pathlib.Path(__file__).parent.resolve()
    with open(f'{current_dir}/out/{name}.md', "w") as f:
        f.write("```mermaid\n")
        f.write("graph TD\n")
        for line in lines:
            f.write(line + "\n")

        f.write("```\n")


def __append_children(node, list):
    # print all child node declarations
    for child in node.children:
        list.append(f"{child.mermaid_id}[{child.type}:{child.value}]")

    # print all edges from this parent to each child
    for child in node.children:
        if hasattr(node, 'mermaid_id'):
            list.append(f"{node.mermaid_id} --> {child.mermaid_id}")
        else:
            list.append(f"{node.type} --> {child.mermaid_id}")

    for child in node.children:
        if child:
            __append_children(child, list)


def __assign_mermaid_id(node):
    __distinguish_children(node)

    for child in node.children:
        if child:
            parent_mermaid_id = ""
            if hasattr(node, 'mermaid_id'):
                parent_mermaid_id = node.mermaid_id + "_"

            if child.type in [NUMBER, IDENTIFIER]:
                child.mermaid_id = f'{parent_mermaid_id}{node.type}_{child.value.upper()}'
            else:
                child.mermaid_id = f'{parent_mermaid_id}{node.type}_{child.type.upper()}'

            __assign_mermaid_id(child)

    return node


def __distinguish_children(node):
    if (
            node.children
            and len(node.children) > 1
            and all(child.value == node.children[0].value for child in node.children)
    ):
        for idx, child in enumerate(node.children):
            child.value = f"{child.value}_{idx}"
