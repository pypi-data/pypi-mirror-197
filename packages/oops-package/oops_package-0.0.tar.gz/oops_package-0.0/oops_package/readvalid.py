from parsearg import *


class ReadFiles:

    def email_validation(self, email):
        if '@' and '.' in email:
            email_list = email.split("@")
            username, domain_name = email_list[0], email_list[1]
            if 0 < len(username) < 255 and 0 < len(domain_name) < 55:
                if email.index("@") > 0 and email.index('.') < len(email) - 1:
                    top_level_domain = email.split('.')[-1]
                    if 2 <= len(top_level_domain) <= 6:
                        return email

    def read_file(self, file):
        Args.file_validation(self, file, file1, file2)
        with open(file, "r") as file:
            line = file.readlines()
            hm = {}
            for i in line:
                try:
                    if self.email_validation(i):
                        hm[i] = True
                    else:
                        raise SyntaxError
                except SyntaxError:
                    print("Email Format is invalid and removing the unsupported formatted emails")
            return hm
