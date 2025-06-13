import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageDraw

import image_utils
from puzzle_logic import Puzzle


TILE_SIZE = 100
GRID_SIZE = 4
WINDOW_SIZE = TILE_SIZE * GRID_SIZE


class PuzzleGUI:
    """Tkinter GUI for the sliding puzzle game."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Sliding Puzzle")
        self.root.resizable(False, False)
        self.puzzle = Puzzle(GRID_SIZE)
        self.tile_imgs = []
        self.buttons = []
        self.empty_img = self._create_empty_tile()
        self.move_label = tk.Label(root, text="Moves: 0")
        self.move_label.pack()
        self.board = tk.Frame(root, width=WINDOW_SIZE, height=WINDOW_SIZE)
        self.board.pack()
        self.create_menu()
        self.load_image()
        self.root.bind("<Key>", self.on_key)

    def create_menu(self) -> None:
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def _create_empty_tile(self) -> ImageTk.PhotoImage:
        """Return a placeholder image for the blank tile."""
        img = Image.new("RGB", (TILE_SIZE, TILE_SIZE), "white")
        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, TILE_SIZE - 1, TILE_SIZE - 1), outline="gray")
        return ImageTk.PhotoImage(img)

    def load_image(self) -> None:
        path = filedialog.askopenfilename(
            title="Select image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")],
        )
        if not path or not os.path.exists(path):
            return
        img = image_utils.load_image(path, WINDOW_SIZE)
        tiles = image_utils.slice_image(img, GRID_SIZE)
        self.tile_imgs = [ImageTk.PhotoImage(t) for t in tiles]
        self.puzzle.reset()
        self.puzzle.shuffled()
        if self.buttons:
            for btn in self.buttons:
                btn.destroy()
            self.buttons.clear()
        for i in range(GRID_SIZE ** 2):
            img = (
                self.tile_imgs[self.puzzle.tiles[i]]
                if self.puzzle.tiles[i] != self.puzzle.blank
                else self.empty_img
            )
            btn = tk.Button(
                self.board,
                command=lambda idx=i: self.on_click(idx),
                image=img,
            )
            if self.puzzle.tiles[i] == self.puzzle.blank:
                btn.config(state=tk.DISABLED)
            btn.grid(row=i // GRID_SIZE, column=i % GRID_SIZE)
            self.buttons.append(btn)
        self.update_board()

    def update_board(self) -> None:
        for i, btn in enumerate(self.buttons):
            tile_index = self.puzzle.tiles[i]
            if tile_index == self.puzzle.blank:
                btn.config(image=self.empty_img, state=tk.DISABLED)
            else:
                btn.config(image=self.tile_imgs[tile_index], state=tk.NORMAL)
        self.move_label.config(text=f"Moves: {self.puzzle.moves}")
        if self.puzzle.is_solved():
            messagebox.showinfo("Puzzle", "Congratulations! You solved it!")

    def on_click(self, idx: int) -> None:
        if self.puzzle.move_tile(idx):
            self.update_board()

    def on_key(self, event: tk.Event) -> None:
        moved = False
        if event.keysym == "Up":
            moved = self.puzzle.move_blank(1, 0)
        elif event.keysym == "Down":
            moved = self.puzzle.move_blank(-1, 0)
        elif event.keysym == "Left":
            moved = self.puzzle.move_blank(0, 1)
        elif event.keysym == "Right":
            moved = self.puzzle.move_blank(0, -1)
        if moved:
            self.update_board()


def main() -> None:
    root = tk.Tk()
    PuzzleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
