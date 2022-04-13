export class UninitializedServiceError extends Error {
  constructor(message?: string) {
    super(message || 'Uninitialized Service Error');
  }
}

export class RefreshTokenError extends Error {
  constructor(message?: string) {
    super(message || 'Refresh Token Error');
  }
}
