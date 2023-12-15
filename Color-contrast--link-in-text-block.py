'''
Last updated 2023-12-15

Color-code suggestions for 'links within blocks of text must be distinguishable without relying 
on color.'

This is only required _when links will not be underlined_, AND you generate the error at
https://www.w3.org/TR/WCAG20-TECHS/F73.html. Give the script your color values for anchor text
and the surrounding text, and it will suggest the 'least discernible difference' between your
non-conformant color and what would be the conformant color that can replace it.

This is based on code suggested by a chatbot. It assumes a white background; the test code
was in an implementation of the U.S. Web Design System framework. The specific focus was on
solving the axe checker's error "link in text block,"
https://dequeuniversity.com/rules/axe/4.8/link-in-text-block?application=AxeChrome

See also:
    https://designsystem.digital.gov/components/link/#what-you-shouldn-t-do-2
    https://www.w3.org/TR/WCAG20-TECHS/G183.html
'''

# One-time setup: pip install Pillow

from PIL import ImageColor

# ---------------------------------------------------------
# Provide your text colors (see your browser's Inspector > Elements
# text_block_color = '#1b1b1b' # for paragraphs
text_block_color = '#1b1b1b' # for lists
current_link_color = '#326295'
# ---------------------------------------------------------


def luminance(r, g, b):
    """Calculate the luminance of a color."""
    a = [r, g, b]
    a = [(component / 255.0) for component in a]
    a = [(component / 12.92 if component <= 0.03928 else ((component + 0.055) / 1.055) ** 2.4) for component in a]
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]

def contrast_ratio(lum1, lum2):
    """Calculate the contrast ratio between two luminances."""
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)

def find_adjusted_color(hex_color, target_ratio, text_lum):
    """Find an adjusted color that meets or exceeds the target contrast ratio."""
    r, g, b = ImageColor.getcolor(hex_color, "RGB")
    for adjustment in range(256):
        adjusted_color = (min(r + adjustment, 255), min(g + adjustment, 255), min(b + adjustment, 255))
        adjusted_lum = luminance(*adjusted_color)
        current_ratio = contrast_ratio(adjusted_lum, text_lum)
        if current_ratio >= target_ratio:
            return '#{:02x}{:02x}{:02x}'.format(*adjusted_color)
    return hex_color


# Calculate luminance of the text color
text_lum = luminance(*ImageColor.getcolor(text_block_color, "RGB"))

# Adjust the background color to achieve the target contrast ratio
adjusted_link_color = find_adjusted_color(current_link_color, 3.1, text_lum)


print(f'Recommendation: Test replacing {current_link_color} with {adjusted_link_color} to meet the 3:1 requirement for links in text blocks.')
print('For example, one option would be to plug the numbers in at https://webaim.org/resources/contrastchecker/')

