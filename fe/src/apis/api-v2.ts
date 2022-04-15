import Vue from 'vue';

import ReccApi from '@recc/api/dist';
import {LocalStore} from '@/store/localStore';
import router from '@/router';
import rootNames from '@/router/names/root';
import {RawLocation} from 'vue-router';

import type {
    AirjoySensorA,
    AirjoyDeviceA,
    AirjoyCreateDeviceQ,
    AirjoyUpdateDeviceQ,
    AirjoyControlQ,
    AirjoyChartA,
    AirjoyServiceA,
    AirjoyCreateServiceQ,
    AirjoyUpdateServiceQ,
} from '@/packet/airjoy';
import type {
    VmsImageA,
    VmsUploadImageQ,
    VmsUploadImageA,
    VmsDeviceA,
    VmsCreateDeviceQ,
    VmsUpdateDeviceQ,
    VmsLayoutA,
    VmsCreateLayoutQ,
    VmsUpdateLayoutQ,
    VmsEventConfigA,
    VmsCreateEventConfigQ,
    VmsUpdateEventConfigQ,
    VmsEventTagA,
    VmsCreateEventTagQ,
    VmsUpdateEventTagQ,
    VmsEventA,
    VmsFilterEventQ,
    VmsNewsEventQ,
    VmsLatestEventQ,
    VmsEventImageA,
    VmsDiscoveryQ,
    VmsDiscoveredHeartbeatQ,
    VmsDiscoveredHeartbeatA,
    VmsOnvifMediaStreamUriQ,
    VmsOnvifMediaStreamUriHeartbeatQ,
    VmsOnvifMediaStreamUriHeartbeatA,
    VmsOnvifMediaSnapshotQ,
    VmsOnvifMediaSnapshotA,
    IceServerA,
    RtcOfferQ,
    RtcAnswerA,
    VmsEventConfigColorQ,
    VmsEventConfigDetectionQ,
    VmsEventConfigMatchingQ,
    VmsEventConfigOcrQ,
} from '@/packet/vms';
import type {VmsRecordRangeA} from '@/packet/vms/record_range';

function moveTo(name: string) {
    if (router.currentRoute.name === name) {
        return;
    }

    const rawLocation = {
        name: name,
    } as RawLocation;

    router.push(rawLocation).catch((reason: any) => {
        if (reason.name !== 'NavigationDuplicated') {
            throw reason;
        }
    });
}

function clearSession() {
    const localStore = Vue.prototype.$localStore as LocalStore;
    localStore.clearSession();
}

function renewalAccessToken(access: string) {
    const localStore = Vue.prototype.$localStore as LocalStore;
    localStore.access = access;
}

export default class ApiV2 extends ReccApi {
    constructor() {
        super({
            onRefreshTokenError: () => {
                clearSession();
                moveTo(rootNames.signin);
            },
            onRenewalAccessToken: (accessToken: string) => {
                renewalAccessToken(accessToken);
            },
            onUninitializedService: () => {
                clearSession();
                moveTo(rootNames.init);
            }
        });
    }

    // --------------
    // Plugins/Airjoy
    // --------------

    getAirjoyLive(group: string, project: string) {
        const url = `/plugins/airjoy/${group}/${project}/live`;
        return this.get<Array<AirjoySensorA>>(url);
    }

    getAirjoyDevices(group: string, project: string) {
        const url = `/plugins/airjoy/${group}/${project}/devices`;
        return this.get<Array<AirjoyDeviceA>>(url);
    }

    postAirjoyDevices(group: string, project: string, body: AirjoyCreateDeviceQ) {
        const url = `/plugins/airjoy/${group}/${project}/devices`;
        return this.post(url, body);
    }

    getAirjoyDevice(
        group: string,
        project: string,
        device: number | string,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
        return this.get<AirjoyDeviceA>(url);
    }

    patchAirjoyDevice(
        group: string,
        project: string,
        device: number | string,
        body: AirjoyUpdateDeviceQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
        return this.patch(url, body);
    }

