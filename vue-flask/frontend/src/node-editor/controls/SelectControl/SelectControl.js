import Rete from "rete";
import VueSelectControl from "./SelectControl.vue";

export class SelectControl extends Rete.Control {
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