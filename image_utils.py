from PIL import Image


def load_image(path: str, size: int) -> Image.Image:
    """Load an image, crop to a square, and resize to ``size`` x ``size``."""
    img = Image.open(path).convert("RGB")
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    img = img.crop((left, top, left + min_dim, top + min_dim))
    img = img.resize((size, size), Image.LANCZOS)
    return img


def slice_image(img: Image.Image, grid_size: int = 4) -> list:
    """Slice the ``img`` into ``grid_size``**2 tiles and return them."""
    tile_size = img.width // grid_size
    tiles = []
    for row in range(grid_size):
        for col in range(grid_size):
            left = col * tile_size
            upper = row * tile_size
            tile = img.crop((left, upper, left + tile_size, upper + tile_size))
            tiles.append(tile)
    return tiles
