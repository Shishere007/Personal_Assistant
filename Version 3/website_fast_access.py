from pathlib import Path
from tkinter import END, Button, Entry, Label, StringVar, Tk, mainloop, ttk
from data_types import convert, log, website
from file_operation import File
from operations import (
    change_status,
    clear_screen,
    complete_website,
    duplicate,
    get_date_time,
    is_a_website,
    is_input_kill,
    write_log,
)


__name__ = "__website_fast_access__"


class website_fast_access(change_status):
    """
    Save website for fast access with keyword
    """

    def __init__(self) -> None:
        super().__init__()
        self.__website_data_path = "Data/website_data.json"
        self.__website_file = File(file_location=self.__website_data_path)

    def add_website(self) -> None:
        """
        To add website from main section
        """
        self.__read_data_for_new_website()

    def __read_data_for_new_website(self) -> None:
        """
        Read data for adding new website
        """
        try:
            self.__dupe = duplicate(
                data_list=self.__website_file.read_data(), data_type="website"
            )
            website_name = input("website Name : ")
            if is_input_kill(data=website_name):
                return
            site = input("website Location(Full) : ")
            if is_input_kill(data=site):
                return
            if not is_a_website(site=site):
                print("Doesnt seems to be valid website")
                return
            # completes the website by adding 'www' and 'https://'
            site = complete_website(site=site)
            # check if the location is alraedy in list
            if self.__dupe.is_file_exists(location=site):
                print("website is already in list")
                return
            print("Type the keywords for faster access seperated buy comma")
            website_codes = input("website codes : ").split(",")
            if self.__dupe.is_keyword_exist(keyword_list=website_codes):
                print("one of the keyword is already in use")
                return
            if not self.__add_new_website(
                new_website=website(
                    title=website_name, location=site, codes=website_codes
                )
            ):
                print("Unable to add new website")
        except Exception as e:
            print(f"website_fast_access > __read_data_for_new_website- {e}")

    def add_new_website(self, title: str, site: str, codes: str) -> bool:
        """
        to add new website from outside from the class
        """
        try:
            self.__dupe = duplicate(
                data_list=self.__website_file.read_data(), data_type="website"
            )
            if not is_a_website(site=site):
                print("Doesnt seems to be valid website")
                return False
            site = complete_website(site=site)
            if self.__dupe.is_file_exists(location=site):
                print("website is already in list")
                return False
            website_codes = codes.split(",")
            if self.__dupe.is_keyword_exist(keyword_list=website_codes):
                print("one of the keyword is already in use")
                return False
            self.__add_new_website(
                new_website=website(title=title, location=site, codes=website_codes)
            )
            return True
        except Exception as e:
            print(f"website_fast_access > add_new_website- {e}")

    def __add_new_website(self, new_website: website) -> bool:
        """
        Add new website for access
        """
        try:
            if not self.__website_file.append_one_data(data_to_append=new_website):
                return False
            print("New website is added Successfully ")
            self.__change_website_status()
            return True
        except Exception as e:
            print(f"website_fast_access > __add_new_website- {e}")
        return False

    def delete_website(self, user_input: str) -> None:
        """
        To delete a website as completed from main section
        """
        self.__delete_website_read_data(user_input=user_input)

    def __delete_website_read_data(self, user_input: str) -> None:
        """
        Delete a website from list
        """
        try:
            if len(user_input.split()) > 1:
                website_code = " ".join(user_input.split()[1:])
            else:
                website_code = input("website code : ")
            if website_code.isalpha():
                self.__delete_website(website_code=website_code)
            else:
                print("incorrent input")
        except Exception as e:
            print(f"website_fast_access > __delete_website_read_data- {e}")

    def __delete_website(self, website_code: str) -> None:
        try:
            website_list = self.__website_file.read_data()
            for item in website_list:
                if website_code in convert(file_data=item).to_website().get_codes():
                    self.__website_file.delete_one_data(
                        file_data=website_list, data_to_delete=item
                    )
                    self.__change_website_status()
                    print("website deleted from list")
                    return
            else:
                print(f" No website found with '{website_code}' keyword'")
        except Exception as e:
            print(f"website_fast_access > __delete_website- {e}")

    def show_website_list(self) -> None:
        """
        Show all the fast access website list
        """
        try:
            website_list = self.__website_file.read_data()
            if len(website_list) == 0:
                print("list is empty")
                return
            for item in website_list:
                convert(file_data=item).to_website().show()
        except Exception as e:
            print(f"website_fast_access > show_website_list- {e}")

    def website_help(self) -> None:
        """
        Website command list
        """
        print(
            """
            Command list
            -> add/new      add new website to fast access list
            -> del/delete   remove website from list
            -> show         List all website list          
        """
        )

    def __change_website_status(self) -> None:
        """
        change no of website count status data
        """
        try:
            current_status = self._change_status__get_status()
            current_status.set_site_list_count(
                site_count=self.__website_file.line_count()
            )
            self._change_status__write_status_to_file(current_status=current_status)
        except Exception as e:
            print(f"website_fast_access > __change_website_status- {e}")

    def user_section(self) -> bool:
        """
        User section for adding removing website's from list
        """
        try:
            input_list = []
            print("Type break/stop to exit section")
            while True:
                user_input = str(input(">>>"))
                input_list.append(
                    log(
                        user_input=user_input,
                        section="website",
                        date_time=get_date_time(),
                    )
                )
                if (
                    len(set(user_input)) == 0
                    or len(set(user_input)) == 1
                    and not user_input.isalnum()
                ):
                    continue
                if user_input in ["new", "add"]:
                    self.__read_data_for_new_website()
                elif user_input.split()[0] in ["del", "delete"]:
                    self.__delete_website_read_data(user_input=user_input)
                elif user_input in ["help"]:
                    self.website_help()
                elif user_input in ["show"]:
                    self.show_website_list()
                elif user_input in ["status"]:
                    change_status().show_status()
                elif user_input in ["quit", "exit"]:
                    return True
                elif user_input in ["break", "stop", "kill"]:
                    return False
                elif user_input in ["clear"]:
                    clear_screen()
                else:
                    print("incorrect input")

        except Exception as e:
            print(f"website_fast_access > user_section - {e}")
        finally:
            write_log(data_list=input_list)


