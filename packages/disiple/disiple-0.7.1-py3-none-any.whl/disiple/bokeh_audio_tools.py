from bokeh.core.properties import Bool, Float, Seq
from bokeh.models import Tool
from bokeh.util.compiler import TypeScript


CODE = """
import {GestureTool, GestureToolView} from "models/tools/gestures/gesture_tool"
import {TapEvent} from "core/ui_events"
import {GlyphRenderer} from "models/renderers"
import * as p from "core/properties"

export class AudioPlayerToolView extends GestureToolView {
  model: AudioPlayerTool

  override _tap(ev: TapEvent): void {
    const {audioContext, samplerate, samples} = this.model;
    if (this.model.buffer == null || this.model.dynamic_audio) {
      let bufferData: Array<number>;
      if (samples.length > 0) {
        bufferData = samples;
      } else if (this.plot_view.model.data_renderers.length > 0) {
        const glyphRenderer = this.plot_view.model.data_renderers[0] as GlyphRenderer;
        bufferData = glyphRenderer.data_source.get_array('y');
      } else {
        return;
      }
      if (this.model.normalize) {
        const maxAmp = bufferData.map(Math.abs).reduce((i: number, j: number) => Math.max(i, j), -Infinity);
        bufferData = bufferData.map((i: number) => i/maxAmp);
      }
      this.model.buffer = audioContext.createBuffer(1, bufferData.length, samplerate);
      this.model.buffer.copyToChannel(Float32Array.from(bufferData), 0);
    }
    this.model.sourceNode?.stop();
    this.model.sourceNode = new AudioBufferSourceNode(audioContext, {buffer: this.model.buffer, loop: ev.shift_key});
    this.model.sourceNode.connect(audioContext.destination);
    if (ev.ctrl_key) {
      const start_time = this.plot_view.frame.x_scale.invert(ev.sx);
      this.model.sourceNode?.start(audioContext.currentTime, start_time);
    } else {
      this.model.sourceNode?.start();
    }
  }

  override _doubletap(_: TapEvent): void {
    this.model.sourceNode?.stop();
  }
}

export namespace AudioPlayerTool {
  export type Attrs = p.AttrsOf<Props>

  export type Props = GestureTool.Props & {
    samplerate: p.Property<number>,
    samples: p.Property<Array<number>>,
    normalize: p.Property<boolean>,
    dynamic_audio: p.Property<boolean>,
  }
}

export interface AudioPlayerTool extends AudioPlayerTool.Attrs {}

export class AudioPlayerTool extends GestureTool {
  override properties: AudioPlayerTool.Props;
  override __view_type__: AudioPlayerToolView;
  audioContext: AudioContext;
  buffer: AudioBuffer | null = null;
  sourceNode: AudioBufferSourceNode | null = null;

  constructor(attrs?: Partial<AudioPlayerTool.Attrs>) {
    super(attrs);
    this.audioContext = new AudioContext();
  }

  static {
    this.prototype.default_view = AudioPlayerToolView;

    this.define<AudioPlayerTool.Props>(({Number, Array, Boolean}) => ({
      samplerate: [ Number, 44100 ],
      samples: [ Array(Number), [] ],
      normalize: [Boolean, false],
      dynamic_audio: [Boolean, true],
    }))

    this.register_alias("play8k", () => new AudioPlayerTool({samplerate: 8000}));
    this.register_alias("play16k", () => new AudioPlayerTool({samplerate: 16000}));
    this.register_alias("play22k", () => new AudioPlayerTool({samplerate: 22050}));
    this.register_alias("play44k", () => new AudioPlayerTool({samplerate: 44100}));
    this.register_alias("play48k", () => new AudioPlayerTool({samplerate: 48000}));
  }

  override tool_name = "Play Audio";
  override tool_icon = "bk-tool-icon-caret-right";
  override event_type = "tap" as "tap";
  override default_order = 12;
}
"""

class AudioPlayerTool(Tool):
    __implementation__ = TypeScript(CODE)
    samplerate = Float(default=44100)
    samples = Seq(Float, default=[])
    normalize = Bool(default=False)
    dynamic_audio = Bool(default=True)
