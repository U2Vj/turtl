export class ClassroomNotLoadedError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'ClassroomNotLoadedError'
  }
}

export class EnrollmentNotLoadedError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'EnrollmentNotLoadedError'
  }
}
