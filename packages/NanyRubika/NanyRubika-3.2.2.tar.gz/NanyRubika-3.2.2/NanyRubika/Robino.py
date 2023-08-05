from ast import Continue
from NanyRubika.Copyright import copyright
from NanyRubika.PostData import method_Rubika,httpregister,_download,_download_with_server
from NanyRubika.Error import AuthError,TypeMethodError
from NanyRubika.Device import DeviceTelephone
from re import findall
from NanyRubika.Clien import clien
from random import randint,choice
import datetime
import io, PIL.Image
from NanyRubika.Getheader import Upload
from tinytag import TinyTag
from NanyRubika.TypeText import TypeText
import asyncio
from threading import Thread
from NanyRubika.Ny_Wb import SetClines,Server
from requests import post,get
import urllib
from NanyRubika.encryption import encryption
from urllib import request,parse
from re import findall
from pathlib import Path
from random import randint, choice
from json import loads, dumps
from socket import (gaierror,)
from json.decoder import (JSONDecodeError,)
class Robot:
    def __init__(self,Sh_account: str):
        self.Auth = str("".join(findall(r"\w",Sh_account)))
        self.prinet = copyright.CopyRight
        self.methods = method_Rubika(Sh_account)
        self.Upload  = Upload(Sh_account)

        if self.Auth.__len__() < 32:
            raise AuthError("The Auth entered is incorrect")
        elif self.Auth.__len__() > 32:
            raise AuthError("The Auth entered is incorrect")
class Robino:
    def __init__(self,Sh_account: str):
        self.Auth = str("".join(findall(r"\w",Sh_account)))
        self.prinet = copyright.CopyRight
        self.methods = method_Rubika(Sh_account)

        if self.Auth.__len__() < 32:
            raise AuthError("The Auth entered is incorrect")
        elif self.Auth.__len__() > 32:
            raise AuthError("The Auth entered is incorrect")
    def ProfileID(self,username):
        ide = username.split("@")[-1]
        return self.methods.methodsRubika("rubino",methode ="isExistUsername",indata = {"username": ide},wn = clien.android).get("data").get("profile").get("id")

    def Follow(self,username,idfollow):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="requestFollow",indata = {"f_type": "Follow", "followee_id": idfollow, "profile_id": profile_id},wn = clien.android)

    def getProfileStories(self,limit,idfollow):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="getProfileStories",indata = {"limit": limit, "profile_id": profile_id},wn = clien.android)

    def addPostViewCount(self,post_id,post_profile_id):
        return self.methods.methodsRubika("rubino",methode ="addPostViewCount",indata = {"post_id": post_id, "post_profile_id": post_profile_id},wn = clien.android)

    def unFollow(self,followid):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="requestFollow",indata = {"f_type": "Unfollow", "followee_id": followid, "profile_id": profile_id},wn = clien.android)

    def updateProfile(self,name,bio,email):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="updateProfile",indata = {"name": name, "bio": bio, "email": email},wn = clien.android)

    def unlikePostAction(self,ide,post_profile_id):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="Unlike",indata = {"action_type": "Unlike", "post_id": ide, "post_profile_id": post_profile_id, "profile_id": profile_id},wn = clien.android)

    def likePostAction(self,ide,post_profile_id):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="likePostAction",indata = {"action_type": "Like", "post_id": ide, "post_profile_id": post_profile_id, "profile_id": profile_id},wn = clien.android)

    def getProfilePosts(self,limit,sort,target_profile_id):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="getProfileStories",indata = {"equal": False, "limit": limit, "sort": sort, "target_profile_id": target_profile_id, "profile_id": profile_id},wn = clien.android)

    def AddStoryNew(self,username,duration,file_id,hash_file_receive,height,width,story_type,thumbnail_file_id,thumbnail_hash_file_receive):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="addStory",indata = {"duration": duration, "file_id": file_id, "hash_file_receive": hash_file_receive, "height": height, "profile_id": profile_id, "rnd": randint(100000, 999999999), "story_type": story_type, "thumbnail_file_id": thumbnail_file_id, "thumbnail_hash_file_receive": thumbnail_hash_file_receive, "width": width},wn = clien.android)

    def AddPostNew(self,username,caption,file_id,hash_file_receive,height,width,is_multi_file,post_type,thumbnail_file_id,thumbnail_hash_file_receive):
        profile_id = self.ProfileID(username)
        return self.methods.methodsRubika("rubino",methode ="addPost",indata = {"caption": caption, "file_id": file_id, "hash_file_receive": hash_file_receive, "height": height, "width": width, "is_multi_file": is_multi_file, "post_type": post_type, "rnd": randint(100000, 999999999), "thumbnail_file_id": thumbnail_file_id, "thumbnail_hash_file_receive": thumbnail_hash_file_receive, "profile_id": profile_id},wn = clien.android)