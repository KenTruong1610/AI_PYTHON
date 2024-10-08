class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.parent = None
        #Thiết lập dữ liệu

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        #Thêm nút con

    def getlevel(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
        #Phân tầng (mức độ)


    def printit(self):
        prefix = (" " * 4 * self.getlevel()) + ("|--" if self.parent else "")
        print(prefix + self.data)
        if self.children:
            for child in self.children:
                child.printit()
        #In cây cấu trúc


def build_tree():
    root = TreeNode("Van Hoa - Cong Trinh")

    France = TreeNode("France")
    France.add_child(TreeNode("Eiffel"))
    France.add_child(TreeNode("Wine"))

    VietNam = TreeNode("VietNam")
    VietNam.add_child(TreeNode("Pho"))
    VietNam.add_child(TreeNode("HaNoi"))
    VietNam.add_child(TreeNode("Banh Mi"))


    root.add_child(France)
    root.add_child(VietNam)

    return root


if __name__ == "__main__":
    root = build_tree()
    root.printit()
