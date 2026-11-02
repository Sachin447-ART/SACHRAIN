import os
import socket
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox

# Optional dependencies
try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    from ollama import chat as ollama_chat
except ImportError:
    ollama_chat = None

try:
    import pyaudio
except ImportError:
    pyaudio = None

try:
    import winsound
except ImportError:
    winsound = None

try:
    import subprocess
except ImportError:
    subprocess = None

try:
    from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    FastAPI = None
    File = None
    Form = None
    HTTPException = None
    UploadFile = None
    status = None
    StaticFiles = None
    BaseModel = None
    uvicorn = None


def run_ollama_query(prompt: str) -> str:
    if ollama_chat is None:
        return "Ollama is not installed or not configured."
    try:
        response = ollama_chat(
            model="gemma4",
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"]
    except Exception as exc:
        return f"Error while contacting Ollama: {exc}"


root = tk.Tk()
root.configure(bg="black")
root.geometry("900x1080")
root.title("EDITH")

nav_frame = tk.Frame(root, bg="black")
nav_frame.pack(side="top", fill="x", padx=10, pady=10)

content_frame = tk.Frame(root, bg="#101010")
content_frame.pack(fill="both", expand=True, padx=20, pady=10)


def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()


def open_selected_file(label_widget):
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=[
            ("All files", "*.*"),
            ("Images", "*.png *.jpg *.jpeg *.gif"),
            ("Documents", "*.pdf *.docx *.txt"),
            ("Python files", "*.py"),
        ],
    )
    if file_path:
        label_widget.config(text=f"Selected: {file_path}")


def home_s(event=None):
    clear_content()

    bar = tk.Frame(
        content_frame,
        bg="#23CE3A",
        highlightbackground="#23CE3A",
        highlightthickness=1,
    )
    bar.pack(fill="x", pady=10)

    selected_file_label = tk.Label(
        content_frame,
        text="No file selected",
        bg="#303030",
        fg="white",
        wraplength=550,
    )
    selected_file_label.pack(pady=(0, 10))

    plus = tk.Button(
        bar,
        text="⊕",
        font=("Arial", 20),
        bg="#16D626",
        fg="white",
        activebackground="#941A1A",
        activeforeground="white",
        bd=5,
        command=lambda: open_selected_file(selected_file_label),
    )
    plus.pack(side="left", padx=12)

    prompt_var = tk.StringVar(value="ASK EDITH:")
    sach = tk.Entry(
        bar,
        textvariable=prompt_var,
        font=("Arial", 13),
        bg="#202020",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=2,
    )
    sach.pack(side="left", fill="both", expand=True, padx=5)

    def mic_button_click():
        if sr is None:
            messagebox.showerror("Missing dependency", "speech_recognition is not installed.")
            return

        def worker():
            recognizer = sr.Recognizer()
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language="en-IN")
                prompt_var.set(text)
            except sr.WaitTimeoutError:
                messagebox.showinfo("EDITH", "No speech detected.")
            except sr.UnknownValueError:
                messagebox.showinfo("EDITH", "Sorry, I could not understand.")
            except sr.RequestError:
                messagebox.showinfo("EDITH", "Check your internet connection.")
            except Exception as exc:
                messagebox.showerror("EDITH", f"Error: {exc}")

        threading.Thread(target=worker, daemon=True).start()

    mic = tk.Button(
        bar,
        text="🎤",
        bg="#16D626",
        fg="white",
        font=("Arial", 14),
        activebackground="#303030",
        bd=0,
        command=mic_button_click,
    )
    mic.pack(side="left", padx=8)

    def run_query():
        text = prompt_var.get().strip()
        if not text or text == "ASK EDITH:":
            messagebox.showinfo("EDITH", "Please type a question first.")
            return
        response = run_ollama_query(text)
        messagebox.showinfo("EDITH", response)

    voice = tk.Button(
        bar,
        text="⎆",
        font=("Arial", 14, "bold"),
        bg="#2875df",
        fg="white",
        activebackground="#1b5fc0",
        bd=0,
        width=3,
        height=1,
        command=run_query,
    )
    voice.pack(side="right", padx=6, pady=5)

    status_label = tk.Label(
        content_frame,
        text="Ready for input",
        bg="#101010",
        fg="white",
        font=("Arial", 12),
    )
    status_label.pack(pady=(10, 0))


def print_apps(event=None):
    clear_content()
    info = tk.Label(
        content_frame,
        text="App updater",
        bg="#101010",
        fg="white",
        font=("Arial", 18, "bold"),
    )
    info.pack(pady=20)

    if subprocess is None or os.name != "nt":
        tk.Label(
            content_frame,
            text="Windows update helpers are unavailable in this environment.",
            bg="#101010",
            fg="white",
            wraplength=600,
        ).pack(pady=10)
        return

    text_box = tk.Text(content_frame, height=14, width=80, bg="#202020", fg="white")
    text_box.pack(padx=20, pady=10)
    text_box.insert("1.0", "This feature would run winget update commands on Windows.\n")


