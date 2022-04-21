import FontFaceObserver from 'fontfaceobserver';
import {IllegalArgumentException} from '@/exceptions';
import {
  Application,
  DisplayObject,
  Graphics,
  IApplicationOptions,
  IPoint,
  Text,
  TextStyle,
} from 'pixi.js';
import TextInput from 'pixi-text-input/PIXI.TextInput.js';
import {DraggingContainer} from '@/pixi/draggingContainer';

export enum LambdaType {
  Signal,
  Function,
  Export,
  Data,
}

export const LAMBDA_TYPE_LOWER_SIGNAL = 'signal';
export const LAMBDA_TYPE_LOWER_FUNCTION = 'function';
export const LAMBDA_TYPE_LOWER_EXPORT = 'export';
export const LAMBDA_TYPE_LOWER_DATA = 'data';

export interface Property {
  type: string;
  name: string;
  value: any;
  mime: string;
}

export interface Lambda {
  type: LambdaType | string | number;
  template: string;

  x1: number;
  y1: number;
  x2: number;
  y2: number;

  props: Array<Property>;
}

export interface Template {
  type: LambdaType | string | number;
}

export interface Slot {
  lambda: string;
  prop: string;
}

export interface Arc {
  from: Slot;
  to: Slot;
}

export function normalizeLambdaType(type: LambdaType | string | number): LambdaType {
  if (typeof type === 'string') {
    const lowerType = type.toLowerCase();
    if (lowerType === LAMBDA_TYPE_LOWER_SIGNAL) {
      return LambdaType.Signal;
    } else if (lowerType === LAMBDA_TYPE_LOWER_FUNCTION) {
      return LambdaType.Function;
    } else if (lowerType === LAMBDA_TYPE_LOWER_EXPORT) {
      return LambdaType.Export;
    } else if (lowerType === LAMBDA_TYPE_LOWER_DATA) {
      return LambdaType.Data;
    } else {
      throw new IllegalArgumentException(`Unknown lambda type: '${type}'`);
    }
  }

  switch (type) {
    case LambdaType.Signal:
      return LambdaType.Signal;
    case LambdaType.Function:
      return LambdaType.Function;
    case LambdaType.Export:
      return LambdaType.Export;
    case LambdaType.Data:
      return LambdaType.Data;
    default:
      throw new IllegalArgumentException(`Unknown lambda type: ${type}`);
  }
}

export interface Graph {
  lambdas: Record<string, Lambda>;
  templates: Record<string, Template>;
  arcs: Array<Arc>;
}

export interface GraphOptions extends IApplicationOptions {
  iconFontFamily?: string;
  iconFontSize?: number;
  iconFillColor?: number;

  iconCodeSignal?: number;
  iconCodeFunction?: number;
  iconCodeExport?: number;
  iconCodeData?: number;
  iconCodeUnknown?: number;

  iconCodeFlowUnlink?: number;
  iconCodeFlowLink?: number;
  iconCodeDataUnlink?: number;
  iconCodeDataLink?: number;

  textFontFamily?: string;
  textFontSize?: number;
  textFillColor?: number;

  waitFontLoad?: boolean;
  fontLoadTimeout?: number;

  lineWidth?: number;
  lineColor?: number;
  lineAlpha?: number;
  fillColor?: number;
  fillAlpha?: number;
  radius?: number;
  iconPadding?: number;
  scale?: number;

  draggingAlpha?: number;
}

async function waitFontLoad(family: string, timeout: number) {
  await new FontFaceObserver(family)
    .load(null, timeout)
    .then(() => {
      console.debug(`waitFontLoad.then('${family}')`);
    })
    .catch(() => {
      console.debug(`waitFontLoad.catch('${family}')`);
    });
}

export class LambdaContainer extends DraggingContainer {
  slots: Record<string, IPoint>;

  constructor(dragAlpha?: number) {
    super(dragAlpha);
    this.slots = {};
  }
}

