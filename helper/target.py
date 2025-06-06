from .jsondb import *
import shutil, os
from helper.colors import *
import threading
from PIL import Image
import uuid
from subprocess import Popen, PIPE


class Target:
    def __init__(self):
        self.jsondb = JSONDB()
        self.DATATYPES = ["text", "file", "image"]

    def handle_target_add(self, args):
        name = args.name
        check_target = self.jsondb.get(name)
        if check_target != None:
            print(f"{RED}Target name already exist.{RESET}")
            return False
        self.jsondb.create([{name: {}}])
        print(f"{name} created.")

    def handle_data_count(self, count):
        all_ = self.jsondb.count_data()
        print( "[> Target:", all_ )

    def handle_target_list(self, args):
        all_ = self.jsondb.allKeys()
        all_ = list(all_.keys())

        header = f" All Targets "
        border_char = "#"
        border_line = border_char * (len(header) + 4)

        print(f"\n{GREEN}{BOLD}{border_line}{RESET}")
        print(f"{GREEN}{BOLD}{border_char}{border_char}{header.center(len(header) + 1)}{border_char}{RESET}")
        print(f"{GREEN}{BOLD}{border_line}{RESET}")

        for targe_name in all_:
            print(f"{GREEN}[> {RESET} {YELLOW}{targe_name}{RESET}")

        print()

    def handle_target_delete(self, args):
        name = args.target
        check_target = self.jsondb.get(name)

        if check_target == None:
            print("Target not found.")
            return False

        c = input(f"[> {YELLOW}All data and files in {name} will be deleted, continue? y/N {RESET}").lower()
        if c != "y":
            print("canceled.")
            return False

        for k_ in check_target.keys():
            if check_target[k_]["type"] == "file" or check_target[k_]["type"] == "image":
                self.delete_file(check_target[k_]["value"])

        self.jsondb.delete(name)
        print(f"{RED}{name} removed.{RESET}")

    def handle_data_add(self, args):
        name = args.target
        label = args.label
        type_ = args.type
        data = args.value

        check_target = self.jsondb.get(name)
        if check_target == None:
            print(f"{RED}Target not found.{RESET}")
            return False

        if type_ == None:
            type_ = "text"

        if not  type_.lower() in self.DATATYPES:
            print(f"{RED}invalid data type.{RESET}")
            return True

        delete_previous_file = ""
        if check_target.get(label, None) != None:
            c = input(f"[>{YELLOW}{label} already exist, overwrite? y/N {RESET}").lower()
            if c != "y":
                print("canceled.")
                return False
            else:
                if check_target[label]["type"] == "file" or check_target[label]["type"] == "image":
                    delete_previous_file = check_target[label]["value"]

        check_target[label] = {"type": type_, "value": data}

        if type_ == "file" or type_ == "image":
            src_path = data
            new_filename = ""

            ext = data.split(".")
            if len( ext ) > 1:
               ext = "." + ext[-1]
            else:
               ext = ""

            while True:
                new_filename  = uuid.uuid4().hex
                if not os.path.exists( os.path.join( FILE_DIRECTORY, new_filename + ext ) ):
                   break

            check_target[label]["value"] = new_filename + ext
            dest_path = FILE_DIRECTORY + new_filename + ext
            shutil.copy(data, dest_path)

        if delete_previous_file != "":
            try:
                self.delete_file(delete_previous_file)
            except:
                pass

        update_data = {}
        update_data[ name ] = check_target
        self.jsondb.update( [update_data] )
        print(f"{GREEN}{label} saved.{RESET}")

    def handle_data_remove(self, args, confirm=True):
        name = args.target
        label = args.label

        check_target = self.jsondb.get(name)
        if check_target == None:
            print(f"{RED}Target not found.{RESET}")
            return False

        if confirm:
            c = input(f"[> {YELLOW}{label} will be delete from {name}, continue? y/N{RESET} ").lower()
            if c != "y":
                print("canceled.")
                return False

        if check_target[label]["type"] == "file" or check_target[label]["type"] == "image":
            self.delete_file(check_target[label]["value"])

        del check_target[label]

        update_data = {}
        update_data[ name ] = check_target
        self.jsondb.update( [update_data] )

        print(f"{RED}{label} removed.{RESET}")

    def delete_file(self, filename):
        os.unlink( FILE_DIRECTORY + filename )

    def dump_dict( self, target_root ):
        check_target = target_root
        for k, val in check_target.items():
            if val["type"] == "text":
                print(
                    f"{GREEN} [>{RESET} {YELLOW}{k}({val['type']}){RESET} {GREEN}:{RESET} {CYAN}{val['value']}{RESET}"
                )
            elif val["type"] == "file" or val["type"] == "image":
                print(
                    f"{YELLOW} [>{RESET} {YELLOW}{k}({val['type']}){RESET} {GREEN}:{RESET} {CYAN}{val['value']}{RESET}"
                )
        print()

    def handle_target_dump(self, args):
        target = args.target
        check_target = self.jsondb.get(target)

        if check_target == None:
            print(f"{RED}Target not found.{RESET}")
            return 0

        header = f" Target: {target} "
        border_char = "#"
        border_line = border_char * (len(header) + 6)

        print(f"\n{GREEN}{BOLD}{border_line}{RESET}")
        print(f"{GREEN}{BOLD}{border_char}{border_char}{header.center(len(header) + 1)}{RESET}")
        print(f"{GREEN}{BOLD}{border_char}{border_char} Data: {len(check_target.keys())}{RESET}")
        print()

        self.dump_dict( check_target )

    def _seek(self, query, target_dict, target_name="", is_dump=False):
        for k in target_dict.keys():
            if query in k:
                part = f"{RED}{query}{RESET}".join( k.split(query) )
                print(f"{GREEN}[> {CYAN}{target_name}.{GREEN}\"{part}\"{RESET}")
                if is_dump:
                    root_ = self.jsondb.get( target_name )
                    self.dump_dict( root_ )
            if query in target_dict[k]["value"]:
                part = f"{RED}{query}{RESET}".join( target_dict[k]["value"].split(query) )
                print(f"{GREEN}[> {CYAN}{target_name}.{YELLOW}{k}{GREEN}[{YELLOW}{target_dict[k]['type']}{GREEN}]={RESET}{GREEN}\"{part}\"{RESET}")
                if is_dump:
                    root_ = self.jsondb.get( target_name )
                    self.dump_dict( root_ )

    def handle_target_search(self, args):
        query = args.query
        target = args.target
        is_dump = args.dump

        if is_dump:
            is_dump = True
        else:
            is_dump = False

        check_target = None

        header = f" Searching: " + query
        within = ""

        border_char = "#"
        border_line = border_char * (len(header) + 6)
        print(f"\n{GREEN}{BOLD}{border_line}{RESET}")
        print(f"{GREEN}{BOLD}{border_char}{header.center(len(header) + 4)}{border_char}{RESET}")
        print(f"{GREEN}{BOLD}{border_line}{RESET}")

        threads = []
        if target:
            check_target = self.jsondb.get(target)
            if check_target == None:
                print(f"{RED}Target not found.{RESET}")
                return 0
            else:
                within = f"Selected target: {target}"
                print(
                    f"{GREEN}{BOLD}{border_char}{within.center(len(within) + 1)}{RESET}"
                )
                print()
                self._seek(query, check_target, target)
        else:
            print()
            alltargets = self.jsondb.allKeys()
            for k in alltargets.keys():
                if query in k:  # search in target name
                    part = f"{RED}{query}{RESET}".join( k.split(query) )
                    print(f"{GREEN}[> {RESET}\"{part}\"{RESET}")
                    if is_dump:
                       root_ = self.jsondb.get( k )
                       self.dump_dict( root_ )

                tmp_part_file = JSONFILE( DATABASE_PATH + DATABASE_FILENAME + str(alltargets[k]) )
                tmp_part_content = tmp_part_file._read_db()
                self._seek(query, tmp_part_content[ k ], k, is_dump )
        print()


    def handle_open_image(self, args):
        path = args.path
        s_path = path.strip("/").split("/")
        check_target = self.jsondb.get(s_path[0])

        if check_target == None:
            print(f"{RED}Target not found.{RESET}")
            return False
        try:
            image_file = check_target[ s_path[-1] ]
            if image_file["type"] != "image":
               print(f"{RED}Failed, it is not an image.{RESET}")
               return 0

            print(f"{YELLOW}[> Showing {image_file["value"]}...{RESET}")
            img = Image.open( os.path.join( FILE_DIRECTORY, image_file["value"] ) )
            img.show()
        except:
            print(f"{RED}Failed to open the image.")

    def handle_open_file(self, args):
        path = args.path
        s_path = path.strip("/").split("/")
        check_target = self.jsondb.get(s_path[0])

        if check_target == None:
            print(f"{RED}Target not found.{RESET}")
            return False
        try:
            _file = check_target[ s_path[-1] ]
            if _file["type"] != "file":
               print(f"{RED}Failed, it is not a file.{RESET}")
               return 0

            print(f"{YELLOW}[> Opening {_file["value"]}...{RESET}")
            Popen( [ "xdg-open",  os.path.join( FILE_DIRECTORY, _file["value"] ) ], stdout=PIPE, stderr=PIPE )
        except Exception as e:
            print(f"{RED}Failed to open the file: {e}")