def zealfire(event=None):
    clear_content()
    label = tk.Label(
        content_frame,
        text="ZEALFIRE",
        bg="#101010",
        fg="white",
        font=("Arial", 18, "bold"),
    )
    label.pack(pady=20)

    prompt = tk.Entry(content_frame, width=60, font=("Arial", 12))
    prompt.pack(pady=10)
    prompt.insert(0, "Ask ZEALFIRE:")

    def ask():
        text = prompt.get().strip()
        if not text or text == "Ask ZEALFIRE:":
            messagebox.showinfo("ZEALFIRE", "Please enter a message.")
            return
        messagebox.showinfo("ZEALFIRE", run_ollama_query(text))

    btn = tk.Button(content_frame, text="Ask", command=ask, bg="#16D626", fg="white")
    btn.pack(pady=10)


def timer(event=None):
    clear_content()
    timer_win = tk.Toplevel(root)
    timer_win.title("TIMER")
    timer_win.configure(bg="black")
    timer_win.geometry("400x200")

    tk.Label(
        timer_win,
        text="SET TIMING FOR ALARM OF:",
        fg="yellow",
        bg="black",
        font=("arial", 14),
    ).pack(pady=10)

    entry = tk.Entry(timer_win, font=("Arial", 14), justify="center", bd=2)
    entry.pack(pady=5)
    entry.insert(0, "30")

    result = tk.Label(timer_win, text="", fg="yellow", bg="black", font=("arial", 12))
    result.pack(pady=10)

    def start_timer():
        try:
            seconds = int(entry.get())
        except ValueError:
            result.config(text="Please enter a whole number!")
            return

        result.config(text=f"Timer started for {seconds} seconds")
        for remaining in range(seconds, 0, -1):
            time.sleep(1)
            if winsound is not None:
                winsound.Beep(1000, 100)
        result.config(text="TIME'S UP!")
        if winsound is not None:
            winsound.Beep(1500, 700)

    tk.Button(
        timer_win,
        text="OK",
        cursor="hand2",
        fg="yellow",
        font=("arial", 14),
        command=lambda: threading.Thread(target=start_timer, daemon=True).start(),
    ).pack(pady=10)


def caller(event=None):
    clear_content()
    if pyaudio is None:
        messagebox.showerror("Missing dependency", "PyAudio is not installed.")
        return

    class VoiceCallApp:
        def __init__(self, master):
            self.master = master
            self.master.title("Python Native VoIP Call")
            self.master.geometry("350x300")
            self.master.resizable(False, False)

            self.p = pyaudio.PyAudio()
            self.is_in_call = False
            self.sock = None
            self.stream_in = None
            self.stream_out = None
            self.audio_thread = None

            tk.Label(master, text="Internet Voice Dialer", font=("Arial", 14, "bold")).pack(pady=15)
            tk.Label(master, text="Destination IP / Host:").pack()
            self.host_entry = tk.Entry(master, width=25, font=("Arial", 11))
            self.host_entry.pack(pady=5)
            self.host_entry.insert(0, "127.0.0.1")

            tk.Label(master, text="Port:").pack()
            self.port_entry = tk.Entry(master, width=10, font=("Arial", 11))
            self.port_entry.pack(pady=5)
            self.port_entry.insert(0, "50007")

            self.status_label = tk.Label(master, text="Status: Idle", fg="gray", font=("Arial", 10))
            self.status_label.pack(pady=10)

            self.call_button = tk.Button(
                master,
                text="Start Outgoing Call",
                bg="green",
                fg="white",
                font=("Arial", 10, "bold"),
                width=18,
                command=self.toggle_call,
            )
            self.call_button.pack(pady=10)

            self.master.protocol("WM_DELETE_WINDOW", self.on_close)

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

            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((dest_ip, dest_port))
                self.is_in_call = True
                self.call_button.config(text="End Call", bg="red")
                self.status_label.config(text="Status: In Call (Connected)", fg="green")
                self.audio_thread = threading.Thread(target=self.audio_stream_loop, daemon=True)
                self.audio_thread.start()
            except Exception as exc:
                messagebox.showerror("Connection Failed", str(exc))
                self.status_label.config(text="Status: Call Failed", fg="red")
                self.sock = None
                self.is_in_call = False

        def audio_stream_loop(self):
            stream_in = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=512,
            )
            stream_out = self.p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                output=True,
                frames_per_buffer=512,
            )
            try:
                while self.is_in_call:
                    try:
                        data_to_send = stream_in.read(512, exception_on_overflow=False)
                        self.sock.sendall(data_to_send)
                    except Exception:
                        break

                    try:
                        self.sock.settimeout(0.05)
                        incoming_data = self.sock.recv(1024)
                        if incoming_data:
                            stream_out.write(incoming_data)
                    except socket.timeout:
                        continue
                    except Exception:
                        break
            finally:
                try:
                    stream_in.stop_stream()
                    stream_in.close()
                except Exception:
                    pass
                try:
                    stream_out.stop_stream()
                    stream_out.close()
                except Exception:
                    pass
                try:
                    if self.sock:
                        self.sock.close()
                except Exception:
                    pass

        def end_call(self):
            self.is_in_call = False
            if self.sock:
                try:
                    self.sock.close()
                except Exception:
                    pass
            self.call_button.config(text="Start Outgoing Call", bg="green")
            self.status_label.config(text="Status: Call Ended", fg="gray")

        def on_close(self):
            self.is_in_call = False
            self.end_call()
            self.p.terminate()
            self.master.destroy()

    call_window = tk.Toplevel(root)
    VoiceCallApp(call_window)


