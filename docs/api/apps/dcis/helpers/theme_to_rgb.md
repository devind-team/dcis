# Модуль theme_to_rgb

Конвертер theme types цветов в rgb hex.

### Функции

| Signature                                           | Decorator | Docstring                                                                                                                   |
| :-------------------------------------------------- | :-------- | :-------------------------------------------------------------------------------------------------------------------------- |
| rgb_to_ms_hls(red, green=None, blue=None)           | -         | Converts rgb values in range (0,1) or a hex string of the form '[#aa]rrggbb' to HLSMAX based HLS,(alpha values are ignored) |
| ms_hls_to_rgb(hue, lightness=None, saturation=None) | -         | Converts HLSMAX based HLS values to rgb values in the range (0,1)                                                           |
| rgb_to_hex(red, green=None, blue=None)              | -         | Converts (0,1) based RGB values to a hex string 'rrggbb'                                                                    |
| get_theme_colors(wb)                                | -         | Gets theme colors from the workbook                                                                                         |
| tint_luminance(tint, lum)                           | -         | Tints a HLSMAX based luminance                                                                                              |
| theme_and_tint_to_rgb(wb, theme, tint)              | -         | Given a workbook, a theme number and a tint return a hex based rgb                                                          |