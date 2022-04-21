import adminAirjoyNames from '@/router/names/external/airjoy/admin';
import AdminAirjoyDevices from '@/pages/external/airjoy/admin/AdminAirjoyDevices.vue';

export const adminAirjoyChildren = [
  {
    path: 'airjoy/devices',
    component: AdminAirjoyDevices,
    name: adminAirjoyNames.adminAirjoyDevices,
  },
];

export default adminAirjoyChildren;
