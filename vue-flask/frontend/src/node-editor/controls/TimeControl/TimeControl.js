import Rete from "rete";
import VueTimeControl from "./TimeControl.vue";

export class TimeControl extends Rete.Control {
  constructor(emitter, key, readonly) {
    super(key);
    this.component = VueTimeControl;
    this.props = { emitter, ikey: key, readonly };
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}