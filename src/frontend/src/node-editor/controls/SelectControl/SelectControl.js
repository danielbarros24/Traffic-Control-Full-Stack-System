import Rete from "rete";
import VueSelectControl from "./SelectControl.vue";

export class SelectControl extends Rete.Control {
  constructor(emitter, key, items, placeholder) {
    super(key)

    this.component = VueSelectControl;

    this.props = {
      emitter,
      ikey: key,
      items,
      placeholder
    };
  }

  setValue(val) {
    this.vueContext.value = val;
  }
} 