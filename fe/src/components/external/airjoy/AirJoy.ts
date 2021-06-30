// export class SIZE {
//   public static get MIN_XS(): number { return 0; }
//   public static get MAX_XS(): number { return 600; }
//   public static get MAX_SM(): number { return 960; }
//   public static get MAX_MD(): number { return 1264; }
//   public static get MAX_LG(): number { return 1904; }
//   public static get MAX_XL(): number { return 9999; }
// }

const enum SIZE {
  xs = 600,
  sm = 960,
  md = 1264,
  lg = 1904,
  xl = 9999
}

export class ManageData {
  metricDatas = new Array<ManageMetricData>()
  nonMetricDatas = new Array<ManageNonMetricData>()
}

export class ManageMetricData {
  serial: string
  on_off: boolean
  sleep: boolean
  wind_control: number
  auto: boolean
  temperature: number
  moisture: number
  pm10: number
  pm25: number
  co2: number
  voc: string
  etc: string

  constructor(
    serial: string,
    on_off = false,
    sleep = false,
    wind_control = 1,
    auto = true,
    temperature = 0,
    moisture = 0.0,
    pm10 = 0,
    pm25 = 0,
    co2 = 0,
    voc = "",
    etc = "",
  ) {
    this.serial = serial;
    this.on_off = on_off
    this.sleep = sleep
    this.wind_control = wind_control
    this.auto = auto
    this.temperature = temperature
    this.moisture = moisture
    this.pm10 = pm10
    this.pm25 = pm25
    this.co2 = co2
    this.voc = voc
    this.etc = etc
  }
}

export class ManageNonMetricData {
  serial: string
  wifi: string
  agency: string
  install_date: string
  install_location: string
  as: string
  firmware_version: string
  kiosk: string
  install_type: string
  filter_life: string
  constructor(
    serial: string,
    wifi = "",
    agency = "",
    install_date = "",
    install_location = "",
    as = "",
    firmware_version = "",
    kiosk = "",
    install_type = "",
    filter_life = "",
  ) {
    this.serial = serial;
    this.wifi = wifi;
    this.agency = agency;
    this.install_date = install_date;
    this.install_location = install_location;
    this.as = as;
    this.firmware_version = firmware_version;
    this.kiosk = kiosk;
    this.install_type = install_type;
    this.filter_life = filter_life;
  }
}

export class ManageHeader {
  firstHeader = new Array<Header>();
  secondHeader = new Array<Header>();
  width: number
  constructor(width = 0) {
    this.width = width;
    this.pushHeader(this.firstHeader, new Header("Serial", "serial", "start", true));
    this.pushHeader(this.firstHeader, new Header("Wifi", "wifi"));
    this.pushHeader(this.firstHeader, new Header("Agency", "agency"), SIZE.xs);
    this.pushHeader(this.firstHeader, new Header("Date", "install_date"), SIZE.xs);
    this.pushHeader(this.firstHeader, new Header("Location", "install_location"), SIZE.sm);
    this.pushHeader(this.firstHeader, new Header("A/S", "as"), SIZE.md);
    this.pushHeader(this.firstHeader, new Header("Firmware", "firmware_version"), SIZE.md);
    this.pushHeader(this.firstHeader, new Header("Kiosk", "kiosk"), SIZE.md);
    this.pushHeader(this.firstHeader, new Header("Type", "install_type"), SIZE.md);
    this.pushHeader(this.firstHeader, new Header("Filter", "filter_life"), SIZE.md);

    this.pushHeader(this.secondHeader, new Header("Serial", "serial"));
    this.pushHeader(this.secondHeader, new Header("ON/OFF", "on_off"));
    this.pushHeader(this.secondHeader, new Header("Sleep", "sleep"), SIZE.xs);
    this.pushHeader(this.secondHeader, new Header("Wind", "wind_control"), SIZE.xs);
    this.pushHeader(this.secondHeader, new Header("Auto", "auto"), SIZE.sm);
    this.pushHeader(this.secondHeader, new Header("Temp", "temperature"), SIZE.sm);
    this.pushHeader(this.secondHeader, new Header("Humidity", "moisture"), SIZE.md);  // TODO moisture - > humidity
    this.pushHeader(this.secondHeader, new Header("PM10", "pm10"), SIZE.md);
    this.pushHeader(this.secondHeader, new Header("PM2.5", "pm25"), SIZE.md);
    this.pushHeader(this.secondHeader, new Header("CO2", "co2"), SIZE.md);
    this.pushHeader(this.secondHeader, new Header("VOC", "voc"), SIZE.md);
    this.pushHeader(this.secondHeader, new Header("etc", "etc"), SIZE.md);
  }

  pushHeader(headers: Array<Header>, header: Header, width = 0) {
    if (this.width > width)
      headers.push(header);
  }
}

export class Header {
  text: string
  value: string
  align: string
  sortable: boolean

  constructor(text = "", value: string, align = "start", sortable = false) {
    this.text = text;
    this.value = value;
    this.align = align;
    this.sortable = sortable;
  }
}

export class EditData {
  serial: string
  editData: [string, string]

  constructor(serial: string, editData: [string, string]) {
    this.serial = serial;
    this.editData = editData;
  }
}