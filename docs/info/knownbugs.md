## Frontend
* Bug when visiting the invitations page through the top navigation bar: The page is sometimes blank. The same applies when going back from the invitations page to any other page.
* There is no validation being performed when editing a classroom or project title in the frontend, only when creating new projects or classrooms.
* There is no warning (e.g. through a modal) when a student unenrolls from a classroom. They should be warned and asked for confirmation because unenrolling results in all of their progress within the classroom being lost.
* The frontend does not show the task type or difficulty of tasks to students anywhere, but they must be set by instructors.
* Sometimes, if the connection to the server is lost for some time, HTTP 500 Errors will appear until the page is hard refreshed.

## Backend
* Validation of incoming data could be better:
  * Text fields often have no minimum value set and can contain anything, including just numbers or special characters.
  * Password validation is only performed in terms of length, the Django password validators are ignored. A workaround can be written to validate the password properly (e.g. not too common, must include letters and numbers etc.).
* For AcceptanceCriteria, the backend defines a `criteria_type`. The sole reason this type is present is because originally, there also should have been a criteria type of `MANUAL`. This would allow instructors to mark a task as solved per-student manually. The model exists but this feature has not been implemented yet. Currently, it is possible to create a task with AcceptanceCriteria of type `MANUAL` via the backend API, but in reality, it behaves exactly the same as no AcceptanceCriteria at all, i.e. a `criteria_type` of `DISABLED`. It should either be implemented properly, or the `criteria_type` should be omitted as it adds unnecessary overhead and confusion.

## Shell
* The shell view could be better. Because it uses noVNC under the hood the display is dependend on the display settings of the underlying VM. A Fullscreen Window has been implemented to mitigate this but offering a xterm shell for VMs that do not need a desktop could be benificial.

* If not used for a while the display will be black and the user needs to press a random key to bring it back.

* The shell does not work in nested vnc environments where different keyboard layouts are translated. When typing gibberish characters will appear.

* Scrolling in the shell does not work.

* To type in the shell a user needs to click on the display itself. Clicking outside of it, to use the Clipboard will loose the focus.

