#test
#https://www.youtube.com/playlist?list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk
# video downloading module or directly?
# add download progress bars for each video, even if all is pressed
# static geometry
# history

__name__ = "KF Youtube Playlist Downloader"
__version__ = "Alpha v0.1"

import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
	

def main():

	global links
	links = []
	global titles
	titles = []
	
	def errPopup(errmsg):
		popupWin = Toplevel()
		popupWin.title("ERROR")
		popupWin.tk.call('wm','iconphoto',popupWin._w,icon)
		ttk.Label(popupWin, textvariable=error_message).grid(column=0,row=0, sticky="W")
		error_message.set(errmsg)
		ttk.Button(popupWin, text="Okay", command=popupWin.destroy).grid(column=0,row=1)
	
	def displayVideos(num_videos):
		
		for x in links:
			print(yturl(x))
		
		ttk.Label(window, text="Enter path to save videos:").grid(column=1,row=2, padx=1, pady=1, sticky="E")
		ttk.Entry(window, width=70, textvariable=input_savepath).grid(column=2, row=2, padx=1, pady=1, stick="W")
		
		vid_id = 5
		
		for t in titles:
			link = links[vid_id-5]
			ttk.Label(window, text="%s" % (t)).grid(column=1,row=int(vid_id), sticky="E", padx=1, pady=1)	
			ttk.Button(window, text="Download", command=lambda: downloadVideo('one', link)).grid(column=2,row=int(vid_id), padx=1, pady=1, sticky="W")
			#ttk.Separator(window, orient=HORIZONTAL).grid(row=int(vid_id+1), sticky="W,E")
			vid_id += 1
	
		ttk.Button(window, text="Download All", command=lambda: downloadVideo('all', link)).grid(column=2,row=int(vid_id+1), padx=1, pady=1, sticky="W")
	
	def findURLs():
		
		url = str(url_entry.get())
	
		try:
			page_data = requests.get(url)
		except:
			errmsg = "A critical error occured. Please check the validity of the url entered."
			errPopup(errmsg)
			return None
			
		souped = BeautifulSoup(page_data.content, 'html.parser')
		#this class specified below is specifically for videos found in playlists, which is why this can only be used with youtube playlists
		videos = souped.find_all('a', class_='pl-video-title-link yt-uix-tile-link yt-uix-sessionlink spf-link ')
		for x in videos:
			x_ = str(x.encode("utf-8")).strip().split('"')
			y_ = x_.index(' href=')
			link = "https://www.youtube.com"+str(x_[y_+1])
			links.append(link)
			title_ = str(x_[y_+2])[9:-11]
			titles.append(title_)
	
		try:
			url_display.set(url)
		except:
			errmsg = "Could not display url."
			errPopup(errmsg)
			return None
		
		#enter_url.delete(0, 'end')
		
		displayVideos(len(titles))
	
	def downloadVideo(which, link):
		
		save_path = input_savepath.get()
	
		if which == 'one':
			try:
				yt = YouTube(link)
			except:
				errmsg = "Could not connect to Youtube."
				errPopup(errmsg)
			mp4files = yt.filter('mp4')
			d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)
			try:
				d_video.download(save_path)
			except:
				errmsg = "A critical error occured. Please check the validity of the save path entered."
				errPopup(errmsg)
				return None
	
		if which == 'all':
			for v in links:
			    try:
			        yt = YouTube(v)
			    except:
			    	errmsg = "Could not connect to Youtube."
			    	errPopup(errmsg)
		
			    mp4files = yt.filter('mp4')
			    d_video = yt.get(mp4files[-1].extension,mp4files[-1].resolution)
			    try:
			        d_video.download(save_path)
			    except:
			    	errmsg = "Could not download video/s."
			    	errPopup(errmsg)
	
	root = Tk()
	#root.tk.call('tk', 'scaling', 2)
	root.title("Kevin's Youtube Playlist Downloader")
	#root.geometry('600x400')
	global icon
	icon = Image("photo", file=r"C:\Users\kevin\Desktop\Tkinter\pydownloader.png")
	root.tk.call('wm','iconphoto',root._w,icon)
	
	window = ttk.Frame(root, padding="3 3 12 12")
	window.grid(column=0, row=0, sticky=(N, W, E, S))
	window.columnconfigure(0, weight=1)
	window.rowconfigure(0, weight=1)
	
	url_entry = StringVar()
	number_of_videos = StringVar()
	video_list = StringVar()
	url_display = StringVar()
	error_message = StringVar()
	input_savepath = StringVar()
	
	enter_url = ttk.Entry(window, width=70, textvariable=url_entry).grid(column=2, row=1, padx=1, pady=1)
	#user input url
	ttk.Label(window, text="Enter URL here").grid(column=1,row=1, padx=1, pady=1, sticky="E")
	#button to get videos
	ttk.Button(window, text="Retrieve Videos", command=findURLs).grid(column=3,row=1,sticky="W, E")
	ttk.Separator(root, orient=HORIZONTAL).grid(row=3,sticky="E,W")
	#display url just entered
	#ttk.Entry(window, textvariable=url_display).grid(column=1,row=4,sticky="W, E")
	root.mainloop()
	
main()