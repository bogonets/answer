export class EmptyException extends Error {
  constructor(message?: string) {
    super(message);
  }
}

export class UndefinedException extends Error {
  constructor(message?: string) {
    super(message);
  }
}

export class TypeException extends TypeError {
  constructor(message?: string) {
    super(message);
  }
}
