# Vue.js
Vue.js is a Javascript Framework to create to create user interfaces.  
It's used to create the frontend for this turtl prototype.

## Setup
### Install Node.js
To be able to develop a Vue.js application, you just need to install Node.js.  
So download and install the current LTS version of [Node.js](https://nodejs.org/en/download/).  
To verify that the installation was successful, open a console/cmd/terminal and run: ```node-v```  
followed by ```npm -v``` both command should print out the current versions.
### Install Dependencies
All dependencies of the project can be found inside the ```package.json``` file.  
To install these dependencies, just run ```npm install``` inside the folder where the ```package.json```  
file is located.
### Conflicting/Broken Dependencies
If some dependencies are conflicting with each other or broken, you can   
find the version, inside the ```npm_versionss.txt``` file, of each dependency used during initial   
development of the prototype. These versions can be hardcoded inside the ```package.json``` as a fallback.

## Scripts
Inside the ```package.json``` are some scripts defined, which can be run like ```npm run <script-name>```.
### Start
With the command ```npm run start``` a local development server will be deployed, so the Vue.js application
can be accessed from the local browser.
### Lint
The code can be linted with the command ```npm run lint```.  
[ESLint](https://eslint.org/) is used to check and enforce a code style.  
The configuration for ESLint can be found inside ```.eslintrc.js```.
### Build
A production version of the Vue.js application can be build with the command ```npm run build```.

## Components
Vue.js uses a component based structure approach. This is a divide and conquer method to handle   
complex logics. So a Calculator for example can be broken into the components display and numpad.  
The numpad can be broken into the components numbers and operations. The components for the  
turtl prototype can be found inside the  ```./src/components``` folder.  
To understand Single-File-Components, have a look at the [Vue.js documentation](https://vuejs.org/v2/guide/single-file-components.html).

## Vuex  
Vuex is a state management pattern + library to implement a global state for Vue.js applications.
If you have two components A and B and booth display a variable like a username, then the username 
must be defined globally so changes to the username will be displayed in booth components.
Otherwise component A will show the new username and component B the old one. 
Vuex is a so called ```store``` to handle this problem. All components inside the application 
can access and modify the ```store```.  It can be found inside the ```./store/index.ts``` file.
How Vuex works is explained inside their [documentation](https://vuex.vuejs.org/).
