# Freezing Internet Tool
`FIT` is a Python3 application for forensic acquisition of contents like web pages, emails, social media, etc. directly from the internet. 
This is a final exam for a Master named Cybersecurity, Digital Forensics e Data Protection and is inspired by [FAW](https://www.fawproject.com/). For this Master Thesis, I have developed a "light" release that allows acquiring a public WEB page (no private) in forensics mode by storing the following elements: source code, screen recorder, network capture etc. The ambition, however, is to create - in subsequent release phases- other modules capable of acquiring additional types of internet contents as, for example, web pages accessible with credentials, emails, Facebook or Instagram profiles/pages, etc. For this reason, the project has been developed with a modular architecture, so that many modules (case, screen recorder, packet capture) can be reused. 

For the implementation, I used:
* MVC Pattern
* Python Language
* Qt as graphical user interface
* Pyshark (wrapper for Tshark) which a sniffer (similar to Sun's snoop or tcpdump)
* OpenVC and Pyautogui for screen capture


## Prerequisites
Make sure you have installed all of the following prerequisites on your development machine:
* Wireshark - [Download & Install Wireshark](https://www.wireshark.org/download/). Network traffic analyzer, or "sniffer", for Linux, macOS, *BSD and other Unix and Unix-like operating systems and for Windows.


## Please note
For save all resource (html, css, js, image, etc.) of a web page I used [pywebcopy](https://pypi.org/project/pywebcopy/), but I don't know why, the "original" version hangs the console and does not exit. 
_If I have correctly understood, this issue is already [known](https://github.com/rajatomar788/pywebcopy/issues/46)_. 
David W Grossman has found a workaround, he removed all multithreading and committed this version [here](https://github.com/davidwgrossman/pywebcopy). 
For this reason, I used this "unofficial" version in the local lib path. **Thanks to David W Grossman @davidwgrossman**.
For the web.py module I started from this [project](https://github.com/tech35/Python-Browser-Version-2). **Thanks to Bilawal Asghar @tech35**
