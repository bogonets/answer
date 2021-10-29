import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainFiles from '@/pages/main/MainFiles.vue';
import MainLayouts from '@/pages/main/MainLayouts.vue';
import MainMembers from '@/pages/main/MainMembers.vue';
import MainSettings from '@/pages/main/MainSettings.vue';
import MainTables from '@/pages/main/MainTables.vue';
import MainTasks from '@/pages/main/MainTasks.vue';
import MainVisualProgramming from '@/pages/main/MainVisualProgramming.vue';
import MainVmsDevices from '@/pages/main/MainVmsDevices.vue';
import MainVmsDevicesDiscovery from '@/pages/main/MainVmsDevicesDiscovery.vue';
import MainVmsDevicesDiscoveryEpr from '@/pages/main/MainVmsDevicesDiscoveryEpr.vue';
import MainVmsDevicesEdit from '@/pages/main/MainVmsDevicesEdit.vue';
import MainVmsDevicesNew from '@/pages/main/MainVmsDevicesNew.vue';
import MainVmsLayouts from '@/pages/main/MainVmsLayouts.vue';
import MainVmsLayoutsEdit from '@/pages/main/MainVmsLayoutsEdit.vue';
import MainVmsLayoutsNew from '@/pages/main/MainVmsLayoutsNew.vue';
import MainVmsLive from '@/pages/main/MainVmsLive.vue';

// External
import mainAirjoyChildren from '@/router/children/external/airjoy/main';

export const mainChildren = [
    {
        path: ':group/:project/dashboard',
        component: MainDashboard,
        name: mainNames.mainDashboard,
    },
    {
        path: ':group/:project/files',
        component: MainFiles,
        name: mainNames.mainFiles,
    },
    {
        path: ':group/:project/layouts',
        component: MainLayouts,
        name: mainNames.mainLayouts,
    },
    {
        path: ':group/:project/members',
        component: MainMembers,
        name: mainNames.mainMembers,
    },
    {
        path: ':group/:project/settings',
        component: MainSettings,
        name: mainNames.mainSettings,
    },
    {
        path: ':group/:project/tables',
        component: MainTables,
        name: mainNames.mainTables,
    },
    {
        path: ':group/:project/tasks',
        component: MainTasks,
        name: mainNames.mainTasks,
    },
    {
        path: ':group/:project/vp',
        component: MainVisualProgramming,
        name: mainNames.mainVisualProgramming,
    },
    {
        path: ':group/:project/vms/live',
        component: MainVmsLive,
        name: mainNames.mainVmsLive,
    },
    {
        path: ':group/:project/vms/devices',
        component: MainVmsDevices,
        name: mainNames.mainVmsDevices,
    },
    {
        path: ':group/:project/vms/devices/discovery',
        component: MainVmsDevicesDiscovery,
        name: mainNames.mainVmsDevicesDiscovery,
    },
    {
        path: ':group/:project/vms/devices/discovery/:epr',
        component: MainVmsDevicesDiscoveryEpr,
        name: mainNames.mainVmsDevicesDiscoveryEpr,
    },
    {
        path: ':group/:project/vms/devices/edit/:device',
        component: MainVmsDevicesEdit,
        name: mainNames.mainVmsDevicesEdit,
    },
    {
        path: ':group/:project/vms/devices/new',
        component: MainVmsDevicesNew,
        name: mainNames.mainVmsDevicesNew,
    },
    {
        path: ':group/:project/vms/layouts',
        component: MainVmsLayouts,
        name: mainNames.mainVmsLayouts,
    },
    {
        path: ':group/:project/vms/layouts/edit/:layout',
        component: MainVmsLayoutsEdit,
        name: mainNames.mainVmsLayoutsEdit,
    },
    {
        path: ':group/:project/vms/layouts/new',
        component: MainVmsLayoutsNew,
        name: mainNames.mainVmsLayoutsNew,
    },

    ...mainAirjoyChildren,
];

export default mainChildren;
