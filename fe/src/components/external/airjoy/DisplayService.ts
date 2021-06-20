export class SIZE {
  public static get MIN_XS(): number { return 0; }
  public static get MAX_XS(): number { return 600; }
  public static get MAX_SM(): number { return 960; }
  public static get MAX_MD(): number { return 1264; }
  public static get MAX_LG(): number { return 1904; }
  public static get MAX_XL(): number { return 9999; }
}

export class Breakpoints {
  xs = new Breakpoint("xs", new Range(SIZE.MIN_XS, SIZE.MAX_XS));
  sm = new Breakpoint("sm", new Range(SIZE.MAX_XS, SIZE.MAX_SM));
  md = new Breakpoint("md", new Range(SIZE.MAX_SM, SIZE.MAX_MD));
  lg = new Breakpoint("lg", new Range(SIZE.MAX_MD, SIZE.MAX_LG));
  xl = new Breakpoint("xl", new Range(SIZE.MAX_LG, SIZE.MAX_XL));
}

export class Breakpoint {
  code: string;
  range: Range;
  constructor(code: string, range: Range) {
    this.code = code;
    this.range = range;
  }
}

export class Range {
  min: number;
  max: number;
  constructor(min = -1, max = -1) {
    this.min = min;
    this.max = max;
  }
}

export function height(name: string) {
  switch (name) {
    case 'xs': return 220
    case 'sm': return 400
    case 'md': return 500
    case 'lg': return 600
    case 'xl': return 800
  }
}

export function isMobile() {
  if (window.innerWidth < 600) {
    return true;
  } else {
    return false;
  }
}
