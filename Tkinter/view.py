import sys
#David De La Cruz

class FileView:
    def __init__(self, fname, view_size):
        self.fname = fname
        self.view_size = view_size
        self.pages = list()
        self.current_page = 1
        self.file = open(fname, "r")
        self.pages.append(self.file.tell())
        index = 1
        line = self.file.readline()
        while line:
            line = self.file.readline()
            index = index + 1
            if index % view_size == 0:
                self.pages.append(self.file.tell())

    def next_page(self, direction):
        if direction == 'u':
            if self.current_page == 1:
                self.current_page = len(self.pages)
            else:
                self.current_page = self.current_page -1
        else:
            if self.current_page == len(self.pages):
                self.current_page = 1
            else:
                self.current_page = self.current_page + 1

    def select_page(self, number):
        if int(number) > len(self.pages):
            self.select_bottom_page()
        elif int(number) <= 0:
            self.select_top_page()
        else:
            self.current_page = number

    def select_top_page(self):
        self.current_page = 1

    def select_bottom_page(self):
        self.current_page = len(self.pages)


def view(fname, view_size=25):
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    if len(sys.argv) > 2:
        view_size = int(sys.argv[2])
    v = FileView(fname, view_size)
    while True:
        v.file.seek(v.pages[int(v.current_page) - 1])
        print("[Page %s]" % v.current_page)
        for x in range(v.view_size):
            print(v.file.readline())
        answer = input("Command [u,d,t,b,#,q]: ")
        if answer == 'q':
            v.file.close()
            break
        elif answer == 'u' or answer == 'd':
            v.next_page(answer)
        elif answer == 't':
            v.select_top_page()
        elif answer == 'b':
            v.select_bottom_page()
        elif answer == '':
            v.next_page('d')
        else:
            try:
                if int(answer):
                    v.select_page(answer)
            except ValueError:
                v.next_page('d')


def main():
    pass


if __name__ == '__main__':
    view("yankee.txt")
    main()

