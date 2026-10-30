import tkinter as tk
from ollama import chat
from tkinter import messagebox
import speech_recognition as sr
import threading
from typing import Iterable
import asyncio
import pyaudio
import socket
from flask import Flask, render_template_string, request, redirect, url_for, abort, flash, send_file
from pathlib import Path
import sqlite3
import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
import shutil
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
# Optional dependencies: the rest of EDITH can still open without these.
try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import ollama
except ImportError:
    ollama = None
# creating window
root=tk.Tk()
root.configure(bg="black")
root.geometry("900x1080")
root.title("EDITH")
# home label
label=tk.Label(root,text="HOME",fg="blue",bd=3,font=("Bold",20),justify="top",cursor="hand2")
label.pack(side="left",ipadx=10,ipady=15)
label.bind("<Button-1>",home_s)
# upadate label
y=tk.Label(root,text="UPDATE",fg="blue",bd=3,font=("Bold",20),justify="top",cursor="hand2")
y.pack(side="left",ipadx=10,ipady=21)
y.bind("<Button-1>",print_apps)
# ZEALFIRE label
z=tk.Label(root,text="ZEALFIRE",fg="blue",bd=3,font=("Bold",20),justify="top",cursor="hand2")
z.pack(side="left",ipadx=10,ipady=24)
z.bind("<Button-1>",zealfire)
# call label
a=tk.Label(root,text="CALL",fg="blue",bd=3,font=("Bold",20),justify="top",cursor="hand2")
a.pack(side="left",ipadx=10,ipady=27)
a.bind("<Button-1>",caller)
# timer label
b=tk.Label(root,text="TIMER",fg="blue",bd=3,font=("Bold",20),justify="top",cursor="hand2")
b.pack(side="left",ipadx=10,ipady=30)
b.bind("<Button-1>",timer)
# watch label
c=tk.Label(root,text="ENTERTAINMENT",fg="blue",bd=3,font=("Bold",20),justify="top",cursor="hand2")
c.pack(side="left",ipadx=10,ipady=30)
c.bind("<Button-1>",watch)

