from cmd import Cmd
import os, json, sys, requests, urllib.request
from urllib.error import HTTPError
from requests_toolbelt.multipart.encoder import MultipartEncoder

class WFTI_SHELL(Cmd):
    prompt = "[" + os.getcwd() + "] "
    server = "127.0.0.1:5000"

    def do_config(self, arg):
        """Configure l'interface:
config url <url>: Permet de modifier l'adresse du serveur cible (par défaut: 127.0.0.1:5000)"""
        args = parse(arg)
        if not args:
            print(self.do_config.__doc__)
        elif args[0] == "url":
            self.server = args[1]

    def do_list(self, arg):
        if self.server:
            with urllib.request.urlopen("http://" + self.server + "/cli/list") as f:
                for filename in json.load(f):
                    print(filename)
        else:
            print("Vous devez d'abord indiquer l'adresse du serveur")
    
    def do_debug(self, arg):
        exec("print(" + arg + ")")

    def do_download(self, arg):
        if arg:
            with urllib.request.urlopen("http://" + self.server + "/uploads/" + parse(arg)[0]) as f:
                savefile = open(arg, "wb")
                savefile.write(f.read())

    def do_cd(self, arg):
        try:
            os.chdir(arg)
        except FileNotFoundError:
            print("FileNotFoundError")
        self.prompt = "[" + os.getcwd() + "] "

    def do_ls(self, arg):
        for filename in os.listdir():
            print(filename)
        
    def do_exit(self, arg):
        """Quitte l'interface de ligne de commande"""
        sys.exit()

    def do_upload(self, arg):
        mp_encoder = MultipartEncoder(
            fields={
                'file': (arg, open(arg, 'rb'))
            }
        )
        response = requests.post("http://" + self.server + "/upload/", data=mp_encoder, headers={'Content-Type':mp_encoder.content_type})
        print(response.status_code)

    def do_delete(self, arg):
        try:
            with urllib.request.urlopen("http://" + self.server + "/cli/delete/" + arg) as f:
                for filename in json.load(f):
                    print(filename)
        except HTTPError:
            print("Fichier non trouvé")

def parse(arg:str) -> tuple:
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(arg.split())

if __name__ == "__main__":
    WFTI_SHELL().cmdloop()
