export class Member {
  id: string
  auth: string
  level: number
  constructor(id: string, auth: string, level = 0) {
    this.id = id
    this.auth = auth
    this.level = level
  }
}