def home_s(event):
    # Input bar
    bar=tk.Frame(
        root,
        bg="#23CE3A",
        highlightbackground="#23CE3A",
        highlightthickness=1
        )
    bar.place(x=20, y=30, width=800, height=55,anchor="s")

    # Plus button
    plus = tk.Button(
        bar, text="⊕",
        font=("Arial", 20),
        bg="#16D626", fg="white",
        activebackground="#941A1A",
        activeforeground="white",
         bd=5
    )
    plus.pack(side="left", padx=12)
    plus.bind("<Button-1",print_plus)
    #text input
    sach=tk.Entry(
        bar,
        font=("Arial", 13),
        bg="#202020",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=2,
    )
    sach.insert(0,"ASK EDITH:")
    sach.pack(side="left", fill="both", expand=True, padx=5)

    # Microphone button
    mic = tk.Button(
        bar,
        bg="#16D626", fg="white",
        text="\U0001F3A4",
        font=("Arial", 14),
        activebackground="#303030",
        bd=0
    )
    mic.pack(side="left", padx=8)
    mic.bind("<Button-1>",mic_button)
    # Voice button
    voice = tk.Button(
        bar, text="⎆",
        font=("Arial", 14, "bold"),
        bg="#2875df", fg="white",
        activebackground="#1b5fc0",
        bd=0,
        width=3,
        height=1
    )
    voice.pack(side="right", padx=6, pady=5)
    voice.bind("<Button-1>",voice_button)

    def print_plus(event):
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[
                ("All files", "*.*"),
                ("Images", "*.png *.jpg *.jpeg *.gif"),
                ("Documents", "*.pdf *.docx *.txt"),
                ("Python files", "*.py")
            ]
        )
        if file_path:
            filename_label.config(text="Selected: " + file_path)

            # Add photos & files button
            btn=tk.Button(
            root,
            text="♧  Add photos & files",
            command=open_file,
            bg="#16C210",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            font=("Arial", 12),
            relief="flat",
            cursor="hand2"
        )
        btn.pack(pady=25)
        # Display selected file
        filename_label = tk.Label(
            root,
            text="No file selected",
            bg="#303030",
            fg="white",
            wraplength=550
        )
        filename_label.pack(pady=5)
    #mia button
    recognizer = sr.Recognizer()

    def show_text(text):
        entry.delete(0, tk.END)
        entry.insert(0, text)
        status.config(text="Speech recognized successfully!")

    def listen():
        mic_button.config(state="disabled")
        status.config(text="Listening... Speak now!")

        def worker():
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(
                        source, duration=0.5
                    )
                    audio = recognizer.listen(
                        source,
                        timeout=5,
                        phrase_time_limit=10
                    )

                text = recognizer.recognize_google(
                    audio, language="en-IN"
                )

                root.after(0, lambda: show_text(text))

            except sr.WaitTimeoutError:
                root.after(
                    0, lambda: status.config(
                        text="No speech detected."
                    )
                )

            except sr.UnknownValueError:
                root.after(
                    0, lambda: status.config(
                        text="Sorry, I couldn't understand."
                    )
                )

            except sr.RequestError:
                root.after(
                    0, lambda: status.config(
                        text="Check your internet connection."
                    )
                )

            except Exception as e:
                root.after(
                    0, lambda: status.config(
                        text=f"Error: {e}"
                    )
                )

            finally:
                root.after(
                    0, lambda: mic_button.config(state="normal")
                )

        threading.Thread(target=worker, daemon=True).start()

    mic_button.config(command=listen)

    def voice_button(logprobs: Iterable[dict], label: str) -> None:
        print(f"\n{label}:")

        for entry in logprobs:
            token = entry.get("token", "")
            logprob = entry.get("logprob")

            if logprob is not None:
                print(f"  token={token!r:<12} logprob={logprob:.3f}")
            else:
                print(f"  token={token!r:<12} logprob=N/A")

            for alt in entry.get("top_logprobs", []):
                if alt.get("token") != token:
                    alt_logprob = alt.get("logprob")

                    if alt_logprob is not None:
                        print(
                            f"    alt -> {alt['token']!r:<12} "
                            f"({alt_logprob:.3f})"
                        )


    def sachi():
        messages = [
            {
                "role": "user",
                "content": str(sach.get()),
            }
        ]

        response = ollama.chat(
            model="gemma4",
            messages=messages,
            logprobs=True,
            top_logprobs=3,
        )


        print("Chat response:", response["message"]["content"])

        voice_button(
            response.get("logprobs") or [],
            "Chat logprobs"
        )

    # Call this function when needed
    sachi()

    def sachin():
        messages = [
            {
                "role": "user",
                "content": str(sach.get()),
            }
        ]

        response = generate('deepseek-r1',token, think=True)

        print('Thinking:\n========\n\n' + response.thinking)
        print('\nResponse:\n========\n\n' + response.response)

        print("Chat response:", response["message"]["content"])

        voice_button(
            response.get("logprobs") or [],
            "Chat logprobs"
        )
        
    # Call this function when needed
    sachin()
# update options
def print_apps(event):

    print("Checking for app updates...")

    subprocess.run(["winget", "upgrade"])

    choice = input("Do you want to install all available updates? (yes/no): ")

    if choice.lower() == "yes":
        subprocess.run([
            "winget", "upgrade",
            "--all",
            "--accept-source-agreements",
            "--accept-package-agreements"
            ])

        print("App update process completed.")
    else:

        app_name = input("Enter the app name to update: ")

        print("Checking for updates for:", app_name)

        subprocess.run([
            "winget",
            "upgrade",
            "--name", app_name
        ])

        choice = input("Do you want to install this update? (yes/no): ")

        if choice.lower() == "yes":
            subprocess.run(
                [
                    "winget",
                    "upgrade",
                    "--name", app_name,
                    "--accept-source-agreements",
                    "--accept-package-agreements"
                ])
            print(app_name, "has been updated.")
        else:
            print("Update cancelled.")
           
    def print_os(event):


        print("Checking for Windows updates...")

        subprocess.run([
            "powershell",
            "-Command",
            "Install-Module PSWindowsUpdate -Force -Scope CurrentUser"
            ])

        subprocess.run([
            "powershell",
            "-Command",
            "Import-Module PSWindowsUpdate; Get-WindowsUpdate -Install -AcceptAll -AutoReboot"
        ])

    print("Windows update process completed.")
    # apps button
    apps =tk.button(root,Text="APPS",cursor="hand2",fg="yellow",font=("arial",14))
    apps.pack(side="left",paddle=10)
    apps.bind("<BUTTON>",print_apps)
    # os button
    os=tk.button(root,Text="HTML",cursor="hand2",fg="yellow",font=("arial",14))
    os.pack(side="left",paddle=10)
    os.bind("<BUTTON>",print_os)
    
