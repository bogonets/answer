/**
 * Base class of 2-Point.
 *
 * @author zer0 <osom8979@gmail.com>
 */
export class Point {
  x = 0.0;
  y = 0.0;

  constructor(x = 0.0, y = 0.0) {
    this.x = x;
    this.y = y;
  }
}

/**
 * Base class of 2-Range.
 *
 * @author zer0 <osom8979@gmail.com>
 */
export class Range {
  min: number;
  max: number;

  constructor(min = 0.0, max = 0.0) {
    this.min = min;
    this.max = max;
  }
}

/**
 * Base class of 3-Color.
 *
 * @author zer0 <osom8979@gmail.com>
 */
export class Color {
  r: number;
  g: number;
  b: number;

  constructor(r = 0, g = 0, b = 1) {
    this.r = r;
    this.g = g;
    this.b = b;
  }

  setByInteger(r = 0, g = 0, b = 1) {
    this.r = r / 255.0;
    this.g = g / 255.0;
    this.b = b / 255.0;
  }

  getIntegerList(r = 0, g = 0, b = 1) {
    return [this.r * 255.0, this.g * 255.0, this.b * 255.0];
  }

  toObject() {
    return { r: this.r, g: this.g, b: this.b };
  }

  toIntegerObject() {
    return { r: this.r * 255.0, g: this.g * 255.0, b: this.b * 255.0 };
  }
}

/**
 * Base class of Properties.
 *
 * @author zer0 <osom8979@gmail.com>
 */
export class Property {
  greaterThanEnable = false;
  greaterThanValue = 0.0;

  lessThanEnable = false;
  lessThanValue = 0.0;

  withinRangeEnable = false;
  withinRangeValue = new Range();

  outOfRangeEnable = false;
  outOfRangeValue = new Range();

  thresholdEnable = false;
  thresholdValue = 0.0;

  rgbColorEnable = false;
  rgbColorValue = new Color();

  lineStyleColorEnable = false;
  lineStyleColorValue = new Color();

  static createFromObject(obj: object): Property {
    let result = new Property();

    if ("greaterThanEnable" in obj) {
      result.greaterThanEnable = obj["greaterThanEnable"];
    }
    if ("greaterThanValue" in obj) {
      result.greaterThanValue = obj["greaterThanValue"];
    }

    if ("lessThanEnable" in obj) {
      result.lessThanEnable = obj["lessThanEnable"];
    }
    if ("lessThanValue" in obj) {
      result.lessThanValue = obj["lessThanValue"];
    }

    if ("withinRangeEnable" in obj) {
      result.withinRangeEnable = obj["withinRangeEnable"];
    }
    if ("withinRangeValue" in obj) {
      result.withinRangeValue = new Range(
        obj["withinRangeValue"]["min"],
        obj["withinRangeValue"]["max"]
      );
    }

    if ("outOfRangeEnable" in obj) {
      result.outOfRangeEnable = obj["outOfRangeEnable"];
    }
    if ("outOfRangeValue" in obj) {
      result.outOfRangeValue = new Range(
        obj["outOfRangeValue"]["min"],
        obj["outOfRangeValue"]["max"]
      );
    }

    if ("thresholdEnable" in obj) {
      result.thresholdEnable = obj["thresholdEnable"];
    }
    if ("thresholdValue" in obj) {
      result.thresholdValue = obj["thresholdValue"];
    }

    if ("rgbColorEnable" in obj) {
      result.rgbColorEnable = obj["rgbColorEnable"];
    }
    if ("rgbColorValue" in obj) {
      result.rgbColorValue = new Color(
        obj["rgbColorValue"]["r"],
        obj["rgbColorValue"]["g"],
        obj["rgbColorValue"]["b"]
      );
    }

    if ("lineStyleColorEnable" in obj) {
      result.lineStyleColorEnable = obj["lineStyleColorEnable"];
    }
    if ("lineStyleColorValue" in obj) {
      result.lineStyleColorValue = new Color(
        obj["lineStyleColorValue"]["r"],
        obj["lineStyleColorValue"]["g"],
        obj["lineStyleColorValue"]["b"]
      );
    }

    return result;
  }
}

