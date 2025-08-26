import sqlite3
con = sqlite3.connect('youtube_videos.db')
cursor = con.cursor()

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS videos(
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               time TEXT NOT NULL
               )
''')


def list_all_videos():
    cursor.execute("SELECT * FROM videos")
    for row in cursor.fetchall():
        print(row)

def add_video(name,time):
    cursor.execute("INSERT INTO videos (name, time) VALUES (?,?)",(name, time))
    con.commit()

def update_video(id,name,time):
    cursor.execute("UPDATE videos SET name = ?, time = ? WHERE id = ?",(name,time,id))
    con.commit()

def delete_video(id):
    cursor.execute("DELETE FROM videos WHERE id = ?",(id,))
    con.commit()

def main():
    while True:
        print("Welcome to Youtube Manager | choice one option ")
        print("1. List the favorite videos")
        print("2. Add a youtube video")
        print("3. Update video details")
        print("4. Delete a youtube video")
        print("5. Exit video app")
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
                con.close()
                break

              



if __name__ == "__main__":
    main()