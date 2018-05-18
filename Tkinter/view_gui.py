from view import FileView
from tkinter import *
from tkinter import simpledialog
#David De La Cruz
def main():
    display = str()
    v = view_gui("yankee.txt")

    root = Tk()
    root.title(v.fname + " - " + "Page %s" % v.current_page)
    main_frame = Frame(root, width=300)
    main_frame.pack(expand=True, fill=BOTH)
    main_frame.show = Text(main_frame, width=50, height=40, wrap =NONE)
    main_frame.scrollbar = Scrollbar(main_frame, orient=HORIZONTAL, command=main_frame.show.xview)
    main_frame.scrollbar.pack(side=BOTTOM, fill=X)
    main_frame.show.pack(side=TOP, expand=True, fill=BOTH)
    main_frame.show.configure(xscrollcommand=main_frame.scrollbar.set, state=NORMAL)

    v.file.seek(v.pages[int(v.current_page) - 1])
    for x in range(v.view_size):
        display = display + v.file.readline() + "\n"
    main_frame.show.insert(1.0, display)
    main_frame.show.config(state=DISABLED)

    topbutton = Button(main_frame, text="Top", command=lambda: top(root, main_frame, v))
    upbutton = Button(main_frame, text="Up", command=lambda: up(root, main_frame, v))
    downbutton = Button(main_frame,text="Down", command=lambda: down(root, main_frame, v))
    buttombutton = Button(main_frame, text="Bottom", command=lambda: bottom(root, main_frame, v))
    pagebutton = Button(main_frame, text="Page", command=lambda: page(root, main_frame, v))
    quitbutton = Button(main_frame, text="Quit", command=lambda: q(root, v))

    topbutton.pack(side=LEFT, expand=True, fill=X)
    upbutton.pack(side=LEFT, expand=True, fill=X)
    downbutton.pack(side=LEFT, expand=True, fill=X)
    buttombutton.pack(side=LEFT, expand=True, fill=X)
    pagebutton.pack(side=LEFT, expand=True, fill=X)
    quitbutton.pack(side=LEFT, expand=True, fill=X)

    main_frame.show.pack()

    root.mainloop()


def top(root, main_frame, v):
    display = str()
    main_frame.show.config(state=NORMAL)
    main_frame.show.delete(1.0, END)
    v.select_top_page()
    root.title(v.fname + " - " + "Page %s" % v.current_page)
    v.file.seek(v.pages[int(v.current_page) - 1])
    for x in range(v.view_size):
        display = display + v.file.readline() + "\n"
    main_frame.show.insert(1.0, display)
    main_frame.show.config(state=DISABLED)


def bottom(root, main_frame, v):
    display = str()
    main_frame.show.config(state=NORMAL)
    main_frame.show.delete(1.0, END)
    v.select_bottom_page()
    root.title(v.fname + " - " + "Page %s" % v.current_page)
    v.file.seek(v.pages[int(v.current_page) - 1])
    for x in range(v.view_size):
        display = display + v.file.readline() + "\n"
    main_frame.show.insert(1.0, display)
    main_frame.show.config(state=DISABLED)


def up(root, main_frame, v):
    display = str()
    main_frame.show.config(state=NORMAL)
    main_frame.show.delete(1.0, END)
    v.next_page('u')
    root.title(v.fname + " - " + "Page %s" % v.current_page)
    v.file.seek(v.pages[int(v.current_page) - 1])
    for x in range(v.view_size):
        display = display + v.file.readline() + "\n"
    main_frame.show.insert(1.0, display)
    main_frame.show.config(state=DISABLED)


def down(root, main_frame, v):
    display = str()
    main_frame.show.config(state=NORMAL)
    main_frame.show.delete(1.0, END)
    v.next_page('d')
    root.title(v.fname + " - " + "Page %s" % v.current_page)
    v.file.seek(v.pages[int(v.current_page) - 1])
    for x in range(v.view_size):
        display = display + v.file.readline() + "\n"
    main_frame.show.insert(1.0, display)
    main_frame.show.config(state=DISABLED)


def page(root, main_frame, v):
    num = simpledialog.askinteger("Page Number", "Enter page number")
    if num is not None:
        v.select_page(num)
    display = str()
    main_frame.show.config(state=NORMAL)
    main_frame.show.delete(1.0, END)
    root.title(v.fname + " - " + "Page %s" % v.current_page)
    v.file.seek(v.pages[int(v.current_page) - 1])
    for x in range(v.view_size):
        display = display + v.file.readline() + "\n"
    main_frame.show.insert(1.0, display)
    main_frame.show.config(state=DISABLED)


def q(root, v):
    v.file.close()
    root.destroy()


def view_gui(fname, view_size=20):
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    if len(sys.argv) > 2:
        view_size = int(sys.argv[2])
    v = FileView(fname, view_size)
    return v


if __name__ == '__main__':
    main()
