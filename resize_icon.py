from PIL import Image

def make_square_icon(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    
    # Check aspect ratio
    if w == h:
        print("Already square.")
        img.save(output_path)
        return

    # Create square canvas
    max_dim = max(w, h)
    new_img = Image.new("RGBA", (max_dim, max_dim), (255, 255, 255, 0)) # Transparent background
    
    # Paste centered
    offset_x = (max_dim - w) // 2
    offset_y = (max_dim - h) // 2
    
    new_img.paste(img, (offset_x, offset_y), img)
    new_img.save(output_path)
    print(f"Created square icon: {output_path} ({max_dim}x{max_dim})")

if __name__ == "__main__":
    make_square_icon("app_icon.png", "app_icon_square.png")
