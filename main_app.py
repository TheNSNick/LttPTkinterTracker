import tkinter as tk
import os


TILE_SIZE = 64
ITEM_NAMES = {
    (0, 0): 'tunic', (1, 0): 'sword', (2, 0): 'bow', (3, 0): 'boomerang', (4, 0): 'hookshot', (5, 0): 'mushroom', (6, 0): 'powder',
    (0, 1): 'shield', (1, 1): 'moon_pearl', (2, 1): 'fire_rod', (3, 1): 'ice_rod', (4, 1): 'bombos', (5, 1): 'ether', (6, 1): 'quake',
    (0, 2): 'armos', (1, 2): 'ep_chests', (2, 2): 'lantern', (3, 2): 'hammer', (4, 2): 'shovel', (5, 2): 'net', (6, 2): 'book',
    (0, 3): 'lanmola', (1, 3): 'dp_chests', (2, 3): 'bottle', (3, 3): 'somaria', (4, 3): 'byrna', (5, 3): 'cape', (6, 3): 'mirror',
    (0, 4): 'moldorm', (1, 4): 'th_chests', (2, 4): 'boots', (3, 4): 'gloves', (4, 4): 'flippers', (5, 4): 'flute', (6, 4): 'aga',
    (0, 5): 'helmasaur', (1, 5): 'arrghus', (2, 5): 'mothula', (3, 5): 'blind', (4, 5): 'kholdstare', (5, 5): 'vitreous', (6, 5): 'trinexx',
    (0, 6): 'pod_chests', (1, 6): 'sp_chests', (2, 6): 'sw_chests', (3, 6): 'tt_chests', (4, 6): 'ip_chests', (5, 6): 'mm_chests', (6, 6): 'tr_chests'
}
ITEM_VALUES = {'tunic': {'min': 0, 'max': 2}, 'sword': {'min': 0, 'max': 4}, 'bow': {'min': 0, 'max': 3},
               'boomerang': {'min': 0, 'max': 3}, 'mushroom': {'min': 0, 'max': 2}, 'powder': {'min': 0, 'max': 2},
               'shield': {'min': 0, 'max': 3}, 'shovel': {'min': 0, 'max': 2}, 'bottle': {'min': 0, 'max': 4},
               'gloves': {'min': 0, 'max': 2}, 'ep_chests': {'min': 0, 'max': 3}, 'dp_chests': {'min': 0, 'max': 2},
               'th_chests': {'min': 0, 'max': 2}, 'pod_chests': {'min': 0, 'max': 5}, 'sp_chests': {'min': 0, 'max': 6},
               'sw_chests': {'min': 0, 'max': 2}, 'tt_chests': {'min': 0, 'max': 4}, 'ip_chests': {'min': 0, 'max': 3},
               'mm_chests': {'min': 0, 'max': 2}, 'tr_chests': {'min': 0, 'max': 5}
               }


class LttPTrackerApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.resizable(0, 0)                        # make the app non-resizable
        container = tk.Frame(self)                  # main container
        container.pack()
        self.frames = {}
        frame = ItemPane(container, self)
        self.frames[ItemPane] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ItemPane)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()


class ItemPane(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, bg='#000000', width=7*TILE_SIZE, height=7*TILE_SIZE)
        self.canvas.bind('<Button-1>', self.left_click)
        self.canvas.bind('<Button-3>', self.right_click)
        self.canvas_images = {}
        self.items = default_item_values()
        for y in range(7):
            for x in range(7):
                item_name = ITEM_NAMES[(x, y)]
                try:
                    item_image = tk.PhotoImage(file=os.path.join('gfx', '{}_{}.gif'.format(item_name, self.items[item_name]['current'])))
                except:     # TESTING MEASURE -- TODO: REMOVE WHEN IMAGES ARE COMPLETE
                    item_image = tk.PhotoImage(file=os.path.join('gfx', 'BLANK.gif'))
                self.canvas.create_image(x * TILE_SIZE, y * TILE_SIZE, image=item_image, anchor=tk.NW, tags=item_name)
                self.canvas_images[item_name] = item_image
        self.canvas.pack()

    def left_click(self, event):
        """Method called when ItemPane canvas is clicked with left mouse button."""
        item_name = ITEM_NAMES[(event.x // TILE_SIZE, event.y // TILE_SIZE)]
        self.items[item_name]['current'] += 1
        if self.items[item_name]['current'] > self.items[item_name]['max']:
            self.items[item_name]['current'] = self.items[item_name]['min']
        new_image = get_item_image(item_name, self.items[item_name]['current'])
        self.canvas.itemconfigure(item_name, image=new_image)
        self.canvas_images[item_name] = new_image

    def right_click(self, event):
        """Method called when ItemPane canvas is clicked with right mouse button."""
        item_name = ITEM_NAMES[(event.x // TILE_SIZE, event.y // TILE_SIZE)]
        self.items[item_name]['current'] -= 1
        if self.items[item_name]['current'] < self.items[item_name]['min']:
            self.items[item_name]['current'] = self.items[item_name]['max']
        new_image = get_item_image(item_name, self.items[item_name]['current'])
        self.canvas.itemconfigure(item_name, image=new_image)
        self.canvas_images[item_name] = new_image


class LightWorldPane(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)    # TODO


class DarkWorldPane(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)     # TODO


def default_item_values():
    items = ITEM_VALUES
    for _, item_name in ITEM_NAMES.items():
        if item_name not in items.keys():
            items[item_name] = {'min': 0, 'max': 1}
    for item in items:
        items[item]['current'] = items[item]['min']
    return items


def get_item_image(item_name, item_value):
    try:
        image = tk.PhotoImage(file=os.path.join('gfx', '{}_{}.gif'.format(item_name, item_value)))
    except tk.TclError:
        image = tk.PhotoImage(file=os.path.join('gfx', 'BLANK.gif'))
    return image


def main():
    root = LttPTrackerApp()
    root.mainloop()


if __name__ == '__main__':
    main()
