<img src="http://www.itcollege.ee/wp-content/themes/itk/images/logo_small.png" /> itc-kit
======

This application is a collection of some tools suitable for a student in the Estonian information technology college.

The application was developed for the Ubuntu linux distribution and can probably run on any linux distibution that runs a desktop environment that uses [GTK](http://en.wikipedia.org/wiki/Category:Desktop_environments_based_on_GTK%2B)
(Notable exception KDE). *Though it has yet to be properly tested.*

The application comes with four main functionalities:

 * Your IT college ÕIS user timetable display on desktop (via Conky) 
 * Email notification for Estonian IT College Webmail
 * Reminder system
 * Productivity tracker

 
### Installation

Just install the .zip of this repo, extract anywhere and run the install.sh script inside with root privleges. 

Note: Please make sure universe repos are enabled: System Settings -> Software & Updates.

In Ubuntu terminal:
```shell
cd path/to/install.sh
sudo sh install.sh
```

This will perform an update for the latest packages, install the necessary dependencies and create a file structure in your home directory (hidden directory .itc-kit). 

An application launcher named "itc-kit" is created. The application can also be run from the terminal with the command "itc-kit.py" or the alias "itc".

<img src="http://enos.itcollege.ee/~kkoert/app_launcher_small.png" />

Running the program creates a toolbar indicator with the IT college icon where you can access all functionality.

<img src="http://enos.itcollege.ee/~kkoert/new_menu.png" />

*Note: Running an untrusted shell script with root privleges can be dangerous, you should check the content of the script first.*

*Don't worry it's simple. :)*

### Timetable

After activating it from the plugins menu you should see a transparent empty timetable on your  desktop. To get your timetable:
 
 * Go to [itcollege.ois.ee](https://itcollege.ois.ee/) and log in
 * Go to timetable and select Ical
 * Copy the URL
 * Select the applications timetable submenu
 * Set ical URL

The color and number of days displayed can be changed in the Timetable submenu.

*Note: Currently the application only supports the english version of the timetable. ÕIS Language can be changed in the upper left corner.*

<img src="http://enos.itcollege.ee/~kkoert/timetable.png" />

### Email

Activating the plugin should prompt you for an email and password. Here use your IT college email username and password.

You should now hear a sound and see a notification icon in the application indicator when you recieve an email. After opening the main menu you will see the the sender. 

<img src="http://enos.itcollege.ee/~kkoert/email_small.png" />

*Note: If you name is for example Mikk Pulk then although your username is mpulk your email is still **mikk.pulk@itcollege.ee***

### Reminders

This plugin allows you to create reminders that will trigger at the specified time in the application indicator.

<img src="http://enos.itcollege.ee/~kkoert/stahp_small.png" />

### Productivity tracker

Activating this plugin will allow the tracking of three types of activities. Those that are productive, neutral or counterproductive. 

Three rings displaying the percentages of each activity are displayed in the lower right corner of the screen. 

<img src="http://enos.itcollege.ee/~kkoert/time_manager.png" />

### Development Team

Itc-kit was created by:

[Kristo Koert](https://github.com/KristoKoert) (Software architecture, all python code, installation script)

[Johannes Vatsfeldt](https://github.com/JVats)
 (Design choices, all lua code, conky configuration files)

[Sten Luhtoja](https://github.com/Steckenbauer)
 (Contributed to designing/testing ical parsing system)
 
### Contact

Kristo Koert email: kristo.koert@itcollege.ee

Note: Olen tavaline tudeng, võtke julgelt ühendust kui probleeme, soovitusi või tahate panustada. :) 

### Contributing

All pull request are welcome!

### Licence

Itc-kit is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
