# X-wing Miniatures Overlay Generator
Work in Progress.

## Overview
Generates a HTML overlay for use in OBS Studio (or similar, not really attempted anything else) for streaming X-wing miniatures games.

Takes XWS files as imports, and allows many of them. Generates the starting stats for the ship based on the base values + upgrades. Pair up squads to create a 'match' and the overlay is generated.

When a match is created, a control panel is available that uses websockets to push the changes (e.g. losing shield/hull, discarding upgrade cards) back to the overlay in realtime, no overlay editing required.

Uses lots of good stuff made by other people: please see point 1 in ToDo for why I've not listed them here...

Feedback & Contributions welcome!

Now with WorksForMe™ vagrant-y goodness:

```bash
git clone https://github.com/sheepeatingtaz/xwingoverlayer.git
cd xwingoverlayer
vagrant up
```

Open a browser and got to http://localhost:8008 and you're in!

{more usage instructions to follow}


### ToDo:
1. write a better readme
2. make Control page nicer
3. when ship hull == 0, grey out all fields
4. match timer displayed on overlay
5. Add Damage Deck, Pilot & Upgrade card "viewer" to the overlay & control
6. Hide upgrade icons? Not really relevant, but look nice.
7. ~~Vagrant Setup for instadeploy~~
8. Heroku Deployment for instadeploy
9. Write some tests & get something to automatically build 

### Screenshots:
#### Home Page
![Home Page](screenshots/home.png?raw=true "Home Page")

#### Import Page
![Import Page](screenshots/import.png?raw=true "Import Page")

#### Create Match Page
![Create Match Page](screenshots/create.png?raw=true "Create Match Page")

#### List Matches Page
![List Matches Page](screenshots/list.png?raw=true "List Matches  Page")

#### Control Page
![Control Page](screenshots/control.png?raw=true "Control Page")

#### Overlay Page
![Overlay Page](screenshots/overlay.png?raw=true "Overlay Page")