const FONT_FAMILY_MATERIAL_DESIGN_ICONS = 'Material Design Icons';
const MDI_PULSE = 0xf0430;
const MDI_FUNCTION = 0xf0295;
const MDI_EXPORT = 0xf0207;
const MDI_FILE_OUTLINE = 0xf0224;
const MDI_HELP = 0xf02d6;

const MDI_ARROW_RIGHT_BOLD = 0xf0734;
const MDI_ARROW_RIGHT_BOLD_OUTLINE = 0xf09c2;
const MDI_ARROW_RIGHT_DROP_CIRCLE_OUTLINE = 0xf005a;
const MDI_ARROW_RIGHT_DROP_CIRCLE = 0xf0059;
const MDI_HEXAGON = 0xf02d8;
const MDI_HEXAGON_OUTLINE = 0xf02d9;
const MDI_HEXAGON_SLICE_6 = 0xf0ac8;

const FONT_FAMILY_SERIF = 'serif';
const FONT_FAMILY_SANS_SERIF = 'sans-serif';
const FONT_FAMILY_MONOSPACE = 'monospace';

const SECOND_BY_MILLISECONDS = 1000;

const DEFAULT_FONT_FAMILY = 'NanumSquareRoundBold';
const DEFAULT_ICON_SIGNAL = 'S'.codePointAt(0) as number;
const DEFAULT_ICON_FUNCTION = 'F'.codePointAt(0) as number;
const DEFAULT_ICON_EXPORT = 'E'.codePointAt(0) as number;
const DEFAULT_ICON_DATA = 'D'.codePointAt(0) as number;
const DEFAULT_ICON_UNKNOWN = '?'.codePointAt(0) as number;
const DEFAULT_LINE_WIDTH = 1;
const DEFAULT_LINE_COLOR = 0x10120f;
const DEFAULT_LINE_ALPHA = 1;
const DEFAULT_FILL_COLOR = 0x171916;
const DEFAULT_FILL_ALPHA = 0.5;
const DEFAULT_RADIUS = 4;
const DEFAULT_ICON_PADDING = 2;
const DEFAULT_SCALE = 1;

const DEFAULT_DRAGGING_ALPHA = 0.5;

export function createDefaultGraphOptions(options?: GraphOptions) {
  return {
    iconFontFamily: FONT_FAMILY_MATERIAL_DESIGN_ICONS,
    iconFontSize: 18,
    iconFillColor: 0xffffff,
    iconCodeSignal: MDI_PULSE,
    iconCodeFunction: MDI_FUNCTION,
    iconCodeExport: MDI_EXPORT,
    iconCodeData: MDI_FILE_OUTLINE,
    iconCodeUnknown: MDI_HELP,
    iconCodeFlowUnlink: MDI_ARROW_RIGHT_BOLD_OUTLINE,
    iconCodeFlowLink: MDI_ARROW_RIGHT_BOLD,
    iconCodeDataUnlink: MDI_HEXAGON_OUTLINE,
    iconCodeDataLink: MDI_HEXAGON,
    textFontFamily: DEFAULT_FONT_FAMILY,
    textFontSize: 12,
    textFillColor: 0xffffff,
    waitFontLoad: true,
    fontLoadTimeout: 4 * SECOND_BY_MILLISECONDS,
    lineWidth: DEFAULT_LINE_WIDTH,
    lineColor: DEFAULT_LINE_COLOR,
    lineAlpha: DEFAULT_LINE_ALPHA,
    fillColor: DEFAULT_FILL_COLOR,
    fillAlpha: DEFAULT_FILL_ALPHA,
    radius: DEFAULT_RADIUS,
    iconPadding: DEFAULT_ICON_PADDING,
    scale: DEFAULT_SCALE,
    draggingAlpha: DEFAULT_DRAGGING_ALPHA,
    antialias: true,
    backgroundColor: 0xfafafa,
    ...options,
  } as GraphOptions;
}

export class Context {
  graph: Graph;
  options: GraphOptions;
  app?: Application;

