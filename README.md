# CLITimeManager

This is time manager to manage time spended on tasks<br>
From programmer to programmers<br>

This app has <b>NO</b> fancy UI, <b>NO</b> big complicated data bases, <b>NO</b> online functions, <b>NO</b> third parties hyped modules<br>
Just bare bone python, cli and json DB<br>
That`s it!<br><br>

Despite simplicity it has all the instruments to track down time spended on a tasks<br>
You can create/edit/delete task, manually add time, search through the working days<br>
App track down every second while you at work and when you do not<br>
(as long as app is up and running)<br>

To run it just proced to working directory and type ``` python main.py ```<br>
If you want it to be compiled type ``` python compiler.py ```. But this require to download heavy stuff<br>

### How to use it?

Basically you can find help inside the app, but here it is


```
Input "Begin" then create and start a new task
Input "Current" and you will continue last active task
Input "Return" will take you back to previous tasks
Input "Read time" show how much time is spend on each task
  add -n chose a task and return all time for one task
  add -d chose a date and return all time for all tasks
    press Enter and return time for current day
Input "Delete task" and chose task to remove (in the current day by default)
Input "Erase" and flush entire json DB
  add -one and chose one date to flush
Input "Enter time" and chose task to add time to 
  add -r and remove last time record
Input "cls" to clean the console
```

#### This is how it looks like

![cmd_Q2Jpe0IIlc](https://github.com/Frisle/CLITimeManager/assets/47441164/ffb8a70e-e435-4d72-b1d5-041bf9ead46d)

Beautiful, is not it?
