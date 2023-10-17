export class ClassroomNotLoadedError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'ClassroomNotLoadedError'
  }
}
export class TaskNotLoadedError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'TaskNotLoadedError'
  }
}
