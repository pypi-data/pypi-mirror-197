import re

from mkdocs.plugins import BasePlugin


class ImageCaptionsPlugin(BasePlugin):

    def on_page_markdown(self, markdown: str, **kwargs) -> str:
        """
        Convert incoming MD image element into HTML <figure> with captions

        Args:
            markdown: MD source text of page

        Return:
            Formatted MD text of page
        """
        pattern = re.compile(r'!\[(.*?)\]\((.*?)\)', flags=re.IGNORECASE)
        
        markdown = re.sub(
            pattern,
            r'<figure class="figure-image">\n' +
            r'  <img src="\2" alt="\1">\n' +
            r'  <figcaption>\1</figcaption>\n' +
            r'</figure>',
            markdown
        )

        return markdown
