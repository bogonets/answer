import AxiosLib, { AxiosInstance, AxiosPromise } from 'axios'

const DEFAULT_PROTOCOL = document.location.protocol;
const DEFAULT_HOST = document.location.host;
const DEFAULT_ORIGIN = document.location.origin;

const DEFAULT_TIMEOUT = 30 * 1000;

export default class ApiV2 {

    private _api: AxiosInstance;

    constructor(
        origin: string = DEFAULT_ORIGIN,
        timeout: number = DEFAULT_TIMEOUT,
    ) {
        this._api = AxiosLib.create({
            baseURL: origin + '/api/v2',
            timeout: timeout,
        });
    }

    async getVersion() {
        return await this._api.get("/version")
            .then(response => {
                return response.data;
            })
            .catch(error => {
                console.debug(error);
                // EMPTY.
            });
    }
}
