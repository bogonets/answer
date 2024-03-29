export class ReccError extends Error {
  constructor(message?: string) {
    super(message || 'Recc Error');
  }
}

export class UnsupportedOperationError extends ReccError {
  constructor(message?: string) {
    super(message || 'Unsupported Operation Error');
  }
}

export class IllegalArgumentError extends ReccError {
  constructor(message?: string) {
    super(message || 'Illegal Argument Error');
  }
}

export class TimeoutError extends ReccError {
  constructor(message?: string) {
    super(message || 'Timeout Error');
  }
}

export class UninitializedError extends ReccError {
  constructor(message?: string) {
    super(message || 'Uninitialized Error');
  }
}

export class UninitializedServiceError extends UninitializedError {
  constructor(message?: string) {
    super(message || 'Uninitialized Service Error');
  }
}

export class RefreshTokenError extends ReccError {
  constructor(message?: string) {
    super(message || 'Refresh Token Error');
  }
}

export class ReccCwcError extends ReccError {
  constructor(message?: string) {
    super(message || 'Recc CWC Error');
  }
}

export class ReccCwcOriginMismatchError extends ReccCwcError {
  constructor(message?: string) {
    super(message || 'Recc CWC Origin Mismatch Error');
  }
}

export class ReccCwcUnknownMessageTypeError extends ReccCwcError {
  constructor(message?: string) {
    super(message || 'Recc CWC Unknown Message Type Error');
  }
}