def watch(event=None):
    clear_content()
    if FastAPI is None or uvicorn is None:
        messagebox.showerror("Missing dependency", "FastAPI or uvicorn is not installed.")
        return

    app = FastAPI(title="Python Netflix Clone Backend", version="1.0")
    upload_dir = "media_storage/videos"
    thumb_dir = "media_storage/thumbnails"
    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(thumb_dir, exist_ok=True)

    app.mount("/media", StaticFiles(directory="media_storage"), name="media")

    fake_db_users = {
        "demo_user": {
            "username": "demo_user",
            "password": "password123",
            "email": "demo@netclone.com",
        }
    }
    fake_db_categories = [
        {"id": 1, "name": "Action"},
        {"id": 2, "name": "Sci-Fi"},
        {"id": 3, "name": "Documentary"},
    ]
    fake_db_videos = [
        {
            "id": 1,
            "title": "Cyberpunk Odyssey",
            "description": "A thrilling journey through a neon-lit futuristic metropolis.",
            "category_id": 2,
            "thumbnail_url": "/media/thumbnails/sample_thumb.jpg",
            "playlist_url": "/media/videos/sample_hls/playlist.m3u8",
        }
    ]
    fake_db_watch_history = []

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

    @app.get("/")
    def root_status():
        return {"message": "Welcome to the Python Netflix Clone API. Visit /docs for interactive Swagger UI."}

    @app.post("/api/auth/login")
    def login(user: UserLogin):
        db_user = fake_db_users.get(user.username)
        if not db_user or db_user["password"] != user.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )
        return {
            "access_token": f"fake-jwt-token-for-{user.username}",
            "token_type": "bearer",
        }

    @app.get("/api/categories")
    def get_categories():
        return fake_db_categories

    @app.get("/api/videos", response_model=list[VideoResponse])
    def get_videos(category_id: int | None = None):
        if category_id:
            return [v for v in fake_db_videos if v["category_id"] == category_id]
        return fake_db_videos

    @app.get("/api/videos/{video_id}", response_model=VideoResponse)
    def get_video_detail(video_id: int):
        for video in fake_db_videos:
            if video["id"] == video_id:
                return video
        raise HTTPException(status_code=404, detail="Video not found")

    @app.post("/api/watch-history")
    def update_watch_history(history: WatchHistorySchema):
        for record in fake_db_watch_history:
            if record["username"] == history.username and record["video_id"] == history.video_id:
                record["watched_seconds"] = history.watched_seconds
                record["completed"] = history.completed
                return {"status": "success", "message": "Watch history updated."}
        fake_db_watch_history.append(history.dict())
        return {"status": "success", "message": "Watch history created."}

    @app.post("/api/admin/upload-video")
    async def upload_video(
        title: str = Form(...),
        description: str = Form(...),
        category_id: int = Form(...),
        video_file: UploadFile = File(...),
        thumbnail_file: UploadFile = File(...),
    ):
        new_id = len(fake_db_videos) + 1

        thumb_path = os.path.join(thumb_dir, f"{new_id}_{thumbnail_file.filename}")
        with open(thumb_path, "wb") as buffer:
            buffer.write(await thumbnail_file.read())

        vid_folder = os.path.join(upload_dir, f"video_{new_id}")
        os.makedirs(vid_folder, exist_ok=True)
        vid_path = os.path.join(vid_folder, video_file.filename)
        with open(vid_path, "wb") as buffer:
            buffer.write(await video_file.read())

        new_video = {
            "id": new_id,
            "title": title,
            "description": description,
            "category_id": category_id,
            "thumbnail_url": f"/media/thumbnails/{new_id}_{thumbnail_file.filename}",
            "playlist_url": f"/media/videos/video_{new_id}/{video_file.filename}",
        }
        fake_db_videos.append(new_video)
        return {"status": "success", "video_id": new_id, "data": new_video}

    def server_runner():
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")

    threading.Thread(target=server_runner, daemon=True).start()
    tk.Label(
        content_frame,
        text="Entertainment backend started at http://127.0.0.1:8000/docs",
        bg="#101010",
        fg="white",
        wraplength=600,
    ).pack(pady=20)


def build_nav():
    buttons = [
        ("HOME", home_s),
        ("UPDATE", print_apps),
        ("ZEALFIRE", zealfire),
        ("CALL", caller),
        ("TIMER", timer),
        ("ENTERTAINMENT", watch),
    ]
    for text, command in buttons:
        btn = tk.Button(
            nav_frame,
            text=text,
            fg="blue",
            bd=3,
            font=("Bold", 20),
            justify="top",
            cursor="hand2",
            bg="black",
            activebackground="black",
            command=command,
        )
        btn.pack(side="left", ipadx=10, ipady=15, padx=5)


build_nav()
home_s()
root.mainloop()
