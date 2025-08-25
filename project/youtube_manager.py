import json

def load_data():
    try:
        with open('youtube.txt', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []
        


def save_data_helper(videos):
    with open('youtube.txt','w') as file:
        json.dump(videos,file)



def list_all_videos(videos):
       print("\n")
       print("*" * 90)
       for index, video in enumerate(videos,start=1):
        print(f"{index}. and {video['name']}, Duration:{video['time']}")

       print("*" * 90)

def add_video(videos):
    name = input("Enter video name: ")
    time = input("Enter video time: ")
    videos.append({'name': name , 'time': time})
    save_data_helper(videos)

def update_video(videos):
    pass

def delete_video(videos):
    pass


def main():
    videos = load_data()

    while True:
        print("Welcome to Youtube Manager | choice one option ")
        print("1. List the favorite videos")
        print("2. Add a youtube video")
        print("3. update video details")
        print("4. delete a youtube video")
        choice = input("Enter your choice ")

        match choice:
            case '1':
                list_all_videos(videos)
            case '2':
                add_video(videos)
            case '3':
                update_video(videos)
            case '4':
                delete_video(videos)
            case '5':
                break
            case _:
                print("Invalid choice")


if __name__ == "__main__":
    main()
