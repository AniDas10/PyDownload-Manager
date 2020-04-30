from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import os.path
from PyQt5.uic import loadUiType
import urllib.request
from pafy import *
import humanize

ui,_ = loadUiType('main.ui')

class MainApp(QMainWindow, ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.InitUI()
        self.Handle_Buttons()

    def InitUI(self):
        ## contain all ui changes in loading
        pass

    def Handle_Buttons(self):
        ## handle all buttons in the app
        self.pushButton.clicked.connect(self.Download)
        self.pushButton_2.clicked.connect(self.Handle_Browse)
        self.pushButton_5.clicked.connect(self.Get_Video_Data)
        self.pushButton_4.clicked.connect(self.Download_Video)
        self.pushButton_3.clicked.connect(self.Save_Browse)
        self.pushButton_8.clicked.connect(self.Playlist_Download)
        self.pushButton_6.clicked.connect(self.Playlist_Save_Browse)
        
        self.pushButton_11.clicked.connect(self.Open_Youtube)
        self.pushButton_12.clicked.connect(self.Open_Download)
        self.pushButton_13.clicked.connect(self.Open_Home)
        self.pushButton_14.clicked.connect(self.Open_Settings)
        
        self.pushButton_7.clicked.connect(self.Theme_DarkOrange)
        self.pushButton_9.clicked.connect(self.Theme_Dark)
        self.pushButton_10.clicked.connect(self.Theme_DarkGray)

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        ## Calculate the progress
        readed_data = blocknum*blocksize
        if totalsize>0:
            download_percentage = readed_data*100/totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()
        
    def Handle_Browse(self):
        ## Enable browsing to our OS, pick save location
        save_location = QFileDialog.getSaveFileName(self, caption='Save As', directory='.',filter="All Files(*)")
        save_location_path = str(save_location[0])
        self.lineEdit_2.setText(save_location_path)
        
    def Download(self):
        ## Downloading any file
        download_url = self.lineEdit.text()
        save_location = self.lineEdit_2.text()
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide valid URL or location")
        else:
            try:
                urllib.request.urlretrieve(download_url, save_location, self.Handle_Progress)
            except Exception:
                QMessageBox.warning(self, "Download Error", "Provide valid URL or location")
                return 

        self.progressBar.setValue(100)

        QMessageBox.information(self, "Download Completed", "Your file has been downloaded successfully")        
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.progressBar.setValue(0)


    ###########################################
    #For downloading a single video
    ###########################################
    

    def Save_Browse(self):
        ## Save the location in the line_edit after we browse
        save_location = QFileDialog.getSaveFileName(self, caption='Save As', directory='.',filter="All Files(*)")
        save_location_path = str(save_location[0])
        self.lineEdit_4.setText(save_location_path)
        
    def Get_Video_Data(self):
        video_url = self.lineEdit_3.text()
        if video_url == '':
            QMessageBox.warning(self, "Data Error", "Provide valid URL or location")
        else:
            video = pafy.new(video_url)
            video_streams = video.videostreams
            for stream in video_streams:
                size = humanize.naturalsize(stream.get_filesize())
                data = "{} {} {} {}".format(stream.mediatype, stream.extension, stream.quality, size)
                self.comboBox.addItem(data)
    
    def Download_Video(self):
        video_url = self.lineEdit_3.text()
        save_location = self.lineEdit_4.text()

        if video_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide a valid URL or Location")
        else:
            video = pafy.new(video_url)
            video_stream = video.videostreams
            video_quality = self.comboBox.currentIndex()
            download = video_stream[video_quality].download(filepath=save_location, callback=self.Video_Progress) 

    def Video_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total>0:
            download_percentage = read_data*100/total
            self.progressBar_2.setValue(download_percentage)
            remaining_time = round(time/60, 2)

            self.label_6.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()
        
    ###########################################
    # For downloading Playlist
    ###########################################
    
    def Playlist_Download(self):
        playlist_url = self.lineEdit_5.text()
        save_location = self.lineEdit_6.text()

        if playlist_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error", "Provide valid PLaylist URL or Location")
        else:
            playlist = get_playlist(playlist_url)
            playlist_videos = playlist['items']
            self.lcdNumber_2.display(len(playlist_videos))

        os.chdir(save_location)
        if os.path.exists(str(playlist['title'])):
            os.chdir(str(playlist['title']))
        else:
            os.mkdir(str(playlist['title']))
            os.chdir(str(playlist['title']))

        current_video_in_download = 1
        quality = self.comboBox_2.currentIndex()
        QApplication.processEvents()
            
        for video in playlist_videos:
            current_video = video['pafy']
            current_video_stream = current_video.videostreams
            self.lcdNumber.display(current_video_in_download)
        
            download = current_video_stream[quality].download(callback=self.Playlist_Progress)
            QApplication.processEvents()
            current_video_in_download += 1


    def Playlist_Progress(self, total, received, ratio, rate, time):
        read_data = received
        if total>0:
            download_percentage = read_data*100/total
            self.progressBar_3.setValue(download_percentage)
            remaining_time = round(time/60, 2)

            self.label_7.setText(str('{} minutes remaining'.format(remaining_time)))
            QApplication.processEvents()
    
    def Playlist_Save_Browse(self):
        playlist_save_location = QFileDialog.getExistingDirectory(self, "Select Download Directory")
        self.lineEdit_6.setText(playlist_save_location)

    ###########################################
    ## UI Changes Method
    ###########################################

    def Open_Home(self):
        self.tabWidget_2.setCurrentIndex(0)

    def Open_Download(self):
        self.tabWidget_2.setCurrentIndex(1)
   
    def Open_Youtube(self):
        self.tabWidget_2.setCurrentIndex(2)
   
    def Open_Settings(self):
        self.tabWidget_2.setCurrentIndex(3)

    ###########################################
    ## App themes
    ###########################################
    def Theme_DarkOrange(self):
        style = open('themes/darkorange.css','r')
        style = style.read()
        self.setStyleSheet(style)

    def Theme_Dark(self):
        style = open('themes/qdark.css','r')
        style = style.read()
        self.setStyleSheet(style)
        
    def Theme_DarkGray(self):
        #style = open('themes/qdarkgray.css','r')
        #style = style.read()
        self.setStyleSheet('')
        


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()