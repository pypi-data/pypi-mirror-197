# markdown-ansi

A `pymdownx.superfences` formatter for rendering console output with ANSI colors using [`ansi2html`](https://github.com/pycontribs/ansi2html).

Note: _Only_ ANSI color escape sequences are supported. Other escape sequences should be removed manually.

## Usage

```yaml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: ansi
          class: ansi
          format: !!python/name:markdown_ansi.ansi.fence_code_format
```
