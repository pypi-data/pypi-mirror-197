import html

from ansi2html import Ansi2HTMLConverter


def fence_code_format(source: str, _language, class_name, _options, _md, **kwargs):
    ansi = Ansi2HTMLConverter(inline=True)
    output = ansi.convert(html.escape(source, quote=False), full=False)

    classes = kwargs["classes"]
    id_value = kwargs["id_value"]
    attrs = kwargs["attrs"]

    if class_name:
        classes.insert(0, class_name)

    id_value = f' id="{id_value}"' if id_value else ""
    classes = f' class="{" ".join(classes)}"' if classes else ""
    attrs = " " + " ".join(f'{k}="{v}"' for k, v in attrs.items()) if attrs else ""

    return f"<pre{id_value}{classes}{attrs}><code>{output}</code></pre>"
