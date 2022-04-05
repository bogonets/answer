import {AssertionException} from '@/exceptions';

export function assertTrue(condition?: any): asserts condition {
  if (!condition) {
    throw new AssertionException('Invalid condition error');
  }
}

export function assertFalse(condition?: any): asserts condition {
  if (condition) {
    throw new AssertionException('Invalid condition error');
  }
}
