import Rete from "rete";
import VueZoneControl from "./ZoneControl.vue";

export class ZoneControl extends Rete.Control {
  constructor(emitter, key, readonly) {
    super(key);
    this.component = VueZoneControl;
    this.props = { emitter, ikey: key, readonly };
  }

  setValue(val) {
    this.vueContext.value = val;
  }
}