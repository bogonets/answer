import adminNames from '@/router/names/admin';
import devNames from '@/router/names/dev';
import groupNames from '@/router/names/group';
import rootNames from '@/router/names/root';
import selfNames from '@/router/names/self';

export const names = {
  ...adminNames,
  ...devNames,
  ...groupNames,
  ...rootNames,
  ...selfNames,
};

export default names;
