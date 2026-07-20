## Overview of Classrooms, Projects, and Tasks

### Classrooms
A **Classroom** in TURTL acts as an overarching entity that encompasses various projects. It serves as a virtual space where all related projects are organized and accessible, providing a structured environment for learning and teaching.

### Projects
Within a Classroom, you find multiple **Projects**. A Project is a collection of tasks aimed at achieving specific learning objectives, organizing tasks into a unit that focuses on a particular theme or skill set. Projects are dynamic, allowing modifications and additions.

### Tasks
**Tasks** are individual learning activities at the core of each Project. They vary in type and difficulty.

#### Task Types
Tasks in TURTL are categorized into three types:
1. **Neutral:** Focus on foundational concepts and skills.
2. **Defense:** Teach protective strategies and cybersecurity practices.
3. **Attack:** Provide insight into offensive techniques and exploitation.

#### Difficulty Levels
Tasks are classified into three difficulty levels:
1. **Beginner:** Cover basic concepts, suitable for newcomers.
2. **Intermediate:** Delve deeper, for learners with foundational knowledge.
3. **Advanced:** Challenging tasks for learners with a strong grasp of core concepts.

#### Acceptance Criteria
Each task comes with specific acceptance criteria:
- **RegEx (Regular Expressions):** Creating or interpreting regular expressions.
- **Flags:** Finding and retrieving flags through command-line interactions.
- **Quizzes:** Single or multiple-choice questions to test understanding.

## Overview of User Roles in TURTL
TURTL supports three distinct user roles: Student, Instructor, and Administrator. Each role provides access to a set of functionalities and determines the content displayed in the header. 

### 1. Student
- **Enrollment:** Students can enroll in classrooms.
- **Access Information:** They have access to information about the classroom and all its associated projects.
- **Task Solving:** Students can solve tasks within their classrooms.

### 2. Instructor
- **Student Capabilities:** Instructors have all the capabilities of a student.
- **Classroom Management:** They can create new classrooms and projects, as well as tasks within these projects.
- **Content Editing:** Instructors have the ability to edit the classrooms and projects they have created.
- **Invitations:** They can invite users to join the TURTL project.

### 3. Administrator
- **Instructor Capabilities:** Administrators have all the capabilities of an instructor.
- **System-Wide Editing:** They can edit any classroom in the system, regardless of who created it.
- **Role Assignment:** Administrators have the authority to assign user roles within the Django admin panel.