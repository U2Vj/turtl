The frontend in TURTL is implemented in ["Vue 3"](https://vuejs.org), ["Vuetify 3"](https://vuetifyjs.com) and ["Typescript"](https://www.typescriptlang.org). 
The source code of the frontend has the following structure: 

### frontend/src/assets/
- TURTL Logo

### frontend/src/communication/
- **APIRequests.ts:** \
An Axios instance for HTTP requests, initialized with a base URL from environment variables. \
_makeAPIRequest:_ Main function for API requests. Performs API requests, handles authorization and errors, attempts token update when necessary.
- **exeptions.ts:** \
Classes can be used to throw and catch specific types of API-related errors.

### frontend/src/components/
- Contain all components of the frontend.

#### buttons/
- Define and style buttons.

#### layouts/
- Define the default layout of the pages.
- Define the layout of the projects in a classroom, called Project Card.

#### menus/
- Define the Header.
- Define the Footer.
- Define the menu in the Header of the project.

#### modals/
- Contains all pop-up modals of the project. 

#### shell/
- Define the Shell for the 'Solving Task' page. It uses the noVNC library to provide a visual interface for the lab environment.
- As the shell does not synchronize the clipboard between the browser and the VM, a clipboard has been implemented that types a text from the user into the VM. keyboardLayouts.ts is used to define a German keyboard and map special characters to send with VNC.

#### tabs/
- Define the tabs for inviting multiple or single Users.

### src/router
- Define all routes to the pages of an Admin, Student and Instructor. 

- **index.ts:** \
Sets up the Vue Router for the TURTL project. It defines routes and navigation guards based on user authentication status.

### frontend/src/stores
- **CatalogStore.ts:** \
This store enables creating, retrieving, updating, and deleting various classroom-related entities like classrooms, projects, tasks, and instructors. It uses makeAPIRequest from '@/communication/APIRequests' to interact with the backend API. \
Contains classroom (a detailed view of a specific classroom) and classroomList (an array of brief classroom overviews).

- **EnrollmentStore.ts:** \
This store is designed to handle the enrollment process of students in classrooms, task submissions, and retrieval of relevant classroom and task details. It uses makeAPIRequest from '@/communication/APIRequests' to interact with the backend API. \ 
Contains myEnrollments (an array of brief enrollment overviews) and enrollment (a detailed view of a specific enrollment).

- **exeptions.ts:** \
Defines two error classes, ClassroomNotLoadedError and EnrollmentNotLoadedError. These errors can be thrown when the requisite data (classroom or enrollment) is not present during an operation.

- **InvitationStore.ts:** \
This store is intended for handling invitations. It allows for inviting users to different roles, managing multiple invitations, and maintaining a list of both all invitations and those specifically issued by the current user. It uses makeAPIRequest from '@/communication/APIRequests' to interact with the backend API. \ 
Contains two reactive properties, allInvitations and myInvitations, both arrays of Invitation type.

- **UserStore.ts** \
This store is essential for managing user authentication, including login, logout, and role verification. It uses JWT for secure authentication and interacts with the API for various user operations. \
_refreshToken_ and _accessToken_: Stored JWT tokens in local storage, used for authentication. \
_refreshTokenPayload_: Decodes the refresh token to get user information. \
_user_: Constructs a user object from refreshTokenPayload. \

- **VMManagerStore.ts** \
This store is essential for managing the lab environments.
It allows users to start, stop or delete a lab environment and calls the functions from the VM manager using makeAPIRequest from '@/communication/APIRequests'. It also provides helper functions to get a VNC ticket for shell authentication, to check the current environment status and to check if a task has a lab environment configured.

### frontend/src/views
Contains all pages of the TURTL project and uses the components defined in 'src/components/'.

#### admin; instructor; student
Contains all specific pages for the Administrator; Instructor; Student.

#### general
Contains all pages needed by every user.

#### shell
Contains a popout view of the shell component, which allows users to work with the lab_environment in fullscreen in a new tab.

### frontend/src/App.vue
Integrates the Vue Router with the Vuetify application. It is the core layout component for TURTL where different pages will be rendered depending on the route.

### frontend/src/main.ts
Initializing and configuring the Vue application. It sets up the routing, state management, UI components, and notification system. The use of the custom theme allows for consistent styling across the application. Vue Toastification display informative notifications to the user.

### frontend/index.html: Main Application Entry
- Serves as the entry point for the web application.
- Contains the root DOM element `<div id="app"></div>` where the Vue app is mounted.

### frontend/package.json, package-lock.json: Package Management
- Lists dependencies and scripts for the application.
- _package-lock.json_ provides a detailed version record of all installed packages.

### frontend/tsconfig.json, tsconfig.app.json, tsconfig.node.json, tsconfig.vitest.json: TypeScript Configuration
- Defines TypeScript compiler options and project settings.
- Separate configurations for the application, Node.js environment, and Vitest (a testing framework).

### frontend/vite.config.ts, vitest.config.ts: Vite and Vitest Configuration
- _vite.config.ts_: Configures Vite as the build tool, including settings for plugins, server, and build options.
- _vitest.config.ts_: Sets up Vitest for unit and integration testing, specifying test environments and related configurations.

### frontend/env.d.ts: Environmental Type Definitions
- Declares types for environment variables.