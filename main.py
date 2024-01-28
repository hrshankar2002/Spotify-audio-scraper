import requests
import time
import downloader
from auth import SPOTIFY_GET_CURRENT_TRACK_URL, SPOTIFY_GET_USER_QUEUE_URL
from pprint import pprint
from tkinter import *


class Spotify:
    def __init__(self):
        self.__url_gct = SPOTIFY_GET_CURRENT_TRACK_URL
        self.__url_gcq = SPOTIFY_GET_USER_QUEUE_URL
        self.__menu()

    def main_gct(self):
        current_track_info = self.get_current_track()
        n = current_track_info["track_name"]
        downloader.Downloader(n).down()

    def main_gcq(self):
        current_track_info = self.get_current_queue()
        ls1 = list((current_track_info.values()))
        for i in ls1:
            downloader.Downloader(i).down()

    def get_current_queue(self):
        response = requests.get(
            self.__url_gcq,
            headers={"Authorization": f"Bearer {self.__access_token_gcq}"},
        )
        json_new = response.json()

        ls_id = []
        ls_name = []
        for i in json_new["queue"]:
            if i["id"] not in ls_id:
                ls_id.append(i["id"])
            if i["name"] not in ls_name:
                ls_name.append(i["name"])
        dict_fn = dict(zip(ls_name, ls_id))
        return dict_fn

    def get_current_track(self):
        response = requests.get(
            self.__url_gct,
            headers={"Authorization": f"Bearer {self.__access_token_gct}"},
        )
        json_resp = response.json()

        track_id = json_resp["item"]["id"]
        track_name = json_resp["item"]["name"]
        artists = [artist for artist in json_resp["item"]["artists"]]
        link = json_resp["item"]["external_urls"]["spotify"]
        artist_names = ", ".join([artist["name"] for artist in artists])

        current_track_info = {
            "id": track_id,
            "track_name": track_name,
            "artists": artist_names,
            "link": link,
        }
        return current_track_info

    def __menu(self):
        self.root = Tk()
        self.root.geometry("1580x380")

        filename = PhotoImage(file="assets/light.png")
        background_label = Label(self.root, image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        img = PhotoImage(file="assets/icon.png")
        self.root.iconphoto(False, img)
        self.root.title("Spotify_Audio_Downloader")

        self.e1 = Entry(self.root, width=40, borderwidth=10, bg="green", fg="white")
        self.e1.grid(row=5, column=0, columnspan=2)
        self.e2 = Entry(self.root, width=40, borderwidth=10, bg="green", fg="white")
        self.e2.grid(row=5, column=2, columnspan=2)

        self.myLabel1 = Label(self.root, text="Developed By Author").grid(
            row=0, column=5
        )
        self.myLabel2 = Label(self.root, text="Date Created on 23/10/2022").grid(
            row=1, column=5
        )
        self.myLabel2 = Label(self.root, text="                          ").grid(
            row=2, column=0
        )

        self.myButton1 = Button(
            self.root,
            text="Enter auth code below and press to download currently playing track",
            borderwidth=5,
            command=self.click1,
            padx=20,
            pady=20,
        ).grid(row=3, column=0, columnspan=2)
        self.myButton2 = Button(
            self.root,
            text="Enter auth code below and press to download top 2 queued playlist tracks",
            borderwidth=5,
            command=self.click2,
            padx=20,
            pady=20,
        ).grid(row=3, column=2, columnspan=2)
        self.myButton3 = Button(
            self.root,
            text="Press to exit the window",
            borderwidth=5,
            command=self.root.quit,
            padx=20,
            pady=20,
        ).grid(row=3, column=4, columnspan=2)
        self.myButton4 = Button(
            self.root,
            text="Press to clear text",
            borderwidth=5,
            command=self.clear1,
            padx=20,
            pady=20,
        ).grid(row=7, column=0, columnspan=2)
        self.myButton5 = Button(
            self.root,
            text="Press to clear text",
            borderwidth=5,
            command=self.clear2,
            padx=20,
            pady=20,
        ).grid(row=7, column=2, columnspan=2)

        self.myLabel3 = Label(self.root, text="                          ").grid(
            row=4, column=0
        )
        self.myLabel0 = Label(self.root, text="                          ").grid(
            row=6, column=0
        )
        self.myLabel6 = Label(self.root, text="                          ").grid(
            row=8, column=0
        )

        self.root.mainloop()

    def click1(self):
        self.__access_token_gct = self.e1.get()
        self.main_gct()

    def click2(self):
        self.__access_token_gcq = self.e2.get()
        self.main_gcq()

    def clear1(self):
        self.e1.delete(0, END)

    def clear2(self):
        self.e2.delete(0, END)


if __name__ == "__main__":
    Spotify()