  constructor(graph?: Graph, options?: GraphOptions) {
    this.graph = graph || ({} as Graph);
    this.options = createDefaultGraphOptions(options);
    this.app = undefined;

    (async () => {
      await this.createPixiContext();
    })();
  }

  async createPixiContext() {
    if (this.options.waitFontLoad) {
      const fontLoadTimeout = this.options.fontLoadTimeout || 0;
      const iconFontFamily = this.options.iconFontFamily || '';
      const textFontFamily = this.options.textFontFamily || '';

      await new FontFaceObserver(iconFontFamily).load(null, fontLoadTimeout);
      await new FontFaceObserver(textFontFamily).load(null, fontLoadTimeout);
    }

    const lambdas = {} as Record<string, LambdaContainer>;
    this.app = new Application(this.options);
    for (const key in this.graph.lambdas) {
      lambdas[key] = this.createLambdaContainer(this.graph.lambdas[key]);
    }

    for (const key in this.graph.arcs) {
      const arc = this.graph.arcs[key];
      const bezier = new Graphics();

      this.app.ticker.add(delta => {
        const fromLambda = lambdas[arc.from.lambda];
        const toLambda = lambdas[arc.to.lambda];

        const from = fromLambda.slots[arc.from.prop];
        const to = toLambda.slots[arc.to.prop];

        const fromX = fromLambda.x + from.x;
        const fromY = fromLambda.y + from.y;
        const from2X = fromX + 36;
        const from2Y = fromY;
        const toX = toLambda.x + to.x;
        const toY = toLambda.y + to.y;
        const to2X = toX - 36;
        const to2Y = toY;

        // bezier.moveTo(fromX, fromY);
        // bezier.lineTo(from2X, from2Y);
        // bezier.lineTo(to2X, to2Y);
        // bezier.lineTo(toX, toY);

        bezier.clear();
        bezier.lineStyle(3, 0xcfcfcf, 1);
        bezier.moveTo(fromX, fromY);
        bezier.bezierCurveTo(from2X, from2Y, to2X, to2Y, toX, toY);
      });

      // bezier.x = fromLambda.x;
      // bezier.y = fromLambda.y;
      this.app.stage.addChild(bezier);
    }

    for (const key in lambdas) {
      this.app.stage.addChild(lambdas[key]);
    }
  }

  close() {
    if (this.app) {
      this.app.destroy();
      this.app = undefined;
    }
  }

  getIconCode(type: LambdaType | string | number) {
    try {
      switch (normalizeLambdaType(type)) {
        case LambdaType.Signal:
          return this.options.iconCodeSignal || DEFAULT_ICON_SIGNAL;
        case LambdaType.Function:
          return this.options.iconCodeFunction || DEFAULT_ICON_FUNCTION;
        case LambdaType.Export:
          return this.options.iconCodeExport || DEFAULT_ICON_EXPORT;
        case LambdaType.Data:
          return this.options.iconCodeData || DEFAULT_ICON_DATA;
        default:
          return this.options.iconCodeUnknown || DEFAULT_ICON_UNKNOWN;
      }
    } catch (_) {
      return this.options.iconCodeUnknown || DEFAULT_ICON_UNKNOWN;
    }
  }

  createGrid(width: number, height: number, widthStep: number, heightStep: number) {}

