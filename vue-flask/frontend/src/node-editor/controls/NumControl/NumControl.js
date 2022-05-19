import Rete from "rete";
import VueNumControl from "./NumControl.vue";

export class NumControl extends Rete.Control {
  constructor(emitter, key, readonly=false, placeholder='Number') {
    super(key);
    
    this.component = VueNumControl;
    this.props = { emitter, ikey: key, readonly, placeholder};
  }

  setValue(val) {
    this.vueContext.value = val;
  }
} 