def timer(event):
    def print_ok(event):
        print(entry,"-SECOND TIMER STARTED!")

        try:
            seconds=int(oj.get())
            result.config(text=f"You entered {seconds} seconds!")

        except ValueError:
            result.config(text="Please enter a whole number!")

        for seconds in range(s, 0, -1):
            print("Time remaining:", seconds)
         
            # Play a short tick sound
            winsound.Beep(1000, 100)

            # Wait approximately one second in total per tick
            time.sleep(0.9)

        print("TIME'S UP!")

        # Play a longer sound when time is up
        winsound.Beep(1500, 700)

    root=tk.Tk()
    root.configure(bg="black")
    root.title("TIMER:")
    root.geometry("900x1080")

    g=tk.Label(root,text="Timer",fg="yellow",bg="black",font=("arial",14))
    g.pack(side="left",ipadx=5,ipady=5)

    labelx=tk.Label(root,text="SET TIMING FOR ALARM OF:",fg="yellow",bg="black",font=("arial",14))
    labelx.pack(side="left",ipadx=5,ipady=7)

    oj=tk.Entry(root,font=("Arial",14),justify="center",text="enter time limit:",bd=2)
    oj.pack(side="left",ipadx=5,ipady=9)

    ok=tk.Button(root,text="OK",cursor="hand2",fg="yellow",font=("arial",14),pady=0,padx=10,command=print_ok)
    ok.pack(side="right",ipadx=12,ipady=12)

