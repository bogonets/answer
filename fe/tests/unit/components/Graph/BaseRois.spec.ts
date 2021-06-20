import * as BaseRois from "@/components/Graph/BaseRois.ts";

describe("BaseRois.ts", () => {
  let info0 = new BaseRois.RoiInfo();
  info0.points.push(new BaseRois.Point(1.0, 2.0));
  info0.points.push(new BaseRois.Point(3.0, 4.0));
  info0.property.greaterThanEnable = true;
  info0.property.greaterThanValue = 1.0;

  let info1 = new BaseRois.RoiInfo();
  info1.points.push(new BaseRois.Point(5.0, 6.0));
  info1.points.push(new BaseRois.Point(7.0, 8.0));
  info1.property.rgbColorEnable = true;
  info1.property.rgbColorValue = new BaseRois.Color(1.0, 0.0, 0.0);

  let props = new BaseRois.RoiInfoDictionary();
  props.set("0", info0);
  props.set("1", info1);

  test("Test convert functions", () => {
    const json = BaseRois.cvtRoisToJson(props);
    console.debug(`Converted json result: ${json}`);
    expect(json.length).toBeGreaterThan(0);

    const converted_props = BaseRois.cvtJsonToRois(json);
    expect(converted_props).toStrictEqual(props);
  });

  test("Test has method.", () => {
    expect(props.has("0")).toBe(true);
    expect(props.has(0)).toBe(true);

    expect(props.has("1")).toBe(true);
    expect(props.has(1)).toBe(true);

    expect(props.has("2")).toBe(false);
    expect(props.has(2)).toBe(false);

    // expect(props.has(Object())).toThrow('Unsupported key type: object'); // Why ??
  });
});
