import mainNames from '@/router/names/main';
import MainDashboard from '@/pages/main/MainDashboard.vue';
import MainFiles from '@/pages/main/MainFiles.vue';
import MainKanban from '@/pages/main/MainKanban.vue';
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
import MainVmsDevicesEditInfo from '@/pages/main/MainVmsDevicesEditInfo.vue';
import MainVmsDevicesEditLive from '@/pages/main/MainVmsDevicesEditLive.vue';
import MainVmsDevicesEditRecord from '@/pages/main/MainVmsDevicesEditRecord.vue';
import MainVmsDevicesEditEvents from '@/pages/main/MainVmsDevicesEditEvents.vue';
import MainVmsDevicesEditEventConfigsEdit from '@/pages/main/MainVmsDevicesEditEventConfigsEdit.vue';
import MainVmsDevicesEditEventConfigsNew from '@/pages/main/MainVmsDevicesEditEventConfigsNew.vue';
import MainVmsDevicesNew from '@/pages/main/MainVmsDevicesNew.vue';
import MainVmsEventsCalendar from '@/pages/main/MainVmsEventsCalendar.vue';
import MainVmsEventsList from '@/pages/main/MainVmsEventsList.vue';
import MainVmsLayouts from '@/pages/main/MainVmsLayouts.vue';
import MainVmsLayoutsEdit from '@/pages/main/MainVmsLayoutsEdit.vue';
import MainVmsLayoutsNew from '@/pages/main/MainVmsLayoutsNew.vue';
import MainVmsLive from '@/pages/main/MainVmsLive.vue';
import MainVmsUserConfigs from '@/pages/main/MainVmsUserConfigs.vue';

// External
import mainAirjoyChildren from '@/router/children/external/airjoy/main';
import RootGroups from "@/pages/RootGroups.vue";
import rootNames from "@/router/names/root";

export const mainChildren = [
    {
        path: ':group/:project/dashboard',
        component: MainDashboard,
        name: mainNames.mainDashboard,
    },
    {
        path: ':group/:project/kanban',
        component: MainKanban,
        name: mainNames.mainKanban,
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
        children: [
            {
                path: 'info',
                component: MainVmsDevicesEditInfo,
                name: mainNames.mainVmsDevicesEditInfo,
            },
            {
                path: 'live',
                component: MainVmsDevicesEditLive,
                name: mainNames.mainVmsDevicesEditLive,
            },
            {
                path: 'record',
                component: MainVmsDevicesEditRecord,
                name: mainNames.mainVmsDevicesEditRecord,
            },
            {
                path: 'events',
                component: MainVmsDevicesEditEvents,
                name: mainNames.mainVmsDevicesEditEvents,
            },
        ]
    },
    {
        path: ':group/:project/vms/devices/edit/:device/event/configs/edit/:config',
        component: MainVmsDevicesEditEventConfigsEdit,
        name: mainNames.mainVmsDevicesEditEventConfigsEdit,
    },
    {
        path: ':group/:project/vms/devices/edit/:device/event/configs/new',
        component: MainVmsDevicesEditEventConfigsNew,
        name: mainNames.mainVmsDevicesEditEventConfigsNew,
    },
    {
        path: ':group/:project/vms/devices/new',
        component: MainVmsDevicesNew,
        name: mainNames.mainVmsDevicesNew,
    },
    {
        path: ':group/:project/vms/events/calendar',
        component: MainVmsEventsCalendar,
        name: mainNames.mainVmsEventsCalendar,
    },
    {
        path: ':group/:project/vms/events/list',
        component: MainVmsEventsList,
        name: mainNames.mainVmsEventsList,
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
    {
        path: ':group/:project/vms/live',
        component: MainVmsLive,
        name: mainNames.mainVmsLive,
    },
    {
        path: ':group/:project/vms/user/configs',
        component: MainVmsUserConfigs,
        name: mainNames.mainVmsUserConfigs,
    },

    ...mainAirjoyChildren,
];

export default mainChildren;
