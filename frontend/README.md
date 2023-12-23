# TURTL 

## Vue

Vue.js is a Javascript Framework to create to create user interfaces.  
It's used to create the frontend for this turtl prototype.

## Recommended IDE Setup for VS Code

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin) to make the TypeScript language service aware of `.vue` types.

If the standalone TypeScript plugin doesn't feel fast enough to you, Volar has also implemented a [Take Over Mode](https://github.com/johnsoncodehk/volar/discussions/471#discussioncomment-1361669) that is more performant. You can enable it by the following steps:

1. Disable the built-in TypeScript Extension
    1) Run `Extensions: Show Built-in Extensions` from VSCode's command palette
    2) Find `TypeScript and JavaScript Language Features`, right click and select `Disable (Workspace)`
2. Reload the VSCode window by running `Developer: Reload Window` from the command palette.

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).
## Bootstrap

This project was created with [create-vue](https://github.com/vuejs/create-vue).

## Setup

### Install Node.js (via nvm)

To be able to develop a Vue.js application, you just need to install Node.js.
You can download and install the current LTS version of [Node.js](https://nodejs.org/en/download/).  

However even node itself recomments to use [nvm](https://github.com/nvm-sh/nvm) to install and manage node.

### Install Dependencies

All dependencies of the project can be found inside the ```package.json``` file.  
To install these dependencies, just run ```npm install``` inside the folder where the ```package.json```  
file is located.

## Scripts

Inside the ```package.json``` are some scripts defined, which can be run like ```npm run <script-name>```.

### Start

With the command ```npm run dev``` a local development server will be deployed, so the Vue.js application
can be accessed from the local browser.

### Lint

The code can be linted with the command ```npm run lint```.  
[ESLint](https://eslint.org/) is used to check and enforce a code style.  
The configuration for ESLint can be found inside ```.eslintrc.cjs```.

### Build

A production version of the Vue.js application can be build with the command ```npm run build```.

## Components

Vue.js uses a component based structure approach. This is a divide and conquer method to handle   
complex logics. So a Calculator for example can be broken into the components display and numpad.  
The numpad can be broken into the components numbers and operations. The components for the  
turtl prototype can be found inside the  ```./src/components``` folder.  
To understand Single-File-Components, have a look at the [Vue.js documentation](https://vuejs.org/guide/scaling-up/sfc.html).

## Pinia  

Pinia is a state management pattern + library to implement a global state for Vue.js applications.
If you have two components A and B and booth display a variable like a username, then the username 
must be defined globally so changes to the username will be displayed in booth components.
Otherwise component A will show the new username and component B the old one. 
Pinia uses so called  ```stores``` to handle this problem. All components inside the application 
can access and modify the ```stores```.  Stores can be found inside ```./stores```.
How Pinia works is explained inside their [documentation](https://pinia.vuejs.org/).