  createLambdaContainer(lambda: Lambda) {
    const container = new LambdaContainer(this.options.draggingAlpha);
    const children = [] as Array<DisplayObject>;

    const lineWidth = this.options.lineWidth ?? DEFAULT_LINE_WIDTH;
    const lineColor = this.options.lineColor ?? DEFAULT_LINE_COLOR;
    const lineAlpha = this.options.lineAlpha ?? DEFAULT_LINE_ALPHA;
    const fillColor = this.options.fillColor ?? DEFAULT_FILL_COLOR;
    const fillAlpha = this.options.fillAlpha ?? DEFAULT_FILL_ALPHA;
    const radius = this.options.radius ?? DEFAULT_RADIUS;
    const iconPadding = this.options.iconPadding ?? DEFAULT_ICON_PADDING;
    const padding = iconPadding;
    const scale = this.options.scale ?? DEFAULT_SCALE;
    const width = lambda.x2 - lambda.x1;
    const height = lambda.y2 - lambda.y1;

    const flowUnlink = this.options.iconCodeFlowUnlink ?? MDI_ARROW_RIGHT_BOLD_OUTLINE;
    const flowLink = this.options.iconCodeFlowLink ?? MDI_ARROW_RIGHT_BOLD;
    const dataUnlink = this.options.iconCodeDataUnlink ?? MDI_HEXAGON_OUTLINE;
    const dataLink = this.options.iconCodeDataLink ?? MDI_HEXAGON;

    const outline = new Graphics();
    children.push(outline);

    // outline.lineStyle(lineWidth, lineColor, lineAlpha);
    outline.beginFill(fillColor, fillAlpha);
    outline.drawRect(0, 0, width, height);
    outline.endFill();

    const iconStyle = new TextStyle({
      fontFamily: this.options.iconFontFamily,
      fontSize: this.options.iconFontSize,
      fill: this.options.iconFillColor,
      // stroke: '#4a1850',
      // strokeThickness: 5,
      // dropShadow: true,
      // dropShadowColor: '#000000',
      // dropShadowBlur: 4,
      // dropShadowAngle: Math.PI / 6,
      // dropShadowDistance: 6,
      // wordWrap: true,
      // wordWrapWidth: 440,
      // lineJoin: 'round',
    });
    const code = String.fromCodePoint(this.getIconCode(lambda.type));
    const icon = new Text(code, iconStyle);
    icon.x = iconPadding;
    icon.y = iconPadding;
    children.push(icon);

    const dividerY = icon.height + iconPadding;
    outline.lineStyle(lineWidth, 0xffffff, lineAlpha);
    outline.moveTo(0, dividerY);
    outline.lineTo(width, dividerY);

    const textStyle = new TextStyle({
      fontFamily: this.options.textFontFamily,
      fontSize: this.options.textFontSize,
      fill: this.options.textFillColor,
    });
    const title = new Text(lambda.template, textStyle);
    title.anchor.y = 0.5;
    title.x = icon.x + icon.width + iconPadding;
    title.y = icon.y + icon.height / 2.0;
    children.push(title);

    const slotIconStyle = new TextStyle({
      fontFamily: this.options.iconFontFamily,
      fontSize: this.options.iconFontSize,
      fill: this.options.iconFillColor,
    });

    // Properties
    const propHeight = 24;
    const propHeightHalf = propHeight / 2;

    // Based on the center anchor
    const propOffsetY = dividerY + padding + propHeightHalf;

    let leftLine = 0;
    let rightLine = 0;
    let maxLine = 0;

    for (let i = 0; i < lambda.props.length; ++i) {
      const prop = lambda.props[i];

      if (prop.type === 'flow_input') {
        const icon = new Text(String.fromCodePoint(flowUnlink), slotIconStyle);
        icon.x = iconPadding + icon.width / 2;
        icon.y = propOffsetY + leftLine * propHeight;
        icon.anchor.set(0.5, 0.5);
        children.push(icon);
        container.slots[prop.name] = {x: icon.x, y: icon.y} as IPoint;

        const att = new Text(prop.name, textStyle);
        att.x = icon.x + icon.width / 2 + padding;
        att.y = icon.y;
        att.anchor.y = 0.5;
        children.push(att);
      } else if (prop.type === 'flow_output') {
        const icon = new Text(String.fromCodePoint(flowLink), slotIconStyle);
        icon.x = width - icon.width / 2;
        icon.y = propOffsetY + rightLine * propHeight;
        icon.anchor.set(0.5, 0.5);
        children.push(icon);
        container.slots[prop.name] = {x: icon.x, y: icon.y} as IPoint;

        const att = new Text(prop.name, textStyle);
        att.x = icon.x - icon.width / 2 - padding;
        att.y = icon.y;
        att.anchor.x = 1;
        att.anchor.y = 0.5;
        children.push(att);
      } else if (prop.type === 'data_input') {
        const icon = new Text(String.fromCodePoint(dataUnlink), slotIconStyle);
        icon.x = iconPadding + icon.width / 2;
        icon.y = propOffsetY + leftLine * propHeight;
        icon.anchor.set(0.5, 0.5);
        children.push(icon);
        container.slots[prop.name] = {x: icon.x, y: icon.y} as IPoint;

        const att = new Text(prop.name, textStyle);
        att.x = icon.x + icon.width / 2 + padding;
        att.y = icon.y;
        att.anchor.y = 0.5;
        children.push(att);
      } else if (prop.type === 'data_output') {
        const icon = new Text(String.fromCodePoint(dataLink), slotIconStyle);
        icon.x = width - icon.width / 2;
        icon.y = propOffsetY + rightLine * propHeight;
        icon.anchor.set(0.5, 0.5);
        children.push(icon);
        container.slots[prop.name] = {x: icon.x, y: icon.y} as IPoint;

        const att = new Text(prop.name, textStyle);
        att.x = icon.x - icon.width / 2 - padding;
        att.y = icon.y;
        att.anchor.x = 1;
        att.anchor.y = 0.5;
        children.push(att);
      } else if (prop.type === 'button') {
        const button = new Graphics();
        button.lineStyle(1, 0xffffff);
        const buttonPadding = padding * 2;
        const x = buttonPadding;
        const y = propOffsetY + maxLine * propHeight - propHeightHalf + buttonPadding;
        const w = width - buttonPadding * 2;
        const h = propHeight - buttonPadding * 2;
        button.drawRoundedRect(x, y, w, h, 16);
        button.endFill();
        children.push(button);

        const buttonText = new Text(prop.value, textStyle);
        buttonText.anchor.set(0.5, 0.5);
        buttonText.anchor.y = 0.5;
        buttonText.x = x + w / 2;
        buttonText.y = y + h / 2;
        children.push(buttonText);
      } else if (prop.type === 'text_input') {
        const input = new TextInput({
          input: {
            fontFamily: this.options.textFontFamily,
            fontSize: '53px',
            fill: this.options.textFillColor,

            padding: '12px',
            // width: '500px',
            color: '#26272E',
          },
          box: {
            default: {fill: 0xe8e9f3, rounded: 12, stroke: {color: 0xcbcee0, width: 3}},
            focused: {fill: 0xe1e3ee, rounded: 12, stroke: {color: 0xabafc6, width: 3}},
            disabled: {fill: 0xdbdbdb, rounded: 12},
          },
        });

        const buttonPadding = padding * 2;
        input.x = buttonPadding;
        input.y = propOffsetY + maxLine * propHeight - propHeightHalf + buttonPadding;
        input.width = width - buttonPadding * 2;
        input.height = propHeight - buttonPadding * 2;
        input.placeholder = 'Enter your path ...';
        input.text = prop.value;
        children.push(input);
      }

      // Calculate next line
      if (['flow_input', 'data_input'].includes(prop.type)) {
        leftLine++;
        maxLine = Math.max(leftLine, rightLine);
      } else if (['flow_output', 'data_output'].includes(prop.type)) {
        rightLine++;
        maxLine = Math.max(leftLine, rightLine);
      } else if (['button', 'text_input'].includes(prop.type)) {
        maxLine++;
        leftLine = maxLine;
        rightLine = maxLine;
      }
    }

    container.x = lambda.x1;
    container.y = lambda.y1;
    container.interactive = true;
    container.buttonMode = true;
    container.scale.set(scale, scale);
    container.registerDragging();

    for (const child of children) {
      container.addChild(child);
    }

    return container;
  }

  openContextMenu() {
    // EMPTY.
  }
}
