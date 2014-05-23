<img src="http://www.itcollege.ee/wp-content/themes/itk/images/logo_small.png" /> itc-kit
======

This application is a collection of some tools suitable for a student in the Estonian Information technology college.

The application was developed for the Ubuntu linux distribution and can probably run on any linux distibution that runs a desktop environment that uses [GTK](http://en.wikipedia.org/wiki/Category:Desktop_environments_based_on_GTK%2B)
(Notable exception KDE). *Though it has yet to be properly tested.*

The application comes with four main functionalities:

 * Your IT college ÕIS user timetable display on desktop (via Conky) 
 * Email notification for Estonian IT College Webmail
 * Reminder system
 * Productivity tracker

 
### Installation

Just install the .zip of this repo, extract anywhere and run the install.sh script inside. 

In Ubuntu terminal:
```shell
cd path/to/install.sh
sudo sh install.sh
```

This will perform an update for the latest packages, install the necessary dependencies and create a file structure in your home directory (hidden directory .itc-kit). 

An application launcher named "itc-kit" is created. The application can also be run from the terminal with the command "itc-kit.py" or the alias "itc".

<img src="http://enos.itcollege.ee/~kkoert/app_launcher_small.png" />

Running the program creates a toolbar indicator with the IT college icon where you can access all functionality.

<img src="http://enos.itcollege.ee/~kkoert/All_small.png" />

*Note: Running an untrusted shell script with root privleges can be dangerous, you should check the content of the script first.*

*Don't worry it's simple. :)*

### Timetable

After activating it from the plugins menu you should see a transparent empty timetable on your  desktop. To get your timetable:
 
 * Go to [itcollege.ois.ee](https://itcollege.ois.ee/) and log in
 * Go to timetable and select Ical
 * Copy the URL
 * Select the applications timetable submenu
 * Set ical URL

*Note: Currently the application only supports the english version of the timetable. ÕIS Language can be changed in the upper left corner.*

<img src="http://enos.itcollege.ee/~kkoert/timetable.png" />

### Email

Activating the plugin should prompt you for an email and password. Here use your IT college email username and password.

You should now see the indicator alert and see the the sender when you have new unread email.

<img src="http://enos.itcollege.ee/~kkoert/email_small.png" />

*Note: If you name is for example Mikk Pulk then although your username is mpulk your email is still **mikk.pulk@itcollege.ee***

### Reminders

This plugin allows you to create reminders that will trigger at the specified time in the application indicator.

<img src="http://enos.itcollege.ee/~kkoert/stahp_small.png" />

### Productivity tracker

This plugin has not been completely implemented yet. Though it can be used and everything works the display conky element is currently not functional. 

