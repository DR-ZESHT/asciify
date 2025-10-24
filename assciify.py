import argparse
from PIL import Image, ImageOps

DEFAULT_RAMP = "@%#*+=-:. "

def get_args():
    p = argparse.ArgumentParser(description="Convert image to ASCII art")
    p.add_argument("input", help="input image file")
    p.add_argument("--width", "-w", type=int, default=80, help="output character width")
    p.add_argument("--out", "-o", default=None, help="output file (default: stdout)")
    p.add_argument("--invert", action="store_true", help="invert brightness mapping")
    p.add_argument("--color", action="store_true", help="output colored ANSI (requires terminal)")
    p.add_argument("--ramp", default=DEFAULT_RAMP, help="character ramp from dark->light")
    p.add_argument("--contrast", type=float, default=1.0, help="contrast factor (1.0 default)")
    p.add_argument("--brightness", type=float, default=1.0, help="brightness factor (1.0 default)")
    return p.parse_args()

def map_pixel_to_char(value, ramp, invert=False):
    # value: 0 (black) .. 255 (white)
    if invert:
        value = 255 - value
    scale = value / 255
    idx = int(scale * (len(ramp) - 1))
    return ramp[idx]

def ansi_color_for_rgb(r, g, b):
    # use 24-bit ANSI escape
    return f"\x1b[38;2;{r};{g};{b}m"

def image_to_ascii(image_path, width=80, ramp=DEFAULT_RAMP, invert=False,
                   color=False, contrast=1.0, brightness=1.0):
    img = Image.open(image_path).convert("RGB")

    # apply brightness/contrast if requested
    if contrast != 1.0:
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast)
    if brightness != 1.0:
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness)

    # resize preserving aspect ratio; adjust for character aspect (height correction)
    orig_w, orig_h = img.size
    aspect_correction = 0.55  # tweak this if characters look squished/tall
    new_w = width
    new_h = max(1, int((orig_h / orig_w) * new_w * aspect_correction))
    img = img.resize((new_w, new_h), Image.LANCZOS)

    # convert to grayscale for mapping
    gray = ImageOps.grayscale(img)

    lines = []
    px = img.load()
    gpx = gray.load()

    for y in range(img.height):
        line = []
        for x in range(img.width):
            g = gpx[x, y]  # 0..255
            ch = map_pixel_to_char(g, ramp, invert=invert)
            if color:
                r, g_, b = px[x, y]
                ansi = ansi_color_for_rgb(r, g_, b)
                line.append(f"{ansi}{ch}\x1b[0m")
            else:
                line.append(ch)
        lines.append("".join(line))
    return "\n".join(lines)

def main():
    args = get_args()
    art = image_to_ascii(args.input, width=args.width, ramp=args.ramp,
                         invert=args.invert, color=args.color,
                         contrast=args.contrast, brightness=args.brightness)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(art)
        print(f"Wrote ASCII art to {args.out}")
    else:
        print(art)

if __name__ == "__main__":
    main()