/**
 * RoI's properties.
 *
 * @author zer0 <osom8979@gmail.com>
 */
export class RoiInfo {
  points = new Array<Point>();
  property = new Property();
  snapshotInBase64Jpeg = "";

  getPoints(): Array<number> {
    let result = new Array<number>();
    for (const p in this.points) {
      result.push(this.points[p].x);
      result.push(this.points[p].y);
    }
    return result;
  }

  static createFromObject(obj: object): RoiInfo {
    let result = new RoiInfo();
    if ("points" in obj) {
      for (const p in obj["points"]) {
        result.points.push(
          new Point(obj["points"][p]["x"], obj["points"][p]["y"])
        );
      }
    }
    if ("property" in obj) {
      result.property = Property.createFromObject(obj["property"]);
    }
    if ("snapshotInBase64Jpeg" in obj) {
      result.snapshotInBase64Jpeg = obj["snapshotInBase64Jpeg"];
    }
    return result;
  }
}

/**
 * Map of the RoI's properties.
 *
 * @author zer0 <osom8979@gmail.com>
 */
export class RoiInfoDictionary {
  elems: Map<string, RoiInfo>;

  constructor(json?: string) {
    this.elems = new Map<string, RoiInfo>();
    if (json) {
      this.parseJSON(json);
    }
  }

  toJSON(): string {
    let jsonObject = {};
    this.elems.forEach((value, key) => {
      jsonObject[key] = value;
    });
    return JSON.stringify(jsonObject);
  }

  parseJSON(json: string): void {
    let jsonObject = JSON.parse(json);
    this.elems.clear();
    for (const key in jsonObject) {
      this.elems.set(key, RoiInfo.createFromObject(jsonObject[key]));
    }
  }

  private _migrateKey(key: string | number): string {
    if (typeof key === "string") {
      return key;
    } else if (typeof key === "number") {
      return key.toString();
    } else {
      throw new Error(`Unsupported key type: ${typeof key}`);
    }
  }

  set(key: string | number, val: RoiInfo): void {
    this.elems.set(this._migrateKey(key), val);
  }

  get(key: string | number): RoiInfo {
    let val: RoiInfo | undefined = this.elems.get(this._migrateKey(key));
    if (val === undefined) {
      throw new Error(`Not found element of key: ${key}`);
    }
    return val;
  }

  has(key: string | number): boolean {
    return this.elems.has(this._migrateKey(key));
  }

  delete(key: string | number): boolean {
    return this.elems.delete(this._migrateKey(key));
  }

  clear(): void {
    this.elems.clear();
  }

  keys(): IterableIterator<string> {
    return this.elems.keys();
  }

  entries(): IterableIterator<[string, RoiInfo]> {
    return this.elems.entries();
  }

  values(): IterableIterator<RoiInfo> {
    return this.elems.values();
  }

  forEach(
    callbackfn: (value: RoiInfo, key: string, map: Map<string, RoiInfo>) => void
  ): void {
    this.elems.forEach(callbackfn);
  }

  get size(): number {
    return this.elems.size;
  }

  get length(): number {
    return this.elems.size;
  }

  toString(): string {
    return this.toJSON();
  }
}

/**
 * Convert RoiInfoDictionary to JSON string.
 *
 * @author zer0 <osom8979@gmail.com>
 */
export function cvtRoisToJson(rois: RoiInfoDictionary): string {
  return rois.toJSON();
}

/**
 * Convert JSON string to RoiInfoDictionary.
 *
 * @author zer0 <osom8979@gmail.com>
 */
export function cvtJsonToRois(json: string): RoiInfoDictionary {
  return new RoiInfoDictionary(json);
}
