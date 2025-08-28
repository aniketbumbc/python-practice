from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)


db = client["youtubepyhton"]
video_collection = db["youtubeVideos"]


def list_all_videos():
     print('***************************************')
     
     for video in video_collection.find():
          print(f"Id: {video['_id']}, Name: {video['name']},Time: {video['time']}")

     print('***************************************')
    

def add_video(name,time):
      video_collection.insert_one({"name":name, "time":time})

def update_video(id,name,time):
     
     video_collection.update_one({'_id': ObjectId(id)},{"$set":{"name":name,"time":time}})

def delete_video(id):
      video_collection.delete_one({'_id': ObjectId(id)})


def main():

    while True:
        print("Welcome to Youtube Manager | choice one option ")
        print("1. List the favorite videos")
        print("2. Add a youtube video")
        print("3. update video details")
        print("4. delete a youtube video")
        print("5. exit video app")
        choice = input("Enter your choice: ")

        match choice:
            case '1':
                list_all_videos()
            case '2':
                name = input("Enter the video name ")
                time = input("Enter the video duration ")
                add_video(name,time)
            case '3':
                    id = input("Enter the update video id ")
                    name = input("Enter the video name ")
                    time = input("Enter the video duration ")
                    update_video(id,name,time)
            case '4':
                    id = input("Enter the video id delete ")
                    delete_video(id)
            case '5':
                print("Invalid choice")
                break


if __name__ == "__main__":
    main()

