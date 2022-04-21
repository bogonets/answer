import sha256 from 'sha256';

export function encryptSha256(password: string): string {
  return sha256(password);
}
