import tkinter
from tkinter import filedialog
from tkinter.ttk import Progressbar
from pytube import YouTube
from pytube.exceptions import RegexMatchError
import os
import logging
import threading
import customtkinter
from pytube import exceptions
import requests

def startDownload():
    global ytobject, download_timer  # Make ytobject and download_timer global
    try:
        # Save current content of the entry field
        current_content = link.get()

        # Clear previous download information
        title.configure(text="", text_color="black")
        finishLabel.configure(text="")

        ytlink = current_content
        ytobject = YouTube(ytlink, on_progress_callback=on_progress)

        # Choose download location
        download_path = filedialog.askdirectory()
        MP4_EXTENSION = 'mp4'
        PROGRESSIVE = True
        video_audio_stream = ytobject.streams.filter(file_extension=MP4_EXTENSION, progressive=PROGRESSIVE).get_highest_resolution()

        # Disable download button during download
        download_button.configure(state="disabled")

        # Show loading animation
        loading_label.configure(text="Downloading...", text_color="green")

        # Download in a separate thread
        download_thread = threading.Thread(target=download_video, args=(video_audio_stream, download_path))
        download_thread.start()

    except RegexMatchError:
        finishLabel.configure(text="Invalid YouTube URL", text_color="red")
    except exceptions.VideoUnavailable:
        finishLabel.configure(text="Age-restricted video. Sign in to download.", text_color="red")
    except Exception as e:
        logging.error(f"Download Error: {e}")
        finishLabel.configure(text="Download Error", text_color="red")

def download_video(video_stream, path):
    global download_timer
    try:
        video_stream.download(path)
        # Display download information
        title.configure(text=ytobject.title, text_color="blue")
        finishLabel.configure(text="Downloaded!", text_color="green")
    except Exception as e:
        logging.error(f"Download Error: {e}")
        finishLabel.configure(text="Download Error", text_color="red")
    finally:
        # Enable the download button after download or error
        download_button.configure(state="normal")
        # Hide loading animation
        loading_label.configure(text="")
        # Set a timer to perform a full reset after 3 seconds
        download_timer = app.after(3000, full_reset)

def full_reset():
    # Clear the entry field
    link.delete(0, "end")
    # Restore the saved content
    link.insert(0, placeholder)
    link.delete(0, "end")  # To force the placeholder color change
    link.insert(0, placeholder)

    # Clear all other information
    title.configure(text="", text_color="black")
    finishLabel.configure(text="")
    pPercentage.configure(text="0%")
    progressBar["value"] = 0


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + "%")

    # Update progress bar
    progressBar["value"] = percentage_of_completion


# apperance
customtkinter.set_appearance_mode("black")
customtkinter.set_default_color_theme("green")

# app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("YouTube Videos Downloader")

# Adding UI
title = customtkinter.CTkLabel(app, text="")
title.pack(padx=10, pady=10)

# Set icon using an absolute path
icon_path = os.path.abspath("C:\\Users\\iqlip\\Desktop\\Python-Modern-GUI\\YouTube-videos-downloader\\youtube.ico")
app.iconbitmap(icon_path)

# link input with placeholder
placeholder = "Insert a YouTube link"
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)

link.insert(0, placeholder)
link.bind("<FocusIn>", lambda event: link.delete(0, "end") if link.get() == placeholder else None)
link.bind("<FocusOut>", lambda event: link.insert(0, placeholder) if not link.get() else None)
link.pack()

# finished downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# progress percentage
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

# progress bar
progressBar = Progressbar(app, orient="horizontal", length=400, mode="determinate")
progressBar.pack(padx=10, pady=10)

# loading label
loading_label = customtkinter.CTkLabel(app, text="")
loading_label.pack()

# Download button
download_button = customtkinter.CTkButton(app, text="Download", command=startDownload)
download_button.pack(padx=10, pady=10)

# run app
app.mainloop()