def caller():
    # Audio Configuration Parameters
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000          # 16kHz sample rate (good balance for voice clarity and bandwidth)
    CHUNK = 512           # Small chunk size for low-latency streaming

    class VoiceCallApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Python Native VoIP Call")
            self.root.geometry("350x300")
            self.root.resizable(False, False)

            self.p = pyaudio.PyAudio()
            self.is_in_call = False
            self.sock = None
            self.stream_in = None
            self.stream_out = None
            self.audio_thread = None

            # --- UI Layout ---
            tk.Label(root, text="Internet Voice Dialer", font=("Arial", 14, "bold")).pack(pady=15)

            tk.Label(root, text="Destination IP / Host:").pack()
            self.host_entry = tk.Entry(root, width=25, font=("Arial", 11))
            self.host_entry.pack(pady=5)
            self.host_entry.insert(0, "127.0.0.1") # Default placeholder for testing

            tk.Label(root, text="Port:").pack()
            self.port_entry = tk.Entry(root, width=10, font=("Arial", 11))
            self.port_entry.pack(pady=5)
            self.port_entry.insert(0, "50007")

            self.status_label = tk.Label(root, text="Status: Idle", fg="gray", font=("Arial", 10))
            self.status_label.pack(pady=10)

            self.call_button = tk.Button(root, text="Start Outgoing Call", bg="green", fg="white", 
                                         font=("Arial", 10, "bold"), width=18, command=self.toggle_call)
            self.call_button.pack(pady=10)

            # Handle window close cleanup
            self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        def toggle_call(self):
            if not self.is_in_call:
                self.start_call()
            else:
                self.end_call()

        def start_call(self):
            dest_ip = self.host_entry.get().strip()
            try:
                dest_port = int(self.port_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Invalid port number.")
                return

            if not dest_ip:
                messagebox.showerror("Error", "Please enter a target address.")
                return

            self.status_label.config(text="Status: Connecting...", fg="blue")
            self.root.update()

            try:
                # Initialize Network Socket (TCP for stable stream delivery)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((dest_ip, dest_port))
                
                self.is_in_call = True
                self.call_button.config(text="End Call", bg="red")
                self.status_label.config(text="Status: In Call (Connected)", fg="green")

                # Start Full-Duplex Audio Worker Thread
                self.audio_thread = threading.Thread(target=self.audio_stream_loop, daemon=True)
                self.audio_thread.start()

            except Exception as e:
                messagebox.showerror("Connection Failed", str(e))
                self.status_label.config(text="Status: Call Failed", fg="red")
                self.sock = None
                self.is_in_call = False

        def audio_stream_loop(self):
            try:
                # Open PyAudio Streams
                self.stream_in = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                                             input=True, frames_per_buffer=CHUNK)
                self.stream_out = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                                              output=True, frames_per_buffer=CHUNK)

                while self.is_in_call:
                    # 1. Capture microphone audio and send over internet socket
                    try:
                        data_to_send = self.stream_in.read(CHUNK, exception_on_overflow=False)
                        self.sock.sendall(data_to_send)
                    except Exception:
                        break

                    # 2. Receive audio data from internet socket and play to speakers
                    try:
                        self.sock.settimeout(0.05) # Prevent blocking indefinitely
                        incoming_data = self.sock.recv(CHUNK * 2) # 2 bytes per sample for paInt16
                        if incoming_data:
                            self.stream_out.write(incoming_data)
                    except socket.timeout:
                        continue
                    except Exception:
                        break
            finally:
                self.cleanup_audio()

        def cleanup_audio(self):
            if self.stream_in:
                try:
                    self.stream_in.stop_stream()
                    self.stream_in.close()
                except:
                    pass
            if self.stream_out:
                try:
                    self.stream_out.stop_stream()
                    self.stream_out.close()
                except:
                    pass
            if self.sock:
                try:
                    self.sock.close()
                except:
                    pass

        def end_call(self):
            self.is_in_call = False
            if self.sock:
                try:
                    self.sock.close()
                except:
                    pass
            self.call_button.config(text="Start Outgoing Call", bg="green")
            self.status_label.config(text="Status: Call Ended", fg="gray")

        def on_close(self):
            self.is_in_call = False
            self.cleanup_audio()
            self.p.terminate()
            self.root.destroy()

    root = tk.Tk()
    app = VoiceCallApp(root)
    root.mainloop()

# To run the application, simply call:
caller()

def zealfire(event):

    messages = [
        {
            "role": "user",
            "content": str(sach.get()),
        }
    ]

    response1 = ollama.chat(
        model="gemma4",
        messages=messages,
        logprobs=True,
        top_logprobs=3,
    )

    print("Chat response:", response["message"]["content"])

    voice_button(
        response.get("logprobs") or [],
        "Chat logprobs"
    )

    response2 = generate('deepseek-r1',token, think=True)

    print('Thinking:\n========\n\n' + response.thinking)
    print('\nResponse:\n========\n\n' + response.response)

    print("Chat response:", response["message"]["content"])

    voice_button(
        response.get("logprobs") or [],
        "Chat logprobs"
    )
    response=response1+response2
    # Call this function when needed
    zealfire()