    deleteAirjoyDevice(
        group: string,
        project: string,
        device: number | string,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}`;
        return this.delete(url);
    }

    postAirjoyControl(
        group: string,
        project: string,
        device: number | string,
        body: AirjoyControlQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/control`;
        return this.post(url, body);
    }

    getAirjoyChart(
        group: string,
        project: string,
        device: number | string,
        begin: string,
        end: string,
    ) {
        const queryBegin = encodeURIComponent(begin);
        const queryEnd = encodeURIComponent(end);
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/chart`;
        const query = `?begin=${queryBegin}&end=${queryEnd}`;
        return this.get<Array<AirjoyChartA>>(url + query);
    }

    getAirjoyChartCsv(
        group: string,
        project: string,
        device: number | string,
        begin: string,
        end: string,
    ) {
        const queryBegin = encodeURIComponent(begin);
        const queryEnd = encodeURIComponent(end);
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/chart/csv`;
        const query = `?begin=${queryBegin}&end=${queryEnd}`;
        return this.get<string>(url + query);
    }

    getAirjoyServices(
        group: string,
        project: string,
        device?: number | string,
    ) {
        if (typeof device === 'undefined') {
            const url = `/plugins/airjoy/${group}/${project}/services`;
            return this.get<Array<AirjoyServiceA>>(url);
        } else {
            const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services`;
            return this.get<Array<AirjoyServiceA>>(url);
        }
    }

    postAirjoyServices(
        group: string,
        project: string,
        device: number | string,
        body: AirjoyCreateServiceQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services`;
        return this.post(url, body);
    }

    patchAirjoyServices(
        group: string,
        project: string,
        device: number | string,
        service: number | string,
        body: AirjoyUpdateServiceQ,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services/${service}`;
        return this.patch(url, body);
    }

    deleteAirjoyServices(
        group: string,
        project: string,
        device: number | string,
        service: number | string,
    ) {
        const url = `/plugins/airjoy/${group}/${project}/devices/${device}/services/${service}`;
        return this.delete(url);
    }

    // -------------------
    // Plugins/VMS/Devices
    // -------------------

    getVmsDevices(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/devices`;
        return this.get<Array<VmsDeviceA>>(url);
    }

    postVmsDevices(group: string, project: string, body: VmsCreateDeviceQ) {
        const url = `/plugins/vms/${group}/${project}/devices`;
        return this.post(url, body);
    }

    getVmsDevice(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}`;
        return this.get<VmsDeviceA>(url);
    }

    patchVmsDevice(
        group: string,
        project: string,
        device: string,
        body: VmsUpdateDeviceQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}`;
        return this.patch(url, body);
    }

    deleteVmsDevice(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}`;
        return this.delete(url);
    }

    postVmsDeviceProcessStart(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/process/start`;
        return this.post(url);
    }

    postVmsDeviceProcessStop(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/process/stop`;
        return this.post(url);
    }

    getVmsDeviceRtcIces(group: string, project: string, device: string) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/rtc/ices`;
        return this.get<Array<IceServerA>>(url);
    }

    postVmsDeviceRtcJsep(
        group: string,
        project: string,
        device: string,
        body: RtcOfferQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/rtc/jsep`;
        return this.post<RtcAnswerA>(url, body);
    }

    deleteVmsDeviceRtcJsep(
        group: string,
        project: string,
        device: string,
        peer: string,
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/rtc/jsep/${peer}`;
        return this.delete(url);
    }

    // --------------------------
    // Plugins/VMS/Devices/Events
    // --------------------------

    getVmsDeviceEventsTimesPdateOffset(
        group: string,
        project: string,
        device: string,
        date: string,
    ) {
        const prefix = `/plugins/vms/${group}/${project}`;
        const suffix = `/devices/${device}/events/times/${date}/offset`;
        const url = prefix + suffix;
        return this.get<Array<number>>(url);
    }

    // ----------------------------------
    // Plugins/VMS/Devices/Events/Configs
    // ----------------------------------

    getVmsDeviceEventsConfigs(
        group: string,
        project: string,
        device: string,
    ) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/events/configs`;
        return this.get<Array<VmsEventConfigA>>(url);
    }

    postVmsDeviceEventsConfigs(
        group: string,
        project: string,
        device: string,
        body: VmsCreateEventConfigQ
    ) {
        const url = `/plugins/vms/${group}/${project}/devices/${device}/events/configs`;
        return this.post(url, body);
    }

    getVmsDeviceEventsConfigsPconfig(
        group: string,
        project: string,
        device: string,
        config: string
    ) {
        const prefix = `/plugins/vms/${group}/${project}`;
        const suffix = `/devices/${device}/events/configs/${config}`;
        const url = prefix + suffix;
        return this.get<VmsEventConfigA>(url);
    }

    patchVmsDeviceEventsConfigsPconfig(
        group: string,
        project: string,
        device: string,
        config: string,
        body: VmsUpdateEventConfigQ,
    ) {
        const prefix = `/plugins/vms/${group}/${project}`;
        const suffix = `/devices/${device}/events/configs/${config}`;
        const url = prefix + suffix;
        return this.patch(url, body);
    }

    deleteVmsDeviceEventsConfigsPconfig(
        group: string,
        project: string,
        device: string,
        config: string,
    ) {
        const prefix = `/plugins/vms/${group}/${project}`;
        const suffix = `/devices/${device}/events/configs/${config}`;
        const url = prefix + suffix;
        return this.delete(url);
    }

    // -----------------------------
    // Plugins/VMS/Devices/Debugging
    // -----------------------------

    postVmsDeviceProcessDebugStart(group: string, project: string, device: string) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/start`;
        return this.post(url);
    }

    postVmsDeviceProcessDebugStop(group: string, project: string, device: string) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/stop`;
        return this.post(url);
    }

    postVmsDeviceProcessDebugEventColor(
        group: string, project: string, device: string, body: VmsEventConfigColorQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/color`;
        return this.post(url, body);
    }

    postVmsDeviceProcessDebugEventDetection(
        group: string, project: string, device: string, body: VmsEventConfigDetectionQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/detection`;
        return this.post(url, body);
    }

    postVmsDeviceProcessDebugEventMatching(
        group: string, project: string, device: string, body: VmsEventConfigMatchingQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/matching`;
        return this.post(url, body);
    }

    getVmsDeviceProcessDebugEventMatchingTrainSnapshots(
        group: string, project: string, device: string
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/matching/train/snapshots`;
        return this.get<Array<string>>(url);
    }

    postVmsDeviceProcessDebugEventMatchingTrainSnapshots(
        group: string, project: string, device: string, body: VmsUploadImageQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/matching/train/snapshots`;
        return this.post<VmsUploadImageA>(url, body);
    }

    getVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
        group: string, project: string, device: string, snapshot: string
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const suffix_url = `/process/debug/event/matching/train/snapshots/${snapshot}`;
        return this.get<VmsImageA>(device_prefix + suffix_url);
    }

    deleteVmsDeviceProcessDebugEventMatchingTrainSnapshotsPsnapshot(
        group: string, project: string, device: string, snapshot: string
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const suffix_url = `/process/debug/event/matching/train/snapshots/${snapshot}`;
        const url = device_prefix + suffix_url;
        return this.delete(url);
    }

    postVmsDeviceProcessDebugEventOcr(
        group: string, project: string, device: string, body: VmsEventConfigOcrQ
    ) {
        const device_prefix = `/plugins/vms/${group}/${project}/devices/${device}`;
        const url = `${device_prefix}/process/debug/event/ocr`;
        return this.post(url, body);
    }

    // -------------------
    // Plugins/VMS/Layouts
    // -------------------

    getVmsLayouts(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/layouts`;
        return this.get<Array<VmsLayoutA>>(url);
    }

    postVmsLayouts(group: string, project: string, body: VmsCreateLayoutQ) {
        const url = `/plugins/vms/${group}/${project}/layouts`;
        return this.post(url, body);
    }

    getVmsLayout(group: string, project: string, layout: string) {
        const url = `/plugins/vms/${group}/${project}/layouts/${layout}`;
        return this.get<VmsLayoutA>(url);
    }

    patchVmsLayout(
        group: string,
        project: string,
        layout: string,
        body: VmsUpdateLayoutQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/layouts/${layout}`;
        return this.patch(url, body);
    }

    deleteVmsLayout(group: string, project: string, layout: string) {
        const url = `/plugins/vms/${group}/${project}/layouts/${layout}`;
        return this.delete(url);
    }

    // -----------------
    // Plugins/VMS/Event
    // -----------------

    getVmsEventsSnapshotsPevent(group: string, project: string, event: string) {
        const url = `/plugins/vms/${group}/${project}/events/snapshots/${event}`;
        return this.get<VmsEventImageA>(url);
    }

    getVmsEventsThumbnailsPevent(group: string, project: string, event: string) {
        const url = `/plugins/vms/${group}/${project}/events/thumbnails/${event}`;
        return this.get<VmsEventImageA>(url);
    }

    postVmsEventsFilter(group: string, project: string, body: VmsFilterEventQ) {
        const url = `/plugins/vms/${group}/${project}/events/filter`;
        return this.post<Array<VmsEventA>>(url, body);
    }

    postVmsEventsNews(group: string, project: string, body: VmsNewsEventQ) {
        const url = `/plugins/vms/${group}/${project}/events/news`;
        return this.post<Array<VmsEventA>>(url, body);
    }

    postVmsEventsLatest(group: string, project: string, body: VmsLatestEventQ) {
        const url = `/plugins/vms/${group}/${project}/events/latest`;
        return this.post<Array<VmsEventA>>(url, body);
    }

    getVmsEventsDates(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/events/dates`;
        return this.get<Array<string>>(url);
    }

    getVmsEventsDevices(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/events/devices`;
        return this.get<Array<number>>(url);
    }

    getVmsEventsTags(group: string, project: string) {
        const url = `/plugins/vms/${group}/${project}/events/tags`;
        return this.get<Array<VmsEventTagA>>(url);
    }

    postVmsEventsTags(group: string, project: string, body: VmsCreateEventTagQ) {
        const url = `/plugins/vms/${group}/${project}/events/tags`;
        return this.post(url, body);
    }

    getVmsEventsTagsPtag(group: string, project: string, tag: string) {
        const url = `/plugins/vms/${group}/${project}/events/tags/${tag}`;
        return this.get<VmsEventTagA>(url);
    }

    patchVmsEventsTagsPtag(
        group: string,
        project: string,
        tag: string,
        body: VmsUpdateEventTagQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/events/tags/${tag}`;
        return this.patch(url, body);
    }

    deleteVmsEventsTagsPtag(group: string, project: string, tag: string) {
        const url = `/plugins/vms/${group}/${project}/events/tags/${tag}`;
        return this.delete(url);
    }

    // ---------------------
    // Plugins/VMS/Discovery
    // ---------------------

    postVmsDiscovery(
        group: string,
        project: string,
        body: VmsDiscoveryQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/discovery`;
        return this.post(url, body);
    }

    postVmsDiscoveryHeartbeat(
        group: string,
        project: string,
        body: VmsDiscoveredHeartbeatQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/discovery/heartbeat`;
        return this.post<VmsDiscoveredHeartbeatA>(url, body);
    }

    // -----------------------
    // Plugins/VMS/ONVIF/Media
    // -----------------------

    postVmsOnvifMedia(
        group: string,
        project: string,
        body: VmsOnvifMediaStreamUriQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/onvif/media`;
        return this.post(url, body);
    }

    postVmsOnvifMediaHeartbeat(
        group: string,
        project: string,
        body: VmsOnvifMediaStreamUriHeartbeatQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/onvif/media/heartbeat`;
        return this.post<VmsOnvifMediaStreamUriHeartbeatA>(url, body);
    }

    postVmsOnvifMediaSnapshot(
        group: string,
        project: string,
        body: VmsOnvifMediaSnapshotQ,
    ) {
        const url = `/plugins/vms/${group}/${project}/onvif/media/snapshot`;
        return this.post<VmsOnvifMediaSnapshotA>(url, body);
    }

    // ------------------
    // Plugins/VMS/Record
    // ------------------

    getVmsRecordsPdeviceDates(
        group: string,
        project: string,
        device: string,
    ) {
        const url = `/plugins/vms/${group}/${project}/records/${device}/dates`;
        return this.get<Array<string>>(url);
    }

    urlVmsRecordsPdevicePlaylistMaster(
        group: string,
        project: string,
        device: string,
        start: string,
        last: string,
    ) {
        const url = `/plugins/vms/${group}/${project}/records/${device}/playlist/master`;
        const params = `?start=${start}&last=${last}`;
        return this.base + url + params;
    }

    getVmsRecordsPdeviceRangesPdate(
        group: string,
        project: string,
        device: string,
        date: string,
    ) {
        const url = `/plugins/vms/${group}/${project}/records/${device}/ranges/${date}`;
        return this.get<Array<VmsRecordRangeA>>(url);
    }
};
