from enum import Enum
from FileSystemExceptions import IllegalFileSystemOperation, PathAlreadyExists, PathNotFound, NotATextFile
import copy


class EntityType(Enum):
    DRIVE = 1
    FOLDER = 2
    TEXTFILE = 3
    ZIPFILE = 4


class TrieNode:
    def __init__(self, content=None, node_name=None, node_size=None):
        self.children = {}
        self.content = content
        self.node_name = node_name
        self.node_size = node_size


root = TrieNode()


class Entity:
    def __init__(self, entity_type=None, name=None, path=None, size=None, content=None):
        self.type = entity_type
        self.name = name
        self.path = path
        self.size = size
        self.content = content

    def update_size(self, current):

        if not current.children:
            return

        current.node_size = 0
        for k, v in current.children.items():

            if current.node_name[1] == EntityType.TEXTFILE:
                node_size = 0
                for k1, v1 in current.children.items():
                    node_size += v1.content.size
                return node_size
            else:
                node_size = self.update_size(v)
            if node_size:
                current.node_size += node_size

        return current.node_size

    def create(self, entity_type, name, path, content=None):
        current = root

        tree = path.split("/")
        for path_name in tree[1:]:
            if path_name not in current.children:
                raise PathNotFound
            current = current.children[path_name]
        if content:
            entity = Entity(entity_type, name, path, len(content), content)
        else:
            entity = Entity(entity_type, name, path, 0)
        if current.children and name in current.children:
            raise PathAlreadyExists
        current.children[name] = TrieNode(entity)
        current.node_name = (name, entity_type)
        current.content = content
        current.node_size = len(content) if content else 0
        # Update the size of file system
        self.update_size(root)

        return f'********************{entity_type} created********************', current

    def delete(self, path):

        current = root
        tree = path.split("/")
        file_to_be_deleted = tree[-1]
        # file_path_of_deleted_node = {}
        for path_name in tree[1:]:
            if path_name not in current.children:
                raise PathNotFound

            if path_name == file_to_be_deleted:
                file_path_of_deleted_node = copy.deepcopy(current)
                current.children.pop(path_name)
                current.content = None
                current.node_name = None
                print(f"!!{file_to_be_deleted} is deleted!!")
                return f"!!{file_to_be_deleted} is deleted!!", file_path_of_deleted_node

            current = current.children[path_name]

    def move(self, source_path, destination_path):
        values = self.delete(source_path)
        current = values[1]
        name = destination_path.split("/")[-1]
        destination_path = destination_path.replace("/folder1", "")
        node_created = self.create(current.node_name[1], name, destination_path)
        node_created[1].children = current.children


class Drive(Entity):

    def create(self, entity_type, name, path):
        count_slash = 0
        for character in path:
            if character == "/":
                count_slash += 1
            if count_slash > 2:
                raise IllegalFileSystemOperation

        current = root
        entity = Entity(entity_type, name, path, 0)
        if current.children and name in current.children:
            raise PathAlreadyExists
        current.children[name] = TrieNode(entity)
        current.node_name = (name, entity_type)
        return f'********************{entity_type} created********************'


class File(Entity):
    def write_to_file(self, path, content):
        current = root

        tree = path.split("/")[1:]
        file_to_be_modified = tree[-1]
        for path_name in tree:
            if path_name not in current.children:
                raise PathNotFound
            if file_to_be_modified == path_name:
                if current.node_name[1] == EntityType.TEXTFILE:
                    current.content = content
                    current.node_size = len(content)
                    self.update_size(root)
                    print("!Current file content updated!")

                    return "!Current file content updated!"
                else:
                    raise NotATextFile
            current = current.children[path_name]

#
# if __name__ == '__main__':
#     drive1 = Drive()
#     drive1.create(EntityType.DRIVE, "drive1", "/")
#     folder1 = Entity()
#     folder1.create(EntityType.FOLDER, "folder1", "/drive1")
#     print(root)
#     text_file = File()
#     text_file.create(EntityType.TEXTFILE, "text_file1", "/drive1/folder1", "Hello")
#     print(root)
#     text_file.write_to_file("/drive1/folder1/text_file1", "Hello World!")
#     print(root)
#
#     text_file.create(EntityType.TEXTFILE, "text_file2", "/drive1/folder1", "Hello 123")
#     print(root)
#
#
# zip_file = Entity()
# zip_file.create(EntityType.ZIPFILE, "zip_file1", "/drive1")

# drive1.create(EntityType.DRIVE, "drive2", "/")
# folder1.move("/drive1/folder1", "/drive2/folder1")
# text_file.write_to_file("/drive2/folder1/text_file1", "Hello World!!")
