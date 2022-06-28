import Rete from "rete";
import VueSelectControl from "./SwitchControl.vue";

export class SwitchControl extends Rete.Control {
  constructor(emitter, key, items) {
    super(key)

    this.component = VueSelectControl;

    this.props = {
      emitter,
      ikey: key,
      items
    };
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}