class add_website_gui:
    """
    GUI to add new website to list
    """

    def __init__(self) -> None:
        self.root = Tk()
        self.root.title(f"Add Website")
        self.root.minsize(500, 300)
        self.root.maxsize(500, 300)

        # ID Label and text box
        self.title_label = Label(self.root, text="Title")
        self.title_label.config(font="15")
        self.title_label.place(x=0, y=0)
        self.title_textbox = Entry(self.root)
        self.title_textbox.config(font="15")
        self.title_textbox.place(x=140, y=0)

        # reminder data label and textbox
        self.location_label = Label(self.root, text="Location")
        self.location_label.config(font="15")
        self.location_label.place(x=0, y=60)
        self.location_textbox = Entry(self.root, width="30")
        self.location_textbox.config(font="15")
        self.location_textbox.place(x=140, y=60)

        # reminder type label and textbox
        self.codes_label = Label(self.root, text="Codes")
        self.codes_label.config(font="15")
        self.codes_label.place(x=0, y=120)
        self.codes_textbox = Entry(self.root)
        self.codes_textbox.config(font="15")
        self.codes_textbox.place(x=140, y=120)

        # Submit button
        self.submit_button = Button(
            self.root, width=10, text="Submit", command=self.__submit_data
        )
        self.submit_button.place(x=120, y=200)

        # Clear button
        self.clear_button = Button(
            self.root, width=10, text="Clear", command=self.__clear_field
        )
        self.clear_button.place(x=250, y=200)

        mainloop()

    def __clear_field(self) -> None:
        """
        Clear all text fields
        """
        self.title_textbox.delete(0, END)
        self.location_textbox.delete(0, END)
        self.codes_textbox.delete(0, END)

    def __submit_data(self) -> None:
        """
        Submit data and save it to file
        """
        try:
            __website_title = self.title_textbox.get()
            __website_location = self.location_textbox.get()
            __website_codes = self.codes_textbox.get()
            if (
                __website_location in ["", " "]
                or __website_codes in [" ", ""]
                or __website_title in [" ", ""]
            ):
                return
            if website_fast_access().add_new_website(
                title=__website_title, site=__website_location, codes=__website_codes
            ):
                # exit()
                self.__clear_field()
        except Exception:
            pass


if __name__ == "__website_fast_access__":
    pass
    # add_website_gui()
