from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk

from selenium import webdriver 
import time
from webdriver_manager.chrome import ChromeDriverManager
import os

class youtubeSearcher:
    def __init__(self, root):
        self.searchLabel = Label(root, text="Video name: ")
        self.searchLabel.grid(row = 0, column = 0)
        videoTitle = StringVar()
        self.searchBox = Entry(root, textvariable=videoTitle)
        self.searchBox.grid(row = 0, column = 1)

        self.viewsLabel = Label(root, text="Min Views: ")
        self.viewsLabel.grid(row = 1, column = 0)
        viewCount = StringVar()
        self.viewsBox = Entry(root, textvariable=viewCount)
        self.viewsBox.grid(row = 1, column = 1)

        searchButton = tk.Button(root, text="SEARCH", command= self.search, height = "1", width = "16")
        searchButton.grid(row = 2, column = 1)
    
    def search(self):
        url = "https://www.youtube.com/results?search_query=" + self.searchBox.get() + "&sp=CAM%253D"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        driver.set_window_position(-3000,0)
        time.sleep(5)

        vidTitle = driver.find_elements_by_xpath('//*[@id="video-title"]')
        titles = []
        urls = []
        aria = []
        for i in vidTitle:
            titles.append(i.get_attribute('title'))
            urls.append(i.get_attribute('href'))
            aria.append(i.get_attribute('aria-label'))
        
        #gets the views to check later
        viewsCount = []
        for i in range(0, len(aria)):
            temp = aria[i].split()
            viewTemp = temp[-2]
            viewsCount.append(int(viewTemp.replace(',', '')))
        
        #saves the top 15 views in the file, not going below the min threshold
        outputFile = open('YoutubeTopViews.txt', 'w')
        viewThreshold = int(self.viewsBox.get())
        count = 1
        for i in range(0, len(viewsCount)):
            if (viewsCount[i] > viewThreshold) and (count < 11):
                outputFile.write("%s)\tTitle: %s\n\tViews: %d\n\tLink: %s\n\n" % (count, titles[i], viewsCount[i], urls[i]))
                count = count + 1
            else:
                continue
        outputFile.close()
        driver.quit()

             

root = tk.Tk()
main = youtubeSearcher(root)
root.mainloop()