def watch(event):
     # Initialize FastAPI App
    app = FastAPI(title="Python Netflix Clone Backend", version="1.0")

    # --- Directory Setup for Media Simulation ---
    UPLOAD_DIR = "media_storage/videos"
    THUMB_DIR = "media_storage/thumbnails"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(THUMB_DIR, exist_ok=True)

    # Mount static directory to serve video files & HLS playlists (.m3u8 / .ts segments)
    app.mount("/media", StaticFiles(directory="media_storage"), name="media")

    # --- In-Memory Database Simulation ---
    fake_db_users = {
        "demo_user": {"username": "demo_user", "password": "password123", "email": "demo@netclone.com"}
    }

    fake_db_categories = [
        {"id": 1, "name": "Action"},
        {"id": 2, "name": "Sci-Fi"},
        {"id": 3, "name": "Documentary"}
    ]

    fake_db_videos = [
        {
            "id": 1,
            "title": "Cyberpunk Odyssey",
            "description": "A thrilling journey through a neon-lit futuristic metropolis.",
            "category_id": 2,
            "thumbnail_url": "/media/thumbnails/sample_thumb.jpg",
            "playlist_url": "/media/videos/sample_hls/playlist.m3u8"
        }
    ]

    fake_db_watch_history = []

    # --- Pydantic Data Validation Models ---
    class UserLogin(BaseModel):
        username: str
        password: str

    class VideoResponse(BaseModel):
        id: int
        title: str
        description: str
        category_id: int
        thumbnail_url: str
        playlist_url: str

    class WatchHistorySchema(BaseModel):
        username: str
        video_id: int
        watched_seconds: int
        completed: bool = False

    # --- API Routes ---
    @app.get("/", tags=["General"])
    def root_status():
        return {"message": "Welcome to the Python Netflix Clone API. Visit /docs for interactive Swagger UI."}

    @app.post("/api/auth/login", tags=["Authentication"])
    def login(user: UserLogin):
        db_user = fake_db_users.get(user.username)
        if not db_user or db_user["password"] != user.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        return {"access_token": f"fake-jwt-token-for-{user.username}", "token_type": "bearer"}

    @app.get("/api/categories", tags=["Catalog"])
    def get_categories():
        return fake_db_categories

    @app.get("/api/videos", response_model=List[VideoResponse], tags=["Catalog"])
    def get_videos(category_id: Optional[int] = None):
        if category_id:
            filtered = [v for v in fake_db_videos if v["category_id"] == category_id]
            return filtered
        return fake_db_videos

    @app.get("/api/videos/{video_id}", response_model=VideoResponse, tags=["Catalog"])
    def get_video_detail(video_id: int):
        for video in fake_db_videos:
            if video["id"] == video_id:
                return video
        raise HTTPException(status_code=404, detail="Video not found")

    @app.post("/api/watch-history", tags=["User Activity"])
    def update_watch_history(history: WatchHistorySchema):
        for record in fake_db_watch_history:
            if record["username"] == history.username and record["video_id"] == history.video_id:
                record["watched_seconds"] = history.watched_seconds
                record["completed"] = history.completed
                return {"status": "success", "message": "Watch history updated."}
        
        fake_db_watch_history.append(history.dict())
        return {"status": "success", "message": "Watch history created."}

    @app.post("/api/admin/upload-video", tags=["Admin Content Management"])
    async def upload_video(
        title: str = Form(...),
        description: str = Form(...),
        category_id: int = Form(...),
        video_file: UploadFile = File(...),
        thumbnail_file: UploadFile = File(...)
    ):
        new_id = len(fake_db_videos) + 1
        
        thumb_path = os.path.join(THUMB_DIR, f"{new_id}_{thumbnail_file.filename}")
        with open(thumb_path, "wb") as buffer:
            shutil.copyfileobj(thumbnail_file.file, buffer)
            
        vid_folder = os.path.join(UPLOAD_DIR, f"video_{new_id}")
        os.makedirs(vid_folder, exist_ok=True)
        vid_path = os.path.join(vid_folder, video_file.filename)
        with open(vid_path, "wb") as buffer:
            shutil.copyfileobj(video_file.file, buffer)

        new_video = {
            "id": new_id,
            "title": title,
            "description": description,
            "category_id": category_id,
            "thumbnail_url": f"/media/thumbnails/{new_id}_{thumbnail_file.filename}",
            "playlist_url": f"/media/videos/video_{new_id}/{video_file.filename}"
        }
        fake_db_videos.append(new_video)
        
        return {"status": "success", "video_id": new_id, "data": new_video}

    # --- Start Server ---
    print("Starting Python Netflix Clone Backend Server...")
    print("Access interactive API documentation at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)

# To run the application, call:
# sachin()
#keep window running
root.mainloop()